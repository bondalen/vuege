#!/usr/bin/env python3
"""
Скрипт для создания таблицы задач миграции
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
log_file = f"{log_dir}/create-migration-tasks-table-{datetime.now().strftime('%Y%m%d_%H%M%S')}.log"

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

def create_migration_tasks_table(pg_conn):
    """Создание таблицы задач миграции"""
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
        logging.info("Таблица задач миграции успешно создана")
        
        return True
        
    except Exception as e:
        logging.error(f"Ошибка создания таблицы задач миграции: {e}")
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

def main():
    """Основная функция"""
    logging.info("Начало создания таблицы задач миграции")
    
    # Получение подключения
    pg_conn = get_pg_connection()
    if not pg_conn:
        return
    
    try:
        # Создание таблицы задач миграции
        success = create_migration_tasks_table(pg_conn)
        
        if success:
            logging.info("=== ТАБЛИЦА ЗАДАЧ МИГРАЦИИ СОЗДАНА ===")
            logging.info("Созданные объекты:")
            logging.info("  - Таблица: migration_control.migration_tasks")
            logging.info("  - Поле: task_id в таблице objects")
            logging.info("  - Индекс: idx_objects_task_id")
            logging.info("  - Триггер: update_migration_tasks_updated_at")
            
            # Создание задачи миграции
            task_id = insert_migration_task(pg_conn, "миграция схемы ags")
            
            if task_id:
                logging.info(f"Задача миграции создана с ID: {task_id}")
                logging.info("Готово к созданию представлений")
            else:
                logging.error("Ошибка создания задачи миграции")
        else:
            logging.error("Ошибка создания таблицы задач миграции")
        
    except Exception as e:
        logging.error(f"Ошибка в основной функции: {e}")
    
    finally:
        if pg_conn:
            pg_conn.close()
    
    logging.info("Создание таблицы задач миграции завершено")

if __name__ == "__main__":
    main()