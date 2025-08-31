#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@file: migrate-foreign-keys.py
@description: Миграция ограничений внешних ключей из SQL Server в PostgreSQL
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
            logging.FileHandler(f'docs/infrastructure/logs/migrate-foreign-keys-{datetime.now().strftime("%Y%m%d_%H%M%S")}.log'),
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

def get_foreign_keys_from_mssql(mssql_conn):
    """Получение всех внешних ключей из SQL Server"""
    try:
        mssql_cursor = mssql_conn.cursor()
        
        # Получаем все внешние ключи для схемы ags
        mssql_cursor.execute("""
            SELECT 
                fk.name as fk_name,
                OBJECT_SCHEMA_NAME(fk.parent_object_id) as schema_name,
                OBJECT_NAME(fk.parent_object_id) as table_name,
                COL_NAME(fkc.parent_object_id, fkc.parent_column_id) as column_name,
                OBJECT_SCHEMA_NAME(fk.referenced_object_id) as referenced_schema_name,
                OBJECT_NAME(fk.referenced_object_id) as referenced_table_name,
                COL_NAME(fkc.referenced_object_id, fkc.referenced_column_id) as referenced_column_name,
                fk.update_referential_action_desc as update_action,
                fk.delete_referential_action_desc as delete_action
            FROM sys.foreign_keys fk
            INNER JOIN sys.foreign_key_columns fkc ON fk.object_id = fkc.constraint_object_id
            WHERE OBJECT_SCHEMA_NAME(fk.parent_object_id) = 'ags'
            ORDER BY fk.parent_object_id, fk.name, fkc.constraint_column_id
        """)
        
        foreign_keys = mssql_cursor.fetchall()
        
        # Группируем по таблицам
        fk_by_table = {}
        for fk in foreign_keys:
            table_name = fk[2].lower()  # Приводим к нижнему регистру
            if table_name not in fk_by_table:
                fk_by_table[table_name] = []
            
            fk_by_table[table_name].append({
                'name': fk[0],
                'schema_name': fk[1],
                'table_name': fk[2],
                'column_name': fk[3].lower(),  # Приводим к нижнему регистру
                'referenced_schema_name': fk[4],
                'referenced_table_name': fk[5].lower(),  # Приводим к нижнему регистру
                'referenced_column_name': fk[6].lower(),  # Приводим к нижнему регистру
                'update_action': fk[7],
                'delete_action': fk[8]
            })
        
        return fk_by_table
        
    except Exception as e:
        logging.error(f"❌ Ошибка получения внешних ключей из SQL Server: {e}")
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

def create_foreign_key_in_pg(pg_conn, fk_info):
    """Создание внешнего ключа в PostgreSQL"""
    try:
        pg_cursor = pg_conn.cursor()
        
        # Проверяем существование таблиц и колонок
        if not check_table_exists_in_pg(pg_conn, fk_info['table_name']):
            logging.warning(f"⚠️ Таблица {fk_info['table_name']} не существует в PostgreSQL")
            return False
        
        if not check_table_exists_in_pg(pg_conn, fk_info['referenced_table_name']):
            logging.warning(f"⚠️ Ссылаемая таблица {fk_info['referenced_table_name']} не существует в PostgreSQL")
            return False
        
        if not check_column_exists_in_pg(pg_conn, fk_info['table_name'], fk_info['column_name']):
            logging.warning(f"⚠️ Колонка {fk_info['column_name']} не существует в таблице {fk_info['table_name']}")
            return False
        
        if not check_column_exists_in_pg(pg_conn, fk_info['referenced_table_name'], fk_info['referenced_column_name']):
            logging.warning(f"⚠️ Ссылаемая колонка {fk_info['referenced_column_name']} не существует в таблице {fk_info['referenced_table_name']}")
            return False
        
        # Формируем SQL для создания внешнего ключа
        fk_name = fk_info['name'].lower()
        table_name = fk_info['table_name'].lower()
        column_name = fk_info['column_name'].lower()
        referenced_table_name = fk_info['referenced_table_name'].lower()
        referenced_column_name = fk_info['referenced_column_name'].lower()
        
        # Определяем действия для UPDATE и DELETE
        update_action = ""
        delete_action = ""
        
        if fk_info['update_action'] == 'CASCADE':
            update_action = " ON UPDATE CASCADE"
        elif fk_info['update_action'] == 'SET_NULL':
            update_action = " ON UPDATE SET NULL"
        elif fk_info['update_action'] == 'SET_DEFAULT':
            update_action = " ON UPDATE SET DEFAULT"
        elif fk_info['update_action'] == 'NO_ACTION':
            update_action = " ON UPDATE NO ACTION"
        
        if fk_info['delete_action'] == 'CASCADE':
            delete_action = " ON DELETE CASCADE"
        elif fk_info['delete_action'] == 'SET_NULL':
            delete_action = " ON DELETE SET NULL"
        elif fk_info['delete_action'] == 'SET_DEFAULT':
            delete_action = " ON DELETE SET DEFAULT"
        elif fk_info['delete_action'] == 'NO_ACTION':
            delete_action = " ON DELETE NO ACTION"
        
        create_sql = f"""
        ALTER TABLE ags."{table_name}" 
        ADD CONSTRAINT "{fk_name}" 
        FOREIGN KEY ("{column_name}") 
        REFERENCES ags."{referenced_table_name}" ("{referenced_column_name}")
        {update_action}{delete_action}
        """
        
        # Проверяем, не существует ли уже такой внешний ключ
        pg_cursor.execute(f"""
            SELECT COUNT(*) FROM information_schema.table_constraints 
            WHERE constraint_schema = 'ags' 
            AND constraint_name = '{fk_name}'
            AND constraint_type = 'FOREIGN KEY'
        """)
        
        if pg_cursor.fetchone()[0] > 0:
            logging.info(f"⚠️ Внешний ключ {fk_name} уже существует в PostgreSQL")
            return True
        
        # Создаем внешний ключ
        pg_cursor.execute(create_sql)
        pg_conn.commit()
        
        logging.info(f"✅ Создан внешний ключ {fk_name} для таблицы {table_name}")
        return True
        
    except Exception as e:
        logging.error(f"❌ Ошибка создания внешнего ключа {fk_info['name']}: {e}")
        pg_conn.rollback()
        return False

def migrate_foreign_keys():
    """Миграция внешних ключей из SQL Server в PostgreSQL"""
    logger = setup_logging()
    
    logging.info("🔗 МИГРАЦИЯ ВНЕШНИХ КЛЮЧЕЙ ИЗ SQL SERVER В POSTGRESQL")
    logging.info("=" * 80)
    
    # Подключение к базам данных
    mssql_conn, pg_conn = connect_databases()
    if not mssql_conn or not pg_conn:
        logging.error("❌ Не удалось подключиться к базам данных")
        return False
    
    try:
        # Получаем внешние ключи из SQL Server
        logging.info("📋 Получение внешних ключей из SQL Server...")
        foreign_keys = get_foreign_keys_from_mssql(mssql_conn)
        
        if not foreign_keys:
            logging.warning("⚠️ Внешние ключи не найдены в SQL Server")
            return True
        
        logging.info(f"📊 Найдено {len(foreign_keys)} таблиц с внешними ключами")
        
        total_fks = sum(len(fks) for fks in foreign_keys.values())
        logging.info(f"📊 Общее количество внешних ключей: {total_fks}")
        
        # Мигрируем внешние ключи
        success_count = 0
        error_count = 0
        skipped_count = 0
        
        for table_name, fk_list in foreign_keys.items():
            logging.info(f"📋 Обработка таблицы: {table_name} ({len(fk_list)} внешних ключей)")
            
            for fk_info in fk_list:
                logging.info(f"   🔗 Обработка внешнего ключа: {fk_info['name']}")
                
                # Проверяем существование таблиц
                if not check_table_exists_in_pg(pg_conn, fk_info['table_name']):
                    logging.warning(f"   ⚠️ Таблица {fk_info['table_name']} не существует в PostgreSQL, пропускаем")
                    skipped_count += 1
                    continue
                
                if not check_table_exists_in_pg(pg_conn, fk_info['referenced_table_name']):
                    logging.warning(f"   ⚠️ Ссылаемая таблица {fk_info['referenced_table_name']} не существует в PostgreSQL, пропускаем")
                    skipped_count += 1
                    continue
                
                # Создаем внешний ключ
                success = create_foreign_key_in_pg(pg_conn, fk_info)
                
                if success:
                    success_count += 1
                    logging.info(f"   ✅ Внешний ключ {fk_info['name']} успешно создан")
                else:
                    error_count += 1
                    logging.error(f"   ❌ Ошибка создания внешнего ключа {fk_info['name']}")
            
            logging.info("-" * 60)
        
        # Итоговый отчет
        logging.info("=" * 80)
        logging.info("📊 ИТОГОВЫЙ ОТЧЕТ МИГРАЦИИ ВНЕШНИХ КЛЮЧЕЙ")
        logging.info("=" * 80)
        logging.info(f"📋 Всего внешних ключей: {total_fks}")
        logging.info(f"✅ Успешно создано: {success_count}")
        logging.info(f"❌ Ошибки создания: {error_count}")
        logging.info(f"⚠️ Пропущено: {skipped_count}")
        logging.info(f"📈 Процент успеха: {(success_count/total_fks*100):.1f}%")
        
        if error_count == 0:
            logging.info("🎉 ВСЕ ВНЕШНИЕ КЛЮЧИ УСПЕШНО МИГРИРОВАНЫ!")
        else:
            logging.warning(f"⚠️ Осталось {error_count} проблемных внешних ключей")
        
        return error_count == 0
        
    finally:
        mssql_conn.close()
        pg_conn.close()

def main():
    """Основная функция"""
    success = migrate_foreign_keys()
    
    if success:
        logging.info("✅ Миграция внешних ключей завершена успешно")
    else:
        logging.error("❌ Ошибка миграции внешних ключей")
    
    return success

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)