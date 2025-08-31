#!/usr/bin/env python3
"""
@file: dbhub-migrate-group1-data.py
@description: Миграция данных группы 1 из SQL Server в PostgreSQL с использованием DBHub
@created: 2025-08-30
"""

import logging
import pyodbc
import psycopg2
from datetime import datetime

class DBHubGroup1DataMigration:
    def __init__(self):
        self.setup_logging()
        self.group_name = "Группа 1: Основные справочники"
        self.tables = ["cn", "org", "cst"]
        
        # Подключение к SQL Server
        self.mssql_conn_str = (
            "DRIVER={ODBC Driver 18 for SQL Server};"
            "SERVER=localhost,1433;"
            "DATABASE=Fish_Eye;"
            "UID=sa;"
            "PWD=Vuege2024!;"
            "Encrypt=no;"
            "TrustServerCertificate=yes;"
        )
        
        # Подключение к PostgreSQL
        self.pg_conn_str = "dbname=Fish_Eye user=postgres password=postgres host=localhost port=5432"
        
        self.mssql_conn = None
        self.pg_conn = None
        
    def setup_logging(self):
        """Настройка логирования"""
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler('dbhub-group1-data-migration.log'),
                logging.StreamHandler()
            ]
        )
    
    def connect_mssql(self):
        """Подключение к SQL Server"""
        try:
            self.mssql_conn = pyodbc.connect(self.mssql_conn_str)
            logging.info("✅ Подключение к SQL Server успешно.")
            return True
        except pyodbc.Error as ex:
            logging.error(f"❌ Ошибка подключения к SQL Server: {ex}")
            return False
    
    def connect_postgres(self):
        """Подключение к PostgreSQL"""
        try:
            self.pg_conn = psycopg2.connect(self.pg_conn_str)
            logging.info("✅ Подключение к PostgreSQL успешно.")
            return True
        except psycopg2.Error as ex:
            logging.error(f"❌ Ошибка подключения к PostgreSQL: {ex}")
            return False
    
    def get_mssql_data(self, table_name):
        """Получение данных из SQL Server"""
        cursor = self.mssql_conn.cursor()
        try:
            cursor.execute(f"SELECT * FROM ags.{table_name}")
            data = cursor.fetchall()
            logging.info(f"📄 Получены данные из SQL Server для таблицы {table_name}: {len(data)} записей")
            return data
        except pyodbc.Error as ex:
            logging.error(f"❌ Ошибка получения данных из таблицы {table_name}: {ex}")
            return []
    
    def insert_postgres_data(self, table_name, data):
        """Вставка данных в PostgreSQL"""
        if not data:
            logging.info(f"⚠️ Нет данных для вставки в таблицу {table_name}.")
            return False
        
        pg_cursor = self.pg_conn.cursor()
        try:
            # Получение структуры таблицы для создания INSERT запроса
            pg_cursor.execute(f"""
                SELECT column_name 
                FROM information_schema.columns 
                WHERE table_schema = 'ags' AND table_name = '{table_name}'
                ORDER BY ordinal_position
            """)
            columns = [row[0] for row in pg_cursor.fetchall()]
            
            # Создание INSERT запроса
            columns_str = ", ".join([f'"{col}"' for col in columns])
            placeholders = ", ".join(['%s'] * len(columns))
            insert_sql = f"INSERT INTO ags.{table_name} ({columns_str}) VALUES ({placeholders})"
            
            # Вставка данных
            pg_cursor.executemany(insert_sql, data)
            self.pg_conn.commit()
            
            logging.info(f"✅ Данные таблицы {table_name} мигрированы: {len(data)} записей")
            return True
            
        except psycopg2.Error as ex:
            logging.error(f"❌ Ошибка вставки данных в таблицу {table_name}: {ex}")
            self.pg_conn.rollback()
            return False
    
    def validate_migration(self, table_name):
        """Валидация миграции"""
        pg_cursor = self.pg_conn.cursor()
        try:
            pg_cursor.execute(f"SELECT COUNT(*) FROM ags.{table_name}")
            pg_count = pg_cursor.fetchone()[0]
            
            mssql_cursor = self.mssql_conn.cursor()
            mssql_cursor.execute(f"SELECT COUNT(*) FROM ags.{table_name}")
            mssql_count = mssql_cursor.fetchone()[0]
            
            if pg_count == mssql_count:
                logging.info(f"✅ Валидация {table_name}: {pg_count} записей")
                return True
            else:
                logging.warning(f"⚠️ Несоответствие в таблице {table_name}: SQL Server {mssql_count} vs PostgreSQL {pg_count}")
                return False
                
        except Exception as ex:
            logging.error(f"❌ Ошибка валидации таблицы {table_name}: {ex}")
            return False
    
    def migrate_table(self, table_name):
        """Миграция одной таблицы"""
        logging.info(f"\n🔄 Миграция таблицы {table_name}")
        print(f"🔄 Миграция таблицы: {table_name}")
        
        try:
            # 1. Получение данных из SQL Server
            data = self.get_mssql_data(table_name)
            
            if not data:
                logging.info(f"⚠️ Таблица {table_name} пустая в SQL Server")
                print(f"⚠️ {table_name}: Пустая таблица")
                return {"status": "empty", "table": table_name}
            
            # 2. Вставка данных в PostgreSQL
            if self.insert_postgres_data(table_name, data):
                # 3. Валидация
                if self.validate_migration(table_name):
                    print(f"✅ {table_name}: {len(data)} записей")
                    return {"status": "success", "table": table_name, "rows": len(data)}
                else:
                    print(f"⚠️ {table_name}: Ошибка валидации")
                    return {"status": "validation_error", "table": table_name}
            else:
                print(f"❌ {table_name}: Ошибка вставки данных")
                return {"status": "insert_error", "table": table_name}
                
        except Exception as e:
            logging.error(f"❌ Ошибка миграции таблицы {table_name}: {e}")
            print(f"❌ {table_name}: Ошибка - {e}")
            return {"status": "error", "table": table_name, "error": str(e)}
    
    def run_migration(self):
        """Запуск миграции группы"""
        logging.info(f"🚀 Начало миграции данных {self.group_name}")
        print(f"\n🚀 МИГРАЦИЯ ДАННЫХ: {self.group_name}")
        print("=" * 60)
        
        if not self.connect_mssql() or not self.connect_postgres():
            logging.error("❌ Не удалось подключиться к базам данных")
            return
        
        successful_migrations = 0
        failed_migrations = 0
        empty_tables = 0
        total_rows = 0
        
        for table in self.tables:
            result = self.migrate_table(table)
            
            if result["status"] == "success":
                successful_migrations += 1
                total_rows += result.get("rows", 0)
            elif result["status"] == "empty":
                empty_tables += 1
            else:
                failed_migrations += 1
        
        # Закрытие соединений
        if self.mssql_conn:
            self.mssql_conn.close()
        if self.pg_conn:
            self.pg_conn.close()
        
        # Итоги
        print("\n" + "=" * 60)
        print("📊 ИТОГИ МИГРАЦИИ ДАННЫХ:")
        print("=" * 60)
        print(f"📋 Группа: {self.group_name}")
        print(f"📊 Всего таблиц: {len(self.tables)}")
        print(f"✅ Успешно: {successful_migrations}")
        print(f"⚠️ Пустых: {empty_tables}")
        print(f"❌ Ошибок: {failed_migrations}")
        print(f"📦 Всего записей: {total_rows}")
        print("=" * 60)
        
        logging.info(f"🎉 Миграция данных завершена: {successful_migrations} успешно, {failed_migrations} ошибок")

def main():
    """Основная функция"""
    print("🚀 Запуск миграции данных группы 1 с DBHub")
    
    migrator = DBHubGroup1DataMigration()
    migrator.run_migration()

if __name__ == "__main__":
    main()