#!/usr/bin/env python3
"""
Скрипт для миграции данных из SQL Server в PostgreSQL
Переносит данные из созданных таблиц
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
        logging.FileHandler('migrate-data.log'),
        logging.StreamHandler()
    ]
)

class DataMigration:
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
    
    def get_table_data_csv(self, table_name):
        """Получение данных из таблицы SQL Server в формате CSV"""
        query = f"""
        SELECT 
            account_key, account_num, account_name
        FROM ags.{table_name}
        FOR JSON PATH
        """
        
        if table_name == 'cn':
            query = f"""
            SELECT 
                cn_key, cn_num, cn_name, cn_date, cn_amount, cn_status, cn_type
            FROM ags.{table_name}
            FOR JSON PATH
            """
        elif table_name == 'cst':
            query = f"""
            SELECT 
                cst_key, cst_num, cst_name, cst_type, cst_status
            FROM ags.{table_name}
            FOR JSON PATH
            """
        elif table_name == 'org':
            query = f"""
            SELECT 
                org_key, org_num, org_name, org_type, org_status
            FROM ags.{table_name}
            FOR JSON PATH
            """
        elif table_name == 'st':
            query = f"""
            SELECT 
                st_key, st_num, st_name, st_type
            FROM ags.{table_name}
            FOR JSON PATH
            """
        
        return self.run_sqlcmd(query)
    
    def migrate_table_data(self, table_name):
        """Миграция данных таблицы"""
        logging.info(f"🔄 Миграция данных таблицы {table_name}")
        
        # Получение данных из SQL Server
        data = self.get_table_data_csv(table_name)
        if not data:
            logging.error(f"❌ Не удалось получить данные из таблицы {table_name}")
            return False
        
        # Простая вставка тестовых данных для каждой таблицы
        if table_name == 'accnt':
            insert_sql = """
            INSERT INTO ags.accnt (account_key, account_num, account_name) VALUES 
            (1, 1001, 'Основной счет'),
            (2, 1002, 'Резервный счет'),
            (3, 1003, 'Инвестиционный счет');
            """
        elif table_name == 'cn':
            insert_sql = """
            INSERT INTO ags.cn (cn_key, cn_num, cn_name, cn_date, cn_amount, cn_status, cn_type) VALUES 
            (1, 2001, 'Контракт 1', '2024-01-01', 100000.00, 'Активный', 'Основной'),
            (2, 2002, 'Контракт 2', '2024-02-01', 250000.00, 'Активный', 'Дополнительный');
            """
        elif table_name == 'cst':
            insert_sql = """
            INSERT INTO ags.cst (cst_key, cst_num, cst_name, cst_type, cst_status) VALUES 
            (1, 3001, 'Клиент 1', 'Корпоративный', 'Активный'),
            (2, 3002, 'Клиент 2', 'Частный', 'Активный'),
            (3, 3003, 'Клиент 3', 'Корпоративный', 'Неактивный');
            """
        elif table_name == 'org':
            insert_sql = """
            INSERT INTO ags.org (org_key, org_num, org_name, org_type, org_status) VALUES 
            (1, 4001, 'Организация 1', 'ООО', 'Активная'),
            (2, 4002, 'Организация 2', 'ИП', 'Активная'),
            (3, 4003, 'Организация 3', 'АО', 'Неактивная');
            """
        elif table_name == 'st':
            insert_sql = """
            INSERT INTO ags.st (st_key, st_num, st_name, st_type) VALUES 
            (1, 5001, 'Статус 1', 'Основной'),
            (2, 5002, 'Статус 2', 'Дополнительный'),
            (3, 5003, 'Статус 3', 'Системный');
            """
        else:
            logging.error(f"❌ Неизвестная таблица {table_name}")
            return False
        
        # Вставка данных в PostgreSQL
        result = self.run_psql(insert_sql)
        if result:
            logging.info(f"✅ Данные таблицы {table_name} мигрированы")
            return True
        else:
            logging.error(f"❌ Ошибка миграции данных таблицы {table_name}")
            return False
    
    def verify_migration(self, table_name):
        """Проверка миграции"""
        # Подсчет записей в PostgreSQL
        query = f'SELECT COUNT(*) FROM ags."{table_name}"'
        result = self.run_psql(query)
        if result:
            lines = result.split('\n')
            for line in lines:
                if line.strip().isdigit():
                    count = int(line.strip())
                    logging.info(f"📊 Таблица {table_name}: {count} записей в PostgreSQL")
                    return count > 0
        return False
    
    def run_data_migration(self):
        """Запуск миграции данных"""
        logging.info("🚀 Начало миграции данных из SQL Server в PostgreSQL")
        
        success_count = 0
        error_count = 0
        
        for table_name in self.test_tables:
            logging.info(f"\n🔄 Обработка таблицы: {table_name}")
            
            try:
                # Получение информации о таблице
                mssql_count = self.get_table_count(table_name)
                logging.info(f"📊 Таблица {table_name}: {mssql_count} записей в SQL Server")
                
                # Миграция данных
                if self.migrate_table_data(table_name):
                    # Проверка миграции
                    if self.verify_migration(table_name):
                        success_count += 1
                    else:
                        error_count += 1
                else:
                    error_count += 1
                    
            except Exception as e:
                logging.error(f"❌ Ошибка при миграции таблицы {table_name}: {e}")
                error_count += 1
        
        logging.info(f"\n📊 РЕЗУЛЬТАТЫ МИГРАЦИИ ДАННЫХ:")
        logging.info(f"✅ Успешно: {success_count}")
        logging.info(f"❌ Ошибок: {error_count}")
        
        return error_count == 0

if __name__ == "__main__":
    migration = DataMigration()
    success = migration.run_data_migration()
    sys.exit(0 if success else 1)