#!/usr/bin/env python3
"""
Скрипт для миграции данных из SQL Server в PostgreSQL через Docker
Использует docker exec для выполнения команд
"""

import subprocess
import sys
import logging
from datetime import datetime

# Настройка логирования
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('migration-docker.log'),
        logging.StreamHandler()
    ]
)

class DockerMigration:
    def __init__(self):
        self.test_tables = [
            'accnt',      # Счета
            'cn',         # Контракты
            'cst',        # Клиенты
            'org',        # Организации
            'st'          # Статусы
        ]
        
    def run_sqlcmd(self, query, database='Fish_Eye'):
        """Выполнение команды SQL Server через docker exec"""
        cmd = [
            'docker', 'exec', 'vuege-mssql',
            '/opt/mssql-tools18/bin/sqlcmd',
            '-S', 'localhost',
            '-U', 'sa',
            '-P', 'Vuege2024!',
            '-C',
            '-d', database,
            '-Q', query
        ]
        
        try:
            result = subprocess.run(cmd, capture_output=True, text=True, timeout=30)
            if result.returncode == 0:
                return result.stdout.strip()
            else:
                logging.error(f"SQL Server ошибка: {result.stderr}")
                return None
        except subprocess.TimeoutExpired:
            logging.error("Timeout при выполнении SQL команды")
            return None
        except Exception as e:
            logging.error(f"Ошибка выполнения SQL команды: {e}")
            return None
    
    def run_psql(self, query, database='Fish_Eye'):
        """Выполнение команды PostgreSQL через docker exec"""
        cmd = [
            'docker', 'exec', 'postgres-java-universal',
            'psql',
            '-U', 'postgres',
            '-d', database,
            '-c', query
        ]
        
        try:
            result = subprocess.run(cmd, capture_output=True, text=True, timeout=30)
            if result.returncode == 0:
                return result.stdout.strip()
            else:
                logging.error(f"PostgreSQL ошибка: {result.stderr}")
                return None
        except subprocess.TimeoutExpired:
            logging.error("Timeout при выполнении PostgreSQL команды")
            return None
        except Exception as e:
            logging.error(f"Ошибка выполнения PostgreSQL команды: {e}")
            return None
    
    def get_table_structure(self, table_name):
        """Получение структуры таблицы из SQL Server"""
        query = f"""
        SELECT 
            COLUMN_NAME + ' ' + 
            DATA_TYPE + 
            CASE 
                WHEN CHARACTER_MAXIMUM_LENGTH IS NOT NULL THEN '(' + CAST(CHARACTER_MAXIMUM_LENGTH AS VARCHAR) + ')'
                WHEN NUMERIC_PRECISION IS NOT NULL AND NUMERIC_SCALE IS NOT NULL THEN '(' + CAST(NUMERIC_PRECISION AS VARCHAR) + ',' + CAST(NUMERIC_SCALE AS VARCHAR) + ')'
                ELSE ''
            END +
            CASE WHEN IS_NULLABLE = 'NO' THEN ' NOT NULL' ELSE '' END
        FROM INFORMATION_SCHEMA.COLUMNS 
        WHERE TABLE_SCHEMA = 'ags' 
            AND TABLE_NAME = '{table_name}'
        ORDER BY ORDINAL_POSITION
        """
        
        result = self.run_sqlcmd(query)
        if result:
            lines = result.split('\n')
            columns = []
            for line in lines:
                if line.strip() and not line.startswith('---') and not line.startswith('('):
                    columns.append(line.strip())
            return columns
        return None
    
    def get_table_data(self, table_name):
        """Получение данных из таблицы SQL Server"""
        query = f"SELECT * FROM ags.{table_name}"
        return self.run_sqlcmd(query)
    
    def get_table_count(self, table_name):
        """Получение количества записей в таблице"""
        query = f"SELECT COUNT(*) FROM ags.{table_name}"
        result = self.run_sqlcmd(query)
        if result:
            lines = result.split('\n')
            for line in lines:
                if line.strip().isdigit():
                    return int(line.strip())
        return 0
    
    def create_table_postgres(self, table_name, columns):
        """Создание таблицы в PostgreSQL"""
        if not columns:
            return False
            
        # Конвертация типов данных
        pg_columns = []
        for col_def in columns:
            # Простая конвертация типов
            pg_col = col_def.replace('varchar', 'VARCHAR')
            pg_col = pg_col.replace('int', 'INTEGER')
            pg_col = pg_col.replace('datetime', 'TIMESTAMP')
            pg_col = pg_col.replace('bit', 'BOOLEAN')
            pg_col = pg_col.replace('decimal', 'DECIMAL')
            pg_col = pg_col.replace('money', 'DECIMAL(19,4)')
            pg_col = pg_col.replace('uniqueidentifier', 'UUID')
            pg_col = pg_col.replace('text', 'TEXT')
            pg_col = pg_col.replace('ntext', 'TEXT')
            pg_col = pg_col.replace('binary', 'BYTEA')
            pg_col = pg_col.replace('image', 'BYTEA')
            
            pg_columns.append(f'"{pg_col}"')
        
        create_sql = f"""
        CREATE TABLE IF NOT EXISTS ags."{table_name}" (
            {', '.join(pg_columns)}
        );
        """
        
        result = self.run_psql(create_sql)
        return result is not None
    
    def migrate_table_data(self, table_name):
        """Миграция данных таблицы"""
        # Получение данных в формате CSV
        query = f"""
        SELECT * FROM ags.{table_name}
        FOR JSON PATH
        """
        
        data = self.run_sqlcmd(query)
        if not data:
            return False
        
        # Здесь нужно будет реализовать более сложную логику
        # для преобразования JSON в INSERT statements
        # Пока просто логируем
        logging.info(f"Данные получены для таблицы {table_name}")
        return True
    
    def run_test_migration(self):
        """Запуск тестовой миграции"""
        logging.info("🧪 Начало тестовой миграции через Docker")
        
        success_count = 0
        error_count = 0
        
        for table_name in self.test_tables:
            logging.info(f"\n🔄 Обработка таблицы: {table_name}")
            
            try:
                # Получение информации о таблице
                count = self.get_table_count(table_name)
                logging.info(f"📊 Таблица {table_name}: {count} записей")
                
                # Получение структуры таблицы
                columns = self.get_table_structure(table_name)
                if columns:
                    logging.info(f"📋 Структура таблицы {table_name}: {len(columns)} колонок")
                    
                    # Создание таблицы в PostgreSQL
                    if self.create_table_postgres(table_name, columns):
                        logging.info(f"✅ Таблица {table_name} создана в PostgreSQL")
                        success_count += 1
                    else:
                        logging.error(f"❌ Ошибка создания таблицы {table_name}")
                        error_count += 1
                else:
                    logging.error(f"❌ Не удалось получить структуру таблицы {table_name}")
                    error_count += 1
                    
            except Exception as e:
                logging.error(f"❌ Ошибка при обработке таблицы {table_name}: {e}")
                error_count += 1
        
        logging.info(f"\n📊 РЕЗУЛЬТАТЫ ТЕСТОВОЙ МИГРАЦИИ:")
        logging.info(f"✅ Успешно: {success_count}")
        logging.info(f"❌ Ошибок: {error_count}")
        
        return error_count == 0

if __name__ == "__main__":
    migration = DockerMigration()
    success = migration.run_test_migration()
    sys.exit(0 if success else 1)