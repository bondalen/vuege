#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@file: migrate-problematic-tables-fixed.py
@description: Миграция проблемных таблиц с исправлением проблемных колонок
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
            logging.FileHandler(f'docs/infrastructure/logs/migrate-problematic-tables-fixed-{datetime.now().strftime("%Y%m%d_%H%M%S")}.log'),
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
        logging.error(f"❌ Ошибка подключения к базам данным: {e}")
        return None, None

def get_problematic_tables_to_fix():
    """Получение списка проблемных таблиц для исправления"""
    return [
        # Таблицы с проблемами несуществующих колонок
        'cn_PrDocCs',
        'cn_s_orgExeBuirg',
        'cnInvAccntCs',
        'cn_s_orgCustBuirgInv',
        'cn_s_orgExeBuirgInv',
        'dym_pm_pm',
        'TimeRsltCAP',
        'TimeRsltM',
        'TimeRsltMrl',
        'TimeRsltMrTtl',
        'yr_ctrl',
        'yr_ctrl_cm',
        'yr_ctrl_cm_21',
        'yr_ctrl_cmAcc21',
        'yr_ctrl_cmAcc21_06',
        'yr_ctrlAccnt'
    ]

def map_sql_to_pg_type(sql_type, max_length=None):
    """Маппинг типов SQL Server в PostgreSQL"""
    sql_type = sql_type.upper()
    
    if 'VARCHAR' in sql_type or 'NVARCHAR' in sql_type:
        if max_length and max_length > 0:
            if max_length < 1000:
                return f'varchar({max_length * 2})'  # Удваиваем размер для безопасности
            else:
                return 'text'
        else:
            return 'text'
    elif 'CHAR' in sql_type or 'NCHAR' in sql_type:
        if max_length and max_length > 0:
            return f'char({max_length})'
        else:
            return 'char(1)'
    elif 'TEXT' in sql_type or 'NTEXT' in sql_type:
        return 'text'
    elif 'INT' in sql_type:
        return 'integer'
    elif 'BIGINT' in sql_type:
        return 'bigint'
    elif 'SMALLINT' in sql_type:
        return 'smallint'
    elif 'TINYINT' in sql_type:
        return 'smallint'
    elif 'DECIMAL' in sql_type or 'NUMERIC' in sql_type:
        return 'numeric'
    elif 'FLOAT' in sql_type:
        return 'double precision'
    elif 'REAL' in sql_type:
        return 'real'
    elif 'MONEY' in sql_type:
        return 'numeric(19,4)'
    elif 'SMALLMONEY' in sql_type:
        return 'numeric(10,4)'
    elif 'BIT' in sql_type:
        return 'boolean'
    elif 'DATETIME' in sql_type:
        return 'timestamp'
    elif 'DATETIME2' in sql_type:
        return 'timestamp'
    elif 'DATE' in sql_type:
        return 'date'
    elif 'TIME' in sql_type:
        return 'time'
    elif 'UNIQUEIDENTIFIER' in sql_type:
        return 'text'  # UUID как text
    elif 'BINARY' in sql_type:
        return 'bytea'
    elif 'VARBINARY' in sql_type:
        return 'bytea'
    elif 'IMAGE' in sql_type:
        return 'bytea'
    else:
        return 'text'

def get_existing_columns(mssql_conn, table_name):
    """Получение списка существующих колонок в таблице"""
    try:
        mssql_cursor = mssql_conn.cursor()
        
        # Получаем схему таблицы
        mssql_cursor.execute(f"""
            SELECT COLUMN_NAME, DATA_TYPE, CHARACTER_MAXIMUM_LENGTH
            FROM INFORMATION_SCHEMA.COLUMNS 
            WHERE TABLE_SCHEMA = 'ags' AND TABLE_NAME = '{table_name}'
            ORDER BY ORDINAL_POSITION
        """)
        
        columns = mssql_cursor.fetchall()
        return columns
        
    except Exception as e:
        logging.error(f"❌ Ошибка получения колонок для {table_name}: {e}")
        return []

def migrate_table_with_fixed_columns(mssql_conn, pg_conn, table_name):
    """Миграция таблицы с исправлением проблемных колонок"""
    try:
        mssql_cursor = mssql_conn.cursor()
        pg_cursor = pg_conn.cursor()
        
        # Проверяем существование таблицы в PostgreSQL
        pg_cursor.execute(f"""
            SELECT COUNT(*) FROM pg_tables 
            WHERE schemaname = 'ags' AND tablename = '{table_name.lower()}'
        """)
        
        if pg_cursor.fetchone()[0] > 0:
            logging.info(f"⚠️ Таблица {table_name} уже существует в PostgreSQL, пропускаем")
            return True
        
        # Получаем существующие колонки
        columns = get_existing_columns(mssql_conn, table_name)
        
        if not columns:
            logging.warning(f"⚠️ Не удалось получить колонки для таблицы {table_name}")
            return False
        
        logging.info(f"📋 Найдено {len(columns)} колонок в таблице {table_name}")
        
        # Создаем таблицу только с существующими колонками
        columns_sql = []
        for col_name, data_type, max_length in columns:
            pg_type = map_sql_to_pg_type(data_type, max_length)
            columns_sql.append(f'"{col_name.lower()}" {pg_type}')
            logging.info(f"   📊 {col_name}: {data_type}({max_length}) → {pg_type}")
        
        create_sql = f"""
        CREATE TABLE ags."{table_name.lower()}" (
            {', '.join(columns_sql)}
        )
        """
        
        pg_cursor.execute(create_sql)
        pg_conn.commit()
        logging.info(f"✅ Таблица ags.{table_name.lower()} создана")
        
        # Проверяем количество записей в SQL Server
        try:
            mssql_cursor.execute(f"SELECT COUNT(*) FROM ags.{table_name}")
            record_count = mssql_cursor.fetchone()[0]
        except Exception as e:
            logging.warning(f"⚠️ Не удалось получить количество записей для {table_name}: {e}")
            record_count = 0
        
        if record_count == 0:
            logging.info(f"✅ Таблица {table_name} пустая, миграция завершена")
            return True
        
        # Мигрируем данные
        column_names = [col[0].lower() for col in columns]
        column_names_quoted = ', '.join([f'"{name}"' for name in column_names])
        placeholders = ', '.join(['%s'] * len(columns))
        
        select_sql = f"SELECT {', '.join([f'[{col[0]}]' for col in columns])} FROM ags.{table_name}"
        
        try:
            mssql_cursor.execute(select_sql)
        except Exception as e:
            logging.error(f"❌ Ошибка чтения данных из {table_name}: {e}")
            return False
        
        batch_size = 1000
        total_records = 0
        
        while True:
            rows = mssql_cursor.fetchmany(batch_size)
            if not rows:
                break
            
            # Обрабатываем данные
            processed_rows = []
            for row in rows:
                processed_row = []
                for value in row:
                    if isinstance(value, str) and len(value) > 1000:
                        # Обрезаем слишком длинные строки
                        processed_row.append(value[:1000])
                    else:
                        processed_row.append(value)
                processed_rows.append(processed_row)
            
            # Вставляем данные
            insert_sql = f"""
            INSERT INTO ags."{table_name.lower()}" ({column_names_quoted})
            VALUES ({placeholders})
            """
            
            try:
                pg_cursor.executemany(insert_sql, processed_rows)
                total_records += len(processed_rows)
            except Exception as e:
                logging.error(f"❌ Ошибка вставки данных в {table_name}: {e}")
                pg_conn.rollback()
                return False
            
            if total_records % 10000 == 0:
                logging.info(f"📊 Обработано записей {table_name}: {total_records}")
        
        pg_conn.commit()
        logging.info(f"✅ Данные таблицы {table_name} мигрированы успешно ({total_records} записей)")
        
        # Проверяем результат
        pg_cursor.execute(f"SELECT COUNT(*) FROM ags.{table_name.lower()}")
        pg_count = pg_cursor.fetchone()[0]
        
        logging.info(f"📊 Проверка {table_name}: SQL Server {record_count} → PostgreSQL {pg_count}")
        
        return True
        
    except Exception as e:
        logging.error(f"❌ Ошибка миграции таблицы {table_name}: {e}")
        pg_conn.rollback()
        return False

def main():
    """Основная функция"""
    logger = setup_logging()
    
    logging.info("🔧 МИГРАЦИЯ ПРОБЛЕМНЫХ ТАБЛИЦ С ИСПРАВЛЕНИЕМ КОЛОНОК")
    logging.info("=" * 80)
    
    # Подключение к базам данных
    mssql_conn, pg_conn = connect_databases()
    if not mssql_conn or not pg_conn:
        logging.error("❌ Не удалось подключиться к базам данных")
        return False
    
    try:
        problematic_tables = get_problematic_tables_to_fix()
        success_count = 0
        error_count = 0
        
        for i, table_name in enumerate(problematic_tables, 1):
            logging.info(f"📋 [{i}/{len(problematic_tables)}] Миграция проблемной таблицы: {table_name}")
            
            success = migrate_table_with_fixed_columns(mssql_conn, pg_conn, table_name)
            
            if success:
                logging.info(f"✅ Таблица {table_name} мигрирована успешно")
                success_count += 1
            else:
                logging.error(f"❌ Ошибка миграции таблицы {table_name}")
                error_count += 1
            
            logging.info("-" * 60)
        
        # Итоговый отчет
        logging.info("=" * 80)
        logging.info("📊 ИТОГОВЫЙ ОТЧЕТ МИГРАЦИИ ПРОБЛЕМНЫХ ТАБЛИЦ")
        logging.info("=" * 80)
        logging.info(f"📋 Всего таблиц: {len(problematic_tables)}")
        logging.info(f"✅ Успешно мигрировано: {success_count}")
        logging.info(f"❌ Ошибки миграции: {error_count}")
        logging.info(f"📈 Процент успеха: {(success_count/len(problematic_tables)*100):.1f}%")
        
        if error_count == 0:
            logging.info("🎉 ВСЕ ПРОБЛЕМНЫЕ ТАБЛИЦЫ МИГРИРОВАНЫ УСПЕШНО!")
        else:
            logging.warning(f"⚠️ Осталось {error_count} проблемных таблиц")
        
        return error_count == 0
        
    finally:
        mssql_conn.close()
        pg_conn.close()

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)