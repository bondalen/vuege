#!/usr/bin/env python3
"""
Скрипт для очистки дублированных данных в PostgreSQL
Удаляет дубли в таблицах для возможности создания первичных ключей
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
log_file = f"{log_dir}/clean-duplicate-data-{datetime.now().strftime('%Y%m%d_%H%M%S')}.log"

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

def get_table_primary_keys():
    """Получение информации о первичных ключах из SQL Server"""
    # Данные о первичных ключах из предыдущего анализа
    primary_keys = {
        'org': ['ogkey'],
        'cn': ['cnkey'],
        'cn_inv': ['cnkey', 'invkey'],
        'cn_inv_dbt': ['cnkey', 'invkey', 'dbtkey'],
        'cn_inv_dbt_upl': ['cnkey', 'invkey', 'dbtkey', 'uplkey'],
        'cn_inv_dbt_upl_g_p': ['cnkey', 'invkey', 'dbtkey', 'uplkey', 'gkey', 'pkey'],
        'cn_inv_doc': ['cnkey', 'invkey', 'dockey'],
        'cn_inv_pm': ['cnkey', 'invkey', 'pmkey'],
        'cninvcmm': ['cnkey', 'invkey', 'cmmkey'],
        'cst': ['cstkey'],
        'cstag': ['cstkey', 'agkey'],
        'cstagpn': ['cstkey', 'agkey', 'pnkey'],
        'inv': ['invkey'],
        'invdbtvalue': ['invkey', 'dbtkey'],
        'ipgutplpncostits': ['ipgkey', 'utkey', 'plkey', 'pnkey', 'costkey', 'itkey'],
        'juundocchnggr': ['juundockey', 'chngkey', 'grkey'],
        'juundocchnggrrel': ['juundockey', 'chngkey', 'grkey', 'relkey'],
        'juundocprmrgrrel': ['juundockey', 'prmrkey', 'grkey', 'relkey'],
        'juundocside': ['juundockey', 'sidekey'],
        'juundocsideorg': ['juundockey', 'sidekey', 'orgkey'],
        'juundocsidetype': ['juundockey', 'sidekey', 'typekey'],
        'ogag': ['ogkey', 'agkey'],
        'ra_period': ['rakey', 'periodkey'],
        'rgtaxreordivismerg': ['rgkey', 'taxkey', 'reorkey', 'diviskey', 'mergkey'],
        'rgtaxreorseparmerg': ['rgkey', 'taxkey', 'reorkey', 'separkey', 'mergkey']
    }
    return primary_keys

def analyze_duplicates(conn, table_name, pk_columns):
    """Анализ дублированных данных в таблице"""
    try:
        cursor = conn.cursor()
        
        # Формируем условие для группировки по первичному ключу
        pk_condition = ", ".join(pk_columns)
        
        # Запрос для подсчета дублей
        query = f"""
        SELECT COUNT(*) as total_records,
               COUNT(*) - COUNT(DISTINCT ({pk_condition})) as duplicates
        FROM ags.{table_name}
        """
        
        cursor.execute(query)
        result = cursor.fetchone()
        
        if result:
            total_records, duplicates = result
            logging.info(f"Таблица {table_name}: {total_records} записей, {duplicates} дублей")
            return total_records, duplicates
        
        return 0, 0
        
    except Exception as e:
        logging.error(f"Ошибка анализа дублей в таблице {table_name}: {e}")
        return 0, 0

def clean_duplicates(conn, table_name, pk_columns):
    """Очистка дублированных данных в таблице"""
    try:
        cursor = conn.cursor()
        
        # Формируем условие для группировки по первичному ключу
        pk_condition = ", ".join(pk_columns)
        
        # Запрос для удаления дублей (оставляем только первую запись)
        query = f"""
        DELETE FROM ags.{table_name}
        WHERE ctid NOT IN (
            SELECT MIN(ctid)
            FROM ags.{table_name}
            GROUP BY {pk_condition}
        )
        """
        
        cursor.execute(query)
        deleted_count = cursor.rowcount
        conn.commit()
        
        logging.info(f"Удалено {deleted_count} дублей из таблицы {table_name}")
        return deleted_count
        
    except Exception as e:
        logging.error(f"Ошибка очистки дублей в таблице {table_name}: {e}")
        conn.rollback()
        return 0

def create_primary_key(conn, table_name, pk_columns):
    """Создание первичного ключа в таблице"""
    try:
        cursor = conn.cursor()
        
        # Формируем имя первичного ключа
        pk_name = f"pk_{table_name}"
        
        # Формируем список колонок для первичного ключа
        pk_columns_str = ", ".join(pk_columns)
        
        # Запрос для создания первичного ключа
        query = f"""
        ALTER TABLE ags.{table_name} 
        ADD CONSTRAINT {pk_name} PRIMARY KEY ({pk_columns_str})
        """
        
        cursor.execute(query)
        conn.commit()
        
        logging.info(f"Создан первичный ключ {pk_name} в таблице {table_name}")
        return True
        
    except Exception as e:
        logging.error(f"Ошибка создания первичного ключа в таблице {table_name}: {e}")
        conn.rollback()
        return False

def main():
    """Основная функция"""
    logging.info("Начало очистки дублированных данных")
    
    # Получение подключения
    conn = get_connection()
    if not conn:
        return
    
    # Получение информации о первичных ключах
    primary_keys = get_table_primary_keys()
    
    # Результаты очистки
    results = {
        'analyzed_tables': 0,
        'cleaned_tables': 0,
        'total_duplicates_removed': 0,
        'primary_keys_created': 0,
        'errors': []
    }
    
    try:
        for table_name, pk_columns in primary_keys.items():
            logging.info(f"Обработка таблицы: {table_name}")
            results['analyzed_tables'] += 1
            
            # Анализ дублей
            total_records, duplicates = analyze_duplicates(conn, table_name, pk_columns)
            
            if duplicates > 0:
                # Очистка дублей
                deleted_count = clean_duplicates(conn, table_name, pk_columns)
                results['total_duplicates_removed'] += deleted_count
                
                if deleted_count > 0:
                    results['cleaned_tables'] += 1
                    
                    # Создание первичного ключа
                    if create_primary_key(conn, table_name, pk_columns):
                        results['primary_keys_created'] += 1
            else:
                # Если дублей нет, пробуем создать первичный ключ
                if create_primary_key(conn, table_name, pk_columns):
                    results['primary_keys_created'] += 1
    
    except Exception as e:
        logging.error(f"Ошибка в основной функции: {e}")
        results['errors'].append(str(e))
    
    finally:
        conn.close()
    
    # Создание отчета
    report = {
        'timestamp': datetime.now().isoformat(),
        'results': results,
        'log_file': log_file
    }
    
    # Сохранение отчета
    report_dir = "/home/alex/vuege/docs/infrastructure/reports"
    os.makedirs(report_dir, exist_ok=True)
    report_file = f"{report_dir}/clean-duplicate-data-report-{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
    
    with open(report_file, 'w', encoding='utf-8') as f:
        json.dump(report, f, ensure_ascii=False, indent=2)
    
    # Вывод результатов
    logging.info("=== РЕЗУЛЬТАТЫ ОЧИСТКИ ===")
    logging.info(f"Проанализировано таблиц: {results['analyzed_tables']}")
    logging.info(f"Очищено таблиц: {results['cleaned_tables']}")
    logging.info(f"Удалено дублей: {results['total_duplicates_removed']}")
    logging.info(f"Создано первичных ключей: {results['primary_keys_created']}")
    
    if results['errors']:
        logging.error(f"Ошибки: {len(results['errors'])}")
        for error in results['errors']:
            logging.error(f"  - {error}")
    
    logging.info(f"Отчет сохранен: {report_file}")
    logging.info("Очистка дублированных данных завершена")

if __name__ == "__main__":
    main()