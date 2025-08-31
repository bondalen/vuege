#!/usr/bin/env python3
"""
Скрипт для миграции данных в уже созданные таблицы PostgreSQL
Мигрирует данные из SQL Server в PostgreSQL по группам
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
        logging.FileHandler('migrate-data-staged.log'),
        logging.StreamHandler()
    ]
)

class DataMigrationStaged:
    def __init__(self):
        # Группы таблиц с данными для миграции
        self.table_groups = {
            'Группа 1 - Основные данные': [
                'accnt',      # Счета (16 записей)
                'org',        # Организации (135 записей)
                'st',         # Статусы (171 запись)
                'ipg',        # Инвестиционные группы (18 записей)
                'cn_s_type'   # Типы контрактов (2 записи)
            ],
            'Группа 2 - Документы': [
                'cn_PrDocT',  # Типы документов (4 записи)
                'cn_PrDoc',   # Документы контрактов (2,761 записей)
                'cn_PrDocP'   # Параметры документов (3,433 записи)
            ],
            'Группа 3 - Контракты': [
                'cn_s',       # Связанные контракты (3,198 записей)
                'cn_s_org'    # Организации контрактов (2,993 записи)
            ],
            'Группа 4 - Инвестиции': [
                'cnInvGr',    # Группы инвестиций (160 записей)
                'cnInvCmmTp', # Типы комиссий (10 записей)
                'cnInvCmmGr', # Группы комиссий (34 записи)
                'cnInvCmmAg', # Агенты комиссий (1,281 запись)
                'cnInvTransfer' # Переводы инвестиций (2,028 записей)
            ],
            'Группа 5 - Большие таблицы': [
                'cnInvAccnt', # Счета инвестиций (12,693 записи)
                'invDbt',     # Долги инвестиций (5,995 записей)
                'cn_inv_dbt', # Долги инвестиций контрактов (42,367 записей)
                'invNum',     # Номера инвестиций (90,816 записей)
                'cn_inv_doc'  # Документы инвестиций (211,583 записи)
            ]
        }
        
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
    
    def export_table_data_csv(self, table_name):
        """Экспорт данных из SQL Server в CSV формат"""
        # Используем BCP для экспорта в CSV
        bcp_cmd = [
            'docker', 'exec', 'vuege-mssql',
            '/opt/mssql-tools18/bin/bcp',
            f'ags.{table_name}',
            'out',
            f'/tmp/{table_name}.csv',
            '-c',
            '-t,',
            '-r\\n',
            '-S', 'localhost',
            '-U', 'sa',
            '-P', 'Vuege2024!'
        ]
        
        try:
            result = subprocess.run(bcp_cmd, capture_output=True, text=True, timeout=300)
            if result.returncode == 0:
                logging.info(f"✅ Данные таблицы {table_name} экспортированы в CSV")
                return True
            else:
                logging.error(f"❌ Ошибка экспорта таблицы {table_name}: {result.stderr}")
                return False
        except Exception as e:
            logging.error(f"❌ Ошибка экспорта таблицы {table_name}: {e}")
            return False
    
    def import_table_data_csv(self, table_name):
        """Импорт данных из CSV в PostgreSQL"""
        # Копируем CSV файл из контейнера SQL Server
        copy_cmd = [
            'docker', 'cp',
            f'vuege-mssql:/tmp/{table_name}.csv',
            f'/tmp/{table_name}.csv'
        ]
        
        try:
            result = subprocess.run(copy_cmd, capture_output=True, text=True, timeout=60)
            if result.returncode != 0:
                logging.error(f"❌ Ошибка копирования CSV файла {table_name}: {result.stderr}")
                return False
        except Exception as e:
            logging.error(f"❌ Ошибка копирования CSV файла {table_name}: {e}")
            return False
        
        # Копируем CSV файл в контейнер PostgreSQL
        copy_to_pg_cmd = [
            'docker', 'cp',
            f'/tmp/{table_name}.csv',
            f'postgres-java-universal:/tmp/{table_name}.csv'
        ]
        
        try:
            result = subprocess.run(copy_to_pg_cmd, capture_output=True, text=True, timeout=60)
            if result.returncode != 0:
                logging.error(f"❌ Ошибка копирования CSV в PostgreSQL {table_name}: {result.stderr}")
                return False
        except Exception as e:
            logging.error(f"❌ Ошибка копирования CSV в PostgreSQL {table_name}: {e}")
            return False
        
        # Импортируем данные в PostgreSQL
        import_cmd = [
            'docker', 'exec', 'postgres-java-universal',
            'psql',
            '-U', 'postgres',
            '-d', 'Fish_Eye',
            '-c', f'\\COPY ags."{table_name}" FROM \'/tmp/{table_name}.csv\' WITH (FORMAT csv, DELIMITER \',\', ENCODING \'UTF8\');'
        ]
        
        try:
            result = subprocess.run(import_cmd, capture_output=True, text=True, timeout=300)
            if result.returncode == 0:
                logging.info(f"✅ Данные таблицы {table_name} импортированы в PostgreSQL")
                return True
            else:
                logging.error(f"❌ Ошибка импорта таблицы {table_name}: {result.stderr}")
                return False
        except Exception as e:
            logging.error(f"❌ Ошибка импорта таблицы {table_name}: {e}")
            return False
    
    def migrate_table_data(self, table_name):
        """Миграция данных одной таблицы"""
        logging.info(f"🔄 Миграция данных таблицы {table_name}")
        
        # Получение количества записей в SQL Server
        mssql_count = self.get_table_count(table_name)
        logging.info(f"📊 Таблица {table_name}: {mssql_count} записей в SQL Server")
        
        if mssql_count == 0:
            logging.info(f"📝 Таблица {table_name} пустая, пропускаем")
            return True
        
        # Экспорт данных из SQL Server
        if not self.export_table_data_csv(table_name):
            return False
        
        # Импорт данных в PostgreSQL
        if not self.import_table_data_csv(table_name):
            return False
        
        # Проверка количества записей в PostgreSQL
        postgres_count = self.get_postgres_count(table_name)
        logging.info(f"📊 Таблица {table_name}: {postgres_count} записей в PostgreSQL")
        
        if mssql_count == postgres_count:
            logging.info(f"✅ Валидация {table_name}: {mssql_count} = {postgres_count} ✓")
            return True
        else:
            logging.error(f"❌ Валидация {table_name}: {mssql_count} ≠ {postgres_count} ✗")
            return False
    
    def migrate_group(self, group_name, tables):
        """Миграция группы таблиц"""
        logging.info(f"\n🚀 Начало миграции данных группы: {group_name}")
        logging.info(f"📋 Таблиц в группе: {len(tables)}")
        
        success_count = 0
        error_count = 0
        
        for table_name in tables:
            try:
                if self.migrate_table_data(table_name):
                    success_count += 1
                else:
                    error_count += 1
            except Exception as e:
                logging.error(f"❌ Ошибка при миграции таблицы {table_name}: {e}")
                error_count += 1
        
        logging.info(f"\n📊 РЕЗУЛЬТАТЫ ГРУППЫ '{group_name}':")
        logging.info(f"✅ Успешно: {success_count}")
        logging.info(f"❌ Ошибок: {error_count}")
        
        return error_count == 0
    
    def run_data_migration(self):
        """Запуск миграции данных"""
        logging.info("🚀 Начало миграции данных из SQL Server в PostgreSQL")
        logging.info(f"📋 Всего групп: {len(self.table_groups)}")
        
        total_success = 0
        total_error = 0
        
        for group_name, tables in self.table_groups.items():
            if self.migrate_group(group_name, tables):
                total_success += len(tables)
            else:
                total_error += len(tables)
            
            # Пауза между группами
            logging.info("⏸️ Пауза между группами...")
        
        logging.info(f"\n📊 ИТОГОВЫЕ РЕЗУЛЬТАТЫ МИГРАЦИИ ДАННЫХ:")
        logging.info(f"✅ Успешно: {total_success}")
        logging.info(f"❌ Ошибок: {total_error}")
        
        return total_error == 0

if __name__ == "__main__":
    migration = DataMigrationStaged()
    success = migration.run_data_migration()
    sys.exit(0 if success else 1)