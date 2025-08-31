#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@file: compare-tables.py
@description: Сравнение таблиц между SQL Server и PostgreSQL
@pager-protection: Встроенная защита от pager для предотвращения блокировки автоматизации
@dependencies: pymssql, psycopg2
@created: 2025-08-30
"""

import os
import sys
import subprocess
import logging
import pymssql
import psycopg2
from datetime import datetime
from typing import List, Dict, Tuple, Optional

def setup_pager_protection():
    """Настройка защиты от pager для предотвращения блокировки автоматизации"""
    os.environ['PAGER'] = 'cat'
    os.environ['LESS'] = '-R -M --shift 5'
    os.environ['MORE'] = '-R'
    os.environ['COMPOSER_NO_INTERACTION'] = '1'
    os.environ['TERM'] = 'xterm-256color'
    os.environ['COLUMNS'] = '120'
    os.environ['LINES'] = '30'
    os.environ['GIT_PAGER'] = 'cat'
    os.environ['GIT_EDITOR'] = 'vim'
    
    try:
        subprocess.run(['git', 'config', '--global', 'core.pager', 'cat'], 
                      capture_output=True, check=True)
        print("✅ Защита от pager настроена")
    except subprocess.CalledProcessError:
        print("⚠️ Не удалось настроить git pager")
    except Exception as e:
        print(f"⚠️ Ошибка настройки pager: {e}")

# Автоматическая настройка защиты от pager при импорте модуля
setup_pager_protection()

def setup_logging():
    """Настройка логирования"""
    # Создаем папку logs если её нет
    os.makedirs('docs/infrastructure/logs', exist_ok=True)
    
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler(f'docs/infrastructure/logs/compare-tables-{datetime.now().strftime("%Y%m%d_%H%M%S")}.log'),
            logging.StreamHandler(sys.stdout)
        ]
    )
    return logging.getLogger(__name__)

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
            user='postgres',
            password='postgres'
        )
        
        logging.info("✅ Подключения к базам данных установлены")
        return mssql_conn, pg_conn
    except Exception as e:
        logging.error(f"❌ Ошибка подключения к базам данных: {e}")
        return None, None

def get_mssql_tables(mssql_conn):
    """Получение списка таблиц из SQL Server"""
    try:
        mssql_cursor = mssql_conn.cursor()
        mssql_cursor.execute("""
            SELECT TABLE_NAME
            FROM INFORMATION_SCHEMA.TABLES 
            WHERE TABLE_SCHEMA = 'ags'
            ORDER BY TABLE_NAME
        """)
        
        tables = [row[0] for row in mssql_cursor.fetchall()]
        return tables
        
    except Exception as e:
        logging.error(f"❌ Ошибка получения таблиц из SQL Server: {e}")
        return []

def get_pg_tables(pg_conn):
    """Получение списка таблиц из PostgreSQL"""
    try:
        pg_cursor = pg_conn.cursor()
        pg_cursor.execute("""
            SELECT tablename
            FROM pg_tables 
            WHERE schemaname = 'ags'
            ORDER BY tablename
        """)
        
        tables = [row[0] for row in pg_cursor.fetchall()]
        return tables
        
    except Exception as e:
        logging.error(f"❌ Ошибка получения таблиц из PostgreSQL: {e}")
        return []

def compare_tables():
    """Сравнение таблиц между SQL Server и PostgreSQL"""
    logger = setup_logging()
    
    logging.info("🔍 СРАВНЕНИЕ ТАБЛИЦ МЕЖДУ SQL SERVER И POSTGRESQL")
    logging.info("=" * 80)
    
    # Подключение к базам данных
    mssql_conn, pg_conn = connect_databases()
    if not mssql_conn or not pg_conn:
        logging.error("❌ Не удалось подключиться к базам данных")
        return False
    
    try:
        # Получаем списки таблиц
        mssql_tables = get_mssql_tables(mssql_conn)
        pg_tables = get_pg_tables(pg_conn)
        
        logging.info(f"📊 SQL Server: {len(mssql_tables)} таблиц")
        logging.info(f"📊 PostgreSQL: {len(pg_tables)} таблиц")
        
        # Находим различия
        mssql_set = set(mssql_tables)
        pg_set = set(pg_tables)
        
        missing_in_pg = mssql_set - pg_set
        extra_in_pg = pg_set - mssql_set
        common = mssql_set & pg_set
        
        logging.info(f"📊 Общих таблиц: {len(common)}")
        logging.info(f"📊 Отсутствует в PostgreSQL: {len(missing_in_pg)}")
        logging.info(f"📊 Лишние в PostgreSQL: {len(extra_in_pg)}")
        
        if missing_in_pg:
            logging.info("📋 ОТСУТСТВУЮЩИЕ В POSTGRESQL ТАБЛИЦЫ:")
            for table in sorted(missing_in_pg):
                logging.info(f"   ❌ {table}")
        
        if extra_in_pg:
            logging.info("📋 ЛИШНИЕ В POSTGRESQL ТАБЛИЦЫ:")
            for table in sorted(extra_in_pg):
                logging.info(f"   ⚠️ {table}")
        
        # Проверяем количество записей в общих таблицах
        logging.info("📊 ПРОВЕРКА КОЛИЧЕСТВА ЗАПИСЕЙ В ОБЩИХ ТАБЛИЦАХ:")
        
        mssql_cursor = mssql_conn.cursor()
        pg_cursor = pg_conn.cursor()
        
        for table in sorted(common)[:10]:  # Проверяем первые 10 таблиц
            try:
                # SQL Server
                mssql_cursor.execute(f"SELECT COUNT(*) FROM ags.{table}")
                mssql_count = mssql_cursor.fetchone()[0]
                
                # PostgreSQL
                pg_cursor.execute(f"SELECT COUNT(*) FROM ags.{table.lower()}")
                pg_count = pg_cursor.fetchone()[0]
                
                if mssql_count == pg_count:
                    logging.info(f"   ✅ {table}: {mssql_count} записей")
                else:
                    logging.warning(f"   ⚠️ {table}: SQL Server {mssql_count} → PostgreSQL {pg_count}")
                    
            except Exception as e:
                logging.error(f"   ❌ {table}: Ошибка проверки - {e}")
        
        return True
        
    finally:
        mssql_conn.close()
        pg_conn.close()

def main():
    """Основная функция"""
    success = compare_tables()
    
    if success:
        logging.info("✅ Сравнение таблиц завершено")
    else:
        logging.error("❌ Ошибка сравнения таблиц")
    
    return success

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)