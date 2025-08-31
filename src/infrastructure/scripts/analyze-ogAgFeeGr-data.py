#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@file: analyze-ogAgFeeGr-data.py
@description: Детальный анализ данных таблицы ogAgFeeGr для выявления проблемных значений
@pager-protection: Встроенная защита от pager для предотвращения блокировки автоматизации
@dependencies: pymssql
@created: 2025-08-30
"""

import os
import sys
import subprocess
import logging
import pymssql
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
            logging.FileHandler(f'docs/infrastructure/logs/analyze-ogAgFeeGr-data-{datetime.now().strftime("%Y%m%d_%H%M%S")}.log'),
            logging.StreamHandler(sys.stdout)
        ]
    )
    return logging.getLogger(__name__)

def connect_mssql():
    """Подключение к SQL Server"""
    try:
        mssql_conn = pymssql.connect(
            server='localhost',
            port=1433,
            user='sa',
            password='Vuege2024!',
            database='Fish_Eye'
        )
        logging.info("✅ Подключение к SQL Server установлено")
        return mssql_conn
    except Exception as e:
        logging.error(f"❌ Ошибка подключения к SQL Server: {e}")
        return None

def analyze_column_lengths(mssql_conn):
    """Анализ длин значений в колонках"""
    try:
        mssql_cursor = mssql_conn.cursor()
        
        # Получаем схему таблицы
        mssql_cursor.execute(f"""
            SELECT COLUMN_NAME, DATA_TYPE, CHARACTER_MAXIMUM_LENGTH
            FROM INFORMATION_SCHEMA.COLUMNS 
            WHERE TABLE_SCHEMA = 'ags' AND TABLE_NAME = 'ogAgFeeGr'
            ORDER BY ORDINAL_POSITION
        """)
        
        columns = mssql_cursor.fetchall()
        
        for col_name, data_type, max_length in columns:
            logging.info(f"📊 Анализ колонки: {col_name} ({data_type})")
            
            if 'char' in data_type.lower() or 'text' in data_type.lower():
                # Анализируем строковые колонки
                try:
                    mssql_cursor.execute(f"""
                        SELECT 
                            MAX(LEN([{col_name}])) as max_length,
                            MIN(LEN([{col_name}])) as min_length,
                            AVG(CAST(LEN([{col_name}]) AS FLOAT)) as avg_length,
                            COUNT(*) as total_records,
                            COUNT(CASE WHEN LEN([{col_name}]) > 100 THEN 1 END) as long_records
                        FROM ags.ogAgFeeGr
                        WHERE [{col_name}] IS NOT NULL
                    """)
                    
                    result = mssql_cursor.fetchone()
                    if result:
                        max_len, min_len, avg_len, total, long_records = result
                        logging.info(f"   📏 Максимальная длина: {max_len}")
                        logging.info(f"   📏 Минимальная длина: {min_len}")
                        logging.info(f"   📏 Средняя длина: {avg_len:.1f}")
                        logging.info(f"   📊 Всего записей: {total}")
                        logging.info(f"   ⚠️ Длинных записей (>100): {long_records}")
                        
                        # Показываем примеры длинных значений
                        if long_records > 0:
                            mssql_cursor.execute(f"""
                                SELECT TOP 5 [{col_name}], LEN([{col_name}]) as length
                                FROM ags.ogAgFeeGr
                                WHERE LEN([{col_name}]) > 100
                                ORDER BY LEN([{col_name}]) DESC
                            """)
                            
                            long_values = mssql_cursor.fetchall()
                            logging.info(f"   🔍 Примеры длинных значений:")
                            for value, length in long_values:
                                preview = str(value)[:100] + "..." if len(str(value)) > 100 else str(value)
                                logging.info(f"      • Длина {length}: {preview}")
                        
                        # Проверяем, есть ли значения длиннее 1000 символов
                        mssql_cursor.execute(f"""
                            SELECT COUNT(*)
                            FROM ags.ogAgFeeGr
                            WHERE LEN([{col_name}]) > 1000
                        """)
                        
                        very_long_count = mssql_cursor.fetchone()[0]
                        if very_long_count > 0:
                            logging.warning(f"   🚨 ОЧЕНЬ ДЛИННЫЕ ЗНАЧЕНИЯ (>1000): {very_long_count}")
                            
                            mssql_cursor.execute(f"""
                                SELECT TOP 3 [{col_name}], LEN([{col_name}]) as length
                                FROM ags.ogAgFeeGr
                                WHERE LEN([{col_name}]) > 1000
                                ORDER BY LEN([{col_name}]) DESC
                            """)
                            
                            very_long_values = mssql_cursor.fetchall()
                            for value, length in very_long_values:
                                preview = str(value)[:200] + "..." if len(str(value)) > 200 else str(value)
                                logging.warning(f"      🚨 Длина {length}: {preview}")
                    
                except Exception as e:
                    logging.error(f"   ❌ Ошибка анализа колонки {col_name}: {e}")
            
            logging.info("-" * 40)
        
    except Exception as e:
        logging.error(f"❌ Ошибка анализа длин колонок: {e}")

def main():
    """Основная функция"""
    logger = setup_logging()
    
    logging.info("🔍 ДЕТАЛЬНЫЙ АНАЛИЗ ДАННЫХ ТАБЛИЦЫ ogAgFeeGr")
    logging.info("=" * 80)
    
    # Подключение к SQL Server
    mssql_conn = connect_mssql()
    if not mssql_conn:
        return False
    
    try:
        # Анализируем длины значений в колонках
        analyze_column_lengths(mssql_conn)
        
        logging.info("✅ Анализ завершен")
        return True
        
    finally:
        mssql_conn.close()

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)