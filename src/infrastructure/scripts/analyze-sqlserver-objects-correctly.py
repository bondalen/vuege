#!/usr/bin/env python3
"""
Скрипт для правильного анализа объектов в SQL Server
Проверяет все объекты в схеме ags и определяет их тип
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
log_file = f"{log_dir}/analyze-sqlserver-objects-correctly-{datetime.now().strftime('%Y%m%d_%H%M%S')}.log"

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

def get_sqlserver_objects_detailed(mssql_conn):
    """Получение детальной информации об объектах из схемы ags в SQL Server"""
    try:
        cursor = mssql_conn.cursor()
        
        query = """
        SELECT 
            o.name as object_name,
            o.type as object_type,
            o.type_desc as object_type_desc,
            o.create_date,
            o.modify_date,
            CASE 
                WHEN o.type = 'U' THEN 'USER_TABLE'
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
        ORDER BY o.type, o.name
        """
        
        cursor.execute(query)
        objects = cursor.fetchall()
        
        return objects
        
    except Exception as e:
        logging.error(f"Ошибка получения объектов из SQL Server: {e}")
        return []

def get_postgres_tables(pg_conn):
    """Получение всех таблиц из схемы ags в PostgreSQL"""
    try:
        cursor = pg_conn.cursor()
        
        query = """
        SELECT table_name
        FROM information_schema.tables
        WHERE table_schema = 'ags'
        AND table_type = 'BASE TABLE'
        ORDER BY table_name
        """
        
        cursor.execute(query)
        tables = [row[0] for row in cursor.fetchall()]
        
        return tables
        
    except Exception as e:
        logging.error(f"Ошибка получения таблиц из PostgreSQL: {e}")
        return []

def analyze_object_types_detailed(sqlserver_objects):
    """Детальный анализ типов объектов из SQL Server"""
    object_types = {}
    views = []
    tables = []
    stored_procedures = []
    functions = []
    other_objects = []
    
    for obj_name, obj_type, obj_type_desc, create_date, modify_date, obj_category in sqlserver_objects:
        if obj_name not in object_types:
            object_types[obj_name] = {
                'type': obj_type,
                'type_desc': obj_type_desc,
                'category': obj_category,
                'create_date': create_date.isoformat() if create_date else None,
                'modify_date': modify_date.isoformat() if modify_date else None
            }
        
        if obj_type == 'V':  # View
            views.append(obj_name)
        elif obj_type == 'U':  # User table
            tables.append(obj_name)
        elif obj_type == 'P':  # Stored procedure
            stored_procedures.append(obj_name)
        elif obj_type in ['FN', 'TF', 'IF']:  # Functions
            functions.append(obj_name)
        else:
            other_objects.append({
                'name': obj_name,
                'type': obj_type,
                'type_desc': obj_type_desc,
                'category': obj_category
            })
    
    return {
        'object_types': object_types,
        'views': views,
        'tables': tables,
        'stored_procedures': stored_procedures,
        'functions': functions,
        'other_objects': other_objects
    }

def check_migrated_views_detailed(sqlserver_objects, postgres_tables):
    """Проверка, какие представления были мигрированы как таблицы"""
    sqlserver_object_types = {obj[0]: obj[1] for obj in sqlserver_objects}
    
    migrated_views = []
    migrated_tables = []
    unknown_objects = []
    
    for pg_table in postgres_tables:
        if pg_table in sqlserver_object_types:
            obj_type = sqlserver_object_types[pg_table]
            if obj_type == 'V':  # View
                migrated_views.append(pg_table)
            elif obj_type == 'U':  # User table
                migrated_tables.append(pg_table)
            else:
                unknown_objects.append({
                    'name': pg_table,
                    'type': obj_type
                })
        else:
            unknown_objects.append({
                'name': pg_table,
                'type': 'NOT_FOUND_IN_SQLSERVER'
            })
    
    return {
        'migrated_views': migrated_views,
        'migrated_tables': migrated_tables,
        'unknown_objects': unknown_objects
    }

def main():
    """Основная функция"""
    logging.info("Начало детального анализа объектов в SQL Server")
    
    # Получение подключений
    mssql_conn = get_mssql_connection()
    pg_conn = get_pg_connection()
    
    if not mssql_conn or not pg_conn:
        return
    
    try:
        # Получение объектов из SQL Server
        logging.info("Получение объектов из SQL Server...")
        sqlserver_objects = get_sqlserver_objects_detailed(mssql_conn)
        logging.info(f"Найдено объектов в SQL Server: {len(sqlserver_objects)}")
        
        # Получение таблиц из PostgreSQL
        logging.info("Получение таблиц из PostgreSQL...")
        postgres_tables = get_postgres_tables(pg_conn)
        logging.info(f"Найдено таблиц в PostgreSQL: {len(postgres_tables)}")
        
        # Анализ типов объектов
        logging.info("Анализ типов объектов...")
        object_analysis = analyze_object_types_detailed(sqlserver_objects)
        
        # Проверка мигрированных представлений
        logging.info("Проверка мигрированных представлений...")
        migration_check = check_migrated_views_detailed(sqlserver_objects, postgres_tables)
        
        # Создание отчета
        report = {
            'timestamp': datetime.now().isoformat(),
            'sqlserver_objects': {
                'total': len(sqlserver_objects),
                'views': len(object_analysis['views']),
                'tables': len(object_analysis['tables']),
                'stored_procedures': len(object_analysis['stored_procedures']),
                'functions': len(object_analysis['functions']),
                'other': len(object_analysis['other_objects'])
            },
            'postgres_tables': {
                'total': len(postgres_tables)
            },
            'migration_analysis': {
                'migrated_views': len(migration_check['migrated_views']),
                'migrated_tables': len(migration_check['migrated_tables']),
                'unknown_objects': len(migration_check['unknown_objects'])
            },
            'object_types': object_analysis['object_types'],
            'views_in_sqlserver': object_analysis['views'],
            'tables_in_sqlserver': object_analysis['tables'],
            'stored_procedures_in_sqlserver': object_analysis['stored_procedures'],
            'functions_in_sqlserver': object_analysis['functions'],
            'other_objects_in_sqlserver': object_analysis['other_objects'],
            'migrated_views': migration_check['migrated_views'],
            'migrated_tables': migration_check['migrated_tables'],
            'unknown_objects': migration_check['unknown_objects'],
            'log_file': log_file
        }
        
        # Сохранение отчета
        report_dir = "/home/alex/vuege/docs/infrastructure/reports"
        os.makedirs(report_dir, exist_ok=True)
        report_file = f"{report_dir}/analyze-sqlserver-objects-correctly-report-{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        
        with open(report_file, 'w', encoding='utf-8') as f:
            json.dump(report, f, ensure_ascii=False, indent=2)
        
        # Вывод результатов
        logging.info("=== РЕЗУЛЬТАТЫ ДЕТАЛЬНОГО АНАЛИЗА ===")
        logging.info(f"Объектов в SQL Server: {len(sqlserver_objects)}")
        logging.info(f"  - Представлений: {len(object_analysis['views'])}")
        logging.info(f"  - Таблиц: {len(object_analysis['tables'])}")
        logging.info(f"  - Хранимых процедур: {len(object_analysis['stored_procedures'])}")
        logging.info(f"  - Функций: {len(object_analysis['functions'])}")
        logging.info(f"  - Других объектов: {len(object_analysis['other_objects'])}")
        
        logging.info(f"Таблиц в PostgreSQL: {len(postgres_tables)}")
        
        logging.info(f"Мигрированных представлений: {len(migration_check['migrated_views'])}")
        if migration_check['migrated_views']:
            logging.info("Представления, мигрированные как таблицы:")
            for view in migration_check['migrated_views']:
                logging.info(f"  - {view}")
        
        logging.info(f"Мигрированных таблиц: {len(migration_check['migrated_tables'])}")
        logging.info(f"Неизвестных объектов: {len(migration_check['unknown_objects'])}")
        
        if object_analysis['views']:
            logging.info("Все представления в SQL Server:")
            for view in object_analysis['views']:
                logging.info(f"  - {view}")
        
        logging.info(f"Отчет сохранен: {report_file}")
        
    except Exception as e:
        logging.error(f"Ошибка в основной функции: {e}")
    
    finally:
        if mssql_conn:
            mssql_conn.close()
        if pg_conn:
            pg_conn.close()
    
    logging.info("Детальный анализ объектов в SQL Server завершен")

if __name__ == "__main__":
    main()