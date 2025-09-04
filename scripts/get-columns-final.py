#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Скрипт для получения информации о колонках с переименованным полем column_description
"""

import psycopg2

def get_columns_final():
    """Получить информацию о колонках с переименованным полем"""
    
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
        # Подключение к PostgreSQL
        conn = psycopg2.connect(
            host='localhost',
            user='postgres',
            password='postgres',
            database='Fish_Eye'
        )
        
        cursor = conn.cursor()
        
        print("=== ИНФОРМАЦИЯ О КОЛОНКАХ 10 ТАБЛИЦ (финальная версия) ===\n")
        
        for table in tables:
            print(f"📋 Таблица: {table}")
            print("Колонки:")
            
            # Запрос с переименованным полем column_description
            query = f"""
            SELECT 
                c.column_name,
                mbt.base_type_name,
                mdt.length_value,
                mdt.precision_value,
                mdt.scale_value,
                mdt.is_nullable,
                c.default_value,
                c.is_identity,
                c.identity_seed,
                c.identity_increment,
                c.is_computed,
                c.computed_definition,
                c.is_persisted,
                c.column_description
            FROM mcl.mssql_columns c
            JOIN mcl.mssql_tables t ON c.table_id = t.id
            JOIN mcl.mssql_derived_types mdt ON c.data_type_id = mdt.id
            JOIN mcl.mssql_base_types mbt ON mdt.base_type_id = mbt.id
            WHERE t.object_name = '{table}'
            ORDER BY c.ordinal_position
            """
            
            cursor.execute(query)
            columns = cursor.fetchall()
            
            if not columns:
                print(f"  ❌ Таблица {table} не найдена в системе контроля миграции")
                print()
                continue
            
            # Вывод первых 3 колонок для каждой таблицы
            for i, col in enumerate(columns[:3]):
                col_name = col[0]
                base_type = col[1]
                length = col[2] if col[2] else ""
                precision = col[3] if col[3] else ""
                scale = col[4] if col[4] else ""
                nullable = col[5]
                default_val = col[6] if col[6] else "NULL"
                is_identity = col[7]
                identity_seed = col[8] if col[8] else ""
                identity_increment = col[9] if col[9] else ""
                is_computed = col[10]
                computed_def = col[11] if col[11] else ""
                is_persisted = col[12]
                description = col[13] if col[13] else ""
                
                # Формирование описания типа
                if length:
                    type_desc = f"{base_type}({length})"
                elif precision:
                    if scale:
                        type_desc = f"{base_type}({precision},{scale})"
                    else:
                        type_desc = f"{base_type}({precision})"
                else:
                    type_desc = base_type
                
                print(f"  {i+1}. {col_name}: {type_desc} - Nullable: {nullable} - Default: {default_val}")
                
                # Дополнительная информация
                if is_identity:
                    print(f"     Identity: {identity_seed}/{identity_increment}")
                if is_computed:
                    print(f"     Computed: {computed_def}")
                if description:
                    print(f"     Description: {description}")
            
            print()  # Пустая строка между таблицами
        
        conn.close()
        print("✅ Данные успешно получены с переименованным полем column_description")
        
    except Exception as e:
        print(f"❌ Ошибка при получении данных: {e}")

if __name__ == "__main__":
    get_columns_final()