#!/usr/bin/env python3
"""
Скрипт для исправления представлений в схеме контроля миграции
"""

import psycopg2
import psycopg2.extras
import logging
from datetime import datetime
import json
import os

# Настройка логирования
log_dir = "/home/alex/vuege/docs/infrastructure/logs"
os.makedirs(log_dir, exist_ok=True)
log_file = f"{log_dir}/fix-migration-control-views-{datetime.now().strftime('%Y%m%d_%H%M%S')}.log"

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(log_file, encoding='utf-8'),
        logging.StreamHandler()
    ]
)

# Параметры подключения к PostgreSQL
PG_HOST = "localhost"
PG_PORT = 5432
PG_DB = "vuege"
PG_USER = "postgres"
PG_PASSWORD = "testpass"

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

def fix_migration_control_views(pg_conn):
    """Исправление представлений в схеме контроля миграции"""
    try:
        cursor = pg_conn.cursor()
        
        # Удаление существующих представлений
        drop_views_query = """
        DROP VIEW IF EXISTS migration_control.migration_progress CASCADE;
        DROP VIEW IF EXISTS migration_control.detailed_progress CASCADE;
        """
        cursor.execute(drop_views_query)
        logging.info("Существующие представления удалены")
        
        # Создание обновленного представления migration_progress
        create_migration_progress_view_query = """
        CREATE VIEW migration_control.migration_progress AS
        SELECT 
            mt.description as migration_task,
            o.object_type,
            o.has_in_mssql,
            o.has_in_postgres,
            COUNT(so.id) as total_objects,
            COUNT(CASE WHEN so.migration_status = 'completed' THEN 1 END) as completed_objects,
            COUNT(CASE WHEN so.migration_status = 'failed' THEN 1 END) as failed_objects,
            COUNT(CASE WHEN so.migration_status = 'pending' THEN 1 END) as pending_objects,
            CASE 
                WHEN COUNT(so.id) > 0 THEN 
                    ROUND((COUNT(CASE WHEN so.migration_status = 'completed' THEN 1 END)::DECIMAL / COUNT(so.id)::DECIMAL) * 100, 2)
                ELSE 0 
            END as completion_percentage
        FROM migration_control.migration_tasks mt
        LEFT JOIN migration_control.objects o ON mt.id = o.task_id
        LEFT JOIN migration_control.specific_objects so ON o.id = so.object_id
        GROUP BY mt.id, mt.description, o.object_type, o.has_in_mssql, o.has_in_postgres
        ORDER BY mt.description, o.object_type;
        """
        cursor.execute(create_migration_progress_view_query)
        logging.info("Представление migration_progress создано")
        
        # Создание обновленного представления detailed_progress
        create_detailed_progress_view_query = """
        CREATE VIEW migration_control.detailed_progress AS
        SELECT 
            mt.description as migration_task,
            o.id as object_id,
            o.object_type,
            o.name_in_mssql as object_name_mssql,
            o.name_in_postgres as object_name_postgres,
            o.has_in_mssql,
            o.has_in_postgres,
            so.id as specific_object_id,
            so.name_in_mssql as specific_name_mssql,
            so.name_in_postgres as specific_name_postgres,
            so.migration_status,
            so.migration_date,
            so.error_message,
            so.created_at,
            so.updated_at
        FROM migration_control.migration_tasks mt
        LEFT JOIN migration_control.objects o ON mt.id = o.task_id
        LEFT JOIN migration_control.specific_objects so ON o.id = so.object_id
        ORDER BY mt.description, o.object_type, o.name_in_mssql, so.name_in_mssql;
        """
        cursor.execute(create_detailed_progress_view_query)
        logging.info("Представление detailed_progress создано")
        
        pg_conn.commit()
        logging.info("Представления успешно исправлены")
        
        return True
        
    except Exception as e:
        logging.error(f"Ошибка исправления представлений: {e}")
        pg_conn.rollback()
        return False

def main():
    """Основная функция"""
    logging.info("Начало исправления представлений в схеме контроля миграции")
    
    # Получение подключения
    pg_conn = get_pg_connection()
    if not pg_conn:
        return
    
    try:
        # Исправление представлений
        success = fix_migration_control_views(pg_conn)
        
        if success:
            logging.info("=== ПРЕДСТАВЛЕНИЯ ИСПРАВЛЕНЫ ===")
            logging.info("Обновленные представления:")
            logging.info("  - migration_control.migration_progress")
            logging.info("  - migration_control.detailed_progress")
            logging.info("Представления теперь включают информацию о задачах миграции")
        else:
            logging.error("Ошибка исправления представлений")
        
    except Exception as e:
        logging.error(f"Ошибка в основной функции: {e}")
    
    finally:
        if pg_conn:
            pg_conn.close()
    
    logging.info("Исправление представлений завершено")

if __name__ == "__main__":
    main()