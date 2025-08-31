#!/usr/bin/env python3
"""
Скрипт для тестовой миграции данных из SQL Server в PostgreSQL
Мигрирует только 5-10 таблиц для проверки процесса
"""

import pyodbc
import psycopg2
import sys
import os
from datetime import datetime
import logging

# Настройка логирования
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('test-migration.log'),
        logging.StreamHandler()
    ]
)

class TestMigration:
    def __init__(self):
        # Параметры подключения к SQL Server
        self.mssql_config = {
            'server': 'localhost,1433',
            'database': 'Fish_Eye',
            'username': 'sa',
            'password': 'Vuege2024!',
            'driver': 'ODBC Driver 18 for SQL Server'
        }
        
        # Параметры подключения к PostgreSQL
        self.postgres_config = {
            'host': 'localhost',
            'port': 5432,
            'database': 'Fish_Eye',
            'user': 'postgres',
            'password': 'postgres'
        }
        
        self.mssql_conn = None
        self.postgres_conn = None
        
        # Список таблиц для тестовой миграции (небольшие таблицы)
        self.test_tables = [
            'accnt',      # Счета
            'cn',         # Контракты (основная таблица)
            'cst',        # Клиенты
            'org',        # Организации
            'st'          # Статусы
        ]
        
    def connect_mssql(self):
        """Подключение к SQL Server"""
        try:
            connection_string = (
                f"DRIVER={{{self.mssql_config['driver']}}};"
                f"SERVER={self.mssql_config['server']};"
                f"DATABASE={self.mssql_config['database']};"
                f"UID={self.mssql_config['username']};"
                f"PWD={self.mssql_config['password']};"
                f"TrustServerCertificate=yes;"
            )
            self.mssql_conn = pyodbc.connect(connection_string)
            logging.info("✅ Подключение к SQL Server установлено")
            return True
        except Exception as e:
            logging.error(f"❌ Ошибка подключения к SQL Server: {e}")
            return False
    
    def connect_postgres(self):
        """Подключение к PostgreSQL"""
        try:
            self.postgres_conn = psycopg2.connect(**self.postgres_config)
            logging.info("✅ Подключение к PostgreSQL установлено")
            return True
        except Exception as e:
            logging.error(f"❌ Ошибка подключения к PostgreSQL: {e}")
            return False
    
    def get_table_info(self, table_name):
        """Получение информации о таблице"""
        cursor = self.mssql_conn.cursor()
        
        # Количество записей
        cursor.execute(f"SELECT COUNT(*) FROM ags.{table_name}")
        row_count = cursor.fetchone()[0]
        
        # Структура таблицы
        cursor.execute(f"""
        SELECT 
            COLUMN_NAME,
            DATA_TYPE,
            CHARACTER_MAXIMUM_LENGTH,
            NUMERIC_PRECISION,
            NUMERIC_SCALE,
            IS_NULLABLE,
            COLUMN_DEFAULT
        FROM INFORMATION_SCHEMA.COLUMNS 
        WHERE TABLE_SCHEMA = 'ags' 
            AND TABLE_NAME = '{table_name}'
        ORDER BY ORDINAL_POSITION
        """)
        columns = cursor.fetchall()
        
        return {
            'row_count': row_count,
            'columns': columns
        }
    
    def convert_data_type(self, mssql_type, max_length, precision, scale):
        """Конвертация типов данных SQL Server в PostgreSQL"""
        type_mapping = {
            'int': 'INTEGER',
            'bigint': 'BIGINT',
            'smallint': 'SMALLINT',
            'tinyint': 'SMALLINT',
            'bit': 'BOOLEAN',
            'char': f'CHAR({max_length})' if max_length else 'CHAR(1)',
            'nchar': f'CHAR({max_length})' if max_length else 'CHAR(1)',
            'varchar': f'VARCHAR({max_length})' if max_length else 'TEXT',
            'nvarchar': f'VARCHAR({max_length})' if max_length else 'TEXT',
            'text': 'TEXT',
            'ntext': 'TEXT',
            'datetime': 'TIMESTAMP',
            'datetime2': 'TIMESTAMP',
            'date': 'DATE',
            'time': 'TIME',
            'decimal': f'DECIMAL({precision},{scale})' if precision and scale else 'DECIMAL',
            'numeric': f'DECIMAL({precision},{scale})' if precision and scale else 'DECIMAL',
            'float': 'DOUBLE PRECISION',
            'real': 'REAL',
            'money': 'DECIMAL(19,4)',
            'smallmoney': 'DECIMAL(10,4)',
            'uniqueidentifier': 'UUID',
            'binary': f'BYTEA',
            'varbinary': f'BYTEA',
            'image': 'BYTEA'
        }
        return type_mapping.get(mssql_type.lower(), 'TEXT')
    
    def create_table_postgres(self, table_name, columns):
        """Создание таблицы в PostgreSQL"""
        cursor = self.postgres_conn.cursor()
        
        # Формирование SQL для создания таблицы
        column_definitions = []
        for col in columns:
            col_name = col[0]
            col_type = col[1]
            max_length = col[2]
            precision = col[3]
            scale = col[4]
            is_nullable = col[5]
            default_value = col[6]
            
            pg_type = self.convert_data_type(col_type, max_length, precision, scale)
            nullable = "" if is_nullable == 'YES' else " NOT NULL"
            default = f" DEFAULT {default_value}" if default_value else ""
            
            column_definitions.append(f'"{col_name}" {pg_type}{nullable}{default}')
        
        create_sql = f"""
        CREATE TABLE IF NOT EXISTS ags."{table_name}" (
            {', '.join(column_definitions)}
        );
        """
        
        try:
            cursor.execute(create_sql)
            self.postgres_conn.commit()
            logging.info(f"✅ Таблица ags.{table_name} создана")
            return True
        except Exception as e:
            logging.error(f"❌ Ошибка создания таблицы {table_name}: {e}")
            self.postgres_conn.rollback()
            return False
    
    def migrate_data(self, table_name):
        """Миграция данных из SQL Server в PostgreSQL"""
        try:
            # Получение данных из SQL Server
            mssql_cursor = self.mssql_conn.cursor()
            mssql_cursor.execute(f"SELECT * FROM ags.{table_name}")
            rows = mssql_cursor.fetchall()
            
            if not rows:
                logging.info(f"📝 Таблица {table_name} пустая, пропускаем")
                return True
            
            # Получение имен колонок
            columns = [column[0] for column in mssql_cursor.description]
            
            # Вставка данных в PostgreSQL
            postgres_cursor = self.postgres_conn.cursor()
            
            # Подготовка SQL для вставки
            placeholders = ', '.join(['%s'] * len(columns))
            column_names = ', '.join([f'"{col}"' for col in columns])
            insert_sql = f'INSERT INTO ags."{table_name}" ({column_names}) VALUES ({placeholders})'
            
            # Вставка данных
            postgres_cursor.executemany(insert_sql, rows)
            self.postgres_conn.commit()
            
            logging.info(f"✅ Данные из таблицы {table_name} мигрированы ({len(rows)} строк)")
            return True
            
        except Exception as e:
            logging.error(f"❌ Ошибка миграции данных из таблицы {table_name}: {e}")
            self.postgres_conn.rollback()
            return False
    
    def validate_migration(self, table_name):
        """Валидация миграции"""
        try:
            # Подсчет записей в SQL Server
            mssql_cursor = self.mssql_conn.cursor()
            mssql_cursor.execute(f"SELECT COUNT(*) FROM ags.{table_name}")
            mssql_count = mssql_cursor.fetchone()[0]
            
            # Подсчет записей в PostgreSQL
            postgres_cursor = self.postgres_conn.cursor()
            postgres_cursor.execute(f'SELECT COUNT(*) FROM ags."{table_name}"')
            postgres_count = postgres_cursor.fetchone()[0]
            
            if mssql_count == postgres_count:
                logging.info(f"✅ Валидация {table_name}: {mssql_count} = {postgres_count} ✓")
                return True
            else:
                logging.error(f"❌ Валидация {table_name}: {mssql_count} ≠ {postgres_count} ✗")
                return False
                
        except Exception as e:
            logging.error(f"❌ Ошибка валидации таблицы {table_name}: {e}")
            return False
    
    def run_test_migration(self):
        """Запуск тестовой миграции"""
        logging.info("🧪 Начало тестовой миграции схемы ags")
        logging.info(f"📋 Тестовые таблицы: {', '.join(self.test_tables)}")
        
        # Подключение к базам данных
        if not self.connect_mssql() or not self.connect_postgres():
            return False
        
        try:
            success_count = 0
            error_count = 0
            
            for table_name in self.test_tables:
                logging.info(f"\n🔄 Миграция таблицы: {table_name}")
                
                try:
                    # Получение информации о таблице
                    table_info = self.get_table_info(table_name)
                    logging.info(f"📊 Таблица {table_name}: {table_info['row_count']} записей, {len(table_info['columns'])} колонок")
                    
                    # Создание таблицы в PostgreSQL
                    if self.create_table_postgres(table_name, table_info['columns']):
                        # Миграция данных
                        if self.migrate_data(table_name):
                            # Валидация
                            if self.validate_migration(table_name):
                                success_count += 1
                            else:
                                error_count += 1
                        else:
                            error_count += 1
                    else:
                        error_count += 1
                        
                except Exception as e:
                    logging.error(f"❌ Ошибка при миграции таблицы {table_name}: {e}")
                    error_count += 1
            
            logging.info(f"\n📊 РЕЗУЛЬТАТЫ ТЕСТОВОЙ МИГРАЦИИ:")
            logging.info(f"✅ Успешно: {success_count}")
            logging.info(f"❌ Ошибок: {error_count}")
            logging.info(f"📋 Всего таблиц: {len(self.test_tables)}")
            
            if error_count == 0:
                logging.info("🎉 Тестовая миграция прошла успешно!")
                logging.info("🚀 Можно переходить к полной миграции")
            else:
                logging.warning("⚠️ Обнаружены ошибки. Требуется анализ перед полной миграцией")
            
            return error_count == 0
            
        finally:
            if self.mssql_conn:
                self.mssql_conn.close()
            if self.postgres_conn:
                self.postgres_conn.close()

if __name__ == "__main__":
    migration = TestMigration()
    success = migration.run_test_migration()
    sys.exit(0 if success else 1)