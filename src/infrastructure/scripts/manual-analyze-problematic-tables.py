#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@file: manual-analyze-problematic-tables.py
@description: Ручной анализ проблемных таблиц для выявления возможностей миграции
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
import json
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
            logging.FileHandler(f'docs/infrastructure/logs/manual-analyze-problematic-tables-{datetime.now().strftime("%Y%m%d_%H%M%S")}.log'),
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

def get_problematic_tables():
    """Получение списка проблемных таблиц для ручного анализа"""
    return [
        # Группа 1: Проблемы с несуществующими колонками
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
        'yr_ctrlAccnt',
        
        # Группа 2: Проблемы с несуществующими объектами
        'dtqInvoice',
        'dtqContract',
        'dtqCounterparty',
        'dtqInvoiceDbt',
        'RaRa_chSmLt_RltYy'
    ]

def analyze_table_structure(mssql_conn, table_name):
    """Детальный анализ структуры таблицы"""
    try:
        mssql_cursor = mssql_conn.cursor()
        
        # Проверяем существование таблицы
        mssql_cursor.execute(f"""
            SELECT COUNT(*) 
            FROM INFORMATION_SCHEMA.TABLES 
            WHERE TABLE_SCHEMA = 'ags' AND TABLE_NAME = '{table_name}'
        """)
        
        table_exists = mssql_cursor.fetchone()[0] > 0
        
        if not table_exists:
            return {
                'table_name': table_name,
                'exists': False,
                'error': 'Table does not exist'
            }
        
        # Получаем структуру таблицы
        mssql_cursor.execute(f"""
            SELECT COLUMN_NAME, DATA_TYPE, CHARACTER_MAXIMUM_LENGTH, IS_NULLABLE, COLUMN_DEFAULT
            FROM INFORMATION_SCHEMA.COLUMNS 
            WHERE TABLE_SCHEMA = 'ags' AND TABLE_NAME = '{table_name}'
            ORDER BY ORDINAL_POSITION
        """)
        
        columns = mssql_cursor.fetchall()
        
        # Проверяем количество записей
        try:
            mssql_cursor.execute(f"SELECT COUNT(*) FROM ags.{table_name}")
            record_count = mssql_cursor.fetchone()[0]
        except Exception as e:
            record_count = f"Error: {str(e)}"
        
        # Проверяем индексы
        mssql_cursor.execute(f"""
            SELECT 
                i.name as index_name,
                i.type_desc as index_type,
                COL_NAME(ic.object_id, ic.column_id) as column_name
            FROM sys.indexes i
            INNER JOIN sys.index_columns ic ON i.object_id = ic.object_id AND i.index_id = ic.index_id
            WHERE OBJECT_NAME(i.object_id) = '{table_name}'
            ORDER BY i.name, ic.key_ordinal
        """)
        
        indexes = mssql_cursor.fetchall()
        
        return {
            'table_name': table_name,
            'exists': True,
            'columns': [
                {
                    'name': col[0],
                    'type': col[1],
                    'max_length': col[2],
                    'nullable': col[3],
                    'default': col[4]
                } for col in columns
            ],
            'record_count': record_count,
            'indexes': [
                {
                    'name': idx[0],
                    'type': idx[1],
                    'column': idx[2]
                } for idx in indexes
            ]
        }
        
    except Exception as e:
        return {
            'table_name': table_name,
            'exists': False,
            'error': str(e)
        }

def analyze_table_dependencies(mssql_conn, table_name):
    """Анализ зависимостей таблицы"""
    try:
        mssql_cursor = mssql_conn.cursor()
        
        # Проверяем внешние ключи
        mssql_cursor.execute(f"""
            SELECT 
                fk.name as fk_name,
                OBJECT_NAME(fk.parent_object_id) as table_name,
                COL_NAME(fkc.parent_object_id, fkc.parent_column_id) as column_name,
                OBJECT_NAME(fk.referenced_object_id) as referenced_table_name,
                COL_NAME(fkc.referenced_object_id, fkc.referenced_column_id) as referenced_column_name
            FROM sys.foreign_keys fk
            INNER JOIN sys.foreign_key_columns fkc ON fk.object_id = fkc.constraint_object_id
            WHERE OBJECT_NAME(fk.parent_object_id) = '{table_name}'
        """)
        
        foreign_keys = mssql_cursor.fetchall()
        
        # Проверяем представления, которые используют эту таблицу
        mssql_cursor.execute(f"""
            SELECT DISTINCT v.name as view_name
            FROM sys.views v
            INNER JOIN sys.sql_expression_dependencies d ON v.object_id = d.referencing_id
            WHERE d.referenced_schema_name = 'ags' AND d.referenced_entity_name = '{table_name}'
        """)
        
        views = mssql_cursor.fetchall()
        
        return {
            'foreign_keys': [
                {
                    'name': fk[0],
                    'column': fk[2],
                    'referenced_table': fk[3],
                    'referenced_column': fk[4]
                } for fk in foreign_keys
            ],
            'views': [view[0] for view in views]
        }
        
    except Exception as e:
        return {
            'error': str(e)
        }

def analyze_table_data_sample(mssql_conn, table_name):
    """Анализ образца данных таблицы"""
    try:
        mssql_cursor = mssql_conn.cursor()
        
        # Получаем образец данных
        mssql_cursor.execute(f"SELECT TOP 5 * FROM ags.{table_name}")
        sample_data = mssql_cursor.fetchall()
        
        # Получаем имена колонок
        mssql_cursor.execute(f"""
            SELECT COLUMN_NAME
            FROM INFORMATION_SCHEMA.COLUMNS 
            WHERE TABLE_SCHEMA = 'ags' AND TABLE_NAME = '{table_name}'
            ORDER BY ORDINAL_POSITION
        """)
        
        column_names = [col[0] for col in mssql_cursor.fetchall()]
        
        return {
            'column_names': column_names,
            'sample_data': [list(row) for row in sample_data]
        }
        
    except Exception as e:
        return {
            'error': str(e)
        }

def analyze_problematic_columns(mssql_conn, table_name, error_message):
    """Анализ проблемных колонок на основе сообщения об ошибке"""
    try:
        mssql_cursor = mssql_conn.cursor()
        
        # Извлекаем имя проблемной колонки из сообщения об ошибке
        if 'Invalid column name' in error_message:
            # Ищем имя колонки в сообщении об ошибке
            import re
            match = re.search(r"'([^']+)'", error_message)
            if match:
                problematic_column = match.group(1)
                
                # Проверяем, существует ли эта колонка в таблице
                mssql_cursor.execute(f"""
                    SELECT COLUMN_NAME, DATA_TYPE, CHARACTER_MAXIMUM_LENGTH
                    FROM INFORMATION_SCHEMA.COLUMNS 
                    WHERE TABLE_SCHEMA = 'ags' AND TABLE_NAME = '{table_name}'
                    AND COLUMN_NAME = '{problematic_column}'
                """)
                
                column_info = mssql_cursor.fetchone()
                
                if column_info:
                    return {
                        'problematic_column': problematic_column,
                        'exists': True,
                        'type': column_info[1],
                        'max_length': column_info[2]
                    }
                else:
                    return {
                        'problematic_column': problematic_column,
                        'exists': False,
                        'suggestion': 'Column does not exist in table'
                    }
        
        return {
            'error': 'Could not extract column name from error message'
        }
        
    except Exception as e:
        return {
            'error': str(e)
        }

def main():
    """Основная функция"""
    logger = setup_logging()
    
    logging.info("🔍 РУЧНОЙ АНАЛИЗ ПРОБЛЕМНЫХ ТАБЛИЦ СХЕМЫ AGS")
    logging.info("=" * 80)
    
    # Подключение к базам данных
    mssql_conn, pg_conn = connect_databases()
    if not mssql_conn or not pg_conn:
        logging.error("❌ Не удалось подключиться к базам данных")
        return False
    
    try:
        problematic_tables = get_problematic_tables()
        analysis_results = []
        
        for i, table_name in enumerate(problematic_tables, 1):
            logging.info(f"📋 [{i}/{len(problematic_tables)}] Ручной анализ таблицы: {table_name}")
            logging.info("-" * 60)
            
            # Анализируем структуру
            structure = analyze_table_structure(mssql_conn, table_name)
            
            if structure['exists']:
                logging.info(f"✅ Таблица {table_name} существует")
                logging.info(f"📊 Колонок: {len(structure['columns'])}")
                logging.info(f"📊 Записей: {structure['record_count']}")
                logging.info(f"🔗 Индексов: {len(structure['indexes'])}")
                
                # Анализируем зависимости
                dependencies = analyze_table_dependencies(mssql_conn, table_name)
                logging.info(f"🔗 Внешних ключей: {len(dependencies.get('foreign_keys', []))}")
                logging.info(f"👁️ Представлений: {len(dependencies.get('views', []))}")
                
                # Анализируем образец данных
                data_sample = analyze_table_data_sample(mssql_conn, table_name)
                if 'error' not in data_sample:
                    logging.info(f"📊 Образец данных: {len(data_sample['sample_data'])} строк")
                
                # Анализируем проблемные колонки (если есть ошибки)
                if 'cnpdCnInvNew' in str(structure.get('record_count', '')):
                    problematic_analysis = analyze_problematic_columns(mssql_conn, table_name, str(structure['record_count']))
                    logging.info(f"🔍 Анализ проблемной колонки: {problematic_analysis}")
                
                analysis_result = {
                    'table_name': table_name,
                    'structure': structure,
                    'dependencies': dependencies,
                    'data_sample': data_sample,
                    'status': 'analyzed',
                    'migration_possibility': 'high' if structure['record_count'] != 'Error' else 'low'
                }
                
            else:
                logging.warning(f"⚠️ Таблица {table_name} не существует: {structure.get('error', 'Unknown error')}")
                
                analysis_result = {
                    'table_name': table_name,
                    'structure': structure,
                    'status': 'not_exists',
                    'migration_possibility': 'none'
                }
            
            analysis_results.append(analysis_result)
            logging.info("=" * 60)
        
        # Сохраняем результаты анализа
        os.makedirs('docs/infrastructure/reports', exist_ok=True)
        report_file = f'docs/infrastructure/reports/manual-analysis-problematic-tables-{datetime.now().strftime("%Y%m%d_%H%M%S")}.json'
        
        with open(report_file, 'w', encoding='utf-8') as f:
            json.dump(analysis_results, f, indent=2, ensure_ascii=False)
        
        # Итоговый отчет
        logging.info("=" * 80)
        logging.info("📊 ИТОГОВЫЙ ОТЧЕТ РУЧНОГО АНАЛИЗА")
        logging.info("=" * 80)
        
        existing_tables = [r for r in analysis_results if r['structure']['exists']]
        non_existing_tables = [r for r in analysis_results if not r['structure']['exists']]
        
        high_migration_possibility = [r for r in analysis_results if r.get('migration_possibility') == 'high']
        low_migration_possibility = [r for r in analysis_results if r.get('migration_possibility') == 'low']
        
        logging.info(f"📋 Всего таблиц: {len(problematic_tables)}")
        logging.info(f"✅ Существующие таблицы: {len(existing_tables)}")
        logging.info(f"❌ Несуществующие таблицы: {len(non_existing_tables)}")
        logging.info(f"🚀 Высокая возможность миграции: {len(high_migration_possibility)}")
        logging.info(f"⚠️ Низкая возможность миграции: {len(low_migration_possibility)}")
        logging.info(f"📄 Отчет сохранен: {report_file}")
        
        if high_migration_possibility:
            logging.info("🚀 ТАБЛИЦЫ С ВЫСОКОЙ ВОЗМОЖНОСТЬЮ МИГРАЦИИ:")
            for table in high_migration_possibility:
                logging.info(f"   • {table['table_name']}")
        
        if low_migration_possibility:
            logging.warning("⚠️ ТАБЛИЦЫ С НИЗКОЙ ВОЗМОЖНОСТЬЮ МИГРАЦИИ:")
            for table in low_migration_possibility:
                logging.info(f"   • {table['table_name']}")
        
        logging.info("🔧 РЕКОМЕНДАЦИИ:")
        logging.info("   1. Начать миграцию с таблиц высокой возможности")
        logging.info("   2. Исследовать таблицы низкой возможности")
        logging.info("   3. Создать план миграции для каждой группы")
        
        return True
        
    finally:
        mssql_conn.close()
        pg_conn.close()

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)