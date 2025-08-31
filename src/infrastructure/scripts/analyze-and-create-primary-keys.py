#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@file: analyze-and-create-primary-keys.py
@description: Анализ и создание первичных ключей для таблиц PostgreSQL
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
            logging.FileHandler(f'docs/infrastructure/logs/analyze-and-create-primary-keys-{datetime.now().strftime("%Y%m%d_%H%M%S")}.log'),
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

def get_primary_keys_from_mssql(mssql_conn):
    """Получение первичных ключей из SQL Server"""
    try:
        mssql_cursor = mssql_conn.cursor()
        
        # Получаем все первичные ключи для схемы ags
        mssql_cursor.execute("""
            SELECT 
                OBJECT_SCHEMA_NAME(t.object_id) as schema_name,
                t.name as table_name,
                c.name as column_name,
                ic.key_ordinal as key_order
            FROM sys.tables t
            INNER JOIN sys.indexes i ON t.object_id = i.object_id
            INNER JOIN sys.index_columns ic ON i.object_id = ic.object_id AND i.index_id = ic.index_id
            INNER JOIN sys.columns c ON ic.object_id = c.object_id AND ic.column_id = c.column_id
            WHERE i.is_primary_key = 1 
            AND OBJECT_SCHEMA_NAME(t.object_id) = 'ags'
            ORDER BY t.name, ic.key_ordinal
        """)
        
        primary_keys = mssql_cursor.fetchall()
        
        # Группируем по таблицам
        pk_by_table = {}
        for pk in primary_keys:
            table_name = pk[1].lower()  # Приводим к нижнему регистру
            if table_name not in pk_by_table:
                pk_by_table[table_name] = []
            
            pk_by_table[table_name].append({
                'column_name': pk[2].lower(),  # Приводим к нижнему регистру
                'key_order': pk[3]
            })
        
        return pk_by_table
        
    except Exception as e:
        logging.error(f"❌ Ошибка получения первичных ключей из SQL Server: {e}")
        return {}

def check_table_exists_in_pg(pg_conn, table_name):
    """Проверка существования таблицы в PostgreSQL"""
    try:
        pg_cursor = pg_conn.cursor()
        pg_cursor.execute(f"""
            SELECT COUNT(*) FROM pg_tables 
            WHERE schemaname = 'ags' AND tablename = '{table_name.lower()}'
        """)
        
        return pg_cursor.fetchone()[0] > 0
        
    except Exception as e:
        logging.error(f"❌ Ошибка проверки таблицы {table_name} в PostgreSQL: {e}")
        return False

def check_column_exists_in_pg(pg_conn, table_name, column_name):
    """Проверка существования колонки в PostgreSQL"""
    try:
        pg_cursor = pg_conn.cursor()
        pg_cursor.execute(f"""
            SELECT COUNT(*) FROM information_schema.columns 
            WHERE table_schema = 'ags' AND table_name = '{table_name.lower()}' 
            AND column_name = '{column_name.lower()}'
        """)
        
        return pg_cursor.fetchone()[0] > 0
        
    except Exception as e:
        logging.error(f"❌ Ошибка проверки колонки {column_name} в таблице {table_name}: {e}")
        return False

def create_primary_key_in_pg(pg_conn, table_name, pk_columns):
    """Создание первичного ключа в PostgreSQL"""
    try:
        pg_cursor = pg_conn.cursor()
        
        # Проверяем существование таблицы
        if not check_table_exists_in_pg(pg_conn, table_name):
            logging.warning(f"⚠️ Таблица {table_name} не существует в PostgreSQL")
            return False
        
        # Проверяем существование всех колонок
        for pk_col in pk_columns:
            if not check_column_exists_in_pg(pg_conn, table_name, pk_col['column_name']):
                logging.warning(f"⚠️ Колонка {pk_col['column_name']} не существует в таблице {table_name}")
                return False
        
        # Проверяем, не существует ли уже первичный ключ
        pg_cursor.execute(f"""
            SELECT COUNT(*) FROM information_schema.table_constraints 
            WHERE constraint_schema = 'ags' 
            AND table_name = '{table_name.lower()}'
            AND constraint_type = 'PRIMARY KEY'
        """)
        
        if pg_cursor.fetchone()[0] > 0:
            logging.info(f"⚠️ Первичный ключ уже существует в таблице {table_name}")
            return True
        
        # Сортируем колонки по порядку ключа
        sorted_columns = sorted(pk_columns, key=lambda x: x['key_order'])
        column_names = [col['column_name'] for col in sorted_columns]
        column_names_quoted = ', '.join([f'"{name}"' for name in column_names])
        
        # Создаем первичный ключ
        pk_name = f"pk_{table_name.lower()}"
        create_sql = f"""
        ALTER TABLE ags."{table_name.lower()}" 
        ADD CONSTRAINT "{pk_name}" 
        PRIMARY KEY ({column_names_quoted})
        """
        
        pg_cursor.execute(create_sql)
        pg_conn.commit()
        
        logging.info(f"✅ Создан первичный ключ {pk_name} для таблицы {table_name}")
        return True
        
    except Exception as e:
        logging.error(f"❌ Ошибка создания первичного ключа для таблицы {table_name}: {e}")
        pg_conn.rollback()
        return False

def analyze_and_create_primary_keys():
    """Анализ и создание первичных ключей"""
    logger = setup_logging()
    
    logging.info("🔑 АНАЛИЗ И СОЗДАНИЕ ПЕРВИЧНЫХ КЛЮЧЕЙ")
    logging.info("=" * 80)
    
    # Подключение к базам данных
    mssql_conn, pg_conn = connect_databases()
    if not mssql_conn or not pg_conn:
        logging.error("❌ Не удалось подключиться к базам данных")
        return False
    
    try:
        # Получаем первичные ключи из SQL Server
        logging.info("📋 Получение первичных ключей из SQL Server...")
        primary_keys = get_primary_keys_from_mssql(mssql_conn)
        
        if not primary_keys:
            logging.warning("⚠️ Первичные ключи не найдены в SQL Server")
            return True
        
        logging.info(f"📊 Найдено {len(primary_keys)} таблиц с первичными ключами")
        
        total_pks = sum(len(pks) for pks in primary_keys.values())
        logging.info(f"📊 Общее количество первичных ключей: {total_pks}")
        
        # Создаем первичные ключи в PostgreSQL
        success_count = 0
        error_count = 0
        skipped_count = 0
        
        for table_name, pk_columns in primary_keys.items():
            logging.info(f"📋 Обработка таблицы: {table_name} ({len(pk_columns)} колонок в PK)")
            
            # Проверяем существование таблицы в PostgreSQL
            if not check_table_exists_in_pg(pg_conn, table_name):
                logging.warning(f"   ⚠️ Таблица {table_name} не существует в PostgreSQL, пропускаем")
                skipped_count += 1
                continue
            
            # Создаем первичный ключ
            success = create_primary_key_in_pg(pg_conn, table_name, pk_columns)
            
            if success:
                success_count += 1
                logging.info(f"   ✅ Первичный ключ для таблицы {table_name} создан успешно")
            else:
                error_count += 1
                logging.error(f"   ❌ Ошибка создания первичного ключа для таблицы {table_name}")
            
            logging.info("-" * 60)
        
        # Итоговый отчет
        logging.info("=" * 80)
        logging.info("📊 ИТОГОВЫЙ ОТЧЕТ СОЗДАНИЯ ПЕРВИЧНЫХ КЛЮЧЕЙ")
        logging.info("=" * 80)
        logging.info(f"📋 Всего таблиц с PK: {len(primary_keys)}")
        logging.info(f"✅ Успешно создано: {success_count}")
        logging.info(f"❌ Ошибки создания: {error_count}")
        logging.info(f"⚠️ Пропущено: {skipped_count}")
        
        if len(primary_keys) > 0:
            logging.info(f"📈 Процент успеха: {(success_count/len(primary_keys)*100):.1f}%")
        
        if error_count == 0:
            logging.info("🎉 ВСЕ ПЕРВИЧНЫЕ КЛЮЧИ УСПЕШНО СОЗДАНЫ!")
        else:
            logging.warning(f"⚠️ Осталось {error_count} проблемных первичных ключей")
        
        return error_count == 0
        
    finally:
        mssql_conn.close()
        pg_conn.close()

def main():
    """Основная функция"""
    success = analyze_and_create_primary_keys()
    
    if success:
        logging.info("✅ Создание первичных ключей завершено успешно")
    else:
        logging.error("❌ Ошибка создания первичных ключей")
    
    return success

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)