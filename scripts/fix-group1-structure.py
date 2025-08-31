#!/usr/bin/env python3
"""
@file: fix-group1-structure.py
@description: Исправление структуры таблиц группы 1 в PostgreSQL
@created: 2025-08-30
"""

import logging
import psycopg2
from datetime import datetime

class FixGroup1Structure:
    def __init__(self):
        self.setup_logging()
        self.pg_conn_str = "dbname=Fish_Eye user=postgres password=postgres host=localhost port=5432"
        self.pg_conn = None
        
    def setup_logging(self):
        """Настройка логирования"""
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler('fix-group1-structure.log'),
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
    
    def fix_table_structure(self, table_name, columns_def):
        """Исправление структуры таблицы"""
        pg_cursor = self.pg_conn.cursor()
        try:
            # Удаляем таблицу, если она существует
            pg_cursor.execute(f'DROP TABLE IF EXISTS ags."{table_name}" CASCADE;')
            self.pg_conn.commit()
            logging.info(f"✅ Таблица ags.\"{table_name}\" удалена (если существовала).")
            
            # Создаем таблицу с новой структурой
            create_table_sql = f'CREATE TABLE ags."{table_name}" ({", ".join(columns_def)});'
            pg_cursor.execute(create_table_sql)
            self.pg_conn.commit()
            logging.info(f"✅ Таблица ags.\"{table_name}\" пересоздана с правильной структурой.")
            return True
            
        except psycopg2.Error as ex:
            logging.error(f"❌ Ошибка пересоздания таблицы ags.\"{table_name}\": {ex}")
            self.pg_conn.rollback()
            return False
    
    def run_fix_structure(self):
        """Запуск исправления структуры"""
        logging.info("🚀 Начало исправления структуры таблиц группы 1")
        
        if not self.connect_postgres():
            return
        
        # Определение правильных структур таблиц
        tables_structure = {
            'cn': [
                '"cn_key" INTEGER NOT NULL',
                '"cn_number" VARCHAR(255)',
                '"cn_date" DATE',
                '"cn_note" TEXT',
                '"cnMark" INTEGER',
                '"cnTimeOfEntry" TIMESTAMP WITHOUT TIME ZONE',
                '"cnName" VARCHAR(500)'
            ],
            'org': [
                '"org_key" INTEGER NOT NULL',
                '"org_number" VARCHAR(50)',
                '"org_name" VARCHAR(255)',
                '"org_type" VARCHAR(100)',
                '"org_status" VARCHAR(50)'
            ],
            'cst': [
                '"cst_key" INTEGER NOT NULL',
                '"cst_number" VARCHAR(50)',
                '"cst_name" VARCHAR(255)',
                '"cst_type" VARCHAR(100)',
                '"cst_status" VARCHAR(50)'
            ]
        }
        
        successful_fixes = 0
        failed_fixes = 0
        
        for table_name, columns_def in tables_structure.items():
            logging.info(f"\n🔧 Исправление структуры таблицы {table_name}")
            print(f"🔧 Исправление структуры таблицы: {table_name}")
            
            if self.fix_table_structure(table_name, columns_def):
                successful_fixes += 1
                print(f"✅ {table_name}: Структура исправлена")
            else:
                failed_fixes += 1
                print(f"❌ {table_name}: Ошибка исправления структуры")
        
        self.pg_conn.close()
        
        print("\n" + "=" * 60)
        print("📊 ИТОГИ ИСПРАВЛЕНИЯ СТРУКТУРЫ:")
        print("=" * 60)
        print(f"✅ Успешно: {successful_fixes}")
        print(f"❌ Ошибок: {failed_fixes}")
        print("=" * 60)
        
        logging.info(f"🎉 Исправление структуры завершено: {successful_fixes} успешно, {failed_fixes} ошибок")

def main():
    """Основная функция"""
    print("🚀 Исправление структуры таблиц группы 1")
    
    fixer = FixGroup1Structure()
    fixer.run_fix_structure()

if __name__ == "__main__":
    main()