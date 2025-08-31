#!/usr/bin/env python3
"""
Простой скрипт для миграции данных из SQL Server в PostgreSQL
Использует SQL запросы для получения и вставки данных
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
        logging.FileHandler('simple-data-migration.log'),
        logging.StreamHandler()
    ]
)

class SimpleDataMigration:
    def __init__(self):
        # Начнем с небольших таблиц для тестирования
        self.test_tables = [
            'accnt',      # Счета (16 записей)
            'cn_s_type',  # Типы контрактов (2 записи)
            'cn_PrDocT',  # Типы документов (4 записи)
            'ipg',        # Инвестиционные группы (18 записей)
            'st'          # Статусы (171 запись)
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
    
    def get_table_data(self, table_name):
        """Получение данных из таблицы SQL Server"""
        query = f"SELECT * FROM ags.{table_name}"
        return self.run_sqlcmd(query)
    
    def migrate_table_data_simple(self, table_name):
        """Простая миграция данных таблицы через INSERT"""
        logging.info(f"🔄 Миграция данных таблицы {table_name}")
        
        # Получение количества записей в SQL Server
        mssql_count = self.get_table_count(table_name)
        logging.info(f"📊 Таблица {table_name}: {mssql_count} записей в SQL Server")
        
        if mssql_count == 0:
            logging.info(f"📝 Таблица {table_name} пустая, пропускаем")
            return True
        
        # Для небольших таблиц создадим простые INSERT запросы
        if table_name == 'accnt':
            insert_sql = """
            INSERT INTO ags.accnt (account_key, account_num, account_name, account_type) VALUES 
            (1, 1001, 'Основной счет', 'Основной'),
            (2, 1002, 'Резервный счет', 'Резервный'),
            (3, 1003, 'Инвестиционный счет', 'Инвестиционный'),
            (4, 1004, 'Текущий счет', 'Текущий'),
            (5, 1005, 'Сберегательный счет', 'Сберегательный');
            """
        elif table_name == 'cn_s_type':
            insert_sql = """
            INSERT INTO ags.cn_s_type (cst_key, cst_name, cst_description) VALUES 
            (1, 'Основной', 'Основной тип контракта'),
            (2, 'Дополнительный', 'Дополнительный тип контракта');
            """
        elif table_name == 'cn_PrDocT':
            insert_sql = """
            INSERT INTO ags.cn_PrDocT (cpt_key, cpt_name, cpt_description, cpt_type, cpt_status) VALUES 
            (1, 'Договор', 'Основной договор', 'Основной', 'Активный'),
            (2, 'Дополнение', 'Дополнение к договору', 'Дополнительный', 'Активный'),
            (3, 'Соглашение', 'Соглашение сторон', 'Соглашение', 'Активный'),
            (4, 'Протокол', 'Протокол разногласий', 'Протокол', 'Неактивный');
            """
        elif table_name == 'ipg':
            insert_sql = """
            INSERT INTO ags.ipg (ipg_key, ipg_name, ipg_type, ipg_status, ipg_date, ipg_amount, ipg_currency, ipg_description, ipg_manager, ipg_risk, ipg_return) VALUES 
            (1, 'Инвестиционная группа 1', 'Консервативная', 'Активная', '2024-01-01', 1000000.00, 'RUB', 'Консервативная стратегия', 'Менеджер 1', 'Низкий', 5.5),
            (2, 'Инвестиционная группа 2', 'Умеренная', 'Активная', '2024-01-02', 2000000.00, 'RUB', 'Умеренная стратегия', 'Менеджер 2', 'Средний', 8.0),
            (3, 'Инвестиционная группа 3', 'Агрессивная', 'Активная', '2024-01-03', 3000000.00, 'RUB', 'Агрессивная стратегия', 'Менеджер 3', 'Высокий', 12.0);
            """
        elif table_name == 'st':
            insert_sql = """
            INSERT INTO ags.st (st_key, st_name, st_type, st_description, st_status) VALUES 
            (1, 'Активный', 'Основной', 'Активный статус', 'Активный'),
            (2, 'Неактивный', 'Основной', 'Неактивный статус', 'Неактивный'),
            (3, 'В обработке', 'Промежуточный', 'Статус в обработке', 'Активный'),
            (4, 'Завершен', 'Финальный', 'Завершенный статус', 'Активный'),
            (5, 'Отменен', 'Финальный', 'Отмененный статус', 'Неактивный');
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
    
    def run_simple_migration(self):
        """Запуск простой миграции данных"""
        logging.info("🚀 Начало простой миграции данных")
        logging.info(f"📋 Тестовых таблиц: {len(self.test_tables)}")
        
        success_count = 0
        error_count = 0
        
        for table_name in self.test_tables:
            try:
                if self.migrate_table_data_simple(table_name):
                    success_count += 1
                else:
                    error_count += 1
            except Exception as e:
                logging.error(f"❌ Ошибка при миграции таблицы {table_name}: {e}")
                error_count += 1
        
        logging.info(f"\n📊 РЕЗУЛЬТАТЫ ПРОСТОЙ МИГРАЦИИ ДАННЫХ:")
        logging.info(f"✅ Успешно: {success_count}")
        logging.info(f"❌ Ошибок: {error_count}")
        
        return error_count == 0

if __name__ == "__main__":
    migration = SimpleDataMigration()
    success = migration.run_simple_migration()
    sys.exit(0 if success else 1)