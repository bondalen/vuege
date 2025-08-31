#!/usr/bin/env python3
"""
Скрипт для валидации данных в системе контроля миграции
Проверяет соответствие имен объектов между системами
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
log_file = f"{log_dir}/validate-migration-control-data-{datetime.now().strftime('%Y%m%d_%H%M%S')}.log"

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

def validate_migration_control_data(pg_conn, mssql_conn):
    """Валидация данных в системе контроля миграции"""
    try:
        cursor = pg_conn.cursor()
        
        # Получение всех записей из системы контроля
        query = """
        SELECT 
            so.id,
            so.object_id,
            so.name_in_mssql,
            so.name_in_postgres,
            so.migration_status,
            o.object_type
        FROM migration_control.specific_objects so
        JOIN migration_control.objects o ON so.object_id = o.id
        ORDER BY o.object_type, so.name_in_mssql
        """
        
        cursor.execute(query)
        control_records = cursor.fetchall()
        
        # Получение объектов из SQL Server
        mssql_cursor = mssql_conn.cursor()
        mssql_query = """
        SELECT 
            o.name as object_name,
            o.type as object_type,
            o.type_desc as object_type_desc
        FROM sys.objects o
        INNER JOIN sys.schemas s ON o.schema_id = s.schema_id
        WHERE s.name = 'ags'
        AND o.type IN ('U', 'V', 'P', 'FN', 'TF', 'IF')
        ORDER BY o.type, o.name
        """
        
        mssql_cursor.execute(mssql_query)
        mssql_objects = {row[0]: row for row in mssql_cursor.fetchall()}
        
        # Получение объектов из PostgreSQL
        pg_query = """
        SELECT 
            table_name as object_name,
            'TABLE' as object_type,
            'BASE TABLE' as object_type_desc
        FROM information_schema.tables
        WHERE table_schema = 'ags'
        AND table_type = 'BASE TABLE'
        UNION ALL
        SELECT 
            table_name as object_name,
            'VIEW' as object_type,
            'VIEW' as object_type_desc
        FROM information_schema.views
        WHERE table_schema = 'ags'
        UNION ALL
        SELECT 
            routine_name as object_name,
            'FUNCTION' as object_type,
            routine_type as object_type_desc
        FROM information_schema.routines
        WHERE routine_schema = 'ags'
        ORDER BY object_type, object_name
        """
        
        cursor.execute(pg_query)
        pg_objects = {row[0]: row for row in cursor.fetchall()}
        
        # Валидация записей
        validation_results = []
        
        for record in control_records:
            record_id, object_id, mssql_name, postgres_name, status, object_type = record
            
            validation_result = {
                'record_id': record_id,
                'mssql_name': mssql_name,
                'postgres_name': postgres_name,
                'status': status,
                'object_type': object_type,
                'issues': []
            }
            
            # Проверка существования в SQL Server
            if mssql_name not in mssql_objects:
                validation_result['issues'].append({
                    'type': 'mssql_not_found',
                    'description': f'Объект {mssql_name} не найден в SQL Server'
                })
            
            # Проверка существования в PostgreSQL (если указан)
            if postgres_name and postgres_name not in pg_objects:
                validation_result['issues'].append({
                    'type': 'postgres_not_found',
                    'description': f'Объект {postgres_name} не найден в PostgreSQL'
                })
            
            # Проверка соответствия статуса
            if status == 'completed' and not postgres_name:
                validation_result['issues'].append({
                    'type': 'completed_without_postgres_name',
                    'description': f'Статус completed, но name_in_postgres не указан'
                })
            
            if validation_result['issues']:
                validation_results.append(validation_result)
        
        # Проверка дублирования
        mssql_names = [record[2] for record in control_records]
        duplicates = [name for name in set(mssql_names) if mssql_names.count(name) > 1]
        
        for duplicate_name in duplicates:
            duplicate_records = [r for r in control_records if r[2] == duplicate_name]
            validation_results.append({
                'record_id': 'multiple',
                'mssql_name': duplicate_name,
                'postgres_name': 'multiple',
                'status': 'multiple',
                'object_type': 'multiple',
                'issues': [{
                    'type': 'duplicate_records',
                    'description': f'Найдено {len(duplicate_records)} записей для имени {duplicate_name}'
                }]
            })
        
        return validation_results, mssql_objects, pg_objects
        
    except Exception as e:
        logging.error(f"Ошибка валидации данных: {e}")
        return [], {}, {}

def main():
    """Основная функция"""
    logging.info("Начало валидации данных в системе контроля миграции")
    
    # Получение подключений
    mssql_conn = get_mssql_connection()
    pg_conn = get_pg_connection()
    
    if not mssql_conn or not pg_conn:
        return
    
    try:
        # Валидация данных
        validation_results, mssql_objects, pg_objects = validate_migration_control_data(pg_conn, mssql_conn)
        
        if validation_results:
            logging.warning(f"Найдено {len(validation_results)} проблем:")
            
            for result in validation_results:
                logging.warning(f"Запись {result['record_id']} ({result['mssql_name']}):")
                for issue in result['issues']:
                    logging.warning(f"  - {issue['description']}")
        else:
            logging.info("Проблем не найдено")
        
        # Статистика
        logging.info(f"Объектов в SQL Server: {len(mssql_objects)}")
        logging.info(f"Объектов в PostgreSQL: {len(pg_objects)}")
        
        # Создание отчета
        report = {
            'timestamp': datetime.now().isoformat(),
            'sqlserver_objects': len(mssql_objects),
            'postgres_objects': len(pg_objects),
            'validation_issues': len(validation_results),
            'issues_details': validation_results,
            'log_file': log_file
        }
        
        # Сохранение отчета
        report_dir = "/home/alex/vuege/docs/infrastructure/reports"
        os.makedirs(report_dir, exist_ok=True)
        report_file = f"{report_dir}/validate-migration-control-data-report-{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        
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
    
    logging.info("Валидация данных завершена")

if __name__ == "__main__":
    main()