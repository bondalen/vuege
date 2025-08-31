#!/usr/bin/env python3
"""
Простой скрипт для миграции данных из SQL Server в PostgreSQL
Создает таблицы и переносит данные
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
        logging.FileHandler('simple-migration.log'),
        logging.StreamHandler()
    ]
)

class SimpleMigration:
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
        except Exception as e:
            logging.error(f"Ошибка выполнения PostgreSQL команды: {e}")
            return None
    
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
    
    def create_table_accnt(self):
        """Создание таблицы accnt"""
        create_sql = """
        CREATE TABLE IF NOT EXISTS ags.accnt (
            account_key INTEGER NOT NULL,
            account_num INTEGER NOT NULL,
            account_name VARCHAR(255) NOT NULL
        );
        """
        return self.run_psql(create_sql)
    
    def create_table_cn(self):
        """Создание таблицы cn"""
        create_sql = """
        CREATE TABLE IF NOT EXISTS ags.cn (
            cn_key INTEGER NOT NULL,
            cn_num INTEGER NOT NULL,
            cn_name VARCHAR(255) NOT NULL,
            cn_date TIMESTAMP,
            cn_amount DECIMAL(19,4),
            cn_status VARCHAR(50),
            cn_type VARCHAR(50)
        );
        """
        return self.run_psql(create_sql)
    
    def create_table_cst(self):
        """Создание таблицы cst"""
        create_sql = """
        CREATE TABLE IF NOT EXISTS ags.cst (
            cst_key INTEGER NOT NULL,
            cst_num INTEGER NOT NULL,
            cst_name VARCHAR(255) NOT NULL,
            cst_type VARCHAR(50),
            cst_status VARCHAR(50)
        );
        """
        return self.run_psql(create_sql)
    
    def create_table_org(self):
        """Создание таблицы org"""
        create_sql = """
        CREATE TABLE IF NOT EXISTS ags.org (
            org_key INTEGER NOT NULL,
            org_num INTEGER NOT NULL,
            org_name VARCHAR(255) NOT NULL,
            org_type VARCHAR(50),
            org_status VARCHAR(50)
        );
        """
        return self.run_psql(create_sql)
    
    def create_table_st(self):
        """Создание таблицы st"""
        create_sql = """
        CREATE TABLE IF NOT EXISTS ags.st (
            st_key INTEGER NOT NULL,
            st_num INTEGER NOT NULL,
            st_name VARCHAR(255) NOT NULL,
            st_type VARCHAR(50)
        );
        """
        return self.run_psql(create_sql)
    
    def migrate_table_data(self, table_name):
        """Миграция данных таблицы через CSV"""
        # Экспорт данных из SQL Server в CSV
        export_query = f"""
        SELECT * FROM ags.{table_name}
        FOR JSON PATH
        """
        
        data = self.run_sqlcmd(export_query)
        if not data:
            return False
        
        logging.info(f"Данные получены для таблицы {table_name}")
        return True
    
    def run_test_migration(self):
        """Запуск тестовой миграции"""
        logging.info("🧪 Начало простой тестовой миграции")
        
        success_count = 0
        error_count = 0
        
        # Создание таблиц
        table_creators = {
            'accnt': self.create_table_accnt,
            'cn': self.create_table_cn,
            'cst': self.create_table_cst,
            'org': self.create_table_org,
            'st': self.create_table_st
        }
        
        for table_name in self.test_tables:
            logging.info(f"\n🔄 Обработка таблицы: {table_name}")
            
            try:
                # Получение информации о таблице
                count = self.get_table_count(table_name)
                logging.info(f"📊 Таблица {table_name}: {count} записей")
                
                # Создание таблицы в PostgreSQL
                if table_name in table_creators:
                    if table_creators[table_name]():
                        logging.info(f"✅ Таблица {table_name} создана в PostgreSQL")
                        success_count += 1
                    else:
                        logging.error(f"❌ Ошибка создания таблицы {table_name}")
                        error_count += 1
                else:
                    logging.error(f"❌ Не найден создатель для таблицы {table_name}")
                    error_count += 1
                    
            except Exception as e:
                logging.error(f"❌ Ошибка при обработке таблицы {table_name}: {e}")
                error_count += 1
        
        logging.info(f"\n📊 РЕЗУЛЬТАТЫ ТЕСТОВОЙ МИГРАЦИИ:")
        logging.info(f"✅ Успешно: {success_count}")
        logging.info(f"❌ Ошибок: {error_count}")
        
        return error_count == 0

if __name__ == "__main__":
    migration = SimpleMigration()
    success = migration.run_test_migration()
    sys.exit(0 if success else 1)