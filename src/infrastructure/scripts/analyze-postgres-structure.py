#!/usr/bin/env python3
"""
Скрипт для анализа структуры таблиц в PostgreSQL
Получает правильные имена колонок для создания первичных ключей
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
log_file = f"{log_dir}/analyze-postgres-structure-{datetime.now().strftime('%Y%m%d_%H%M%S')}.log"

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

def get_connection():
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

def get_table_columns(conn, table_name):
    """Получение списка колонок таблицы"""
    try:
        cursor = conn.cursor()
        
        query = """
        SELECT column_name, data_type, is_nullable
        FROM information_schema.columns
        WHERE table_schema = 'ags' 
        AND table_name = %s
        ORDER BY ordinal_position
        """
        
        cursor.execute(query, (table_name,))
        columns = cursor.fetchall()
        
        return [col[0] for col in columns]
        
    except Exception as e:
        logging.error(f"Ошибка получения колонок для таблицы {table_name}: {e}")
        return []

def get_existing_primary_keys(conn):
    """Получение существующих первичных ключей"""
    try:
        cursor = conn.cursor()
        
        query = """
        SELECT 
            tc.table_name,
            kcu.column_name
        FROM information_schema.table_constraints tc
        JOIN information_schema.key_column_usage kcu 
            ON tc.constraint_name = kcu.constraint_name
        WHERE tc.constraint_type = 'PRIMARY KEY'
        AND tc.table_schema = 'ags'
        ORDER BY tc.table_name, kcu.ordinal_position
        """
        
        cursor.execute(query)
        results = cursor.fetchall()
        
        # Группируем по таблицам
        primary_keys = {}
        for table_name, column_name in results:
            if table_name not in primary_keys:
                primary_keys[table_name] = []
            primary_keys[table_name].append(column_name)
        
        return primary_keys
        
    except Exception as e:
        logging.error(f"Ошибка получения первичных ключей: {e}")
        return {}

def analyze_table_structure(conn, table_name):
    """Анализ структуры таблицы"""
    try:
        cursor = conn.cursor()
        
        # Получаем колонки
        columns = get_table_columns(conn, table_name)
        
        # Получаем количество записей
        cursor.execute(f"SELECT COUNT(*) FROM ags.{table_name}")
        record_count = cursor.fetchone()[0]
        
        # Получаем информацию о первичном ключе
        cursor.execute(f"""
        SELECT 
            tc.constraint_name,
            kcu.column_name
        FROM information_schema.table_constraints tc
        JOIN information_schema.key_column_usage kcu 
            ON tc.constraint_name = kcu.constraint_name
        WHERE tc.constraint_type = 'PRIMARY KEY'
        AND tc.table_schema = 'ags'
        AND tc.table_name = %s
        ORDER BY kcu.ordinal_position
        """, (table_name,))
        
        pk_columns = [row[1] for row in cursor.fetchall()]
        
        return {
            'table_name': table_name,
            'columns': columns,
            'record_count': record_count,
            'has_primary_key': len(pk_columns) > 0,
            'primary_key_columns': pk_columns
        }
        
    except Exception as e:
        logging.error(f"Ошибка анализа структуры таблицы {table_name}: {e}")
        return None

def main():
    """Основная функция"""
    logging.info("Начало анализа структуры PostgreSQL")
    
    # Получение подключения
    conn = get_connection()
    if not conn:
        return
    
    try:
        cursor = conn.cursor()
        
        # Получаем список всех таблиц в схеме ags
        cursor.execute("""
        SELECT table_name 
        FROM information_schema.tables 
        WHERE table_schema = 'ags' 
        AND table_type = 'BASE TABLE'
        ORDER BY table_name
        """)
        
        tables = [row[0] for row in cursor.fetchall()]
        logging.info(f"Найдено таблиц в схеме ags: {len(tables)}")
        
        # Получаем существующие первичные ключи
        existing_pks = get_existing_primary_keys(conn)
        logging.info(f"Найдено таблиц с первичными ключами: {len(existing_pks)}")
        
        # Анализируем структуру каждой таблицы
        table_structures = {}
        
        for table_name in tables:
            logging.info(f"Анализ таблицы: {table_name}")
            structure = analyze_table_structure(conn, table_name)
            if structure:
                table_structures[table_name] = structure
        
        # Создаем отчет
        report = {
            'timestamp': datetime.now().isoformat(),
            'total_tables': len(tables),
            'tables_with_pk': len(existing_pks),
            'table_structures': table_structures,
            'existing_primary_keys': existing_pks,
            'log_file': log_file
        }
        
        # Сохранение отчета
        report_dir = "/home/alex/vuege/docs/infrastructure/reports"
        os.makedirs(report_dir, exist_ok=True)
        report_file = f"{report_dir}/postgres-structure-analysis-{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        
        with open(report_file, 'w', encoding='utf-8') as f:
            json.dump(report, f, ensure_ascii=False, indent=2)
        
        # Вывод результатов
        logging.info("=== РЕЗУЛЬТАТЫ АНАЛИЗА ===")
        logging.info(f"Всего таблиц: {len(tables)}")
        logging.info(f"Таблиц с первичными ключами: {len(existing_pks)}")
        logging.info(f"Таблиц без первичных ключей: {len(tables) - len(existing_pks)}")
        
        # Показываем таблицы без первичных ключей
        tables_without_pk = [t for t in tables if t not in existing_pks]
        if tables_without_pk:
            logging.info("Таблицы без первичных ключей:")
            for table in tables_without_pk[:10]:  # Показываем первые 10
                logging.info(f"  - {table}")
            if len(tables_without_pk) > 10:
                logging.info(f"  ... и еще {len(tables_without_pk) - 10} таблиц")
        
        logging.info(f"Отчет сохранен: {report_file}")
        
    except Exception as e:
        logging.error(f"Ошибка в основной функции: {e}")
    
    finally:
        conn.close()
    
    logging.info("Анализ структуры PostgreSQL завершен")

if __name__ == "__main__":
    main()