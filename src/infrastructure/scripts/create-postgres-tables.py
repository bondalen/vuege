#!/usr/bin/env python3
"""
Скрипт для создания целевых таблиц PostgreSQL на основе исходных таблиц MS SQL
Согласно диаграмме table-migration-detailed-process.puml: "Создание аналогов таблиц без объектов таблиц"

Автор: AI Assistant
Дата: 4 сентября 2025
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

def get_mssql_tables(conn):
    """Получение списка исходных таблиц MS SQL"""
    try:
        cursor = conn.cursor()
        query = """
        SELECT id, object_name, object_type, schema_name, migration_status
        FROM mcl.mssql_tables 
        WHERE schema_name = 'ags' 
        ORDER BY object_name
        """
        cursor.execute(query)
        return cursor.fetchall()
    except Exception as e:
        print(f"Ошибка получения списка таблиц MS SQL: {e}")
        return []

def create_postgres_table_record(conn, mssql_table):
    """Создание записи целевой таблицы PostgreSQL"""
    try:
        cursor = conn.cursor()
        
        # Извлекаем данные из исходной таблицы
        table_id, object_name, object_type, schema_name, migration_status = mssql_table
        
        # Создаем запись в postgres_tables
        insert_query = """
        INSERT INTO mcl.postgres_tables (
            task_id,
            object_name,
            object_type,
            schema_name,
            migration_status,
            source_table_id,
            created_at,
            updated_at
        ) VALUES (
            %s, %s, %s, %s, %s, %s, %s, %s
        ) RETURNING id
        """
        
        cursor.execute(insert_query, (
            2,  # task_id для текущей задачи миграции
            object_name,  # Имя таблицы (пока без изменений)
            object_type,  # Тип объекта
            'ags',  # Схема (пока та же)
            'pending',  # Статус миграции
            table_id,  # Ссылка на исходную таблицу
            datetime.now(),
            datetime.now()
        ))
        
        postgres_table_id = cursor.fetchone()[0]
        conn.commit()
        
        print(f"✅ Создана целевая таблица: {object_name} (ID: {postgres_table_id})")
        return postgres_table_id
        
    except Exception as e:
        print(f"❌ Ошибка создания записи для таблицы {object_name}: {e}")
        conn.rollback()
        return None

def main():
    """Основная функция"""
    print("🚀 Начало создания целевых таблиц PostgreSQL")
    print("=" * 60)
    
    # Подключение к базе данных
    conn = connect_to_database()
    
    try:
        # Получение списка исходных таблиц
        print("📋 Получение списка исходных таблиц MS SQL...")
        mssql_tables = get_mssql_tables(conn)
        
        if not mssql_tables:
            print("❌ Не найдено исходных таблиц для миграции")
            return
        
        print(f"📊 Найдено {len(mssql_tables)} исходных таблиц")
        print()
        
        # Создание целевых таблиц
        created_count = 0
        failed_count = 0
        
        for mssql_table in mssql_tables:
            table_id, object_name, object_type, schema_name, migration_status = mssql_table
            
            print(f"🔄 Обработка таблицы: {object_name}")
            
            postgres_table_id = create_postgres_table_record(conn, mssql_table)
            
            if postgres_table_id:
                created_count += 1
            else:
                failed_count += 1
        
        print()
        print("=" * 60)
        print("📊 ИТОГИ СОЗДАНИЯ ЦЕЛЕВЫХ ТАБЛИЦ:")
        print(f"✅ Успешно создано: {created_count}")
        print(f"❌ Ошибок: {failed_count}")
        print(f"📈 Общий прогресс: {created_count}/{len(mssql_tables)} ({created_count/len(mssql_tables)*100:.1f}%)")
        
        # Проверка результата
        cursor = conn.cursor()
        cursor.execute("SELECT COUNT(*) FROM mcl.postgres_tables")
        total_postgres_tables = cursor.fetchone()[0]
        print(f"📋 Всего целевых таблиц в системе: {total_postgres_tables}")
        
    except Exception as e:
        print(f"❌ Критическая ошибка: {e}")
        conn.rollback()
    finally:
        conn.close()
        print("🔌 Подключение к базе данных закрыто")

if __name__ == "__main__":
    main()