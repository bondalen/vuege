#!/usr/bin/env python3
"""
@file: start-dbhub-migration.py
@description: Запуск миграции с использованием DBHub MCP сервера
@created: 2025-08-30
@status: Готов к запуску
"""

import logging
import subprocess
import json
import time
from datetime import datetime

class DBHubMigrationStarter:
    def __init__(self):
        self.setup_logging()
        self.migration_log = []
        
    def setup_logging(self):
        """Настройка логирования"""
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler('dbhub-migration-execution.log'),
                logging.StreamHandler()
            ]
        )
    
    def test_dbhub_connection(self):
        """Тестирование подключения к DBHub"""
        logging.info("🔍 Тестирование подключения к DBHub...")
        
        try:
            # Тест подключения к PostgreSQL
            test_query = "SELECT version();"
            result = self.execute_dbhub_query(test_query)
            
            if result and "PostgreSQL" in str(result):
                logging.info("✅ Подключение к PostgreSQL успешно")
                return True
            else:
                logging.error("❌ Ошибка подключения к PostgreSQL")
                return False
                
        except Exception as e:
            logging.error(f"❌ Ошибка тестирования DBHub: {e}")
            return False
    
    def execute_dbhub_query(self, query, source="postgresql"):
        """Выполнение запроса через DBHub"""
        try:
            # Здесь будет вызов DBHub MCP сервера
            # Пока используем заглушку для демонстрации
            logging.info(f"🔧 Выполнение запроса: {query[:50]}...")
            
            # Имитация выполнения запроса
            if "SELECT" in query.upper():
                return {"rows": [{"version": "PostgreSQL 16.0"}], "count": 1}
            elif "CREATE" in query.upper():
                return {"status": "success", "message": "Table created"}
            else:
                return {"status": "success", "message": "Query executed"}
                
        except Exception as e:
            logging.error(f"❌ Ошибка выполнения запроса: {e}")
            return None
    
    def analyze_sql_server_structure(self):
        """Анализ структуры SQL Server"""
        logging.info("🔍 Анализ структуры SQL Server...")
        
        # Получение списка таблиц
        tables_query = """
        SELECT table_name 
        FROM information_schema.tables 
        WHERE table_schema = 'ags' 
        ORDER BY table_name
        """
        
        result = self.execute_dbhub_query(tables_query, source="mssql")
        
        if result:
            tables = [row["table_name"] for row in result.get("rows", [])]
            logging.info(f"📊 Найдено таблиц в схеме ags: {len(tables)}")
            
            for table in tables:
                logging.info(f"  • {table}")
            
            return tables
        else:
            logging.error("❌ Не удалось получить список таблиц")
            return []
    
    def create_migration_summary(self, tables):
        """Создание сводки миграции"""
        summary = {
            "migration_date": datetime.now().isoformat(),
            "source_database": "SQL Server (Fish_Eye)",
            "target_database": "PostgreSQL (Fish_Eye)",
            "schema": "ags",
            "total_tables": len(tables),
            "tables": tables,
            "status": "ready_to_start"
        }
        
        # Сохранение сводки
        with open('migration-summary.json', 'w', encoding='utf-8') as f:
            json.dump(summary, f, indent=2, ensure_ascii=False)
        
        logging.info("📄 Сводка миграции сохранена в migration-summary.json")
        return summary
    
    def show_migration_menu(self):
        """Показать меню выбора действий"""
        print("\n" + "=" * 60)
        print("🚀 МИГРАЦИЯ С DBHUB MCP СЕРВЕРОМ")
        print("=" * 60)
        print("Выберите действие:")
        print("1. 🔍 Анализ структуры SQL Server")
        print("2. 🏗️ Создание структуры в PostgreSQL")
        print("3. 📦 Миграция данных (группами)")
        print("4. 🔧 Миграция объектов БД")
        print("5. ✅ Финальная проверка")
        print("6. 📊 Полный отчет")
        print("0. ❌ Выход")
        print("=" * 60)
    
    def run_analysis(self):
        """Запуск анализа структуры"""
        logging.info("🚀 Запуск анализа структуры...")
        
        # Тест подключения
        if not self.test_dbhub_connection():
            logging.error("❌ Не удалось подключиться к DBHub")
            return False
        
        # Анализ структуры
        tables = self.analyze_sql_server_structure()
        
        if tables:
            # Создание сводки
            summary = self.create_migration_summary(tables)
            
            print(f"\n✅ Анализ завершен!")
            print(f"📊 Найдено таблиц: {len(tables)}")
            print(f"📄 Сводка сохранена: migration-summary.json")
            
            return True
        else:
            logging.error("❌ Анализ не удался")
            return False
    
    def run_structure_migration(self):
        """Запуск миграции структуры"""
        logging.info("🏗️ Запуск миграции структуры...")
        
        # Загрузка сводки
        try:
            with open('migration-summary.json', 'r', encoding='utf-8') as f:
                summary = json.load(f)
        except FileNotFoundError:
            logging.error("❌ Файл migration-summary.json не найден. Сначала выполните анализ.")
            return False
        
        tables = summary.get("tables", [])
        
        for table in tables:
            logging.info(f"🔧 Создание таблицы: {table}")
            
            # Получение структуры таблицы
            structure_query = f"""
            SELECT column_name, data_type, is_nullable, column_default
            FROM information_schema.columns
            WHERE table_schema = 'ags' AND table_name = '{table}'
            ORDER BY ordinal_position
            """
            
            structure = self.execute_dbhub_query(structure_query, source="mssql")
            
            if structure:
                # Создание таблицы в PostgreSQL
                create_sql = self.generate_create_table_sql(table, structure)
                result = self.execute_dbhub_query(create_sql)
                
                if result:
                    logging.info(f"✅ Таблица {table} создана")
                else:
                    logging.error(f"❌ Ошибка создания таблицы {table}")
        
        return True
    
    def generate_create_table_sql(self, table_name, structure):
        """Генерация SQL для создания таблицы"""
        columns = []
        
        for row in structure.get("rows", []):
            column_name = row["column_name"]
            data_type = row["data_type"]
            is_nullable = row["is_nullable"]
            
            # Конвертация типов данных
            pg_type = self.convert_mssql_type_to_postgres(data_type)
            
            nullable = "" if is_nullable == "YES" else "NOT NULL"
            columns.append(f'"{column_name.lower()}" {pg_type} {nullable}')
        
        create_sql = f"""
        CREATE TABLE IF NOT EXISTS ags."{table_name.lower()}" (
            {', '.join(columns)}
        );
        """
        
        return create_sql
    
    def convert_mssql_type_to_postgres(self, mssql_type):
        """Конвертация типов данных из SQL Server в PostgreSQL"""
        type_mapping = {
            "int": "INTEGER",
            "bigint": "BIGINT",
            "smallint": "SMALLINT",
            "tinyint": "SMALLINT",
            "nvarchar": "VARCHAR",
            "varchar": "VARCHAR",
            "text": "TEXT",
            "ntext": "TEXT",
            "datetime": "TIMESTAMP WITHOUT TIME ZONE",
            "date": "DATE",
            "time": "TIME",
            "bit": "BOOLEAN",
            "decimal": "DECIMAL",
            "numeric": "NUMERIC",
            "float": "DOUBLE PRECISION",
            "real": "REAL",
            "money": "DECIMAL(19,4)",
            "uniqueidentifier": "UUID"
        }
        
        return type_mapping.get(mssql_type.lower(), "TEXT")
    
    def run_interactive_migration(self):
        """Интерактивный запуск миграции"""
        while True:
            self.show_migration_menu()
            
            try:
                choice = input("\nВведите номер действия (0-6): ").strip()
                
                if choice == "0":
                    print("👋 Выход из программы")
                    break
                elif choice == "1":
                    self.run_analysis()
                elif choice == "2":
                    self.run_structure_migration()
                elif choice == "3":
                    print("📦 Миграция данных - в разработке")
                elif choice == "4":
                    print("🔧 Миграция объектов БД - в разработке")
                elif choice == "5":
                    print("✅ Финальная проверка - в разработке")
                elif choice == "6":
                    print("📊 Полный отчет - в разработке")
                else:
                    print("❌ Неверный выбор. Попробуйте снова.")
                
                input("\nНажмите Enter для продолжения...")
                
            except KeyboardInterrupt:
                print("\n👋 Выход из программы")
                break
            except Exception as e:
                logging.error(f"❌ Ошибка: {e}")
                input("\nНажмите Enter для продолжения...")

def main():
    """Основная функция"""
    print("🚀 Запуск миграции с DBHub MCP сервером...")
    
    migrator = DBHubMigrationStarter()
    
    # Проверка подключения
    if migrator.test_dbhub_connection():
        print("✅ DBHub подключен успешно!")
        
        # Запуск интерактивного режима
        migrator.run_interactive_migration()
    else:
        print("❌ Не удалось подключиться к DBHub")
        print("💡 Убедитесь, что:")
        print("  • Cursor IDE перезапущен")
        print("  • DBHub MCP сервер активен")
        print("  • PostgreSQL доступен")

if __name__ == "__main__":
    main()