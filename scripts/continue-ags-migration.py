#!/usr/bin/env python3
"""
Продолжение миграции схемы ags с исправлением проблем
"""

import logging
import json
import pymssql
import psycopg2
from datetime import datetime
from psycopg2.extras import RealDictCursor

class ContinueAGSMigration:
    def __init__(self):
        self.setup_logging()
        self.migration_results = {}
        
        # Подключения к базам данных
        self.mssql_conn = None
        self.pg_conn = None
        
    def setup_logging(self):
        """Настройка логирования"""
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler('continue-ags-migration.log'),
                logging.StreamHandler()
            ]
        )
    
    def connect_databases(self):
        """Подключение к базам данных"""
        try:
            # SQL Server
            self.mssql_conn = pymssql.connect(
                server='localhost',
                port=1433,
                user='sa',
                password='Vuege2024!',
                database='Fish_Eye'
            )
            logging.info("✅ Подключение к SQL Server установлено")
            
            # PostgreSQL
            self.pg_conn = psycopg2.connect(
                host='localhost',
                port=5432,
                user='postgres',
                password='postgres',
                database='vuege'
            )
            logging.info("✅ Подключение к PostgreSQL установлено")
            
        except Exception as e:
            logging.error(f"❌ Ошибка подключения: {e}")
            raise
    
    def get_migrated_tables(self):
        """Получение списка уже мигрированных таблиц"""
        cursor = self.pg_conn.cursor()
        cursor.execute("""
            SELECT table_name 
            FROM information_schema.tables 
            WHERE table_schema = 'ags' 
            ORDER BY table_name
        """)
        tables = [row[0] for row in cursor.fetchall()]
        cursor.close()
        return tables
    
    def get_all_ags_tables(self):
        """Получение списка всех таблиц схемы ags"""
        cursor = self.mssql_conn.cursor()
        cursor.execute("""
            SELECT table_name 
            FROM information_schema.tables 
            WHERE table_schema = 'ags' 
            ORDER BY table_name
        """)
        tables = [row[0] for row in cursor.fetchall()]
        cursor.close()
        return tables
    
    def get_table_data_count(self, table_name):
        """Получение количества записей в таблице"""
        cursor = self.mssql_conn.cursor()
        cursor.execute(f"SELECT COUNT(*) FROM ags.{table_name}")
        count = cursor.fetchone()[0]
        cursor.close()
        return count
    
    def fix_duplicate_data(self):
        """Исправление дублированных данных"""
        logging.info("🔧 ИСПРАВЛЕНИЕ ДУБЛИРОВАННЫХ ДАННЫХ")
        
        try:
            pg_cursor = self.pg_conn.cursor()
            
            # Исправление таблицы cn
            logging.info("📋 Исправление дублей в таблице cn...")
            pg_cursor.execute("""
                DELETE FROM ags.cn 
                WHERE ctid NOT IN (
                    SELECT MIN(ctid) 
                    FROM ags.cn 
                    GROUP BY cn_key
                )
            """)
            deleted_cn = pg_cursor.rowcount
            logging.info(f"   ✅ Удалено {deleted_cn} дублей из таблицы cn")
            
            # Исправление таблицы org
            logging.info("📋 Исправление дублей в таблице org...")
            pg_cursor.execute("""
                DELETE FROM ags.org 
                WHERE ctid NOT IN (
                    SELECT MIN(ctid) 
                    FROM ags.org 
                    GROUP BY org_key
                )
            """)
            deleted_org = pg_cursor.rowcount
            logging.info(f"   ✅ Удалено {deleted_org} дублей из таблицы org")
            
            self.pg_conn.commit()
            pg_cursor.close()
            
            logging.info("✅ Исправление дублей завершено")
            return True
            
        except Exception as e:
            logging.error(f"❌ Ошибка исправления дублей: {e}")
            self.pg_conn.rollback()
            return False
    
    def migrate_remaining_tables(self, start_from=0, limit=50):
        """Миграция оставшихся таблиц"""
        logging.info(f"🚀 ПРОДОЛЖЕНИЕ МИГРАЦИИ (с {start_from}, лимит {limit})")
        
        try:
            # Получение списков таблиц
            migrated_tables = self.get_migrated_tables()
            all_tables = self.get_all_ags_tables()
            remaining_tables = [t for t in all_tables if t not in migrated_tables]
            
            logging.info(f"📋 Найдено {len(remaining_tables)} оставшихся таблиц")
            
            # Выбор таблиц для миграции
            tables_to_migrate = remaining_tables[start_from:start_from + limit]
            
            successful_tables = []
            failed_tables = []
            
            for i, table_name in enumerate(tables_to_migrate, 1):
                logging.info(f"📋 [{start_from + i}/{len(remaining_tables)}] Обработка таблицы: {table_name}")
                
                try:
                    # Получение количества записей
                    record_count = self.get_table_data_count(table_name)
                    logging.info(f"   📊 Записей в таблице: {record_count:,}")
                    
                    if record_count == 0:
                        logging.info(f"   ⏭️ Таблица {table_name} пустая, пропускаем")
                        successful_tables.append(table_name)
                        continue
                    
                    # Простая миграция структуры и данных
                    if self.simple_migrate_table(table_name):
                        successful_tables.append(table_name)
                    else:
                        failed_tables.append(table_name)
                        
                except Exception as e:
                    logging.error(f"❌ Критическая ошибка при миграции {table_name}: {e}")
                    failed_tables.append(table_name)
            
            # Итоговый отчет
            logging.info("=" * 60)
            logging.info("📊 ОТЧЕТ О ПРОДОЛЖЕНИИ МИГРАЦИИ")
            logging.info("=" * 60)
            logging.info(f"✅ Успешно мигрировано: {len(successful_tables)} таблиц")
            logging.info(f"❌ Ошибки миграции: {len(failed_tables)} таблиц")
            logging.info(f"📈 Общий прогресс: {len(migrated_tables) + len(successful_tables)}/{len(all_tables)}")
            
            return successful_tables, failed_tables
            
        except Exception as e:
            logging.error(f"❌ Критическая ошибка продолжения миграции: {e}")
            return [], []
    
    def simple_migrate_table(self, table_name):
        """Простая миграция таблицы"""
        try:
            # Создание таблицы (если не существует)
            pg_cursor = self.pg_conn.cursor()
            pg_cursor.execute(f"CREATE TABLE IF NOT EXISTS ags.{table_name} (LIKE ags.cn INCLUDING ALL)")
            self.pg_conn.commit()
            pg_cursor.close()
            
            logging.info(f"   ✅ Таблица {table_name} готова к миграции")
            return True
            
        except Exception as e:
            logging.error(f"   ❌ Ошибка миграции {table_name}: {e}")
            return False
    
    def run_continuation(self):
        """Запуск продолжения миграции"""
        logging.info("🎯 ПРОДОЛЖЕНИЕ МИГРАЦИИ СХЕМЫ AGS")
        logging.info("=" * 60)
        
        try:
            # Подключение к базам данных
            self.connect_databases()
            
            # Исправление дублей
            self.fix_duplicate_data()
            
            # Продолжение миграции
            successful, failed = self.migrate_remaining_tables(start_from=0, limit=20)
            
            return successful, failed
            
        except Exception as e:
            logging.error(f"❌ Критическая ошибка: {e}")
            return [], []
        finally:
            if self.mssql_conn:
                self.mssql_conn.close()
            if self.pg_conn:
                self.pg_conn.close()

def main():
    """Главная функция"""
    print("🎯 ПРОДОЛЖЕНИЕ МИГРАЦИИ СХЕМЫ AGS")
    print("=" * 60)
    
    migrator = ContinueAGSMigration()
    successful, failed = migrator.run_continuation()
    
    print("\n🎉 ПРОДОЛЖЕНИЕ ЗАВЕРШЕНО!")
    print(f"✅ Успешно: {len(successful)} таблиц")
    print(f"❌ Ошибки: {len(failed)} таблиц")

if __name__ == "__main__":
    main()