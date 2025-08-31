#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Исправление проблем с UUID типами в схеме AGS
Автор: AI Assistant
Дата: 30 августа 2025
"""

import pymssql
import psycopg2
import psycopg2.extras
import logging
import sys
import os
import uuid
from datetime import datetime

# Настройка логирования
def setup_logging():
    """Настройка логирования"""
    # Создаем папку logs если её нет
    logs_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'logs')
    os.makedirs(logs_dir, exist_ok=True)
    
    log_file = os.path.join(logs_dir, f'fix-uuid-{datetime.now().strftime("%Y%m%d_%H%M%S")}.log')
    
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler(log_file),
            logging.StreamHandler(sys.stdout)
        ]
    )
    return logging.getLogger(__name__)

# Проблемные таблицы с UUID
PROBLEMATIC_TABLES = [
    'cstAg',
    'cstAgPn', 
    'ogAg'
]

def connect_databases():
    """Подключение к базам данных"""
    try:
        # SQL Server
        mssql_conn = pymssql.connect(
            server='localhost',
            port=1433,
            user='sa',
            password='Vuege2024!',
            database='Fish_Eye'
        )
        
        # PostgreSQL
        pg_conn = psycopg2.connect(
            host='localhost',
            port=5432,
            database='vuege',
            user='testuser',
            password='testpass'
        )
        
        logging.info("✅ Подключения к базам данных установлены")
        return mssql_conn, pg_conn
        
    except Exception as e:
        logging.error(f"❌ Ошибка подключения к базам данным: {e}")
        raise

def get_table_schema_from_mssql(mssql_conn, table_name):
    """Получение схемы таблицы из SQL Server"""
    try:
        cursor = mssql_conn.cursor()
        query = f"""
        SELECT 
            COLUMN_NAME,
            DATA_TYPE,
            IS_NULLABLE,
            CHARACTER_MAXIMUM_LENGTH,
            NUMERIC_PRECISION,
            NUMERIC_SCALE
        FROM INFORMATION_SCHEMA.COLUMNS 
        WHERE TABLE_NAME = '{table_name}'
        ORDER BY ORDINAL_POSITION
        """
        cursor.execute(query)
        columns = cursor.fetchall()
        cursor.close()
        
        schema = []
        for col in columns:
            column_info = {
                'name': col[0].lower(),
                'type': col[1],
                'nullable': col[2] == 'YES',
                'max_length': col[3],
                'precision': col[4],
                'scale': col[5]
            }
            schema.append(column_info)
        
        return schema
        
    except Exception as e:
        logging.error(f"❌ Ошибка получения схемы таблицы {table_name}: {e}")
        raise

def map_sql_to_pg_type_with_uuid_fix(column_info):
    """Маппинг типов SQL Server в PostgreSQL с исправлением UUID"""
    sql_type = column_info['type'].lower()
    
    if sql_type in ['int', 'bigint', 'smallint', 'tinyint']:
        return 'integer'
    elif sql_type in ['decimal', 'numeric']:
        if column_info['precision'] and column_info['scale']:
            return f"numeric({column_info['precision']},{column_info['scale']})"
        return 'numeric'
    elif sql_type in ['varchar', 'nvarchar', 'char', 'nchar']:
        if column_info['max_length']:
            return f"varchar({column_info['max_length']})"
        return 'varchar'
    elif sql_type in ['text', 'ntext']:
        return 'text'
    elif sql_type in ['datetime', 'datetime2', 'smalldatetime']:
        return 'timestamp'
    elif sql_type in ['date']:
        return 'date'
    elif sql_type in ['time']:
        return 'time'
    elif sql_type in ['bit']:
        return 'boolean'
    elif sql_type in ['uniqueidentifier']:
        return 'text'  # UUID всегда как text
    elif sql_type in ['money', 'smallmoney']:
        return 'numeric(19,4)'
    else:
        return 'text'

def create_table_in_pg_with_uuid_fix(pg_conn, table_name, schema):
    """Создание таблицы в PostgreSQL с исправлением UUID"""
    try:
        cursor = pg_conn.cursor()
        
        # Генерация SQL для создания таблицы
        columns_sql = []
        for col in schema:
            pg_type = map_sql_to_pg_type_with_uuid_fix(col)
            nullable = "" if col['nullable'] else " NOT NULL"
            columns_sql.append(f'"{col["name"]}" {pg_type}{nullable}')
        
        create_sql = f"""
        CREATE TABLE IF NOT EXISTS ags."{table_name.lower()}" (
            {', '.join(columns_sql)}
        )
        """
        
        cursor.execute(create_sql)
        pg_conn.commit()
        cursor.close()
        
        logging.info(f"✅ Таблица ags.{table_name.lower()} создана с исправлением UUID")
        return True
        
    except Exception as e:
        logging.error(f"❌ Ошибка создания таблицы {table_name}: {e}")
        pg_conn.rollback()
        return False

def convert_uuid_to_text(value):
    """Конвертация UUID в text"""
    if isinstance(value, uuid.UUID):
        return str(value)
    elif value is None:
        return None
    else:
        return str(value)

def migrate_table_data_with_uuid_fix(mssql_conn, pg_conn, table_name):
    """Миграция данных таблицы с исправлением UUID"""
    try:
        # Получаем данные из SQL Server
        mssql_cursor = mssql_conn.cursor()
        query = f"SELECT * FROM ags.{table_name}"
        mssql_cursor.execute(query)
        rows = mssql_cursor.fetchall()
        mssql_cursor.close()
        
        if not rows:
            logging.info(f"📋 Таблица {table_name} пустая, пропускаем")
            return True
        
        # Получаем имена колонок
        mssql_cursor = mssql_conn.cursor()
        mssql_cursor.execute(f"SELECT * FROM ags.{table_name} WHERE 1=0")
        column_names = [desc[0].lower() for desc in mssql_cursor.description]
        mssql_cursor.close()
        
        # Вставляем данные в PostgreSQL
        pg_cursor = pg_conn.cursor()
        
        # Подготавливаем SQL для вставки
        placeholders = ', '.join(['%s'] * len(column_names))
        column_names_quoted = ', '.join([f'"{name}"' for name in column_names])
        
        insert_sql = f"""
        INSERT INTO ags."{table_name.lower()}" ({column_names_quoted})
        VALUES ({placeholders})
        """
        
        # Вставляем данные пакетами
        batch_size = 1000
        total_rows = len(rows)
        
        for i in range(0, total_rows, batch_size):
            batch = rows[i:i + batch_size]
            
            # Конвертируем данные с исправлением UUID
            converted_batch = []
            for row in batch:
                converted_row = []
                for value in row:
                    converted_value = convert_uuid_to_text(value)
                    converted_row.append(converted_value)
                converted_batch.append(converted_row)
            
            pg_cursor.executemany(insert_sql, converted_batch)
            
            if i + batch_size < total_rows:
                logging.info(f"   📊 Прогресс: {i + batch_size}/{total_rows} записей")
        
        pg_conn.commit()
        pg_cursor.close()
        
        logging.info(f"✅ Данные таблицы {table_name} мигрированы с исправлением UUID ({total_rows} записей)")
        return True
        
    except Exception as e:
        logging.error(f"❌ Ошибка миграции данных таблицы {table_name}: {e}")
        pg_conn.rollback()
        return False

def fix_table_uuid_issues(mssql_conn, pg_conn, table_name):
    """Исправление проблем с UUID для одной таблицы"""
    try:
        logging.info(f"🔧 Исправление UUID таблицы: {table_name}")
        
        # Получаем схему из SQL Server
        schema = get_table_schema_from_mssql(mssql_conn, table_name)
        logging.info(f"   📋 Найдено {len(schema)} колонок")
        
        # Проверяем наличие UUID колонок
        uuid_columns = [col for col in schema if col['type'].lower() == 'uniqueidentifier']
        if uuid_columns:
            logging.info(f"   🔍 Найдено {len(uuid_columns)} UUID колонок: {[col['name'] for col in uuid_columns]}")
        
        # Создаем таблицу в PostgreSQL
        if not create_table_in_pg_with_uuid_fix(pg_conn, table_name, schema):
            return False
        
        # Мигрируем данные
        if not migrate_table_data_with_uuid_fix(mssql_conn, pg_conn, table_name):
            return False
        
        logging.info(f"✅ Таблица {table_name} исправлена успешно")
        return True
        
    except Exception as e:
        logging.error(f"❌ Критическая ошибка при исправлении {table_name}: {e}")
        return False

def main():
    """Основная функция"""
    logger = setup_logging()
    
    logging.info("🔧 ИСПРАВЛЕНИЕ ПРОБЛЕМ С UUID ТИПАМИ")
    logging.info("=" * 60)
    
    try:
        # Подключение к базам данных
        mssql_conn, pg_conn = connect_databases()
        
        # Обработка каждой проблемной таблицы
        success_count = 0
        error_count = 0
        
        for i, table_name in enumerate(PROBLEMATIC_TABLES, 1):
            logging.info(f"📋 [{i}/{len(PROBLEMATIC_TABLES)}] Обработка таблицы: {table_name}")
            
            if fix_table_uuid_issues(mssql_conn, pg_conn, table_name):
                success_count += 1
            else:
                error_count += 1
        
        # Закрытие соединений
        mssql_conn.close()
        pg_conn.close()
        
        # Итоговый отчет
        logging.info("=" * 60)
        logging.info("📊 ИТОГОВЫЙ ОТЧЕТ ИСПРАВЛЕНИЯ UUID")
        logging.info("=" * 60)
        logging.info(f"📋 Всего таблиц: {len(PROBLEMATIC_TABLES)}")
        logging.info(f"✅ Успешно исправлено: {success_count}")
        logging.info(f"❌ Ошибки исправления: {error_count}")
        logging.info(f"📈 Процент успеха: {(success_count/len(PROBLEMATIC_TABLES)*100):.1f}%")
        
        if error_count == 0:
            logging.info("🎉 ВСЕ ПРОБЛЕМЫ С UUID ИСПРАВЛЕНЫ!")
        else:
            logging.warning(f"⚠️ Осталось {error_count} проблемных таблиц")
        
    except Exception as e:
        logging.error(f"❌ Критическая ошибка: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()