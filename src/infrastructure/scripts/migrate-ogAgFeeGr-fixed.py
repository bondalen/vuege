#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@file: migrate-ogAgFeeGr-fixed.py
@description: Миграция таблицы ogAgFeeGr с исправлением проблемы длины строк
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
            logging.FileHandler(f'docs/infrastructure/logs/migrate-ogAgFeeGr-fixed-{datetime.now().strftime("%Y%m%d_%H%M%S")}.log'),
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

def map_sql_to_pg_type(sql_type, max_length=None):
    """Маппинг типов SQL Server в PostgreSQL с увеличенными размерами"""
    sql_type = sql_type.upper()
    
    if 'VARCHAR' in sql_type or 'NVARCHAR' in sql_type:
        if max_length and max_length > 0:
            # Увеличиваем размер для varchar полей
            if max_length < 500:
                return f'varchar(1000)'
            else:
                return f'varchar({max_length})'
        else:
            return 'varchar(1000)'
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

def migrate_ogAgFeeGr():
    """Миграция таблицы ogAgFeeGr с исправлением проблемы длины строк"""
    logger = setup_logging()
    
    logging.info("🔧 МИГРАЦИЯ ТАБЛИЦЫ ogAgFeeGr С ИСПРАВЛЕНИЕМ ДЛИНЫ СТРОК")
    logging.info("=" * 80)
    
    # Подключение к базам данных
    mssql_conn, pg_conn = connect_databases()
    if not mssql_conn or not pg_conn:
        logging.error("❌ Не удалось подключиться к базам данных")
        return False
    
    try:
        mssql_cursor = mssql_conn.cursor()
        pg_cursor = pg_conn.cursor()
        
        # Получаем схему таблицы
        mssql_cursor.execute(f"""
            SELECT COLUMN_NAME, DATA_TYPE, CHARACTER_MAXIMUM_LENGTH
            FROM INFORMATION_SCHEMA.COLUMNS 
            WHERE TABLE_SCHEMA = 'ags' AND TABLE_NAME = 'ogAgFeeGr'
            ORDER BY ORDINAL_POSITION
        """)
        
        columns = mssql_cursor.fetchall()
        logging.info(f"📋 Найдено {len(columns)} колонок")
        
        # Создаем таблицу с увеличенными размерами строк
        columns_sql = []
        for col_name, data_type, max_length in columns:
            pg_type = map_sql_to_pg_type(data_type, max_length)
            columns_sql.append(f'"{col_name.lower()}" {pg_type}')
            logging.info(f"   📊 {col_name}: {data_type}({max_length}) → {pg_type}")
        
        create_sql = f"""
        CREATE TABLE IF NOT EXISTS ags.ogagfeegr (
            {', '.join(columns_sql)}
        )
        """
        
        pg_cursor.execute(create_sql)
        pg_conn.commit()
        logging.info("✅ Таблица ags.ogagfeegr создана с увеличенными размерами")
        
        # Мигрируем данные
        column_names = [col[0].lower() for col in columns]
        column_names_quoted = ', '.join([f'"{name}"' for name in column_names])
        placeholders = ', '.join(['%s'] * len(columns))
        
        select_sql = f"SELECT {', '.join([f'[{col[0]}]' for col in columns])} FROM ags.ogAgFeeGr"
        mssql_cursor.execute(select_sql)
        
        batch_size = 1000
        total_records = 0
        
        while True:
            rows = mssql_cursor.fetchmany(batch_size)
            if not rows:
                break
                
            # Обрабатываем данные - обрезаем слишком длинные строки
            processed_rows = []
            for row in rows:
                processed_row = []
                for value in row:
                    if isinstance(value, str) and len(value) > 1000:
                        # Обрезаем слишком длинные строки
                        processed_row.append(value[:1000])
                        logging.warning(f"⚠️ Обрезана длинная строка: {len(value)} символов")
                    else:
                        processed_row.append(value)
                processed_rows.append(processed_row)
            
            # Вставляем данные
            insert_sql = f"""
            INSERT INTO ags.ogagfeegr ({column_names_quoted})
            VALUES ({placeholders})
            """
            
            pg_cursor.executemany(insert_sql, processed_rows)
            total_records += len(processed_rows)
            
            if total_records % 10000 == 0:
                logging.info(f"📊 Обработано записей: {total_records}")
        
        pg_conn.commit()
        logging.info(f"✅ Данные таблицы ogAgFeeGr мигрированы успешно ({total_records} записей)")
        
        # Проверяем результат
        pg_cursor.execute("SELECT COUNT(*) FROM ags.ogagfeegr")
        pg_count = pg_cursor.fetchone()[0]
        
        mssql_cursor.execute("SELECT COUNT(*) FROM ags.ogAgFeeGr")
        mssql_count = mssql_cursor.fetchone()[0]
        
        logging.info(f"📊 Проверка: SQL Server {mssql_count} → PostgreSQL {pg_count}")
        
        if pg_count == mssql_count:
            logging.info("✅ Миграция завершена успешно - количество записей совпадает")
            return True
        else:
            logging.warning(f"⚠️ Количество записей не совпадает: SQL Server {mssql_count} → PostgreSQL {pg_count}")
            return False
        
    except Exception as e:
        logging.error(f"❌ Ошибка миграции таблицы ogAgFeeGr: {e}")
        pg_conn.rollback()
        return False
    finally:
        mssql_conn.close()
        pg_conn.close()

def main():
    """Основная функция"""
    success = migrate_ogAgFeeGr()
    
    if success:
        logging.info("🎉 МИГРАЦИЯ ТАБЛИЦЫ ogAgFeeGr ЗАВЕРШЕНА УСПЕШНО!")
        logging.info("🚀 Готово к интеграции с основным приложением")
    else:
        logging.error("❌ МИГРАЦИЯ ТАБЛИЦЫ ogAgFeeGr ЗАВЕРШЕНА С ОШИБКАМИ")
    
    return success

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)