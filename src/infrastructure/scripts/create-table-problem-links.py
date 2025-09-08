#!/usr/bin/env python3
"""
Скрипт для создания связей между способом решения и таблицами с заглавными буквами

Автор: AI Assistant
Дата: 6 сентября 2025
Версия: 1.0
"""

import psycopg2
import sys
from datetime import datetime

def connect_to_database():
    """Подключение к базе данных Fish_Eye"""
    try:
        conn = psycopg2.connect(
            host="localhost",
            port="5432",
            database="Fish_Eye",
            user="postgres",
            password="postgres"
        )
        return conn
    except Exception as e:
        print(f"Ошибка подключения к базе данных: {e}")
        sys.exit(1)

def get_tables_with_capitals(conn):
    """Получение таблиц с заглавными буквами"""
    try:
        cursor = conn.cursor()
        query = """
        SELECT id, object_name
        FROM mcl.mssql_tables 
        WHERE schema_name = 'ags'
        AND object_name ~ '[A-Z]'
        ORDER BY object_name
        """
        cursor.execute(query)
        return cursor.fetchall()
    except Exception as e:
        print(f"Ошибка получения таблиц: {e}")
        return []

def create_problem_links(conn, tables, solution_id):
    """Создание связей между таблицами и способом решения"""
    try:
        cursor = conn.cursor()
        
        created_count = 0
        failed_count = 0
        
        for table_id, table_name in tables:
            try:
                insert_query = """
                INSERT INTO mcl.problems_tb_slt_mp (
                    table_id,
                    solution_id,
                    solution_status,
                    problem_detected_date,
                    created_at,
                    updated_at
                ) VALUES (
                    %s, %s, %s, %s, %s, %s
                )
                """
                
                cursor.execute(insert_query, (
                    table_id,
                    solution_id,
                    'pending',
                    datetime.now(),
                    datetime.now(),
                    datetime.now()
                ))
                
                created_count += 1
                print(f"✅ Создана связь для таблицы: {table_name} (ID: {table_id})")
                
            except Exception as e:
                failed_count += 1
                print(f"❌ Ошибка создания связи для таблицы {table_name}: {e}")
        
        conn.commit()
        return created_count, failed_count
        
    except Exception as e:
        print(f"Ошибка создания связей: {e}")
        conn.rollback()
        return 0, len(tables)

def main():
    """Основная функция"""
    print("🚀 Создание связей между способом решения и таблицами с заглавными буквами")
    print("=" * 70)
    
    # Подключение к базе данных
    conn = connect_to_database()
    
    try:
        # Получение таблиц с заглавными буквами
        print("📋 Получение таблиц с заглавными буквами...")
        tables = get_tables_with_capitals(conn)
        
        if not tables:
            print("❌ Не найдено таблиц с заглавными буквами")
            return
        
        print(f"📊 Найдено {len(tables)} таблиц с заглавными буквами")
        print()
        
        # Создание связей
        solution_id = 4  # ID способа решения "Способ решения не определен"
        created_count, failed_count = create_problem_links(conn, tables, solution_id)
        
        print()
        print("=" * 70)
        print("📊 ИТОГИ СОЗДАНИЯ СВЯЗЕЙ:")
        print(f"✅ Успешно создано: {created_count}")
        print(f"❌ Ошибок: {failed_count}")
        print(f"📈 Общий прогресс: {created_count}/{len(tables)} ({created_count/len(tables)*100:.1f}%)")
        
        # Проверка результата
        cursor = conn.cursor()
        cursor.execute("SELECT COUNT(*) FROM mcl.problems_tb_slt_mp WHERE solution_id = %s", (solution_id,))
        total_links = cursor.fetchone()[0]
        print(f"📋 Всего связей для способа решения ID {solution_id}: {total_links}")
        
    except Exception as e:
        print(f"❌ Критическая ошибка: {e}")
        conn.rollback()
    finally:
        conn.close()
        print("🔌 Подключение к базе данных закрыто")

if __name__ == "__main__":
    main()