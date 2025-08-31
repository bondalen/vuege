#!/usr/bin/env python3
"""
Скрипт для исправления структуры таблиц PostgreSQL
Создает правильные таблицы с именами колонок как в SQL Server
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
        logging.FileHandler('fix-table-structure.log'),
        logging.StreamHandler()
    ]
)

class FixTableStructure:
    def __init__(self):
        # Таблицы для исправления структуры
        self.tables_to_fix = [
            'st',         # Статусы
            'cn_s_type',  # Типы контрактов
            'cn_PrDocT',  # Типы документов
            'ipg'         # Инвестиционные группы
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
            result = subprocess.run(cmd, capture_output=True, text=True, timeout=60)
            if result.returncode == 0:
                return result.stdout.strip()
            else:
                logging.error(f"SQL Server ошибка: {result.stderr}")
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
            result = subprocess.run(cmd, capture_output=True, text=True, timeout=60)
            if result.returncode == 0:
                return result.stdout.strip()
            else:
                logging.error(f"PostgreSQL ошибка: {result.stderr}")
                return None
        except Exception as e:
            logging.error(f"Ошибка выполнения PostgreSQL команды: {e}")
            return None
    
    def get_sqlserver_structure(self, table_name):
        """Получение структуры таблицы из SQL Server"""
        query = f"""
        SELECT 
            COLUMN_NAME,
            DATA_TYPE,
            CHARACTER_MAXIMUM_LENGTH,
            IS_NULLABLE,
            COLUMN_DEFAULT
        FROM INFORMATION_SCHEMA.COLUMNS 
        WHERE TABLE_SCHEMA = 'ags' AND TABLE_NAME = '{table_name}'
        ORDER BY ORDINAL_POSITION
        """
        return self.run_sqlcmd(query)
    
    def create_correct_table(self, table_name):
        """Создание правильной таблицы с именами колонок как в SQL Server"""
        logging.info(f"🔧 Исправление структуры таблицы {table_name}")
        
        # Получение структуры из SQL Server
        structure = self.get_sqlserver_structure(table_name)
        if not structure:
            logging.error(f"❌ Не удалось получить структуру таблицы {table_name} из SQL Server")
            return False
        
        logging.info(f"📋 Структура таблицы {table_name} в SQL Server:")
        logging.info(structure)
        
        # Создание правильной таблицы
        if table_name == 'st':
            # Удаляем старую таблицу
            drop_sql = 'DROP TABLE IF EXISTS ags.st;'
            self.run_psql(drop_sql)
            
            # Создаем правильную таблицу
            create_sql = """
            CREATE TABLE ags.st (
                stKey INTEGER NOT NULL,
                stType INTEGER,
                stNote VARCHAR(100),
                stTimeOfEntry TIMESTAMP
            );
            """
        elif table_name == 'cn_s_type':
            drop_sql = 'DROP TABLE IF EXISTS ags.cn_s_type;'
            self.run_psql(drop_sql)
            
            create_sql = """
            CREATE TABLE ags.cn_s_type (
                cst_key INTEGER NOT NULL,
                cst_name VARCHAR(255),
                cst_type VARCHAR(50)
            );
            """
        elif table_name == 'cn_PrDocT':
            drop_sql = 'DROP TABLE IF EXISTS ags."cn_PrDocT";'
            self.run_psql(drop_sql)
            
            create_sql = """
            CREATE TABLE ags."cn_PrDocT" (
                pdtoKey INTEGER NOT NULL,
                pdtoType VARCHAR(5),
                pdtoCode VARCHAR(50),
                pdtoText VARCHAR(255)
            );
            """
        elif table_name == 'ipg':
            drop_sql = 'DROP TABLE IF EXISTS ags.ipg;'
            self.run_psql(drop_sql)
            
            create_sql = """
            CREATE TABLE ags.ipg (
                ipgKey INTEGER NOT NULL,
                ipgOg INTEGER,
                ipgNm VARCHAR(150),
                ipgYy INTEGER,
                ipgNum SMALLINT,
                ipgStr DATE,
                ipgEnd DATE,
                ipgRepl INTEGER,
                ipgStRlSh INTEGER,
                ipgYyYear INTEGER
            );
            """
        else:
            logging.error(f"❌ Неизвестная таблица {table_name}")
            return False
        
        # Создание таблицы
        result = self.run_psql(create_sql)
        if result:
            logging.info(f"✅ Таблица {table_name} пересоздана с правильной структурой")
            return True
        else:
            logging.error(f"❌ Ошибка создания таблицы {table_name}")
            return False
    
    def run_fix_structure(self):
        """Запуск исправления структуры таблиц"""
        logging.info("🚀 Начало исправления структуры таблиц")
        logging.info(f"📋 Таблиц для исправления: {len(self.tables_to_fix)}")
        
        success_count = 0
        error_count = 0
        
        for table_name in self.tables_to_fix:
            try:
                if self.create_correct_table(table_name):
                    success_count += 1
                else:
                    error_count += 1
            except Exception as e:
                logging.error(f"❌ Ошибка при исправлении таблицы {table_name}: {e}")
                error_count += 1
        
        logging.info(f"\n📊 РЕЗУЛЬТАТЫ ИСПРАВЛЕНИЯ СТРУКТУРЫ:")
        logging.info(f"✅ Успешно: {success_count}")
        logging.info(f"❌ Ошибок: {error_count}")
        
        return error_count == 0

if __name__ == "__main__":
    fixer = FixTableStructure()
    success = fixer.run_fix_structure()
    sys.exit(0 if success else 1)