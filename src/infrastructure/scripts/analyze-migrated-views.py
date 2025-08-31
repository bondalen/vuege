#!/usr/bin/env python3
"""
Скрипт для анализа мигрированных представлений и подготовки предложений
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
log_file = f"{log_dir}/analyze-migrated-views-{datetime.now().strftime('%Y%m%d_%H%M%S')}.log"

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

def get_sqlserver_views(mssql_conn):
    """Получение всех представлений из схемы ags в SQL Server"""
    try:
        cursor = mssql_conn.cursor()
        
        query = """
        SELECT 
            o.name as view_name,
            o.create_date,
            o.modify_date
        FROM sys.objects o
        INNER JOIN sys.schemas s ON o.schema_id = s.schema_id
        WHERE s.name = 'ags'
        AND o.type = 'V'
        ORDER BY o.name
        """
        
        cursor.execute(query)
        views = cursor.fetchall()
        
        return views
        
    except Exception as e:
        logging.error(f"Ошибка получения представлений из SQL Server: {e}")
        return []

def get_postgres_tables(pg_conn):
    """Получение всех таблиц из схемы ags в PostgreSQL"""
    try:
        cursor = pg_conn.cursor()
        
        query = """
        SELECT table_name
        FROM information_schema.tables
        WHERE table_schema = 'ags'
        AND table_type = 'BASE TABLE'
        ORDER BY table_name
        """
        
        cursor.execute(query)
        tables = [row[0] for row in cursor.fetchall()]
        
        return tables
        
    except Exception as e:
        logging.error(f"Ошибка получения таблиц из PostgreSQL: {e}")
        return []

def analyze_migrated_views(sqlserver_views, postgres_tables):
    """Анализ мигрированных представлений"""
    sqlserver_view_names = [view[0] for view in sqlserver_views]
    
    migrated_views = []
    not_migrated_views = []
    
    for view_name in sqlserver_view_names:
        if view_name in postgres_tables:
            migrated_views.append(view_name)
        else:
            not_migrated_views.append(view_name)
    
    return {
        'migrated_views': migrated_views,
        'not_migrated_views': not_migrated_views
    }

def get_view_definition(mssql_conn, view_name):
    """Получение определения представления из SQL Server"""
    try:
        cursor = mssql_conn.cursor()
        
        query = f"""
        SELECT OBJECT_DEFINITION(OBJECT_ID('ags.{view_name}')) as view_definition
        """
        
        cursor.execute(query)
        result = cursor.fetchone()
        
        return result[0] if result else None
        
    except Exception as e:
        logging.error(f"Ошибка получения определения представления {view_name}: {e}")
        return None

def main():
    """Основная функция"""
    logging.info("Начало анализа мигрированных представлений")
    
    # Получение подключений
    mssql_conn = get_mssql_connection()
    pg_conn = get_pg_connection()
    
    if not mssql_conn or not pg_conn:
        return
    
    try:
        # Получение представлений из SQL Server
        logging.info("Получение представлений из SQL Server...")
        sqlserver_views = get_sqlserver_views(mssql_conn)
        logging.info(f"Найдено представлений в SQL Server: {len(sqlserver_views)}")
        
        # Получение таблиц из PostgreSQL
        logging.info("Получение таблиц из PostgreSQL...")
        postgres_tables = get_postgres_tables(pg_conn)
        logging.info(f"Найдено таблиц в PostgreSQL: {len(postgres_tables)}")
        
        # Анализ мигрированных представлений
        logging.info("Анализ мигрированных представлений...")
        analysis = analyze_migrated_views(sqlserver_views, postgres_tables)
        
        # Получение определений представлений
        logging.info("Получение определений представлений...")
        view_definitions = {}
        for view_name in analysis['migrated_views']:
            definition = get_view_definition(mssql_conn, view_name)
            if definition:
                view_definitions[view_name] = definition
        
        # Создание отчета
        report = {
            'timestamp': datetime.now().isoformat(),
            'sqlserver_views': {
                'total': len(sqlserver_views),
                'names': [view[0] for view in sqlserver_views]
            },
            'postgres_tables': {
                'total': len(postgres_tables)
            },
            'migration_analysis': {
                'migrated_views': len(analysis['migrated_views']),
                'not_migrated_views': len(analysis['not_migrated_views'])
            },
            'migrated_views': analysis['migrated_views'],
            'not_migrated_views': analysis['not_migrated_views'],
            'view_definitions': view_definitions,
            'log_file': log_file
        }
        
        # Сохранение отчета
        report_dir = "/home/alex/vuege/docs/infrastructure/reports"
        os.makedirs(report_dir, exist_ok=True)
        report_file = f"{report_dir}/analyze-migrated-views-report-{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        
        with open(report_file, 'w', encoding='utf-8') as f:
            json.dump(report, f, ensure_ascii=False, indent=2)
        
        # Вывод результатов
        logging.info("=== РЕЗУЛЬТАТЫ АНАЛИЗА МИГРИРОВАННЫХ ПРЕДСТАВЛЕНИЙ ===")
        logging.info(f"Представлений в SQL Server: {len(sqlserver_views)}")
        logging.info(f"Таблиц в PostgreSQL: {len(postgres_tables)}")
        
        logging.info(f"Мигрированных представлений: {len(analysis['migrated_views'])}")
        if analysis['migrated_views']:
            logging.info("Представления, мигрированные как таблицы:")
            for view in analysis['migrated_views']:
                logging.info(f"  - {view}")
        
        logging.info(f"Немигрированных представлений: {len(analysis['not_migrated_views'])}")
        if analysis['not_migrated_views']:
            logging.info("Представления, НЕ мигрированные как таблицы:")
            for view in analysis['not_migrated_views']:
                logging.info(f"  - {view}")
        
        logging.info(f"Отчет сохранен: {report_file}")
        
        # Подготовка предложений
        logging.info("=== ПРЕДЛОЖЕНИЯ ПО ДАЛЬНЕЙШИМ ДЕЙСТВИЯМ ===")
        
        if analysis['migrated_views']:
            logging.info("1. УДАЛЕНИЕ МИГРИРОВАННЫХ ПРЕДСТАВЛЕНИЙ:")
            logging.info("   Следующие объекты должны быть удалены из PostgreSQL, так как они являются представлениями:")
            for view in analysis['migrated_views']:
                logging.info(f"   - DROP TABLE ags.{view};")
            
            logging.info("")
            logging.info("2. СОЗДАНИЕ ПРЕДСТАВЛЕНИЙ В POSTGRESQL:")
            logging.info("   После удаления таблиц необходимо создать соответствующие представления:")
            for view in analysis['migrated_views']:
                logging.info(f"   - Создать представление ags.{view}")
                if view in view_definitions:
                    logging.info(f"     Определение: {view_definitions[view][:100]}...")
        
        logging.info("")
        logging.info("3. ПРОВЕРКА ЗАВИСИМОСТЕЙ:")
        logging.info("   Необходимо проверить, не используются ли мигрированные представления в других объектах")
        logging.info("   (внешние ключи, индексы, триггеры и т.д.)")
        
        logging.info("")
        logging.info("4. ОБНОВЛЕНИЕ ДОКУМЕНТАЦИИ:")
        logging.info("   Обновить отчеты о миграции с учетом того, что некоторые объекты являются представлениями")
        
    except Exception as e:
        logging.error(f"Ошибка в основной функции: {e}")
    
    finally:
        if mssql_conn:
            mssql_conn.close()
        if pg_conn:
            pg_conn.close()
    
    logging.info("Анализ мигрированных представлений завершен")

if __name__ == "__main__":
    main()