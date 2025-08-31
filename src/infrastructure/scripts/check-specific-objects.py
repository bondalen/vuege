#!/usr/bin/env python3
"""
Скрипт для проверки конкретных объектов в SQL Server
Проверяет конкретно invCs и другие объекты
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
log_file = f"{log_dir}/check-specific-objects-{datetime.now().strftime('%Y%m%d_%H%M%S')}.log"

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

def check_specific_objects(mssql_conn):
    """Проверка конкретных объектов в SQL Server"""
    try:
        cursor = mssql_conn.cursor()
        
        # Проверяем конкретно invCs
        query_invcs = """
        SELECT 
            o.name as object_name,
            o.type as object_type,
            o.type_desc as object_type_desc,
            o.create_date,
            o.modify_date
        FROM sys.objects o
        INNER JOIN sys.schemas s ON o.schema_id = s.schema_id
        WHERE s.name = 'ags'
        AND o.name LIKE '%inv%'
        ORDER BY o.name
        """
        
        cursor.execute(query_invcs)
        inv_objects = cursor.fetchall()
        
        # Проверяем все объекты с типом V (VIEW)
        query_views = """
        SELECT 
            o.name as object_name,
            o.type as object_type,
            o.type_desc as object_type_desc,
            o.create_date,
            o.modify_date
        FROM sys.objects o
        INNER JOIN sys.schemas s ON o.schema_id = s.schema_id
        WHERE s.name = 'ags'
        AND o.type = 'V'
        ORDER BY o.name
        """
        
        cursor.execute(query_views)
        views = cursor.fetchall()
        
        # Проверяем все объекты с типом U (USER_TABLE)
        query_tables = """
        SELECT 
            o.name as object_name,
            o.type as object_type,
            o.type_desc as object_type_desc,
            o.create_date,
            o.modify_date
        FROM sys.objects o
        INNER JOIN sys.schemas s ON o.schema_id = s.schema_id
        WHERE s.name = 'ags'
        AND o.type = 'U'
        ORDER BY o.name
        """
        
        cursor.execute(query_tables)
        tables = cursor.fetchall()
        
        return {
            'inv_objects': inv_objects,
            'views': views,
            'tables': tables
        }
        
    except Exception as e:
        logging.error(f"Ошибка проверки конкретных объектов: {e}")
        return {'inv_objects': [], 'views': [], 'tables': []}

def check_postgres_invcs(pg_conn):
    """Проверка объекта invcs в PostgreSQL"""
    try:
        cursor = pg_conn.cursor()
        
        # Проверяем, есть ли таблица invcs
        query = """
        SELECT table_name, table_type
        FROM information_schema.tables
        WHERE table_schema = 'ags'
        AND table_name = 'invcs'
        """
        
        cursor.execute(query)
        result = cursor.fetchone()
        
        if result:
            return {
                'exists': True,
                'name': result[0],
                'type': result[1]
            }
        else:
            return {
                'exists': False,
                'name': None,
                'type': None
            }
        
    except Exception as e:
        logging.error(f"Ошибка проверки invcs в PostgreSQL: {e}")
        return {'exists': False, 'name': None, 'type': None}

def main():
    """Основная функция"""
    logging.info("Начало проверки конкретных объектов в SQL Server")
    
    # Получение подключений
    mssql_conn = get_mssql_connection()
    pg_conn = get_pg_connection()
    
    if not mssql_conn or not pg_conn:
        return
    
    try:
        # Проверка конкретных объектов в SQL Server
        logging.info("Проверка конкретных объектов в SQL Server...")
        sqlserver_objects = check_specific_objects(mssql_conn)
        
        # Проверка invcs в PostgreSQL
        logging.info("Проверка invcs в PostgreSQL...")
        postgres_invcs = check_postgres_invcs(pg_conn)
        
        # Вывод результатов
        logging.info("=== РЕЗУЛЬТАТЫ ПРОВЕРКИ ===")
        
        logging.info(f"Объектов с 'inv' в названии в SQL Server: {len(sqlserver_objects['inv_objects'])}")
        for obj in sqlserver_objects['inv_objects']:
            logging.info(f"  - {obj[0]} (тип: {obj[1]}, описание: {obj[2]})")
        
        logging.info(f"Представлений в SQL Server: {len(sqlserver_objects['views'])}")
        for view in sqlserver_objects['views']:
            logging.info(f"  - {view[0]} (тип: {view[1]}, описание: {view[2]})")
        
        logging.info(f"Таблиц в SQL Server: {len(sqlserver_objects['tables'])}")
        for table in sqlserver_objects['tables']:
            logging.info(f"  - {table[0]} (тип: {table[1]}, описание: {table[2]})")
        
        logging.info(f"invcs в PostgreSQL: {postgres_invcs['exists']}")
        if postgres_invcs['exists']:
            logging.info(f"  - Имя: {postgres_invcs['name']}, Тип: {postgres_invcs['type']}")
        
        # Создание отчета
        report = {
            'timestamp': datetime.now().isoformat(),
            'sqlserver_inv_objects': [
                {
                    'name': obj[0],
                    'type': obj[1],
                    'type_desc': obj[2],
                    'create_date': obj[3].isoformat() if obj[3] else None,
                    'modify_date': obj[4].isoformat() if obj[4] else None
                }
                for obj in sqlserver_objects['inv_objects']
            ],
            'sqlserver_views': [
                {
                    'name': obj[0],
                    'type': obj[1],
                    'type_desc': obj[2],
                    'create_date': obj[3].isoformat() if obj[3] else None,
                    'modify_date': obj[4].isoformat() if obj[4] else None
                }
                for obj in sqlserver_objects['views']
            ],
            'sqlserver_tables': [
                {
                    'name': obj[0],
                    'type': obj[1],
                    'type_desc': obj[2],
                    'create_date': obj[3].isoformat() if obj[3] else None,
                    'modify_date': obj[4].isoformat() if obj[4] else None
                }
                for obj in sqlserver_objects['tables']
            ],
            'postgres_invcs': postgres_invcs,
            'log_file': log_file
        }
        
        # Сохранение отчета
        report_dir = "/home/alex/vuege/docs/infrastructure/reports"
        os.makedirs(report_dir, exist_ok=True)
        report_file = f"{report_dir}/check-specific-objects-report-{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        
        with open(report_file, 'w', encoding='utf-8') as f:
            json.dump(report, f, ensure_ascii=False, indent=2)
        
        logging.info(f"Отчет сохранен: {report_file}")
        
    except Exception as e:
        logging.error(f"Ошибка в основной функции: {e}")
    
    finally:
        if mssql_conn:
            mssql_conn.close()
        if pg_conn:
            pg_conn.close()
    
    logging.info("Проверка конкретных объектов завершена")

if __name__ == "__main__":
    main()