#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Скрипт для получения производных типов данных MS SQL Server
"""

import pymssql

def get_derived_types_from_mssql():
    """Получить производные типы данных из MS SQL Server"""
    
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
        SELECT 
            c.data_type as base_type_name,
            c.character_maximum_length as length_value,
            c.numeric_precision as precision_value,
            c.numeric_scale as scale_value,
            c.is_nullable,
            CASE 
                WHEN c.character_maximum_length = -1 THEN 'max'
                WHEN c.character_maximum_length IS NULL THEN NULL
                ELSE CAST(c.character_maximum_length AS varchar)
            END as max_value,
            CASE 
                WHEN c.character_maximum_length = -1 THEN 1
                ELSE 0
            END as is_max_length,
            CASE 
                WHEN c.data_type IN ('varchar', 'nvarchar', 'char', 'nchar', 'binary', 'varbinary') THEN 1
                ELSE 0
            END as is_variable_length,
            c.data_type as parameter_value,
            c.collation_name,
            CASE 
                WHEN c.data_type IN ('varchar', 'nvarchar', 'char', 'nchar') AND c.character_maximum_length = -1 
                    THEN c.data_type + '(max)'
                WHEN c.data_type IN ('varchar', 'nvarchar', 'char', 'nchar') AND c.character_maximum_length IS NOT NULL
                    THEN c.data_type + '(' + CAST(c.character_maximum_length AS varchar) + ')'
                WHEN c.data_type IN ('decimal', 'numeric') AND c.numeric_precision IS NOT NULL AND c.numeric_scale IS NOT NULL
                    THEN c.data_type + '(' + CAST(c.numeric_precision AS varchar) + ',' + CAST(c.numeric_scale AS varchar) + ')'
                WHEN c.data_type IN ('decimal', 'numeric') AND c.numeric_precision IS NOT NULL
                    THEN c.data_type + '(' + CAST(c.numeric_precision AS varchar) + ')'
                WHEN c.data_type IN ('float') AND c.numeric_precision IS NOT NULL
                    THEN c.data_type + '(' + CAST(c.numeric_precision AS varchar) + ')'
                ELSE c.data_type
            END as derived_type_description,
            COUNT(*) as usage_count
        FROM INFORMATION_SCHEMA.COLUMNS c
        INNER JOIN INFORMATION_SCHEMA.TABLES t
            ON c.table_name = t.table_name
            AND c.table_schema = t.table_schema
        WHERE c.table_schema = 'ags'
            AND t.table_type = 'BASE TABLE'
        GROUP BY 
            c.data_type,
            c.character_maximum_length,
            c.numeric_precision,
            c.numeric_scale,
            c.is_nullable,
            c.collation_name
        ORDER BY 
            c.data_type,
            c.character_maximum_length,
            c.numeric_precision,
            c.numeric_scale,
            c.is_nullable
        """
        
        cursor.execute(query)
        rows = cursor.fetchall()
        
        print("Полученные производные типы:")
        print("=" * 100)
        
        for i, row in enumerate(rows, 1):
            (base_type_name, length_value, precision_value, scale_value, is_nullable,
             max_value, is_max_length, is_variable_length, parameter_value, collation_name,
             derived_type_description, usage_count) = row
            
            print(f"{i:2d}. {base_type_name:15} | {str(length_value):8} | {str(precision_value):8} | {str(scale_value):8} | {str(is_nullable):8} | {str(max_value):8} | {usage_count:3d} использований")
        
        print("=" * 100)
        print(f"Всего производных типов: {len(rows)}")
        
        # Подготовка данных для вставки в PostgreSQL
        derived_types = []
        for row in rows:
            (base_type_name, length_value, precision_value, scale_value, is_nullable,
             max_value, is_max_length, is_variable_length, parameter_value, collation_name,
             derived_type_description, usage_count) = row
            
            derived_types.append({
                'base_type_name': base_type_name,
                'length_value': length_value,
                'precision_value': precision_value,
                'scale_value': scale_value,
                'is_nullable': is_nullable,
                'max_value': max_value,
                'is_max_length': bool(is_max_length),
                'is_variable_length': bool(is_variable_length),
                'parameter_value': parameter_value,
                'collation_name': collation_name,
                'derived_type_description': derived_type_description,
                'usage_count': usage_count
            })
        
        return derived_types
        
    except Exception as e:
        print(f"Ошибка при получении данных из MS SQL: {e}")
        return None
    
    finally:
        if 'conn' in locals():
            conn.close()

if __name__ == "__main__":
    derived_types = get_derived_types_from_mssql()
    if derived_types:
        print("\nДанные готовы для вставки в PostgreSQL!")
        print(f"Первый тип: {derived_types[0]}")