#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Скрипт для получения информации о колонках 10 таблиц из MS SQL Server
для сверки с данными в PostgreSQL
"""

import pymssql

def get_columns_info():
    """Получить информацию о колонках для 10 выбранных таблиц"""
    
    # Список таблиц для проверки
    tables = [
        'cnInvCmmCstN',
        'invDbtValue', 
        'ipgCh',
        'importDbt_23-0630_Test',
        'importDbt_23-0331_Test',
        'JuUnDocChngGrRel',
        'JuUnDocPrmrGr',
        'rgTaxReorDivisMerg',
        'ralpRa',
        'org'
    ]
    
    try:
        # Подключение к MS SQL Server
        conn = pymssql.connect(
            server='localhost:1433',
            user='sa',
            password='Vuege2024!',
            database='Fish_Eye'
        )
        
        cursor = conn.cursor()
        
        print("=== ИНФОРМАЦИЯ О КОЛОНКАХ 10 ТАБЛИЦ ИЗ MS SQL SERVER ===\n")
        
        for table in tables:
            print(f"📋 Таблица: {table}")
            print("Колонки:")
            
            # Получение информации о колонках
            query = f"""
            SELECT 
                COLUMN_NAME, 
                DATA_TYPE, 
                CHARACTER_MAXIMUM_LENGTH, 
                NUMERIC_PRECISION, 
                NUMERIC_SCALE, 
                IS_NULLABLE,
                COLUMN_DEFAULT
            FROM INFORMATION_SCHEMA.COLUMNS 
            WHERE TABLE_SCHEMA = 'ags' 
                AND TABLE_NAME = '{table}' 
            ORDER BY ORDINAL_POSITION
            """
            
            cursor.execute(query)
            columns = cursor.fetchall()
            
            # Вывод первых 3 колонок для каждой таблицы
            for i, col in enumerate(columns[:3]):
                col_name = col[0]
                data_type = col[1]
                length = col[2] if col[2] else ""
                precision = col[3] if col[3] else ""
                scale = col[4] if col[4] else ""
                nullable = col[5]
                default_val = col[6] if col[6] else "NULL"
                
                # Формирование описания типа
                if length:
                    type_desc = f"{data_type}({length})"
                elif precision:
                    if scale:
                        type_desc = f"{data_type}({precision},{scale})"
                    else:
                        type_desc = f"{data_type}({precision})"
                else:
                    type_desc = data_type
                
                print(f"  {i+1}. {col_name}: {type_desc} - Nullable: {nullable} - Default: {default_val}")
            
            print()  # Пустая строка между таблицами
        
        conn.close()
        print("✅ Данные успешно получены из MS SQL Server")
        
    except Exception as e:
        print(f"❌ Ошибка при получении данных: {e}")

if __name__ == "__main__":
    get_columns_info()