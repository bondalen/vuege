#!/usr/bin/env python3
"""
Скрипт для миграции данных из SQL Server в PostgreSQL
Мигрирует схему ags из базы данных Fish_Eye
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
        logging.FileHandler('migration.log'),
        logging.StreamHandler()
    ]
)

class MSSQLToPostgresMigration:
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
    
    def get_table_structure(self, table_name):
        """Получение структуры таблицы из SQL Server"""
        cursor = self.mssql_conn.cursor()
        query = """
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
            AND TABLE_NAME = ?
        ORDER BY ORDINAL_POSITION
        """
        cursor.execute(query, (table_name,))
        return cursor.fetchall()
    
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
    
    def get_tables_list(self):
        """Получение списка таблиц в схеме ags"""
        cursor = self.mssql_conn.cursor()
        cursor.execute("""
            SELECT TABLE_NAME 
            FROM INFORMATION_SCHEMA.TABLES 
            WHERE TABLE_SCHEMA = 'ags' 
                AND TABLE_TYPE = 'BASE TABLE'
            ORDER BY TABLE_NAME
        """)
        return [row[0] for row in cursor.fetchall()]
    
    def run_migration(self):
        """Запуск полной миграции"""
        logging.info("🚀 Начало миграции схемы ags из SQL Server в PostgreSQL")
        
        # Подключение к базам данных
        if not self.connect_mssql() or not self.connect_postgres():
            return False
        
        try:
            # Получение списка таблиц
            tables = self.get_tables_list()
            logging.info(f"📋 Найдено {len(tables)} таблиц для миграции")
            
            success_count = 0
            error_count = 0
            
            for table_name in tables:
                logging.info(f"🔄 Миграция таблицы: {table_name}")
                
                try:
                    # Получение структуры таблицы
                    columns = self.get_table_structure(table_name)
                    
                    # Создание таблицы в PostgreSQL
                    if self.create_table_postgres(table_name, columns):
                        # Миграция данных
                        if self.migrate_data(table_name):
                            success_count += 1
                        else:
                            error_count += 1
                    else:
                        error_count += 1
                        
                except Exception as e:
                    logging.error(f"❌ Ошибка при миграции таблицы {table_name}: {e}")
                    error_count += 1
            
            logging.info(f"✅ Миграция завершена. Успешно: {success_count}, Ошибок: {error_count}")
            return error_count == 0
            
        finally:
            if self.mssql_conn:
                self.mssql_conn.close()
            if self.postgres_conn:
                self.postgres_conn.close()

if __name__ == "__main__":
    migration = MSSQLToPostgresMigration()
    success = migration.run_migration()
    sys.exit(0 if success else 1)