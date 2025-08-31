#!/usr/bin/env python3
"""
Миграция ТОЛЬКО схемы ags из SQL Server в PostgreSQL
"""

import logging
import json
import pymssql
import psycopg2
from datetime import datetime
from psycopg2.extras import RealDictCursor

class MigrateOnlyAGSSchema:
    def __init__(self):
        self.setup_logging()
        self.migration_results = {}
        
        # Подключения к базам данных
        self.mssql_conn = None
        self.pg_conn = None
        
    def setup_logging(self):
        """Настройка логирования"""
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler('migrate-only-ags-schema.log'),
                logging.StreamHandler()
            ]
        )
    
    def connect_databases(self):
        """Подключение к базам данных"""
        try:
            # SQL Server
            self.mssql_conn = pymssql.connect(
                server='localhost',
                port=1433,
                user='sa',
                password='Vuege2024!',
                database='Fish_Eye'
            )
            logging.info("✅ Подключение к SQL Server установлено")
            
            # PostgreSQL
            self.pg_conn = psycopg2.connect(
                host='localhost',
                port=5432,
                user='postgres',
                password='postgres',
                database='vuege'
            )
            logging.info("✅ Подключение к PostgreSQL установлено")
            
        except Exception as e:
            logging.error(f"❌ Ошибка подключения: {e}")
            raise
    
    def get_ags_tables_from_mssql(self):
        """Получение списка всех таблиц схемы ags из SQL Server"""
        cursor = self.mssql_conn.cursor()
        cursor.execute("""
            SELECT table_name 
            FROM information_schema.tables 
            WHERE table_schema = 'ags' 
            ORDER BY table_name
        """)
        tables = [row[0] for row in cursor.fetchall()]
        cursor.close()
        logging.info(f"📋 Найдено {len(tables)} таблиц в схеме ags (SQL Server)")
        return tables
    
    def get_migrated_tables_from_pg(self):
        """Получение списка уже мигрированных таблиц из PostgreSQL"""
        cursor = self.pg_conn.cursor()
        cursor.execute("""
            SELECT table_name 
            FROM information_schema.tables 
            WHERE table_schema = 'ags' 
            ORDER BY table_name
        """)
        tables = [row[0] for row in cursor.fetchall()]
        cursor.close()
        logging.info(f"📋 Уже мигрировано {len(tables)} таблиц в PostgreSQL")
        return tables
    
    def get_table_structure(self, table_name):
        """Получение структуры таблицы"""
        cursor = self.mssql_conn.cursor()
        cursor.execute(f"""
            SELECT 
                column_name,
                data_type,
                is_nullable,
                column_default,
                character_maximum_length,
                numeric_precision,
                numeric_scale
            FROM information_schema.columns 
            WHERE table_schema = 'ags' 
            AND table_name = '{table_name}'
            ORDER BY ordinal_position
        """)
        columns = cursor.fetchall()
        cursor.close()
        return columns
    
    def convert_data_type(self, mssql_type, max_length, precision, scale):
        """Конвертация типов данных SQL Server в PostgreSQL"""
        type_mapping = {
            'int': 'integer',
            'bigint': 'bigint',
            'smallint': 'smallint',
            'tinyint': 'smallint',
            'bit': 'boolean',
            'char': 'character',
            'nchar': 'character',
            'varchar': 'character varying',
            'nvarchar': 'character varying',
            'text': 'text',
            'ntext': 'text',
            'datetime': 'timestamp',
            'datetime2': 'timestamp',
            'date': 'date',
            'time': 'time',
            'decimal': 'numeric',
            'numeric': 'numeric',
            'float': 'double precision',
            'real': 'real',
            'money': 'numeric(19,4)',
            'smallmoney': 'numeric(10,4)',
            'binary': 'bytea',
            'varbinary': 'bytea',
            'image': 'bytea',
            'uniqueidentifier': 'uuid',
            'xml': 'xml'
        }
        
        pg_type = type_mapping.get(mssql_type.lower(), 'text')
        
        if pg_type in ['character', 'character varying'] and max_length:
            if max_length == -1:  # MAX
                pg_type = 'text'
            else:
                pg_type = f"{pg_type}({max_length})"
        elif pg_type == 'numeric' and precision and scale:
            pg_type = f"numeric({precision},{scale})"
        elif pg_type == 'numeric' and precision:
            pg_type = f"numeric({precision})"
            
        return pg_type
    
    def create_table_sql(self, table_name, columns):
        """Создание SQL для создания таблицы"""
        column_definitions = []
        
        for col in columns:
            col_name = col[0]
            data_type = col[1]
            is_nullable = col[2]
            default_value = col[3]
            max_length = col[4]
            precision = col[5]
            scale = col[6]
            
            pg_type = self.convert_data_type(data_type, max_length, precision, scale)
            nullable = "" if is_nullable == "YES" else " NOT NULL"
            
            # Обработка значений по умолчанию
            default_clause = ""
            if default_value:
                if "getdate()" in default_value.lower():
                    default_clause = " DEFAULT CURRENT_TIMESTAMP"
                elif "newid()" in default_value.lower():
                    default_clause = " DEFAULT gen_random_uuid()"
                else:
                    default_clause = f" DEFAULT {default_value}"
            
            column_definitions.append(f"{col_name} {pg_type}{nullable}{default_clause}")
        
        sql = f"""
        CREATE TABLE IF NOT EXISTS ags.{table_name} (
            {', '.join(column_definitions)}
        );
        """
        return sql
    
    def create_table(self, table_name):
        """Создание таблицы в PostgreSQL"""
        try:
            columns = self.get_table_structure(table_name)
            create_sql = self.create_table_sql(table_name, columns)
            
            cursor = self.pg_conn.cursor()
            cursor.execute(create_sql)
            self.pg_conn.commit()
            cursor.close()
            
            logging.info(f"✅ Таблица ags.{table_name} создана")
            return True
            
        except Exception as e:
            logging.error(f"❌ Ошибка создания таблицы {table_name}: {e}")
            self.pg_conn.rollback()
            return False
    
    def get_table_data_count(self, table_name):
        """Получение количества записей в таблице"""
        cursor = self.mssql_conn.cursor()
        cursor.execute(f"SELECT COUNT(*) FROM ags.{table_name}")
        count = cursor.fetchone()[0]
        cursor.close()
        return count
    
    def migrate_table_data(self, table_name, batch_size=1000):
        """Миграция данных таблицы"""
        try:
            # Получаем количество записей
            total_count = self.get_table_data_count(table_name)
            if total_count == 0:
                logging.info(f"📋 Таблица {table_name} пустая, пропускаем")
                return True
            
            logging.info(f"🔄 Миграция данных таблицы {table_name} ({total_count:,} записей)")
            
            # Получаем структуру таблицы
            columns = self.get_table_structure(table_name)
            column_names = [col[0] for col in columns]
            
            # Миграция по батчам
            offset = 0
            migrated_count = 0
            
            while offset < total_count:
                # Получаем данные из SQL Server
                mssql_cursor = self.mssql_conn.cursor()
                mssql_cursor.execute(f"""
                    SELECT {', '.join(column_names)}
                    FROM ags.{table_name}
                    ORDER BY {column_names[0]}
                    OFFSET {offset} ROWS
                    FETCH NEXT {batch_size} ROWS ONLY
                """)
                
                rows = mssql_cursor.fetchall()
                mssql_cursor.close()
                
                if not rows:
                    break
                
                # Вставляем данные в PostgreSQL
                pg_cursor = self.pg_conn.cursor()
                
                # Создаем placeholders для INSERT
                placeholders = ', '.join(['%s'] * len(column_names))
                insert_sql = f"""
                    INSERT INTO ags.{table_name} ({', '.join(column_names)})
                    VALUES ({placeholders})
                    ON CONFLICT DO NOTHING
                """
                
                pg_cursor.executemany(insert_sql, rows)
                self.pg_conn.commit()
                pg_cursor.close()
                
                migrated_count += len(rows)
                offset += batch_size
                
                if migrated_count % 10000 == 0:
                    logging.info(f"   📊 Прогресс: {migrated_count:,}/{total_count:,} записей")
            
            logging.info(f"✅ Таблица {table_name} мигрирована успешно")
            return True
            
        except Exception as e:
            logging.error(f"❌ Ошибка миграции данных таблицы {table_name}: {e}")
            self.pg_conn.rollback()
            return False
    
    def migrate_table(self, table_name):
        """Полная миграция таблицы"""
        logging.info(f"🚀 Начинаем миграцию таблицы: {table_name}")
        
        # Создание таблицы
        if not self.create_table(table_name):
            return False
        
        # Миграция данных
        if not self.migrate_table_data(table_name):
            return False
        
        return True
    
    def migrate_only_ags_schema(self):
        """Миграция ТОЛЬКО схемы ags"""
        logging.info("🎯 МИГРАЦИЯ ТОЛЬКО СХЕМЫ AGS")
        logging.info("=" * 60)
        
        try:
            # Подключение к базам данных
            self.connect_databases()
            
            # Получение списков таблиц
            all_ags_tables = self.get_ags_tables_from_mssql()
            migrated_tables = self.get_migrated_tables_from_pg()
            
            # Определение таблиц для миграции
            tables_to_migrate = [t for t in all_ags_tables if t not in migrated_tables]
            
            logging.info(f"📋 Всего таблиц в схеме ags: {len(all_ags_tables)}")
            logging.info(f"📋 Уже мигрировано: {len(migrated_tables)}")
            logging.info(f"📋 Осталось мигрировать: {len(tables_to_migrate)}")
            
            # Создание схемы ags в PostgreSQL если не существует
            pg_cursor = self.pg_conn.cursor()
            pg_cursor.execute("CREATE SCHEMA IF NOT EXISTS ags")
            self.pg_conn.commit()
            pg_cursor.close()
            logging.info("✅ Схема ags создана в PostgreSQL")
            
            # Миграция таблиц
            successful_tables = []
            failed_tables = []
            
            for i, table_name in enumerate(tables_to_migrate, 1):
                logging.info(f"📋 [{i}/{len(tables_to_migrate)}] Обработка таблицы: {table_name}")
                
                try:
                    if self.migrate_table(table_name):
                        successful_tables.append(table_name)
                    else:
                        failed_tables.append(table_name)
                except Exception as e:
                    logging.error(f"❌ Критическая ошибка при миграции {table_name}: {e}")
                    failed_tables.append(table_name)
            
            # Итоговый отчет
            logging.info("=" * 60)
            logging.info("📊 ИТОГОВЫЙ ОТЧЕТ МИГРАЦИИ СХЕМЫ AGS")
            logging.info("=" * 60)
            logging.info(f"📋 Всего таблиц в схеме ags: {len(all_ags_tables)}")
            logging.info(f"✅ Успешно мигрировано: {len(successful_tables)} таблиц")
            logging.info(f"❌ Ошибки миграции: {len(failed_tables)} таблиц")
            logging.info(f"📈 Общий прогресс: {len(migrated_tables) + len(successful_tables)}/{len(all_ags_tables)} ({((len(migrated_tables) + len(successful_tables))/len(all_ags_tables)*100):.1f}%)")
            
            if successful_tables:
                logging.info("✅ Успешно мигрированные таблицы:")
                for table in successful_tables:
                    logging.info(f"   • {table}")
            
            if failed_tables:
                logging.info("❌ Таблицы с ошибками:")
                for table in failed_tables:
                    logging.info(f"   • {table}")
            
            return successful_tables, failed_tables
            
        except Exception as e:
            logging.error(f"❌ Критическая ошибка миграции: {e}")
            return [], all_ags_tables
        finally:
            if self.mssql_conn:
                self.mssql_conn.close()
            if self.pg_conn:
                self.pg_conn.close()

def main():
    """Главная функция"""
    print("🎯 МИГРАЦИЯ ТОЛЬКО СХЕМЫ AGS ИЗ SQL SERVER В POSTGRESQL")
    print("=" * 70)
    
    migrator = MigrateOnlyAGSSchema()
    successful, failed = migrator.migrate_only_ags_schema()
    
    print("\n🎉 МИГРАЦИЯ СХЕМЫ AGS ЗАВЕРШЕНА!")
    print(f"✅ Успешно: {len(successful)} таблиц")
    print(f"❌ Ошибки: {len(failed)} таблиц")
    
    if successful:
        print(f"\n📋 Успешно мигрированные таблицы:")
        for table in successful[:10]:  # Показываем первые 10
            print(f"   • {table}")
        if len(successful) > 10:
            print(f"   ... и еще {len(successful) - 10} таблиц")

if __name__ == "__main__":
    main()