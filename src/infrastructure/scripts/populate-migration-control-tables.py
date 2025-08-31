#!/usr/bin/env python3
"""
Скрипт для заполнения таблиц контроля миграции данными из SQL Server и PostgreSQL
"""

import pymssql
import psycopg2
import psycopg2.extras
import logging
from datetime import datetime
import json
import os

# Настройка логирования
log_dir = "/home/alex/vuege/docs/infrastructure/logs"
os.makedirs(log_dir, exist_ok=True)
log_file = f"{log_dir}/populate-migration-control-tables-{datetime.now().strftime('%Y%m%d_%H%M%S')}.log"

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(log_file, encoding='utf-8'),
        logging.StreamHandler()
    ]
)

# Параметры подключения к SQL Server
MSSQL_HOST = "localhost"
MSSQL_PORT = 1433
MSSQL_DB = "Fish_Eye"
MSSQL_USER = "sa"
MSSQL_PASSWORD = "Vuege2024!"

# Параметры подключения к PostgreSQL
PG_HOST = "localhost"
PG_PORT = 5432
PG_DB = "vuege"
PG_USER = "postgres"
PG_PASSWORD = "testpass"

def get_mssql_connection():
    """Создание подключения к SQL Server"""
    try:
        conn = pymssql.connect(
            server=MSSQL_HOST,
            port=MSSQL_PORT,
            database=MSSQL_DB,
            user=MSSQL_USER,
            password=MSSQL_PASSWORD,
            charset='utf8'
        )
        return conn
    except Exception as e:
        logging.error(f"Ошибка подключения к SQL Server: {e}")
        return None

def get_pg_connection():
    """Создание подключения к PostgreSQL"""
    try:
        conn = psycopg2.connect(
            host=PG_HOST,
            port=PG_PORT,
            database=PG_DB,
            user=PG_USER,
            password=PG_PASSWORD
        )
        return conn
    except Exception as e:
        logging.error(f"Ошибка подключения к PostgreSQL: {e}")
        return None

def get_sqlserver_objects(mssql_conn):
    """Получение всех объектов из схемы ags в SQL Server"""
    try:
        cursor = mssql_conn.cursor()
        
        query = """
        SELECT 
            o.name as object_name,
            o.type as object_type,
            o.type_desc as object_type_desc,
            CASE 
                WHEN o.type = 'U' THEN 'TABLE'
                WHEN o.type = 'V' THEN 'VIEW'
                WHEN o.type = 'P' THEN 'STORED_PROCEDURE'
                WHEN o.type = 'FN' THEN 'FUNCTION'
                WHEN o.type = 'TF' THEN 'TABLE_FUNCTION'
                WHEN o.type = 'IF' THEN 'INLINE_FUNCTION'
                ELSE 'OTHER'
            END as object_category
        FROM sys.objects o
        INNER JOIN sys.schemas s ON o.schema_id = s.schema_id
        WHERE s.name = 'ags'
        AND o.type IN ('U', 'V', 'P', 'FN', 'TF', 'IF')
        ORDER BY o.type, o.name
        """
        
        cursor.execute(query)
        objects = cursor.fetchall()
        
        return objects
        
    except Exception as e:
        logging.error(f"Ошибка получения объектов из SQL Server: {e}")
        return []

def get_postgres_objects(pg_conn):
    """Получение всех объектов из схемы ags в PostgreSQL"""
    try:
        cursor = pg_conn.cursor()
        
        # Получение таблиц
        tables_query = """
        SELECT 
            table_name as object_name,
            'TABLE' as object_type,
            'BASE TABLE' as object_type_desc,
            'TABLE' as object_category
        FROM information_schema.tables
        WHERE table_schema = 'ags'
        AND table_type = 'BASE TABLE'
        ORDER BY table_name
        """
        
        cursor.execute(tables_query)
        tables = cursor.fetchall()
        
        # Получение представлений
        views_query = """
        SELECT 
            table_name as object_name,
            'VIEW' as object_type,
            'VIEW' as object_type_desc,
            'VIEW' as object_category
        FROM information_schema.views
        WHERE table_schema = 'ags'
        ORDER BY table_name
        """
        
        cursor.execute(views_query)
        views = cursor.fetchall()
        
        # Получение функций
        functions_query = """
        SELECT 
            routine_name as object_name,
            'FUNCTION' as object_type,
            routine_type as object_type_desc,
            'FUNCTION' as object_category
        FROM information_schema.routines
        WHERE routine_schema = 'ags'
        ORDER BY routine_name
        """
        
        cursor.execute(functions_query)
        functions = cursor.fetchall()
        
        return tables + views + functions
        
    except Exception as e:
        logging.error(f"Ошибка получения объектов из PostgreSQL: {e}")
        return []

def clear_migration_control_tables(pg_conn):
    """Очистка таблиц контроля миграции"""
    try:
        cursor = pg_conn.cursor()
        
        # Очистка таблиц в правильном порядке (из-за внешних ключей)
        cursor.execute("DELETE FROM migration_control.specific_objects;")
        cursor.execute("DELETE FROM migration_control.objects;")
        
        # Сброс последовательностей
        cursor.execute("ALTER SEQUENCE migration_control.objects_id_seq RESTART WITH 1;")
        cursor.execute("ALTER SEQUENCE migration_control.specific_objects_id_seq RESTART WITH 1;")
        
        pg_conn.commit()
        logging.info("Таблицы контроля миграции очищены")
        
    except Exception as e:
        logging.error(f"Ошибка очистки таблиц: {e}")
        pg_conn.rollback()

def insert_object_type(pg_conn, object_type, has_in_mssql, has_in_postgres):
    """Вставка типа объекта в таблицу objects"""
    try:
        cursor = pg_conn.cursor()
        
        query = """
        INSERT INTO migration_control.objects 
        (object_type, has_in_mssql, has_in_postgres, name_in_mssql, name_in_postgres)
        VALUES (%s, %s, %s, %s, %s)
        RETURNING id;
        """
        
        cursor.execute(query, (object_type, has_in_mssql, has_in_postgres, object_type, object_type))
        object_id = cursor.fetchone()[0]
        
        return object_id
        
    except Exception as e:
        logging.error(f"Ошибка вставки типа объекта {object_type}: {e}")
        return None

def insert_specific_object(pg_conn, object_id, name_in_mssql, name_in_postgres, status='pending'):
    """Вставка конкретного объекта в таблицу specific_objects"""
    try:
        cursor = pg_conn.cursor()
        
        query = """
        INSERT INTO migration_control.specific_objects 
        (object_id, name_in_mssql, name_in_postgres, migration_status)
        VALUES (%s, %s, %s, %s);
        """
        
        cursor.execute(query, (object_id, name_in_mssql, name_in_postgres, status))
        
    except Exception as e:
        logging.error(f"Ошибка вставки конкретного объекта {name_in_mssql}: {e}")

def populate_migration_control_tables(mssql_conn, pg_conn):
    """Заполнение таблиц контроля миграции"""
    try:
        # Получение объектов из обеих баз данных
        logging.info("Получение объектов из SQL Server...")
        sqlserver_objects = get_sqlserver_objects(mssql_conn)
        logging.info(f"Найдено объектов в SQL Server: {len(sqlserver_objects)}")
        
        logging.info("Получение объектов из PostgreSQL...")
        postgres_objects = get_postgres_objects(pg_conn)
        logging.info(f"Найдено объектов в PostgreSQL: {len(postgres_objects)}")
        
        # Очистка таблиц
        clear_migration_control_tables(pg_conn)
        
        # Группировка объектов по типам
        sqlserver_by_type = {}
        postgres_by_type = {}
        
        for obj in sqlserver_objects:
            obj_type = obj[3]  # object_category
            if obj_type not in sqlserver_by_type:
                sqlserver_by_type[obj_type] = []
            sqlserver_by_type[obj_type].append(obj[0])  # object_name
        
        for obj in postgres_objects:
            obj_type = obj[3]  # object_category
            if obj_type not in postgres_by_type:
                postgres_by_type[obj_type] = []
            postgres_by_type[obj_type].append(obj[0])  # object_name
        
        # Объединение всех типов объектов
        all_types = set(sqlserver_by_type.keys()) | set(postgres_by_type.keys())
        
        # Вставка типов объектов
        object_type_ids = {}
        for obj_type in all_types:
            has_in_mssql = obj_type in sqlserver_by_type
            has_in_postgres = obj_type in postgres_by_type
            
            object_id = insert_object_type(pg_conn, obj_type, has_in_mssql, has_in_postgres)
            if object_id:
                object_type_ids[obj_type] = object_id
        
        # Вставка конкретных объектов
        for obj_type in all_types:
            object_id = object_type_ids.get(obj_type)
            if not object_id:
                continue
            
            # Объекты из SQL Server
            if obj_type in sqlserver_by_type:
                for obj_name in sqlserver_by_type[obj_type]:
                    # Проверяем, есть ли объект в PostgreSQL
                    status = 'completed' if (obj_type in postgres_by_type and obj_name in postgres_by_type[obj_type]) else 'pending'
                    insert_specific_object(pg_conn, object_id, obj_name, obj_name, status)
            
            # Объекты из PostgreSQL (которые могут отсутствовать в SQL Server)
            if obj_type in postgres_by_type:
                for obj_name in postgres_by_type[obj_type]:
                    # Если объект уже добавлен из SQL Server, пропускаем
                    if obj_type in sqlserver_by_type and obj_name in sqlserver_by_type[obj_type]:
                        continue
                    # Иначе добавляем как объект, существующий только в PostgreSQL
                    insert_specific_object(pg_conn, object_id, obj_name, obj_name, 'completed')
        
        pg_conn.commit()
        logging.info("Таблицы контроля миграции заполнены")
        
        return {
            'sqlserver_objects': len(sqlserver_objects),
            'postgres_objects': len(postgres_objects),
            'object_types': len(all_types)
        }
        
    except Exception as e:
        logging.error(f"Ошибка заполнения таблиц: {e}")
        pg_conn.rollback()
        return None

def main():
    """Основная функция"""
    logging.info("Начало заполнения таблиц контроля миграции")
    
    # Получение подключений
    mssql_conn = get_mssql_connection()
    pg_conn = get_pg_connection()
    
    if not mssql_conn or not pg_conn:
        return
    
    try:
        # Заполнение таблиц
        results = populate_migration_control_tables(mssql_conn, pg_conn)
        
        if results:
            logging.info("=== ТАБЛИЦЫ КОНТРОЛЯ МИГРАЦИИ ЗАПОЛНЕНЫ ===")
            logging.info(f"Объектов в SQL Server: {results['sqlserver_objects']}")
            logging.info(f"Объектов в PostgreSQL: {results['postgres_objects']}")
            logging.info(f"Типов объектов: {results['object_types']}")
            
            # Создание отчета
            report = {
                'timestamp': datetime.now().isoformat(),
                'sqlserver_objects': results['sqlserver_objects'],
                'postgres_objects': results['postgres_objects'],
                'object_types': results['object_types'],
                'log_file': log_file
            }
            
            # Сохранение отчета
            report_dir = "/home/alex/vuege/docs/infrastructure/reports"
            os.makedirs(report_dir, exist_ok=True)
            report_file = f"{report_dir}/populate-migration-control-tables-report-{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
            
            with open(report_file, 'w', encoding='utf-8') as f:
                json.dump(report, f, ensure_ascii=False, indent=2)
            
            logging.info(f"Отчет сохранен: {report_file}")
        else:
            logging.error("Ошибка заполнения таблиц контроля миграции")
        
    except Exception as e:
        logging.error(f"Ошибка в основной функции: {e}")
    
    finally:
        if mssql_conn:
            mssql_conn.close()
        if pg_conn:
            pg_conn.close()
    
    logging.info("Заполнение таблиц контроля миграции завершено")

if __name__ == "__main__":
    main()