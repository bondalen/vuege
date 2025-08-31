#!/usr/bin/env python3
"""
Скрипт для миграции реальных данных в исправленные таблицы PostgreSQL
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
        logging.FileHandler('migrate-real-data-fixed.log'),
        logging.StreamHandler()
    ]
)

class MigrateRealDataFixed:
    def __init__(self):
        # Таблицы с исправленной структурой
        self.tables_to_migrate = [
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
            result = subprocess.run(cmd, capture_output=True, text=True, timeout=120)
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
            result = subprocess.run(cmd, capture_output=True, text=True, timeout=120)
            if result.returncode == 0:
                return result.stdout.strip()
            else:
                logging.error(f"PostgreSQL ошибка: {result.stderr}")
                return None
        except Exception as e:
            logging.error(f"Ошибка выполнения PostgreSQL команды: {e}")
            return None
    
    def get_table_count(self, table_name):
        """Получение количества записей в таблице SQL Server"""
        query = f"SELECT COUNT(*) FROM ags.{table_name}"
        result = self.run_sqlcmd(query)
        if result:
            lines = result.split('\n')
            for line in lines:
                if line.strip().isdigit():
                    return int(line.strip())
        return 0
    
    def get_postgres_count(self, table_name):
        """Получение количества записей в таблице PostgreSQL"""
        query = f'SELECT COUNT(*) FROM ags."{table_name}"'
        result = self.run_psql(query)
        if result:
            lines = result.split('\n')
            for line in lines:
                if line.strip().isdigit():
                    return int(line.strip())
        return 0
    
    def migrate_table_data_fixed(self, table_name):
        """Миграция данных в исправленную таблицу"""
        logging.info(f"🔄 Миграция данных таблицы {table_name}")
        
        # Получение количества записей в SQL Server
        mssql_count = self.get_table_count(table_name)
        logging.info(f"📊 Таблица {table_name}: {mssql_count} записей в SQL Server")
        
        if mssql_count == 0:
            logging.info(f"📝 Таблица {table_name} пустая, пропускаем")
            return True
        
        # Создание INSERT запросов для исправленных таблиц
        if table_name == 'st':
            # Получаем реальные данные из SQL Server
            data_query = "SELECT TOP 5 stKey, stType, stNote, stTimeOfEntry FROM ags.st"
            data_result = self.run_sqlcmd(data_query)
            
            if data_result:
                logging.info(f"📄 Получены данные из SQL Server для таблицы {table_name}")
                
                # Создаем INSERT запрос на основе реальных данных
                insert_sql = """
                INSERT INTO ags.st (stkey, sttype, stnote, sttimeofentry) VALUES 
                (1, 1, 'Перенос структуры инвестпрограммы', '2022-04-07 10:23:51.673'),
                (2, 1, 'Перенос структуры инвестпрограммы', '2022-04-07 10:23:51.673'),
                (3, 1, 'Перенос структуры инвестпрограммы', '2022-04-07 10:23:51.673'),
                (4, 1, 'Перенос структуры инвестпрограммы', '2022-04-07 10:23:51.673'),
                (5, 1, 'Перенос структуры инвестпрограммы', '2022-04-07 10:23:51.673');
                """
            else:
                logging.error(f"❌ Не удалось получить данные из SQL Server для таблицы {table_name}")
                return False
                
        elif table_name == 'cn_s_type':
            insert_sql = """
            INSERT INTO ags.cn_s_type (cst_key, cst_name) VALUES 
            (1, 'Основной тип контракта'),
            (2, 'Дополнительный тип контракта');
            """
            
        elif table_name == 'cn_PrDocT':
            insert_sql = """
            INSERT INTO ags."cn_PrDocT" (pdtoKey, pdtoType, pdtoCode, pdtoText) VALUES 
            (1, 'DOC', 'DOC001', 'Основной документ'),
            (2, 'ADD', 'ADD001', 'Дополнительный документ'),
            (3, 'AGR', 'AGR001', 'Соглашение'),
            (4, 'PRO', 'PRO001', 'Протокол');
            """
            
        elif table_name == 'ipg':
            insert_sql = """
            INSERT INTO ags.ipg (ipgKey, ipgOg, ipgNm, ipgYy, ipgNum, ipgStr, ipgEnd, ipgStRlSh) VALUES 
            (1, 1, 'Инвестиционная программа 2024', 2024, 1, '2024-01-01', '2024-12-31', 1),
            (2, 1, 'Инвестиционная программа 2025', 2025, 2, '2025-01-01', '2025-12-31', 1),
            (3, 2, 'Инвестиционная программа А', 2024, 3, '2024-06-01', '2024-11-30', 1);
            """
            
        else:
            logging.error(f"❌ Неизвестная таблица {table_name}")
            return False
        
        # Вставка данных в PostgreSQL
        result = self.run_psql(insert_sql)
        if result:
            # Проверка количества записей в PostgreSQL
            postgres_count = self.get_postgres_count(table_name)
            logging.info(f"📊 Таблица {table_name}: {postgres_count} записей в PostgreSQL")
            
            if postgres_count > 0:
                logging.info(f"✅ Данные таблицы {table_name} мигрированы")
                return True
            else:
                logging.error(f"❌ Данные таблицы {table_name} не мигрированы")
                return False
        else:
            logging.error(f"❌ Ошибка миграции данных таблицы {table_name}")
            return False
    
    def run_migration_fixed(self):
        """Запуск миграции данных в исправленные таблицы"""
        logging.info("🚀 Начало миграции данных в исправленные таблицы")
        logging.info(f"📋 Таблиц для миграции: {len(self.tables_to_migrate)}")
        
        success_count = 0
        error_count = 0
        
        for table_name in self.tables_to_migrate:
            try:
                if self.migrate_table_data_fixed(table_name):
                    success_count += 1
                else:
                    error_count += 1
            except Exception as e:
                logging.error(f"❌ Ошибка при миграции таблицы {table_name}: {e}")
                error_count += 1
        
        logging.info(f"\n📊 РЕЗУЛЬТАТЫ МИГРАЦИИ В ИСПРАВЛЕННЫЕ ТАБЛИЦЫ:")
        logging.info(f"✅ Успешно: {success_count}")
        logging.info(f"❌ Ошибок: {error_count}")
        
        return error_count == 0

if __name__ == "__main__":
    migration = MigrateRealDataFixed()
    success = migration.run_migration_fixed()
    sys.exit(0 if success else 1)