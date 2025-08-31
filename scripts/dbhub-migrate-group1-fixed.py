#!/usr/bin/env python3
"""
@file: dbhub-migrate-group1-fixed.py
@description: Исправленная миграция данных группы 1 через Docker
@created: 2025-08-30
"""

import logging
import subprocess
import psycopg2
from datetime import datetime

class DBHubGroup1FixedMigration:
    def __init__(self):
        self.setup_logging()
        self.group_name = "Группа 1: Основные справочники"
        self.tables = ["cn", "org", "cst"]
        
        # Подключение к PostgreSQL
        self.pg_conn_str = "dbname=Fish_Eye user=postgres password=postgres host=localhost port=5432"
        self.pg_conn = None
        
    def setup_logging(self):
        """Настройка логирования"""
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler('dbhub-group1-fixed-migration.log'),
                logging.StreamHandler()
            ]
        )
    
    def connect_postgres(self):
        """Подключение к PostgreSQL"""
        try:
            self.pg_conn = psycopg2.connect(self.pg_conn_str)
            logging.info("✅ Подключение к PostgreSQL успешно.")
            return True
        except psycopg2.Error as ex:
            logging.error(f"❌ Ошибка подключения к PostgreSQL: {ex}")
            return False
    
    def get_mssql_data_via_docker(self, table_name):
        """Получение данных из SQL Server через Docker"""
        try:
            # Команда для получения данных через Docker
            cmd = [
                "docker", "exec", "vuege-mssql",
                "/opt/mssql-tools18/bin/sqlcmd",
                "-S", "localhost,1433",
                "-U", "sa",
                "-P", "Vuege2024!",
                "-d", "Fish_Eye",
                "-Q", f"SELECT * FROM ags.{table_name}",
                "-C"
            ]
            
            logging.info(f"🔍 Получение данных из SQL Server: {table_name}")
            result = subprocess.run(cmd, capture_output=True, text=True, timeout=30)
            
            if result.returncode == 0:
                # Парсинг результата
                lines = result.stdout.strip().split('\n')
                # Удаляем заголовки и пустые строки
                data_lines = []
                for line in lines:
                    line = line.strip()
                    if line and not line.startswith('---') and not line.startswith('(') and not line.startswith('cn_key') and not line.startswith('org_key') and not line.startswith('cstKey'):
                        data_lines.append(line)
                
                if len(data_lines) > 0:
                    logging.info(f"📄 Получены данные из SQL Server для таблицы {table_name}: {len(data_lines)} строк")
                    return data_lines
                else:
                    logging.info(f"⚠️ Таблица {table_name} пустая в SQL Server")
                    return []
            else:
                logging.error(f"❌ Ошибка получения данных из SQL Server: {result.stderr}")
                return []
                
        except subprocess.TimeoutExpired:
            logging.error(f"❌ Таймаут получения данных из SQL Server: {table_name}")
            return []
        except Exception as e:
            logging.error(f"❌ Ошибка получения данных из SQL Server: {e}")
            return []
    
    def parse_data_line(self, line, table_name):
        """Парсинг строки данных"""
        try:
            # Разделение по пробелам, но учитывая кавычки
            parts = []
            current_part = ""
            in_quotes = False
            
            for char in line:
                if char == '"':
                    in_quotes = not in_quotes
                elif char == ' ' and not in_quotes:
                    if current_part:
                        parts.append(current_part.strip('"'))
                        current_part = ""
                else:
                    current_part += char
            
            if current_part:
                parts.append(current_part.strip('"'))
            
            return parts
        except Exception as e:
            logging.error(f"❌ Ошибка парсинга строки: {line[:50]}... - {e}")
            return []
    
    def insert_postgres_data(self, table_name, data_lines):
        """Вставка данных в PostgreSQL"""
        if not data_lines:
            logging.info(f"⚠️ Нет данных для вставки в таблицу {table_name}.")
            return False
        
        pg_cursor = self.pg_conn.cursor()
        try:
            # Получение структуры таблицы
            pg_cursor.execute(f"""
                SELECT column_name, data_type
                FROM information_schema.columns 
                WHERE table_schema = 'ags' AND table_name = '{table_name}'
                ORDER BY ordinal_position
            """)
            columns_info = pg_cursor.fetchall()
            columns = [col[0] for col in columns_info]
            types = [col[1] for col in columns_info]
            
            successful_inserts = 0
            
            for line in data_lines:
                if line.strip():
                    # Парсинг строки
                    values = self.parse_data_line(line, table_name)
                    
                    if len(values) >= len(columns):
                        # Преобразование типов данных
                        converted_values = []
                        for i, value in enumerate(values[:len(columns)]):
                            try:
                                if types[i] == 'integer':
                                    converted_values.append(int(value) if value else None)
                                elif types[i] == 'numeric':
                                    converted_values.append(float(value) if value else None)
                                elif types[i] == 'timestamp without time zone':
                                    # Обработка даты
                                    if value and value != 'NULL':
                                        converted_values.append(value)
                                    else:
                                        converted_values.append(None)
                                else:
                                    converted_values.append(value if value != 'NULL' else None)
                            except (ValueError, TypeError):
                                converted_values.append(None)
                        
                        # Создание INSERT запроса
                        columns_str = ", ".join([f'"{col}"' for col in columns])
                        placeholders = ", ".join(['%s'] * len(columns))
                        insert_sql = f"INSERT INTO ags.{table_name} ({columns_str}) VALUES ({placeholders})"
                        
                        # Вставка данных
                        pg_cursor.execute(insert_sql, converted_values)
                        successful_inserts += 1
            
            self.pg_conn.commit()
            logging.info(f"✅ Данные таблицы {table_name} мигрированы: {successful_inserts} записей")
            return True
            
        except psycopg2.Error as ex:
            logging.error(f"❌ Ошибка вставки данных в таблицу {table_name}: {ex}")
            self.pg_conn.rollback()
            return False
    
    def validate_migration(self, table_name):
        """Валидация миграции"""
        pg_cursor = self.pg_conn.cursor()
        try:
            pg_cursor.execute(f"SELECT COUNT(*) FROM ags.{table_name}")
            pg_count = pg_cursor.fetchone()[0]
            
            logging.info(f"✅ Валидация {table_name}: {pg_count} записей в PostgreSQL")
            return pg_count > 0
                
        except Exception as ex:
            logging.error(f"❌ Ошибка валидации таблицы {table_name}: {ex}")
            return False
    
    def migrate_table(self, table_name):
        """Миграция одной таблицы"""
        logging.info(f"\n🔄 Миграция таблицы {table_name}")
        print(f"🔄 Миграция таблицы: {table_name}")
        
        try:
            # 1. Получение данных из SQL Server через Docker
            data_lines = self.get_mssql_data_via_docker(table_name)
            
            if not data_lines:
                print(f"⚠️ {table_name}: Пустая таблица или ошибка получения данных")
                return {"status": "empty", "table": table_name}
            
            # 2. Вставка данных в PostgreSQL
            if self.insert_postgres_data(table_name, data_lines):
                # 3. Валидация
                if self.validate_migration(table_name):
                    print(f"✅ {table_name}: {len(data_lines)} строк")
                    return {"status": "success", "table": table_name, "rows": len(data_lines)}
                else:
                    print(f"⚠️ {table_name}: Ошибка валидации")
                    return {"status": "validation_error", "table": table_name}
            else:
                print(f"❌ {table_name}: Ошибка вставки данных")
                return {"status": "insert_error", "table": table_name}
                
        except Exception as e:
            logging.error(f"❌ Ошибка миграции таблицы {table_name}: {e}")
            print(f"❌ {table_name}: Ошибка - {e}")
            return {"status": "error", "table": table_name, "error": str(e)}
    
    def run_migration(self):
        """Запуск миграции группы"""
        logging.info(f"🚀 Начало миграции данных {self.group_name}")
        print(f"\n🚀 МИГРАЦИЯ ДАННЫХ: {self.group_name}")
        print("=" * 60)
        
        if not self.connect_postgres():
            logging.error("❌ Не удалось подключиться к PostgreSQL")
            return
        
        successful_migrations = 0
        failed_migrations = 0
        empty_tables = 0
        total_rows = 0
        
        for table in self.tables:
            result = self.migrate_table(table)
            
            if result["status"] == "success":
                successful_migrations += 1
                total_rows += result.get("rows", 0)
            elif result["status"] == "empty":
                empty_tables += 1
            else:
                failed_migrations += 1
        
        # Закрытие соединения
        if self.pg_conn:
            self.pg_conn.close()
        
        # Итоги
        print("\n" + "=" * 60)
        print("📊 ИТОГИ МИГРАЦИИ ДАННЫХ:")
        print("=" * 60)
        print(f"📋 Группа: {self.group_name}")
        print(f"📊 Всего таблиц: {len(self.tables)}")
        print(f"✅ Успешно: {successful_migrations}")
        print(f"⚠️ Пустых: {empty_tables}")
        print(f"❌ Ошибок: {failed_migrations}")
        print(f"📦 Всего строк: {total_rows}")
        print("=" * 60)
        
        logging.info(f"🎉 Миграция данных завершена: {successful_migrations} успешно, {failed_migrations} ошибок")

def main():
    """Основная функция"""
    print("🚀 Запуск исправленной миграции данных группы 1")
    
    migrator = DBHubGroup1FixedMigration()
    migrator.run_migration()

if __name__ == "__main__":
    main()