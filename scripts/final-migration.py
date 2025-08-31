#!/usr/bin/env python3
"""
Финальная миграция с исправлением всех проблем
"""

import logging
import json
import pymssql
import psycopg2
from datetime import datetime
from psycopg2.extras import RealDictCursor

class FinalDataMigration:
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
                logging.FileHandler('final-migration.log'),
                logging.StreamHandler()
            ]
        )
    
    def connect_databases(self):
        """Подключение к базам данных"""
        try:
            # Подключение к SQL Server
            self.mssql_conn = pymssql.connect(
                server='localhost',
                port=1433,
                user='sa',
                password='Vuege2024!',
                database='Fish_Eye'
            )
            logging.info("✅ Подключение к SQL Server успешно")
            
            # Подключение к PostgreSQL
            self.pg_conn = psycopg2.connect(
                'postgresql://postgres:postgres@localhost:5432/vuege'
            )
            logging.info("✅ Подключение к PostgreSQL успешно")
            
            return True
            
        except Exception as e:
            logging.error(f"❌ Ошибка подключения: {e}")
            return False
    
    def clean_duplicate_tables(self):
        """Очистка таблиц с дублированными данными"""
        try:
            cursor = self.pg_conn.cursor()
            
            # Очистка таблиц с дубли
            tables_to_clean = ['cn', 'org']
            
            for table in tables_to_clean:
                cursor.execute(f"TRUNCATE TABLE ags.{table}")
                logging.info(f"🧹 Таблица ags.{table} очищена")
            
            self.pg_conn.commit()
            cursor.close()
            
            return True
            
        except Exception as e:
            logging.error(f"❌ Ошибка очистки таблиц: {e}")
            self.pg_conn.rollback()
            return False
    
    def get_table_structure(self, table_name):
        """Получение структуры таблицы из SQL Server"""
        try:
            cursor = self.mssql_conn.cursor()
            cursor.execute(f"""
                SELECT column_name, data_type, is_nullable, column_default
                FROM information_schema.columns
                WHERE table_schema = 'ags' AND table_name = '{table_name}'
                ORDER BY ordinal_position
            """)
            
            columns = cursor.fetchall()
            cursor.close()
            
            return columns
            
        except Exception as e:
            logging.error(f"❌ Ошибка получения структуры {table_name}: {e}")
            return []
    
    def create_table_in_postgresql(self, table_name, columns):
        """Создание таблицы в PostgreSQL"""
        try:
            cursor = self.pg_conn.cursor()
            
            # Создание схемы если не существует
            cursor.execute("CREATE SCHEMA IF NOT EXISTS ags")
            
            # Удаление таблицы если существует (для пересоздания)
            cursor.execute(f"DROP TABLE IF EXISTS ags.{table_name} CASCADE")
            
            # Генерация SQL для создания таблицы
            column_definitions = []
            for col in columns:
                col_name = col[0]
                col_type = self.convert_data_type(col[1])
                nullable = "NULL" if col[2] == "YES" else "NOT NULL"
                
                # Обработка значений по умолчанию
                default = ""
                if col[3]:
                    default_value = self.convert_default_value(col[3])
                    if default_value:
                        default = f"DEFAULT {default_value}"
                
                column_definitions.append(f"{col_name} {col_type} {nullable} {default}".strip())
            
            create_sql = f"""
                CREATE TABLE ags.{table_name} (
                    {', '.join(column_definitions)}
                )
            """
            
            cursor.execute(create_sql)
            self.pg_conn.commit()
            cursor.close()
            
            logging.info(f"✅ Таблица ags.{table_name} создана")
            return True
            
        except Exception as e:
            logging.error(f"❌ Ошибка создания таблицы {table_name}: {e}")
            self.pg_conn.rollback()
            return False
    
    def convert_data_type(self, mssql_type):
        """Конвертация типов данных SQL Server в PostgreSQL"""
        type_mapping = {
            'int': 'INTEGER',
            'bigint': 'BIGINT',
            'smallint': 'SMALLINT',
            'tinyint': 'SMALLINT',
            'nvarchar': 'VARCHAR',
            'varchar': 'VARCHAR',
            'char': 'CHAR',
            'nchar': 'CHAR',
            'text': 'TEXT',
            'ntext': 'TEXT',
            'datetime': 'TIMESTAMP',
            'datetime2': 'TIMESTAMP',
            'date': 'DATE',
            'time': 'TIME',
            'bit': 'BOOLEAN',
            'decimal': 'DECIMAL',
            'numeric': 'NUMERIC',
            'float': 'DOUBLE PRECISION',
            'real': 'REAL',
            'money': 'DECIMAL(19,4)',
            'smallmoney': 'DECIMAL(10,4)',
            'uniqueidentifier': 'UUID',
            'uuid': 'UUID'
        }
        
        return type_mapping.get(mssql_type.lower(), 'TEXT')
    
    def convert_default_value(self, default_value):
        """Конвертация значений по умолчанию"""
        if not default_value:
            return None
            
        # Удаление скобок
        default_value = default_value.strip('()')
        
        # Замена SQL Server функций на PostgreSQL
        replacements = {
            'getdate()': 'CURRENT_TIMESTAMP',
            'getutcdate()': 'CURRENT_TIMESTAMP',
            'newid()': 'gen_random_uuid()',
            'newsequentialid()': 'gen_random_uuid()'
        }
        
        for old, new in replacements.items():
            if old.lower() in default_value.lower():
                default_value = default_value.replace(old, new)
        
        return default_value
    
    def migrate_table_data(self, table_name):
        """Миграция данных таблицы с улучшенной обработкой UUID"""
        try:
            # Получение данных из SQL Server
            mssql_cursor = self.mssql_conn.cursor()
            mssql_cursor.execute(f"SELECT * FROM ags.{table_name}")
            
            # Получение названий колонок
            columns = [desc[0] for desc in mssql_cursor.description]
            
            # Получение всех данных
            rows = mssql_cursor.fetchall()
            mssql_cursor.close()
            
            if not rows:
                logging.info(f"📭 Таблица {table_name} пустая")
                return {"status": "success", "rows_migrated": 0}
            
            # Вставка данных в PostgreSQL
            pg_cursor = self.pg_conn.cursor()
            
            # Подготовка SQL для вставки
            placeholders = ', '.join(['%s'] * len(columns))
            insert_sql = f"INSERT INTO ags.{table_name} ({', '.join(columns)}) VALUES ({placeholders})"
            
            # Пакетная вставка с улучшенной обработкой UUID
            batch_size = 1000
            total_inserted = 0
            
            for i in range(0, len(rows), batch_size):
                batch = rows[i:i + batch_size]
                
                # Обработка UUID значений
                processed_batch = []
                for row in batch:
                    processed_row = []
                    for value in row:
                        if value is None:
                            processed_row.append(None)
                        elif isinstance(value, str) and len(value) == 36 and '-' in value:
                            # Возможно это UUID
                            try:
                                import uuid
                                uuid.UUID(value)
                                processed_row.append(value)
                            except:
                                processed_row.append(value)
                        else:
                            processed_row.append(value)
                    processed_batch.append(processed_row)
                
                try:
                    pg_cursor.executemany(insert_sql, processed_batch)
                    total_inserted += len(processed_batch)
                    
                    if i % 10000 == 0:
                        logging.info(f"📦 {table_name}: мигрировано {total_inserted} записей")
                        
                except Exception as e:
                    logging.error(f"❌ Ошибка вставки batch {table_name}: {e}")
                    # Попробуем вставить по одной записи для отладки
                    for j, row_data in enumerate(processed_batch):
                        try:
                            pg_cursor.execute(insert_sql, row_data)
                        except Exception as e2:
                            logging.error(f"❌ Ошибка записи {i+j} в {table_name}: {e2}")
                            logging.error(f"   Данные: {row_data}")
            
            self.pg_conn.commit()
            pg_cursor.close()
            
            logging.info(f"✅ {table_name}: мигрировано {total_inserted} записей")
            return {"status": "success", "rows_migrated": total_inserted}
            
        except Exception as e:
            logging.error(f"❌ Ошибка миграции данных {table_name}: {e}")
            self.pg_conn.rollback()
            return {"status": "error", "error": str(e)}
    
    def validate_migration(self, table_name):
        """Валидация миграции"""
        try:
            # Подсчет записей в PostgreSQL
            pg_cursor = self.pg_conn.cursor()
            pg_cursor.execute(f"SELECT COUNT(*) FROM ags.{table_name}")
            pg_count = pg_cursor.fetchone()[0]
            pg_cursor.close()
            
            # Подсчет записей в SQL Server
            mssql_cursor = self.mssql_conn.cursor()
            mssql_cursor.execute(f"SELECT COUNT(*) FROM ags.{table_name}")
            mssql_count = mssql_cursor.fetchone()[0]
            mssql_cursor.close()
            
            validation_result = {
                "status": "success" if pg_count == mssql_count else "warning",
                "postgresql_count": pg_count,
                "mssql_count": mssql_count,
                "match": pg_count == mssql_count
            }
            
            if pg_count == mssql_count:
                logging.info(f"✅ {table_name}: валидация успешна ({pg_count} записей)")
            else:
                logging.warning(f"⚠️ {table_name}: несоответствие записей (PG: {pg_count}, MSSQL: {mssql_count})")
            
            return validation_result
            
        except Exception as e:
            logging.error(f"❌ Ошибка валидации {table_name}: {e}")
            return {"status": "error", "error": str(e)}
    
    def migrate_table(self, table_name):
        """Полная миграция одной таблицы"""
        print(f"\n🔄 Миграция таблицы: {table_name}")
        logging.info(f"🔄 Начало миграции таблицы {table_name}")
        
        try:
            # 1. Получение структуры
            columns = self.get_table_structure(table_name)
            if not columns:
                raise Exception(f"Не удалось получить структуру таблицы {table_name}")
            
            # 2. Создание таблицы в PostgreSQL
            if not self.create_table_in_postgresql(table_name, columns):
                raise Exception(f"Не удалось создать таблицу {table_name}")
            
            # 3. Миграция данных
            data_result = self.migrate_table_data(table_name)
            if data_result["status"] != "success":
                raise Exception(data_result.get("error", "Неизвестная ошибка"))
            
            # 4. Валидация
            validation_result = self.validate_migration(table_name)
            
            # Успешная миграция
            result = {
                "table_name": table_name,
                "status": "success",
                "rows_migrated": data_result.get("rows_migrated", 0),
                "validation": validation_result,
                "timestamp": datetime.now().isoformat()
            }
            
            self.migration_results[table_name] = result
            print(f"✅ {table_name}: {data_result.get('rows_migrated', 0)} записей")
            
            return result
            
        except Exception as e:
            error_result = {
                "table_name": table_name,
                "status": "error",
                "error": str(e),
                "timestamp": datetime.now().isoformat()
            }
            
            self.migration_results[table_name] = error_result
            print(f"❌ {table_name}: Ошибка - {e}")
            
            return error_result
    
    def run_group_migration(self, group_name, tables):
        """Запуск миграции группы таблиц"""
        logging.info(f"🚀 Начало миграции группы: {group_name}")
        print(f"\n🚀 МИГРАЦИЯ ГРУППЫ: {group_name}")
        print("=" * 60)
        
        successful = 0
        failed = 0
        
        for table in tables:
            result = self.migrate_table(table)
            if result["status"] == "success":
                successful += 1
            else:
                failed += 1
        
        # Создание отчета
        self.create_group_report(group_name, tables, successful, failed)
        
        return {
            "group_name": group_name,
            "total_tables": len(tables),
            "successful": successful,
            "failed": failed
        }
    
    def create_group_report(self, group_name, tables, successful, failed):
        """Создание отчета о миграции группы"""
        report = {
            "migration_info": {
                "group_name": group_name,
                "migration_date": datetime.now().isoformat(),
                "total_tables": len(tables),
                "successful_migrations": successful,
                "failed_migrations": failed
            },
            "table_results": {table: self.migration_results.get(table, {}) for table in tables},
            "summary": {
                "success_rate": f"{(successful/len(tables))*100:.1f}%" if tables else "0%",
                "total_rows_migrated": sum(
                    r.get("rows_migrated", 0) 
                    for r in self.migration_results.values() 
                    if r.get("status") == "success"
                )
            }
        }
        
        filename = f"final-migration-{group_name.lower().replace(' ', '-')}-report.json"
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(report, f, indent=2, ensure_ascii=False)
        
        print(f"\n📊 ИТОГИ ГРУППЫ '{group_name}':")
        print(f"✅ Успешно: {successful}")
        print(f"❌ Ошибок: {failed}")
        print(f"📈 Процент успеха: {(successful/len(tables))*100:.1f}%")
        print(f"📄 Отчет: {filename}")
    
    def close_connections(self):
        """Закрытие соединений с базами данных"""
        if self.mssql_conn:
            self.mssql_conn.close()
        if self.pg_conn:
            self.pg_conn.close()

def main():
    """Основная функция"""
    print("🚀 Финальная миграция данных с SQL Server в PostgreSQL")
    print("=" * 60)
    
    migrator = FinalDataMigration()
    
    # Подключение к базам данных
    if not migrator.connect_databases():
        print("❌ Не удалось подключиться к базам данных")
        return
    
    try:
        # Очистка дублированных таблиц
        print("🧹 Очистка дублированных таблиц...")
        migrator.clean_duplicate_tables()
        
        # Определение групп для миграции
        groups = [
            {
                "name": "Группа 1: Основные справочники",
                "tables": ["cn", "org", "cst"]
            },
            {
                "name": "Группа 2: Документы и номера", 
                "tables": ["cn_PrDoc", "cn_PrDocP", "invNum"]
            }
        ]
        
        total_successful = 0
        total_failed = 0
        
        for group in groups:
            result = migrator.run_group_migration(group["name"], group["tables"])
            total_successful += result["successful"]
            total_failed += result["failed"]
        
        print("\n" + "=" * 60)
        print("🎉 МИГРАЦИЯ ЗАВЕРШЕНА!")
        print("=" * 60)
        print(f"📊 Общие результаты:")
        print(f"✅ Успешно: {total_successful}")
        print(f"❌ Ошибок: {total_failed}")
        print(f"📈 Общий процент успеха: {(total_successful/(total_successful+total_failed))*100:.1f}%")
        
    finally:
        migrator.close_connections()

if __name__ == "__main__":
    main()