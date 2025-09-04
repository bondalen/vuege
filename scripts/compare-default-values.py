#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Скрипт для сравнения значений по умолчанию между MS SQL Server и PostgreSQL
"""

import pymssql
import psycopg2

def compare_default_values():
    """Сравнить значения по умолчанию между MS SQL и PostgreSQL"""
    
    table_name = 'rgTaxReorDivisMerg'
    
    print(f"=== СРАВНЕНИЕ ЗНАЧЕНИЙ ПО УМОЛЧАНИЮ ДЛЯ ТАБЛИЦЫ {table_name} ===\n")
    
    try:
        # Подключение к MS SQL Server
        mssql_conn = pymssql.connect(
            server='localhost:1433',
            user='sa',
            password='Vuege2024!',
            database='Fish_Eye'
        )
        
        mssql_cursor = mssql_conn.cursor()
        
        # Получение данных из MS SQL
        mssql_query = f"""
        SELECT 
            COLUMN_NAME, 
            DATA_TYPE, 
            COLUMN_DEFAULT, 
            IS_NULLABLE
        FROM INFORMATION_SCHEMA.COLUMNS 
        WHERE TABLE_SCHEMA = 'ags' 
            AND TABLE_NAME = '{table_name}' 
        ORDER BY ORDINAL_POSITION
        """
        
        mssql_cursor.execute(mssql_query)
        mssql_columns = mssql_cursor.fetchall()
        
        # Подключение к PostgreSQL
        pg_conn = psycopg2.connect(
            host='localhost',
            user='postgres',
            password='postgres',
            database='Fish_Eye'
        )
        
        pg_cursor = pg_conn.cursor()
        
        # Получение данных из PostgreSQL
        pg_query = f"""
        SELECT 
            c.column_name,
            mbt.base_type_name,
            c.default_value,
            mdt.is_nullable
        FROM mcl.mssql_columns c
        JOIN mcl.mssql_tables t ON c.table_id = t.id
        JOIN mcl.mssql_derived_types mdt ON c.data_type_id = mdt.id
        JOIN mcl.mssql_base_types mbt ON mdt.base_type_id = mbt.id
        WHERE t.object_name = '{table_name}'
        ORDER BY c.ordinal_position
        """
        
        pg_cursor.execute(pg_query)
        pg_columns = pg_cursor.fetchall()
        
        # Создание словарей для сравнения
        mssql_data = {col[0]: col for col in mssql_columns}
        pg_data = {col[0]: col for col in pg_columns}
        
        print("СРАВНЕНИЕ ПО КОЛОНКАМ:\n")
        
        for col_name in mssql_data.keys():
            if col_name in pg_data:
                mssql_col = mssql_data[col_name]
                pg_col = pg_data[col_name]
                
                print(f"📋 Колонка: {col_name}")
                print(f"  MS SQL Server:")
                print(f"    Тип: {mssql_col[1]}")
                print(f"    Default: \"{mssql_col[2]}\"")
                print(f"    Nullable: {mssql_col[3]}")
                
                print(f"  PostgreSQL (mcl):")
                print(f"    Тип: {pg_col[1]}")
                print(f"    Default: \"{pg_col[2]}\"")
                print(f"    Nullable: {pg_col[3]}")
                
                # Сравнение значений по умолчанию
                mssql_default = mssql_col[2] if mssql_col[2] else "NULL"
                pg_default = pg_col[2] if pg_col[2] else "NULL"
                
                if mssql_default == "NULL" and pg_default == "NULL":
                    print(f"  ✅ Default: Оба NULL")
                elif mssql_default != "NULL" and pg_default != "NULL":
                    print(f"  ✅ Default: Оба имеют значения")
                    print(f"     MS SQL: {mssql_default}")
                    print(f"     PostgreSQL: {pg_default}")
                else:
                    print(f"  ❌ Default: НЕСООТВЕТСТВИЕ!")
                    print(f"     MS SQL: {mssql_default}")
                    print(f"     PostgreSQL: {pg_default}")
                
                print()
        
        mssql_conn.close()
        pg_conn.close()
        
        print("✅ Сравнение завершено")
        
    except Exception as e:
        print(f"❌ Ошибка при сравнении: {e}")

if __name__ == "__main__":
    compare_default_values()