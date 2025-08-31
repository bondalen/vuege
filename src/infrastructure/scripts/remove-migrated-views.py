#!/usr/bin/env python3
"""
Скрипт для безопасного удаления мигрированных представлений из PostgreSQL
Удаляет объекты, которые были ошибочно мигрированы как таблицы, но являются представлениями в SQL Server
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
log_file = f"{log_dir}/remove-migrated-views-{datetime.now().strftime('%Y%m%d_%H%M%S')}.log"

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

# Список мигрированных представлений для удаления
MIGRATED_VIEWS = [
    'cn_inv_dbt_double',
    'cn_inv_dbt_upl_pm_upl',
    'dym_pm_pm',
    'q_cn_inv_dbt_upl_sum',
    'q_cn_inv_pm_upl_sum',
    'ralp',
    'yr_ctrl',
    'yr_ctrl_cm',
    'yr_ctrl_cm_21'
]

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

def check_table_exists(pg_conn, table_name):
    """Проверка существования таблицы"""
    try:
        cursor = pg_conn.cursor()
        
        query = """
        SELECT table_name
        FROM information_schema.tables
        WHERE table_schema = 'ags'
        AND table_name = %s
        AND table_type = 'BASE TABLE'
        """
        
        cursor.execute(query, (table_name,))
        result = cursor.fetchone()
        
        return result is not None
        
    except Exception as e:
        logging.error(f"Ошибка проверки существования таблицы {table_name}: {e}")
        return False

def check_dependencies(pg_conn, table_name):
    """Проверка зависимостей от таблицы"""
    try:
        cursor = pg_conn.cursor()
        
        # Проверка внешних ключей
        fk_query = """
        SELECT 
            tc.constraint_name,
            tc.table_name,
            kcu.column_name
        FROM information_schema.table_constraints tc
        JOIN information_schema.key_column_usage kcu 
            ON tc.constraint_name = kcu.constraint_name
        WHERE tc.constraint_type = 'FOREIGN KEY'
        AND tc.table_schema = 'ags'
        AND kcu.referenced_table_name = %s
        """
        
        cursor.execute(fk_query, (table_name,))
        foreign_keys = cursor.fetchall()
        
        # Проверка индексов
        index_query = """
        SELECT indexname
        FROM pg_indexes
        WHERE schemaname = 'ags'
        AND tablename = %s
        """
        
        cursor.execute(index_query, (table_name,))
        indexes = cursor.fetchall()
        
        return {
            'foreign_keys': foreign_keys,
            'indexes': indexes
        }
        
    except Exception as e:
        logging.error(f"Ошибка проверки зависимостей для {table_name}: {e}")
        return {'foreign_keys': [], 'indexes': []}

def remove_dependencies(pg_conn, table_name, dependencies):
    """Удаление зависимостей от таблицы"""
    try:
        cursor = pg_conn.cursor()
        
        # Удаление внешних ключей
        for fk in dependencies['foreign_keys']:
            constraint_name = fk[0]
            drop_fk_query = f"ALTER TABLE ags.{fk[1]} DROP CONSTRAINT {constraint_name};"
            logging.info(f"Удаление внешнего ключа: {drop_fk_query}")
            cursor.execute(drop_fk_query)
        
        # Удаление индексов (кроме первичных ключей)
        for index in dependencies['indexes']:
            index_name = index[0]
            if not index_name.endswith('_pkey'):  # Не удаляем первичные ключи
                drop_index_query = f"DROP INDEX ags.{index_name};"
                logging.info(f"Удаление индекса: {drop_index_query}")
                cursor.execute(drop_index_query)
        
        pg_conn.commit()
        logging.info(f"Зависимости для таблицы {table_name} удалены")
        
    except Exception as e:
        logging.error(f"Ошибка удаления зависимостей для {table_name}: {e}")
        pg_conn.rollback()

def drop_table(pg_conn, table_name):
    """Удаление таблицы"""
    try:
        cursor = pg_conn.cursor()
        
        drop_query = f"DROP TABLE ags.{table_name};"
        logging.info(f"Удаление таблицы: {drop_query}")
        cursor.execute(drop_query)
        
        pg_conn.commit()
        logging.info(f"Таблица {table_name} успешно удалена")
        return True
        
    except Exception as e:
        logging.error(f"Ошибка удаления таблицы {table_name}: {e}")
        pg_conn.rollback()
        return False

def main():
    """Основная функция"""
    logging.info("Начало удаления мигрированных представлений")
    
    # Получение подключения
    pg_conn = get_pg_connection()
    if not pg_conn:
        return
    
    try:
        results = {
            'timestamp': datetime.now().isoformat(),
            'total_views': len(MIGRATED_VIEWS),
            'successful_removals': 0,
            'failed_removals': 0,
            'details': []
        }
        
        for view_name in MIGRATED_VIEWS:
            logging.info(f"Обработка: {view_name}")
            
            # Проверка существования таблицы
            if not check_table_exists(pg_conn, view_name):
                logging.warning(f"Таблица {view_name} не существует, пропускаем")
                results['details'].append({
                    'view_name': view_name,
                    'status': 'not_exists',
                    'message': 'Таблица не существует'
                })
                continue
            
            # Проверка зависимостей
            dependencies = check_dependencies(pg_conn, view_name)
            logging.info(f"Зависимости для {view_name}: {len(dependencies['foreign_keys'])} FK, {len(dependencies['indexes'])} индексов")
            
            # Удаление зависимостей
            if dependencies['foreign_keys'] or dependencies['indexes']:
                remove_dependencies(pg_conn, view_name, dependencies)
            
            # Удаление таблицы
            if drop_table(pg_conn, view_name):
                results['successful_removals'] += 1
                results['details'].append({
                    'view_name': view_name,
                    'status': 'success',
                    'dependencies_removed': len(dependencies['foreign_keys']) + len(dependencies['indexes'])
                })
            else:
                results['failed_removals'] += 1
                results['details'].append({
                    'view_name': view_name,
                    'status': 'failed',
                    'message': 'Ошибка удаления таблицы'
                })
        
        # Сохранение отчета
        report_dir = "/home/alex/vuege/docs/infrastructure/reports"
        os.makedirs(report_dir, exist_ok=True)
        report_file = f"{report_dir}/remove-migrated-views-report-{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        
        with open(report_file, 'w', encoding='utf-8') as f:
            json.dump(results, f, ensure_ascii=False, indent=2)
        
        # Вывод результатов
        logging.info("=== РЕЗУЛЬТАТЫ УДАЛЕНИЯ МИГРИРОВАННЫХ ПРЕДСТАВЛЕНИЙ ===")
        logging.info(f"Всего представлений для удаления: {results['total_views']}")
        logging.info(f"Успешно удалено: {results['successful_removals']}")
        logging.info(f"Ошибок удаления: {results['failed_removals']}")
        
        for detail in results['details']:
            if detail['status'] == 'success':
                logging.info(f"✅ {detail['view_name']} - удалено")
            elif detail['status'] == 'failed':
                logging.error(f"❌ {detail['view_name']} - ошибка удаления")
            else:
                logging.warning(f"⚠️ {detail['view_name']} - не существует")
        
        logging.info(f"Отчет сохранен: {report_file}")
        
    except Exception as e:
        logging.error(f"Ошибка в основной функции: {e}")
    
    finally:
        if pg_conn:
            pg_conn.close()
    
    logging.info("Удаление мигрированных представлений завершено")

if __name__ == "__main__":
    main()