#!/usr/bin/env python3
"""
Скрипт для исправления имен объектов в системе контроля миграции
Исправляет проблемы с неправильными именами и дублированием записей
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
log_file = f"{log_dir}/fix-migration-control-names-{datetime.now().strftime('%Y%m%d_%H%M%S')}.log"

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

def get_sqlserver_tables_exact_names(mssql_conn):
    """Получение точных имен таблиц из SQL Server"""
    try:
        cursor = mssql_conn.cursor()
        
        query = """
        SELECT 
            o.name as table_name,
            o.type as object_type,
            o.type_desc as object_type_desc
        FROM sys.objects o
        INNER JOIN sys.schemas s ON o.schema_id = s.schema_id
        WHERE s.name = 'ags'
        AND o.type = 'U'
        ORDER BY o.name
        """
        
        cursor.execute(query)
        tables = cursor.fetchall()
        
        return {table[0]: table for table in tables}
        
    except Exception as e:
        logging.error(f"Ошибка получения таблиц из SQL Server: {e}")
        return {}

def get_postgres_tables_exact_names(pg_conn):
    """Получение точных имен таблиц из PostgreSQL"""
    try:
        cursor = pg_conn.cursor()
        
        query = """
        SELECT 
            table_name,
            'TABLE' as object_type,
            'BASE TABLE' as object_type_desc
        FROM information_schema.tables
        WHERE table_schema = 'ags'
        AND table_type = 'BASE TABLE'
        ORDER BY table_name
        """
        
        cursor.execute(query)
        tables = cursor.fetchall()
        
        return {table[0]: table for table in tables}
        
    except Exception as e:
        logging.error(f"Ошибка получения таблиц из PostgreSQL: {e}")
        return {}

def get_migration_control_records(pg_conn):
    """Получение записей из системы контроля миграции"""
    try:
        cursor = pg_conn.cursor()
        
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
        WHERE o.object_type = 'TABLE'
        ORDER BY so.name_in_mssql
        """
        
        cursor.execute(query)
        records = cursor.fetchall()
        
        return records
        
    except Exception as e:
        logging.error(f"Ошибка получения записей из системы контроля: {e}")
        return []

def find_name_mismatches(sqlserver_tables, postgres_tables, control_records):
    """Поиск несоответствий имен"""
    mismatches = []
    
    # Проверка записей в системе контроля
    for record in control_records:
        record_id, object_id, mssql_name, postgres_name, status, object_type = record
        
        # Проверка соответствия имени в SQL Server
        if mssql_name not in sqlserver_tables:
            mismatches.append({
                'type': 'mssql_name_not_found',
                'record_id': record_id,
                'mssql_name': mssql_name,
                'postgres_name': postgres_name,
                'status': status,
                'description': f'Имя {mssql_name} не найдено в SQL Server'
            })
        
        # Проверка соответствия имени в PostgreSQL
        if postgres_name and postgres_name not in postgres_tables:
            mismatches.append({
                'type': 'postgres_name_not_found',
                'record_id': record_id,
                'mssql_name': mssql_name,
                'postgres_name': postgres_name,
                'status': status,
                'description': f'Имя {postgres_name} не найдено в PostgreSQL'
            })
    
    # Поиск дублирования записей
    mssql_names = [record[2] for record in control_records]
    duplicates = [name for name in set(mssql_names) if mssql_names.count(name) > 1]
    
    for duplicate_name in duplicates:
        duplicate_records = [r for r in control_records if r[2] == duplicate_name]
        mismatches.append({
            'type': 'duplicate_records',
            'mssql_name': duplicate_name,
            'records': duplicate_records,
            'description': f'Найдено {len(duplicate_records)} записей для имени {duplicate_name}'
        })
    
    return mismatches

def fix_migration_control_records(pg_conn, mismatches, sqlserver_tables, postgres_tables):
    """Исправление записей в системе контроля миграции"""
    try:
        cursor = pg_conn.cursor()
        fixed_count = 0
        
        for mismatch in mismatches:
            if mismatch['type'] == 'mssql_name_not_found':
                # Удаление записи с неправильным именем
                cursor.execute(
                    "DELETE FROM migration_control.specific_objects WHERE id = %s",
                    (mismatch['record_id'],)
                )
                logging.info(f"Удалена запись {mismatch['record_id']} с неправильным именем {mismatch['mssql_name']}")
                fixed_count += 1
                
            elif mismatch['type'] == 'duplicate_records':
                # Обработка дублирующихся записей
                records = mismatch['records']
                if len(records) > 1:
                    # Оставляем первую запись, удаляем остальные
                    for record in records[1:]:
                        cursor.execute(
                            "DELETE FROM migration_control.specific_objects WHERE id = %s",
                            (record[0],)
                        )
                        logging.info(f"Удалена дублирующаяся запись {record[0]} для имени {mismatch['mssql_name']}")
                        fixed_count += 1
        
        pg_conn.commit()
        logging.info(f"Исправлено {fixed_count} записей в системе контроля")
        
        return fixed_count
        
    except Exception as e:
        logging.error(f"Ошибка исправления записей: {e}")
        pg_conn.rollback()
        return 0

def create_correct_records(pg_conn, sqlserver_tables, postgres_tables):
    """Создание правильных записей для отсутствующих таблиц"""
    try:
        cursor = pg_conn.cursor()
        created_count = 0
        
        # Получение ID типа объекта TABLE
        cursor.execute("SELECT id FROM migration_control.objects WHERE object_type = 'TABLE'")
        table_object_id = cursor.fetchone()[0]
        
        # Получение существующих записей
        cursor.execute("SELECT name_in_mssql FROM migration_control.specific_objects WHERE object_id = %s", (table_object_id,))
        existing_names = [row[0] for row in cursor.fetchall()]
        
        # Создание записей для таблиц из SQL Server
        for mssql_name, mssql_info in sqlserver_tables.items():
            if mssql_name not in existing_names:
                # Определение соответствующего имени в PostgreSQL
                postgres_name = None
                migration_status = 'pending'
                
                # Поиск соответствующей таблицы в PostgreSQL (с учетом регистра)
                for pg_name in postgres_tables.keys():
                    if pg_name.lower() == mssql_name.lower():
                        postgres_name = pg_name
                        migration_status = 'completed'
                        break
                
                # Вставка записи
                cursor.execute("""
                    INSERT INTO migration_control.specific_objects 
                    (object_id, name_in_mssql, name_in_postgres, migration_status)
                    VALUES (%s, %s, %s, %s)
                """, (table_object_id, mssql_name, postgres_name, migration_status))
                
                logging.info(f"Создана запись для таблицы {mssql_name} -> {postgres_name} (статус: {migration_status})")
                created_count += 1
        
        pg_conn.commit()
        logging.info(f"Создано {created_count} новых записей")
        
        return created_count
        
    except Exception as e:
        logging.error(f"Ошибка создания записей: {e}")
        pg_conn.rollback()
        return 0

def main():
    """Основная функция"""
    logging.info("Начало исправления имен объектов в системе контроля миграции")
    
    # Получение подключений
    mssql_conn = get_mssql_connection()
    pg_conn = get_pg_connection()
    
    if not mssql_conn or not pg_conn:
        return
    
    try:
        # Получение данных из всех источников
        logging.info("Получение таблиц из SQL Server...")
        sqlserver_tables = get_sqlserver_tables_exact_names(mssql_conn)
        logging.info(f"Найдено таблиц в SQL Server: {len(sqlserver_tables)}")
        
        logging.info("Получение таблиц из PostgreSQL...")
        postgres_tables = get_postgres_tables_exact_names(pg_conn)
        logging.info(f"Найдено таблиц в PostgreSQL: {len(postgres_tables)}")
        
        logging.info("Получение записей из системы контроля...")
        control_records = get_migration_control_records(pg_conn)
        logging.info(f"Найдено записей в системе контроля: {len(control_records)}")
        
        # Поиск несоответствий
        logging.info("Поиск несоответствий имен...")
        mismatches = find_name_mismatches(sqlserver_tables, postgres_tables, control_records)
        
        if mismatches:
            logging.warning(f"Найдено {len(mismatches)} несоответствий:")
            for mismatch in mismatches:
                logging.warning(f"  - {mismatch['description']}")
            
            # Исправление записей
            logging.info("Исправление записей в системе контроля...")
            fixed_count = fix_migration_control_records(pg_conn, mismatches, sqlserver_tables, postgres_tables)
            
            # Создание правильных записей
            logging.info("Создание правильных записей...")
            created_count = create_correct_records(pg_conn, sqlserver_tables, postgres_tables)
            
            logging.info(f"Исправлено записей: {fixed_count}")
            logging.info(f"Создано записей: {created_count}")
        else:
            logging.info("Несоответствий не найдено")
        
        # Создание отчета
        report = {
            'timestamp': datetime.now().isoformat(),
            'sqlserver_tables': len(sqlserver_tables),
            'postgres_tables': len(postgres_tables),
            'control_records_before': len(control_records),
            'mismatches_found': len(mismatches),
            'mismatches_details': mismatches,
            'log_file': log_file
        }
        
        # Сохранение отчета
        report_dir = "/home/alex/vuege/docs/infrastructure/reports"
        os.makedirs(report_dir, exist_ok=True)
        report_file = f"{report_dir}/fix-migration-control-names-report-{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        
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
    
    logging.info("Исправление имен объектов завершено")

if __name__ == "__main__":
    main()