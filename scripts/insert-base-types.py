#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Скрипт для вставки базовых типов данных в PostgreSQL
"""

import psycopg2
import pymssql

def get_base_types_from_mssql():
    """Получить базовые типы данных из MS SQL Server"""
    
    try:
        conn = pymssql.connect(
            server='localhost',
            port=1433,
            user='sa',
            password='Vuege2024!',
            database='Fish_Eye'
        )
        
        cursor = conn.cursor()
        
        query = """
        SELECT DISTINCT
            c.data_type as base_type_name,
            CASE
                WHEN c.data_type IN ('int', 'bigint', 'smallint', 'tinyint') THEN 'integer'
                WHEN c.data_type IN ('decimal', 'numeric', 'money', 'smallmoney') THEN 'decimal'
                WHEN c.data_type IN ('float', 'real') THEN 'float'
                WHEN c.data_type IN ('char', 'varchar', 'nchar', 'nvarchar', 'text', 'ntext') THEN 'string'
                WHEN c.data_type IN ('date', 'datetime', 'datetime2', 'smalldatetime') THEN 'datetime'
                WHEN c.data_type IN ('bit') THEN 'boolean'
                WHEN c.data_type IN ('binary', 'varbinary', 'image') THEN 'binary'
                WHEN c.data_type IN ('uniqueidentifier') THEN 'uuid'
                ELSE 'other'
            END as type_category,
            CASE
                WHEN c.data_type IN ('int', 'bigint', 'smallint', 'tinyint') THEN 'integer'
                WHEN c.data_type IN ('decimal', 'numeric', 'money', 'smallmoney') THEN 'decimal'
                WHEN c.data_type IN ('float', 'real') THEN 'float'
                WHEN c.data_type IN ('char', 'varchar', 'nchar', 'nvarchar', 'text', 'ntext') THEN 'string'
                WHEN c.data_type IN ('date', 'datetime', 'datetime2', 'smalldatetime') THEN 'datetime'
                WHEN c.data_type IN ('bit') THEN 'boolean'
                WHEN c.data_type IN ('binary', 'varbinary', 'image') THEN 'binary'
                WHEN c.data_type IN ('uniqueidentifier') THEN 'uuid'
                ELSE 'other'
            END as type_family,
            COUNT(DISTINCT c.table_name) as table_usage_count
        FROM INFORMATION_SCHEMA.COLUMNS c
        INNER JOIN INFORMATION_SCHEMA.TABLES t
            ON c.table_name = t.table_name
            AND c.table_schema = t.table_schema
        WHERE c.table_schema = 'ags'
            AND t.table_type = 'BASE TABLE'
        GROUP BY c.data_type
        ORDER BY COUNT(DISTINCT c.table_name) DESC, c.data_type
        """
        
        cursor.execute(query)
        rows = cursor.fetchall()
        
        base_types = []
        for row in rows:
            base_type_name, type_category, type_family, table_usage_count = row
            description = f"Базовый тип данных MS SQL Server: {base_type_name}"
            
            base_types.append({
                'base_type_name': base_type_name,
                'type_category': type_category,
                'type_family': type_family,
                'is_user_defined': False,
                'description': description,
                'table_usage_count': table_usage_count
            })
        
        return base_types
        
    except Exception as e:
        print(f"Ошибка при получении данных из MS SQL: {e}")
        return None
    
    finally:
        if 'conn' in locals():
            conn.close()

def insert_base_types_to_postgres(base_types):
    """Вставить базовые типы в PostgreSQL"""
    
    try:
        conn = psycopg2.connect(
            host='localhost',
            port=5432,
            database='Fish_Eye',
            user='postgres',
            password='postgres'
        )
        
        cursor = conn.cursor()
        
        # Очистить таблицу перед вставкой
        cursor.execute("DELETE FROM mcl.mssql_base_types")
        print("Таблица mcl.mssql_base_types очищена")
        
        # Вставить новые данные
        insert_query = """
        INSERT INTO mcl.mssql_base_types 
        (base_type_name, type_category, type_family, is_user_defined, description)
        VALUES (%s, %s, %s, %s, %s)
        """
        
        inserted_count = 0
        for base_type in base_types:
            cursor.execute(insert_query, (
                base_type['base_type_name'],
                base_type['type_category'],
                base_type['type_family'],
                base_type['is_user_defined'],
                base_type['description']
            ))
            inserted_count += 1
            print(f"Вставлен тип {base_type['base_type_name']}")
        
        # Подтвердить изменения
        conn.commit()
        print(f"\nУспешно вставлено {inserted_count} базовых типов")
        
        # Проверить результат
        cursor.execute("SELECT COUNT(*) FROM mcl.mssql_base_types")
        total_count = cursor.fetchone()[0]
        print(f"Всего записей в таблице: {total_count}")
        
        return True
        
    except Exception as e:
        print(f"Ошибка при вставке в PostgreSQL: {e}")
        if 'conn' in locals():
            conn.rollback()
        return False
    
    finally:
        if 'conn' in locals():
            conn.close()

def main():
    """Основная функция"""
    
    print("Получение базовых типов из MS SQL Server...")
    base_types = get_base_types_from_mssql()
    
    if not base_types:
        print("Не удалось получить данные из MS SQL Server")
        return
    
    print(f"Получено {len(base_types)} базовых типов")
    
    print("\nВставка базовых типов в PostgreSQL...")
    success = insert_base_types_to_postgres(base_types)
    
    if success:
        print("\n✅ Заполнение таблицы базовых типов завершено успешно!")
    else:
        print("\n❌ Ошибка при заполнении таблицы")

if __name__ == "__main__":
    main()