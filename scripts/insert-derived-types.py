#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Скрипт для вставки производных типов данных в PostgreSQL
"""

import psycopg2
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

def insert_derived_types_to_postgres(derived_types):
    """Вставить производные типы в PostgreSQL"""
    
    try:
        conn = psycopg2.connect(
            host='localhost',
            port=5432,
            database='Fish_Eye',
            user='postgres',
            password='postgres'
        )
        
        cursor = conn.cursor()
        
        # Получить ID базовых типов для связи
        cursor.execute("SELECT id, base_type_name FROM mcl.mssql_base_types")
        base_types_map = {row[1]: row[0] for row in cursor.fetchall()}
        
        print(f"Найдено {len(base_types_map)} базовых типов для связи")
        
        # Очистить таблицу перед вставкой
        cursor.execute("DELETE FROM mcl.mssql_derived_types")
        print("Таблица mcl.mssql_derived_types очищена")
        
        # Вставить новые данные
        insert_query = """
        INSERT INTO mcl.mssql_derived_types 
        (task_id, is_nullable, default_precision, default_scale, max_length, 
         base_type_id, precision_value, scale_value, length_value, max_value, 
         parameter_value, is_max_length, is_variable_length, collation_name)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        """
        
        inserted_count = 0
        for derived_type in derived_types:
            base_type_name = derived_type['base_type_name']
            base_type_id = base_types_map.get(base_type_name)
            
            if base_type_id is None:
                print(f"⚠️  Базовый тип '{base_type_name}' не найден, пропускаем")
                continue
            
            # task_id = 1 (предполагаем, что это основная задача миграции)
            cursor.execute(insert_query, (
                1,  # task_id
                derived_type['is_nullable'],
                derived_type['precision_value'],
                derived_type['scale_value'],
                derived_type['length_value'],
                base_type_id,
                derived_type['precision_value'],
                derived_type['scale_value'],
                derived_type['length_value'],
                derived_type['max_value'],
                derived_type['parameter_value'],
                derived_type['is_max_length'],
                derived_type['is_variable_length'],
                derived_type['collation_name']
            ))
            inserted_count += 1
            
            if inserted_count % 10 == 0:
                print(f"Вставлено {inserted_count} типов...")
        
        # Подтвердить изменения
        conn.commit()
        print(f"\nУспешно вставлено {inserted_count} производных типов")
        
        # Проверить результат
        cursor.execute("SELECT COUNT(*) FROM mcl.mssql_derived_types")
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
    
    print("Получение производных типов из MS SQL Server...")
    derived_types = get_derived_types_from_mssql()
    
    if not derived_types:
        print("Не удалось получить данные из MS SQL Server")
        return
    
    print(f"Получено {len(derived_types)} производных типов")
    
    print("\nВставка производных типов в PostgreSQL...")
    success = insert_derived_types_to_postgres(derived_types)
    
    if success:
        print("\n✅ Заполнение таблицы производных типов завершено успешно!")
    else:
        print("\n❌ Ошибка при заполнении таблицы")

if __name__ == "__main__":
    main()