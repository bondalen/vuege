#!/usr/bin/env python3
"""
Скрипт для создания схемы контроля миграции в PostgreSQL
Создает схему migration_control с таблицами для учета мигрирующих объектов
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
log_file = f"{log_dir}/create-migration-control-schema-{datetime.now().strftime('%Y%m%d_%H%M%S')}.log"

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

def create_migration_control_schema(pg_conn):
    """Создание схемы контроля миграции"""
    try:
        cursor = pg_conn.cursor()
        
        # Создание схемы
        create_schema_query = """
        CREATE SCHEMA IF NOT EXISTS migration_control;
        """
        cursor.execute(create_schema_query)
        logging.info("Схема migration_control создана")
        
        # Создание таблицы объектов
        create_objects_table_query = """
        CREATE TABLE IF NOT EXISTS migration_control.objects (
            id SERIAL PRIMARY KEY,
            has_in_mssql BOOLEAN NOT NULL DEFAULT false,
            has_in_postgres BOOLEAN NOT NULL DEFAULT false,
            object_type VARCHAR(50) NOT NULL,
            name_in_mssql VARCHAR(255),
            name_in_postgres VARCHAR(255),
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );
        """
        cursor.execute(create_objects_table_query)
        logging.info("Таблица migration_control.objects создана")
        
        # Создание таблицы конкретных объектов
        create_specific_objects_table_query = """
        CREATE TABLE IF NOT EXISTS migration_control.specific_objects (
            id SERIAL PRIMARY KEY,
            object_id INTEGER NOT NULL REFERENCES migration_control.objects(id) ON DELETE CASCADE,
            name_in_mssql VARCHAR(255) NOT NULL,
            name_in_postgres VARCHAR(255),
            migration_status VARCHAR(50) DEFAULT 'pending',
            migration_date TIMESTAMP,
            error_message TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );
        """
        cursor.execute(create_specific_objects_table_query)
        logging.info("Таблица migration_control.specific_objects создана")
        
        # Создание индексов
        create_indexes_query = """
        CREATE INDEX IF NOT EXISTS idx_objects_type ON migration_control.objects(object_type);
        CREATE INDEX IF NOT EXISTS idx_objects_mssql ON migration_control.objects(has_in_mssql);
        CREATE INDEX IF NOT EXISTS idx_objects_postgres ON migration_control.objects(has_in_postgres);
        CREATE INDEX IF NOT EXISTS idx_specific_objects_object_id ON migration_control.specific_objects(object_id);
        CREATE INDEX IF NOT EXISTS idx_specific_objects_status ON migration_control.specific_objects(migration_status);
        """
        cursor.execute(create_indexes_query)
        logging.info("Индексы созданы")
        
        # Создание представления для прогресса миграции
        create_progress_view_query = """
        CREATE OR REPLACE VIEW migration_control.migration_progress AS
        SELECT 
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
        FROM migration_control.objects o
        LEFT JOIN migration_control.specific_objects so ON o.id = so.object_id
        GROUP BY o.object_type, o.has_in_mssql, o.has_in_postgres
        ORDER BY o.object_type;
        """
        cursor.execute(create_progress_view_query)
        logging.info("Представление migration_control.migration_progress создано")
        
        # Создание представления для детального прогресса
        create_detailed_progress_view_query = """
        CREATE OR REPLACE VIEW migration_control.detailed_progress AS
        SELECT 
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
        FROM migration_control.objects o
        LEFT JOIN migration_control.specific_objects so ON o.id = so.object_id
        ORDER BY o.object_type, o.name_in_mssql, so.name_in_mssql;
        """
        cursor.execute(create_detailed_progress_view_query)
        logging.info("Представление migration_control.detailed_progress создано")
        
        # Создание функции для обновления timestamp
        create_update_timestamp_function_query = """
        CREATE OR REPLACE FUNCTION migration_control.update_updated_at_column()
        RETURNS TRIGGER AS $$
        BEGIN
            NEW.updated_at = CURRENT_TIMESTAMP;
            RETURN NEW;
        END;
        $$ language 'plpgsql';
        """
        cursor.execute(create_update_timestamp_function_query)
        logging.info("Функция update_updated_at_column создана")
        
        # Создание триггеров для автоматического обновления timestamp
        create_triggers_query = """
        DROP TRIGGER IF EXISTS update_objects_updated_at ON migration_control.objects;
        CREATE TRIGGER update_objects_updated_at 
            BEFORE UPDATE ON migration_control.objects 
            FOR EACH ROW EXECUTE FUNCTION migration_control.update_updated_at_column();
            
        DROP TRIGGER IF EXISTS update_specific_objects_updated_at ON migration_control.specific_objects;
        CREATE TRIGGER update_specific_objects_updated_at 
            BEFORE UPDATE ON migration_control.specific_objects 
            FOR EACH ROW EXECUTE FUNCTION migration_control.update_updated_at_column();
        """
        cursor.execute(create_triggers_query)
        logging.info("Триггеры для обновления timestamp созданы")
        
        pg_conn.commit()
        logging.info("Схема контроля миграции успешно создана")
        
        return True
        
    except Exception as e:
        logging.error(f"Ошибка создания схемы контроля миграции: {e}")
        pg_conn.rollback()
        return False

def main():
    """Основная функция"""
    logging.info("Начало создания схемы контроля миграции")
    
    # Получение подключения
    pg_conn = get_pg_connection()
    if not pg_conn:
        return
    
    try:
        # Создание схемы контроля миграции
        success = create_migration_control_schema(pg_conn)
        
        if success:
            logging.info("=== СХЕМА КОНТРОЛЯ МИГРАЦИИ СОЗДАНА УСПЕШНО ===")
            logging.info("Созданные объекты:")
            logging.info("  - Схема: migration_control")
            logging.info("  - Таблица: migration_control.objects")
            logging.info("  - Таблица: migration_control.specific_objects")
            logging.info("  - Представление: migration_control.migration_progress")
            logging.info("  - Представление: migration_control.detailed_progress")
            logging.info("  - Функция: migration_control.update_updated_at_column()")
            logging.info("  - Триггеры для автоматического обновления timestamp")
            logging.info("  - Индексы для оптимизации запросов")
        else:
            logging.error("Ошибка создания схемы контроля миграции")
        
    except Exception as e:
        logging.error(f"Ошибка в основной функции: {e}")
    
    finally:
        if pg_conn:
            pg_conn.close()
    
    logging.info("Создание схемы контроля миграции завершено")

if __name__ == "__main__":
    main()