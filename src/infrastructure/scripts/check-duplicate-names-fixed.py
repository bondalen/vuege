#!/usr/bin/env python3
"""
Скрипт для проверки дублирования имен объектов в системе контроля миграции (исправленный)
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
log_file = f"{log_dir}/check-duplicate-names-fixed-{datetime.now().strftime('%Y%m%d_%H%M%S')}.log"

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

def check_migration_control_duplicates_fixed(pg_conn):
    """Проверка дублирования имен в системе контроля миграции (исправленный)"""
    try:
        cursor = pg_conn.cursor()
        
        # Проверка дублирования в таблице specific_objects
        query = """
        SELECT 
            so.name_in_mssql,
            o.object_type,
            COUNT(*) as count
        FROM migration_control.specific_objects so
        JOIN migration_control.objects o ON so.object_id = o.id
        WHERE so.name_in_mssql IS NOT NULL
        GROUP BY so.name_in_mssql, o.object_type
        HAVING COUNT(*) > 1
        ORDER BY so.name_in_mssql, o.object_type
        """
        
        cursor.execute(query)
        duplicates = cursor.fetchall()
        
        return duplicates
        
    except Exception as e:
        logging.error(f"Ошибка проверки дублирования в системе контроля: {e}")
        return []

def check_specific_names_fixed(mssql_conn, pg_conn):
    """Проверка конкретных имен, упомянутых пользователем (исправленный)"""
    try:
        cursor_mssql = mssql_conn.cursor()
        cursor_pg = pg_conn.cursor()
        
        # Проверка cnInvAccnt в SQL Server
        mssql_query = """
        SELECT 
            o.name as object_name,
            o.type as object_type,
            o.type_desc as object_type_desc
        FROM sys.objects o
        INNER JOIN sys.schemas s ON o.schema_id = s.schema_id
        WHERE s.name = 'ags'
        AND o.name LIKE '%cnInvAccnt%'
        ORDER BY o.name
        """
        
        cursor_mssql.execute(mssql_query)
        mssql_results = cursor_mssql.fetchall()
        
        # Проверка cninvaccnt в PostgreSQL
        pg_query = """
        SELECT 
            table_name as object_name,
            'TABLE' as object_type,
            'BASE TABLE' as object_type_desc
        FROM information_schema.tables
        WHERE table_schema = 'ags'
        AND table_name LIKE '%cninvaccnt%'
        ORDER BY table_name
        """
        
        cursor_pg.execute(pg_query)
        pg_results = cursor_pg.fetchall()
        
        return {
            'sqlserver': mssql_results,
            'postgres': pg_results
        }
        
    except Exception as e:
        logging.error(f"Ошибка проверки конкретных имен: {e}")
        return {'sqlserver': [], 'postgres': []}

def check_all_names_in_migration_control(pg_conn):
    """Проверка всех имен в системе контроля миграции"""
    try:
        cursor = pg_conn.cursor()
        
        query = """
        SELECT 
            so.name_in_mssql,
            o.object_type,
            so.name_in_postgres,
            so.migration_status
        FROM migration_control.specific_objects so
        JOIN migration_control.objects o ON so.object_id = o.id
        WHERE so.name_in_mssql IS NOT NULL
        ORDER BY so.name_in_mssql
        """
        
        cursor.execute(query)
        results = cursor.fetchall()
        
        return results
        
    except Exception as e:
        logging.error(f"Ошибка проверки всех имен в системе контроля: {e}")
        return []

def main():
    """Основная функция"""
    logging.info("Начало проверки дублирования имен объектов (исправленный)")
    
    # Получение подключений
    mssql_conn = get_mssql_connection()
    pg_conn = get_pg_connection()
    
    if not mssql_conn or not pg_conn:
        return
    
    try:
        # Проверка дублирования в системе контроля миграции
        logging.info("Проверка дублирования имен в системе контроля миграции...")
        control_duplicates = check_migration_control_duplicates_fixed(pg_conn)
        
        if control_duplicates:
            logging.warning(f"Найдены дублирующиеся имена в системе контроля: {len(control_duplicates)}")
            for dup in control_duplicates:
                logging.warning(f"  - {dup[0]} ({dup[1]}) - {dup[2]} раз")
        else:
            logging.info("Дублирующихся имен в системе контроля не найдено")
        
        # Проверка конкретных имен
        logging.info("Проверка конкретных имен (cnInvAccnt/cninvaccnt)...")
        specific_results = check_specific_names_fixed(mssql_conn, pg_conn)
        
        logging.info("Результаты проверки конкретных имен:")
        logging.info(f"  SQL Server (cnInvAccnt): {len(specific_results['sqlserver'])} объектов")
        for obj in specific_results['sqlserver']:
            logging.info(f"    - {obj[0]} ({obj[1]})")
        
        logging.info(f"  PostgreSQL (cninvaccnt): {len(specific_results['postgres'])} объектов")
        for obj in specific_results['postgres']:
            logging.info(f"    - {obj[0]} ({obj[1]})")
        
        # Проверка всех имен в системе контроля
        logging.info("Проверка всех имен в системе контроля миграции...")
        all_names = check_all_names_in_migration_control(pg_conn)
        
        logging.info(f"Всего объектов в системе контроля: {len(all_names)}")
        
        # Поиск объектов с похожими именами
        logging.info("Поиск объектов с похожими именами...")
        similar_names = []
        for i, name1 in enumerate(all_names):
            for j, name2 in enumerate(all_names[i+1:], i+1):
                if name1[0].lower() == name2[0].lower() and name1[0] != name2[0]:
                    similar_names.append((name1, name2))
        
        if similar_names:
            logging.warning(f"Найдены объекты с похожими именами: {len(similar_names)}")
            for name1, name2 in similar_names[:10]:  # Показываем первые 10
                logging.warning(f"  - {name1[0]} vs {name2[0]} (оба типа {name1[1]})")
        else:
            logging.info("Объектов с похожими именами не найдено")
        
        # Создание отчета
        report = {
            'timestamp': datetime.now().isoformat(),
            'control_duplicates': [
                {
                    'name': dup[0],
                    'type': dup[1],
                    'count': dup[2]
                }
                for dup in control_duplicates
            ],
            'specific_names': {
                'sqlserver': [
                    {
                        'name': obj[0],
                        'type': obj[1],
                        'type_desc': obj[2]
                    }
                    for obj in specific_results['sqlserver']
                ],
                'postgres': [
                    {
                        'name': obj[0],
                        'type': obj[1],
                        'type_desc': obj[2]
                    }
                    for obj in specific_results['postgres']
                ]
            },
            'similar_names': [
                {
                    'name1': name1[0],
                    'type1': name1[1],
                    'name2': name2[0],
                    'type2': name2[1]
                }
                for name1, name2 in similar_names
            ],
            'total_objects': len(all_names),
            'log_file': log_file
        }
        
        # Сохранение отчета
        report_dir = "/home/alex/vuege/docs/infrastructure/reports"
        os.makedirs(report_dir, exist_ok=True)
        report_file = f"{report_dir}/check-duplicate-names-fixed-report-{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        
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
    
    logging.info("Проверка дублирования имен завершена")

if __name__ == "__main__":
    main()