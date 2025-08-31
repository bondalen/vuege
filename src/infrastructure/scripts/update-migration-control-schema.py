#!/usr/bin/env python3
"""
Скрипт для обновления схемы контроля миграции
Добавляет таблицу задач миграции и исправляет структуру существующих таблиц
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
log_file = f"{log_dir}/update-migration-control-schema-{datetime.now().strftime('%Y%m%d_%H%M%S')}.log"

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

def update_migration_control_schema(pg_conn):
    """Обновление схемы контроля миграции"""
    try:
        cursor = pg_conn.cursor()
        
        # Создание таблицы задач миграции
        create_migration_tasks_table_query = """
        CREATE TABLE IF NOT EXISTS migration_control.migration_tasks (
            id SERIAL PRIMARY KEY,
            description TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );
        """
        cursor.execute(create_migration_tasks_table_query)
        logging.info("Таблица migration_control.migration_tasks создана")
        
        # Добавление поля task_id в таблицу objects
        add_task_id_to_objects_query = """
        ALTER TABLE migration_control.objects 
        ADD COLUMN IF NOT EXISTS task_id INTEGER REFERENCES migration_control.migration_tasks(id);
        """
        cursor.execute(add_task_id_to_objects_query)
        logging.info("Поле task_id добавлено в таблицу objects")
        
        # Создание индекса для task_id
        create_task_id_index_query = """
        CREATE INDEX IF NOT EXISTS idx_objects_task_id ON migration_control.objects(task_id);
        """
        cursor.execute(create_task_id_index_query)
        logging.info("Индекс для task_id создан")
        
        # Обновление представления migration_progress
        update_migration_progress_view_query = """
        CREATE OR REPLACE VIEW migration_control.migration_progress AS
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
        cursor.execute(update_migration_progress_view_query)
        logging.info("Представление migration_progress обновлено")
        
        # Обновление представления detailed_progress
        update_detailed_progress_view_query = """
        CREATE OR REPLACE VIEW migration_control.detailed_progress AS
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
        cursor.execute(update_detailed_progress_view_query)
        logging.info("Представление detailed_progress обновлено")
        
        # Создание триггера для обновления timestamp в migration_tasks
        create_migration_tasks_trigger_query = """
        DROP TRIGGER IF EXISTS update_migration_tasks_updated_at ON migration_control.migration_tasks;
        CREATE TRIGGER update_migration_tasks_updated_at 
            BEFORE UPDATE ON migration_control.migration_tasks 
            FOR EACH ROW EXECUTE FUNCTION migration_control.update_updated_at_column();
        """
        cursor.execute(create_migration_tasks_trigger_query)
        logging.info("Триггер для migration_tasks создан")
        
        pg_conn.commit()
        logging.info("Схема контроля миграции успешно обновлена")
        
        return True
        
    except Exception as e:
        logging.error(f"Ошибка обновления схемы: {e}")
        pg_conn.rollback()
        return False

def insert_migration_task(pg_conn, description):
    """Вставка задачи миграции"""
    try:
        cursor = pg_conn.cursor()
        
        query = """
        INSERT INTO migration_control.migration_tasks (description)
        VALUES (%s)
        RETURNING id;
        """
        
        cursor.execute(query, (description,))
        task_id = cursor.fetchone()[0]
        
        pg_conn.commit()
        logging.info(f"Задача миграции '{description}' создана с ID: {task_id}")
        
        return task_id
        
    except Exception as e:
        logging.error(f"Ошибка создания задачи миграции: {e}")
        pg_conn.rollback()
        return None

def clear_existing_data(pg_conn):
    """Очистка существующих данных для перезаполнения с правильными именами"""
    try:
        cursor = pg_conn.cursor()
        
        # Очистка таблиц в правильном порядке
        cursor.execute("DELETE FROM migration_control.specific_objects;")
        cursor.execute("DELETE FROM migration_control.objects;")
        cursor.execute("DELETE FROM migration_control.migration_tasks;")
        
        # Сброс последовательностей
        cursor.execute("ALTER SEQUENCE migration_control.migration_tasks_id_seq RESTART WITH 1;")
        cursor.execute("ALTER SEQUENCE migration_control.objects_id_seq RESTART WITH 1;")
        cursor.execute("ALTER SEQUENCE migration_control.specific_objects_id_seq RESTART WITH 1;")
        
        pg_conn.commit()
        logging.info("Существующие данные очищены")
        
    except Exception as e:
        logging.error(f"Ошибка очистки данных: {e}")
        pg_conn.rollback()

def main():
    """Основная функция"""
    logging.info("Начало обновления схемы контроля миграции")
    
    # Получение подключения
    pg_conn = get_pg_connection()
    if not pg_conn:
        return
    
    try:
        # Обновление схемы
        success = update_migration_control_schema(pg_conn)
        
        if success:
            logging.info("=== СХЕМА КОНТРОЛЯ МИГРАЦИИ ОБНОВЛЕНА ===")
            logging.info("Добавленные объекты:")
            logging.info("  - Таблица: migration_control.migration_tasks")
            logging.info("  - Поле: task_id в таблице objects")
            logging.info("  - Индекс: idx_objects_task_id")
            logging.info("  - Обновлены представления: migration_progress, detailed_progress")
            logging.info("  - Триггер: update_migration_tasks_updated_at")
            
            # Очистка существующих данных
            clear_existing_data(pg_conn)
            
            # Создание задачи миграции
            task_id = insert_migration_task(pg_conn, "миграция схемы ags")
            
            if task_id:
                logging.info(f"Задача миграции создана с ID: {task_id}")
                logging.info("Готово к заполнению данными с правильными именами объектов")
            else:
                logging.error("Ошибка создания задачи миграции")
        else:
            logging.error("Ошибка обновления схемы контроля миграции")
        
    except Exception as e:
        logging.error(f"Ошибка в основной функции: {e}")
    
    finally:
        if pg_conn:
            pg_conn.close()
    
    logging.info("Обновление схемы контроля миграции завершено")

if __name__ == "__main__":
    main()