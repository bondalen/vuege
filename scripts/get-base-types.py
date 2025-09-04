#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Скрипт для получения базовых типов данных MS SQL Server
"""

import pymssql

def get_base_types():
    """Получить базовые типы данных из MS SQL Server"""
    
    try:
        # Подключение к MS SQL Server
        conn = pymssql.connect(
            server='localhost',
            port=1433,
            user='sa',
            password='Vuege2024!',
            database='Fish_Eye'
        )
        
        cursor = conn.cursor()
        
        # Запрос для получения базовых типов
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
        
        print("Полученные базовые типы:")
        print("=" * 80)
        
        for i, row in enumerate(rows, 1):
            base_type_name, type_category, type_family, table_usage_count = row
            print(f"{i:2d}. {base_type_name:15} | {type_category:10} | {type_family:10} | {table_usage_count:3d} таблиц")
        
        print("=" * 80)
        print(f"Всего типов: {len(rows)}")
        
        # Подготовка данных для вставки в PostgreSQL
        insert_data = []
        for row in rows:
            base_type_name, type_category, type_family, table_usage_count = row
            description = f"Базовый тип данных MS SQL Server: {base_type_name}"
            
            insert_data.append({
                'base_type_name': base_type_name,
                'type_category': type_category,
                'type_family': type_family,
                'is_user_defined': False,
                'description': description,
                'table_usage_count': table_usage_count
            })
        
        return insert_data
        
    except Exception as e:
        print(f"Ошибка: {e}")
        return None
    
    finally:
        if 'conn' in locals():
            conn.close()

if __name__ == "__main__":
    base_types = get_base_types()
    if base_types:
        print("\nДанные готовы для вставки в PostgreSQL!")