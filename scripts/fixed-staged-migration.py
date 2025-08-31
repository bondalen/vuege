#!/usr/bin/env python3
"""
Исправленный скрипт для поэтапной миграции данных из SQL Server в PostgreSQL
Исправлена проблема с VARCHAR(-1) - заменяется на TEXT
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
        logging.FileHandler('fixed-staged-migration.log'),
        logging.StreamHandler()
    ]
)

class FixedStagedMigration:
    def __init__(self):
        # Группы таблиц для поэтапной миграции (только успешные из предыдущего запуска)
        self.table_groups = {
            'Группа 1 - Успешные таблицы': [
                'accnt',      # Счета
                'org',        # Организации
                'st',         # Статусы
                'ipg',        # Инвестиционные группы
                'cn_PrDoc',   # Документы контрактов
                'cn_PrDocP',  # Параметры документов
                'cn_PrDocT',  # Типы документов
                'cn_s',       # Связанные контракты
                'cn_s_org',   # Организации контрактов
                'cn_s_type'   # Типы контрактов
            ],
            'Группа 2 - Инвестиции': [
                'cnInvAccnt', # Счета инвестиций
                'cnInvGr',    # Группы инвестиций
                'cnInvTransfer', # Переводы инвестиций
                'cn_inv_dbt', # Долги инвестиций
                'cn_inv_doc', # Документы инвестиций
                'cnInvCmmAg', # Агенты комиссий
                'cnInvCmmGr', # Группы комиссий
                'cnInvCmmTp', # Типы комиссий
                'invDbt',     # Долги инвестиций
                'invNum'      # Номера инвестиций
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
    
    def get_table_structure(self, table_name):
        """Получение структуры таблицы из SQL Server"""
        query = f"""
        SELECT 
            COLUMN_NAME,
            DATA_TYPE,
            CHARACTER_MAXIMUM_LENGTH,
            NUMERIC_PRECISION,
            NUMERIC_SCALE,
            IS_NULLABLE
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
                    parts = line.split()
                    if len(parts) >= 6:
                        columns.append({
                            'name': parts[0],
                            'type': parts[1],
                            'max_length': parts[2] if parts[2] != 'NULL' else None,
                            'precision': parts[3] if parts[3] != 'NULL' else None,
                            'scale': parts[4] if parts[4] != 'NULL' else None,
                            'nullable': parts[5]
                        })
            return columns
        return None
    
    def convert_data_type(self, mssql_type, max_length, precision, scale):
        """Исправленная конвертация типов данных SQL Server в PostgreSQL"""
        # Обработка случая VARCHAR(-1) - заменяем на TEXT
        if mssql_type.lower() in ['varchar', 'nvarchar', 'char', 'nchar'] and max_length == '-1':
            return 'TEXT'
        
        type_mapping = {
            'int': 'INTEGER',
            'bigint': 'BIGINT',
            'smallint': 'SMALLINT',
            'tinyint': 'SMALLINT',
            'bit': 'BOOLEAN',
            'char': f'CHAR({max_length})' if max_length and max_length != '-1' else 'CHAR(1)',
            'nchar': f'CHAR({max_length})' if max_length and max_length != '-1' else 'CHAR(1)',
            'varchar': f'VARCHAR({max_length})' if max_length and max_length != '-1' else 'TEXT',
            'nvarchar': f'VARCHAR({max_length})' if max_length and max_length != '-1' else 'TEXT',
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
        if not columns:
            return False
            
        # Формирование SQL для создания таблицы
        column_definitions = []
        for col in columns:
            col_name = col['name']
            col_type = col['type']
            max_length = col['max_length']
            precision = col['precision']
            scale = col['scale']
            is_nullable = col['nullable']
            
            pg_type = self.convert_data_type(col_type, max_length, precision, scale)
            nullable = "" if is_nullable == 'YES' else " NOT NULL"
            
            column_definitions.append(f'"{col_name}" {pg_type}{nullable}')
        
        create_sql = f"""
        CREATE TABLE IF NOT EXISTS ags."{table_name}" (
            {', '.join(column_definitions)}
        );
        """
        
        result = self.run_psql(create_sql)
        return result is not None
    
    def migrate_table_data(self, table_name):
        """Миграция данных таблицы (пока без данных)"""
        logging.info(f"📝 Таблица {table_name} - структура создана (данные будут мигрированы позже)")
        return True
    
    def migrate_group(self, group_name, tables):
        """Миграция группы таблиц"""
        logging.info(f"\n🚀 Начало миграции группы: {group_name}")
        logging.info(f"📋 Таблиц в группе: {len(tables)}")
        
        success_count = 0
        error_count = 0
        
        for table_name in tables:
            logging.info(f"\n🔄 Обработка таблицы: {table_name}")
            
            try:
                # Получение информации о таблице
                count = self.get_table_count(table_name)
                logging.info(f"📊 Таблица {table_name}: {count} записей в SQL Server")
                
                # Получение структуры таблицы
                columns = self.get_table_structure(table_name)
                if columns:
                    logging.info(f"📋 Структура таблицы {table_name}: {len(columns)} колонок")
                    
                    # Создание таблицы в PostgreSQL
                    if self.create_table_postgres(table_name, columns):
                        # Миграция данных (пока только структура)
                        if self.migrate_table_data(table_name):
                            success_count += 1
                        else:
                            error_count += 1
                    else:
                        error_count += 1
                else:
                    logging.error(f"❌ Не удалось получить структуру таблицы {table_name}")
                    error_count += 1
                    
            except Exception as e:
                logging.error(f"❌ Ошибка при обработке таблицы {table_name}: {e}")
                error_count += 1
        
        logging.info(f"\n📊 РЕЗУЛЬТАТЫ ГРУППЫ '{group_name}':")
        logging.info(f"✅ Успешно: {success_count}")
        logging.info(f"❌ Ошибок: {error_count}")
        
        return error_count == 0
    
    def run_staged_migration(self):
        """Запуск поэтапной миграции"""
        logging.info("🚀 Начало исправленной поэтапной миграции схемы ags")
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
        
        logging.info(f"\n📊 ИТОГОВЫЕ РЕЗУЛЬТАТЫ ПОЭТАПНОЙ МИГРАЦИИ:")
        logging.info(f"✅ Успешно: {total_success}")
        logging.info(f"❌ Ошибок: {total_error}")
        
        return total_error == 0

if __name__ == "__main__":
    migration = FixedStagedMigration()
    success = migration.run_staged_migration()
    sys.exit(0 if success else 1)