#!/usr/bin/env python3
"""
Скрипт для заполнения системы контроля миграции реальными данными о таблицах MS SQL Server.

Этот скрипт выполняет запрос к MS SQL Server для получения метаданных таблиц
и заполняет систему контроля миграции в PostgreSQL.
"""

import pymssql
import psycopg2
import sys
import os
from datetime import datetime

# Конфигурация подключений
MSSQL_CONFIG = {
    'server': 'localhost:1433',
    'user': 'sa',
    'password': 'Vuege2024!',
    'database': 'Fish_Eye'
}

POSTGRES_CONFIG = {
    'host': 'localhost',
    'database': 'Fish_Eye',
    'user': 'postgres',
    'password': 'postgres'
}

def connect_mssql():
    """Подключение к MS SQL Server"""
    try:
        conn = pymssql.connect(**MSSQL_CONFIG)
        print("✅ Подключение к MS SQL Server успешно")
        return conn
    except Exception as e:
        print(f"❌ Ошибка подключения к MS SQL Server: {e}")
        return None

def connect_postgres():
    """Подключение к PostgreSQL"""
    try:
        conn = psycopg2.connect(**POSTGRES_CONFIG)
        print("✅ Подключение к PostgreSQL успешно")
        return conn
    except Exception as e:
        print(f"❌ Ошибка подключения к PostgreSQL: {e}")
        return None

def get_mssql_metadata(mssql_conn):
    """Получение метаданных таблиц из MS SQL Server"""
    query = """
    SELECT 
        t.TABLE_SCHEMA,
        t.TABLE_NAME,
        t.TABLE_TYPE,
        p.rows AS ROW_COUNT,
        CAST(ROUND(((SUM(a.total_pages) * 8) / 1024.00), 2) AS DECIMAL(18,2)) AS SIZE_MB,
        c.COLUMN_COUNT,
        pk.PRIMARY_KEY_COUNT,
        fk.FOREIGN_KEY_COUNT,
        idx.INDEX_COUNT,
        t.TABLE_CATALOG,
        ISNULL(ep.value, 'Описание отсутствует') AS TABLE_DESCRIPTION,
        o.create_date AS CREATION_DATE,
        o.modify_date AS MODIFICATION_DATE,
        CASE 
            WHEN o.is_ms_shipped = 1 THEN 'Системный объект'
            ELSE 'Пользовательский объект'
        END AS OBJECT_TYPE_DESCRIPTION
    FROM INFORMATION_SCHEMA.TABLES t
    LEFT JOIN sys.partitions p ON p.object_id = OBJECT_ID(t.TABLE_SCHEMA + '.' + t.TABLE_NAME)
    LEFT JOIN sys.allocation_units a ON a.container_id = p.hobt_id
    LEFT JOIN sys.extended_properties ep ON ep.major_id = OBJECT_ID(t.TABLE_SCHEMA + '.' + t.TABLE_NAME)
        AND ep.minor_id = 0
        AND ep.name = 'MS_Description'
    LEFT JOIN sys.objects o ON o.object_id = OBJECT_ID(t.TABLE_SCHEMA + '.' + t.TABLE_NAME)
    LEFT JOIN (
        SELECT TABLE_SCHEMA, TABLE_NAME, COUNT(*) AS COLUMN_COUNT
        FROM INFORMATION_SCHEMA.COLUMNS 
        WHERE TABLE_SCHEMA = 'ags'
        GROUP BY TABLE_SCHEMA, TABLE_NAME
    ) c ON c.TABLE_SCHEMA = t.TABLE_SCHEMA AND c.TABLE_NAME = t.TABLE_NAME
    LEFT JOIN (
        SELECT TABLE_SCHEMA, TABLE_NAME, COUNT(*) AS PRIMARY_KEY_COUNT
        FROM INFORMATION_SCHEMA.KEY_COLUMN_USAGE 
        WHERE CONSTRAINT_NAME LIKE '%PK%' AND TABLE_SCHEMA = 'ags'
        GROUP BY TABLE_SCHEMA, TABLE_NAME
    ) pk ON pk.TABLE_SCHEMA = t.TABLE_SCHEMA AND pk.TABLE_NAME = t.TABLE_NAME
    LEFT JOIN (
        SELECT TABLE_SCHEMA, TABLE_NAME, COUNT(*) AS FOREIGN_KEY_COUNT
        FROM INFORMATION_SCHEMA.KEY_COLUMN_USAGE 
        WHERE CONSTRAINT_NAME LIKE '%FK%' AND TABLE_SCHEMA = 'ags'
        GROUP BY TABLE_SCHEMA, TABLE_NAME
    ) fk ON fk.TABLE_SCHEMA = t.TABLE_SCHEMA AND fk.TABLE_NAME = t.TABLE_NAME
    LEFT JOIN (
        SELECT OBJECT_SCHEMA_NAME(object_id) AS TABLE_SCHEMA,
               OBJECT_NAME(object_id) AS TABLE_NAME,
               COUNT(*) AS INDEX_COUNT
        FROM sys.indexes 
        WHERE type > 0 AND OBJECT_SCHEMA_NAME(object_id) = 'ags'
        GROUP BY object_id
    ) idx ON idx.TABLE_SCHEMA = t.TABLE_SCHEMA AND idx.TABLE_NAME = t.TABLE_NAME
    WHERE t.TABLE_TYPE = 'BASE TABLE'
        AND t.TABLE_SCHEMA = 'ags'
        AND p.index_id IN (0, 1)
    GROUP BY 
        t.TABLE_SCHEMA, t.TABLE_NAME, t.TABLE_TYPE, p.rows, t.TABLE_CATALOG,
        c.COLUMN_COUNT, pk.PRIMARY_KEY_COUNT, fk.FOREIGN_KEY_COUNT, idx.INDEX_COUNT,
        ep.value, o.create_date, o.modify_date, o.is_ms_shipped
    ORDER BY t.TABLE_NAME
    """
    
    try:
        cursor = mssql_conn.cursor()
        cursor.execute(query)
        results = cursor.fetchall()
        print(f"✅ Получено {len(results)} таблиц из MS SQL Server")
        return results
    except Exception as e:
        print(f"❌ Ошибка выполнения запроса MS SQL: {e}")
        return []

def insert_into_migration_control(postgres_conn, mssql_data, task_id):
    """Вставка данных в систему контроля миграции"""
    try:
        cursor = postgres_conn.cursor()
        
        # Подготовка данных для вставки
        for row in mssql_data:
            (table_schema, table_name, table_type, row_count, size_mb, column_count,
             primary_key_count, foreign_key_count, index_count, table_catalog,
             table_description, creation_date, modification_date, object_type_description) = row
            
            # Обработка NULL значений
            row_count = row_count if row_count is not None else 0
            size_mb = size_mb if size_mb is not None else 0
            column_count = column_count if column_count is not None else 0
            primary_key_count = primary_key_count if primary_key_count is not None else 0
            foreign_key_count = foreign_key_count if foreign_key_count is not None else 0
            index_count = index_count if index_count is not None else 0
            table_catalog = table_catalog if table_catalog is not None else 'Fish_Eye'
            
            # Обработка описания - преобразование в читаемый текст
            if table_description and table_description != 'Описание отсутствует':
                # Если описание содержит hex данные, преобразуем их
                if isinstance(table_description, bytes):
                    try:
                        table_description = table_description.decode('utf-8')
                    except:
                        table_description = str(table_description)
                elif table_description.startswith('\\x'):
                    # Убираем hex префикс и декодируем
                    try:
                        hex_data = table_description[2:]  # Убираем \x
                        decoded = bytes.fromhex(hex_data).decode('utf-8')
                        table_description = decoded
                    except:
                        table_description = 'Описание в нечитаемом формате'
            else:
                table_description = 'Описание отсутствует'
            
            try:
                # Вставка в mssql_tables с доступными полями - наследование автоматически создаст записи в mssql_objects
                cursor.execute("""
                    INSERT INTO mcl.mssql_tables 
                    (task_id, object_name, object_type, schema_name, migration_status, 
                     object_type_description, object_description, create_date, modify_date,
                     table_catalog, row_count, table_size, primary_key_count, foreign_key_count, 
                     index_count, column_count)
                    VALUES (%s, %s, %s, %s, 'pending', %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                """, (task_id, table_name, table_type, table_schema, object_type_description,
                      table_description, creation_date, modification_date,
                      table_catalog, row_count, int(size_mb * 1024 * 1024), primary_key_count, 
                      foreign_key_count, index_count, column_count))
                    
            except Exception as e:
                print(f"⚠️ Ошибка при вставке таблицы {table_name}: {e}")
                continue
        
        postgres_conn.commit()
        print(f"✅ Успешно вставлено {len(mssql_data)} таблиц в систему контроля миграции")
        return True
        
    except Exception as e:
        postgres_conn.rollback()
        print(f"❌ Ошибка вставки в PostgreSQL: {e}")
        return False

def main():
    """Основная функция"""
    print("🚀 Начало заполнения системы контроля миграции реальными данными")
    print("=" * 60)
    
    # Подключение к MS SQL Server
    mssql_conn = connect_mssql()
    if not mssql_conn:
        sys.exit(1)
    
    # Подключение к PostgreSQL
    postgres_conn = connect_postgres()
    if not postgres_conn:
        mssql_conn.close()
        sys.exit(1)
    
    try:
        # Получение метаданных из MS SQL Server
        print("\n📊 Получение метаданных таблиц...")
        mssql_data = get_mssql_metadata(mssql_conn)
        
        if not mssql_data:
            print("❌ Не удалось получить данные из MS SQL Server")
            return
        
        # Вставка в систему контроля миграции
        print("\n💾 Вставка данных в систему контроля миграции...")
        task_id = 2  # ID текущей задачи миграции
        
        success = insert_into_migration_control(postgres_conn, mssql_data, task_id)
        
        if success:
            print("\n✅ Система контроля миграции успешно заполнена реальными данными!")
            print(f"📊 Количество таблиц: {len(mssql_data)}")
            print(f"🎯 Задача миграции: {task_id}")
        else:
            print("\n❌ Ошибка при заполнении системы контроля миграции")
            
    except Exception as e:
        print(f"❌ Критическая ошибка: {e}")
        
    finally:
        # Закрытие соединений
        mssql_conn.close()
        postgres_conn.close()
        print("\n🔌 Соединения закрыты")

if __name__ == "__main__":
    main()