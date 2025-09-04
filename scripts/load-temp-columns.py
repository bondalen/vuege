#!/usr/bin/env python3
"""
Скрипт для загрузки данных о колонках MS SQL в временную таблицу mcl.temp_mssql_columns
"""

import pymssql
import psycopg2
from psycopg2.extras import RealDictCursor
import sys

def connect_mssql():
    """Подключение к MS SQL Server"""
    try:
        conn = pymssql.connect(
            server='localhost',
            port=1433,
            user='sa',
            password='Vuege2024!',
            database='Fish_Eye'
        )
        print("✅ Подключение к MS SQL Server успешно")
        return conn
    except Exception as e:
        print(f"❌ Ошибка подключения к MS SQL Server: {e}")
        return None

def connect_postgres():
    """Подключение к PostgreSQL"""
    try:
        conn = psycopg2.connect(
            host='localhost',
            port=5432,
            database='Fish_Eye',
            user='postgres',
            password='postgres'
        )
        print("✅ Подключение к PostgreSQL успешно")
        return conn
    except Exception as e:
        print(f"❌ Ошибка подключения к PostgreSQL: {e}")
        return None

def get_mssql_columns(mssql_conn):
    """Получение данных о колонках из MS SQL"""
    query = """
    SELECT 
        c.table_name,
        c.column_name,
        c.ordinal_position,
        c.column_default,
        c.data_type,
        c.character_maximum_length as length_value,
        c.numeric_precision as precision_value,
        c.numeric_scale as scale_value,
        c.is_nullable,
        c.collation_name,
        ISNULL(sc.is_identity, 0) as is_identity,
        ISNULL(ic.seed_value, 0) as identity_seed,
        ISNULL(ic.increment_value, 0) as identity_increment,
        ISNULL(sc.is_computed, 0) as is_computed,
        ISNULL(cc.definition, '') as computed_definition,
        ISNULL(cc.is_persisted, 0) as is_persisted,
        ISNULL(ep.value, '') as COLUMN_DESCRIPTION,
        COUNT(*) OVER() as total_columns,
        ROW_NUMBER() OVER(ORDER BY c.table_name, c.ordinal_position) as row_num
    FROM INFORMATION_SCHEMA.COLUMNS c
    INNER JOIN INFORMATION_SCHEMA.TABLES t
        ON c.table_name = t.table_name 
        AND c.table_schema = t.table_schema
    LEFT JOIN sys.columns sc 
        ON sc.object_id = OBJECT_ID('ags.' + c.table_name)
        AND sc.name = c.column_name
    LEFT JOIN sys.identity_columns ic 
        ON ic.object_id = OBJECT_ID('ags.' + c.table_name)
        AND ic.column_id = sc.column_id
    LEFT JOIN sys.computed_columns cc 
        ON cc.object_id = OBJECT_ID('ags.' + c.table_name)
        AND cc.column_id = sc.column_id
    LEFT JOIN sys.extended_properties ep 
        ON ep.major_id = OBJECT_ID('ags.' + c.table_name)
        AND ep.minor_id = sc.column_id
        AND ep.name = 'MS_Description'
        AND ep.class_desc = 'OBJECT_OR_COLUMN'
    WHERE c.table_schema = 'ags'
        AND t.table_type = 'BASE TABLE'
    ORDER BY c.table_name, c.ordinal_position
    """
    
    try:
        cursor = mssql_conn.cursor(as_dict=True)
        cursor.execute(query)
        columns = cursor.fetchall()
        cursor.close()
        
        print(f"✅ Получено {len(columns)} колонок из MS SQL Server")
        return columns
    except Exception as e:
        print(f"❌ Ошибка получения данных из MS SQL: {e}")
        return None

def insert_temp_columns(postgres_conn, columns):
    """Вставка данных в временную таблицу"""
    if not columns:
        return False
    
    query = """
    INSERT INTO mcl.temp_mssql_columns (
        table_name, column_name, ordinal_position, column_default,
        data_type, length_value, precision_value, scale_value,
        is_nullable, collation_name, is_identity, identity_seed,
        identity_increment, is_computed, computed_definition,
        is_persisted, column_description, table_id, data_type_id,
        total_columns, row_num
    ) VALUES (
        %(table_name)s, %(column_name)s, %(ordinal_position)s, %(column_default)s,
        %(data_type)s, %(length_value)s, %(precision_value)s, %(scale_value)s,
        %(is_nullable)s, %(collation_name)s, %(is_identity)s, %(identity_seed)s,
        %(identity_increment)s, %(is_computed)s, %(computed_definition)s,
        %(is_persisted)s, %(COLUMN_DESCRIPTION)s, %(table_id)s, %(data_type_id)s,
        %(total_columns)s, %(row_num)s
    )
    """
    
    try:
        cursor = postgres_conn.cursor()
        
        # Очищаем временную таблицу
        cursor.execute("DELETE FROM mcl.temp_mssql_columns")
        print("✅ Временная таблица очищена")
        
        # Вставляем данные
        for column in columns:
            # Инициализируем поля связей как NULL
            column['table_id'] = None
            column['data_type_id'] = None
            
            # Преобразуем boolean в integer для PostgreSQL
            if 'is_identity' in column and column['is_identity'] is not None:
                column['is_identity'] = 1 if column['is_identity'] else 0
            if 'is_computed' in column and column['is_computed'] is not None:
                column['is_computed'] = 1 if column['is_computed'] else 0
            if 'is_persisted' in column and column['is_persisted'] is not None:
                column['is_persisted'] = 1 if column['is_persisted'] else 0
            
            # Преобразуем bytea в integer для identity полей
            if 'identity_seed' in column and column['identity_seed'] is not None:
                try:
                    if isinstance(column['identity_seed'], bytes):
                        column['identity_seed'] = int.from_bytes(column['identity_seed'], byteorder='little')
                    else:
                        column['identity_seed'] = int(column['identity_seed']) if column['identity_seed'] else 0
                except:
                    column['identity_seed'] = 0
            
            if 'identity_increment' in column and column['identity_increment'] is not None:
                try:
                    if isinstance(column['identity_increment'], bytes):
                        column['identity_increment'] = int.from_bytes(column['identity_increment'], byteorder='little')
                    else:
                        column['identity_increment'] = int(column['identity_increment']) if column['identity_increment'] else 0
                except:
                    column['identity_increment'] = 0
            
            cursor.execute(query, column)
        
        postgres_conn.commit()
        cursor.close()
        
        print(f"✅ Вставлено {len(columns)} колонок в временную таблицу")
        return True
    except Exception as e:
        postgres_conn.rollback()
        print(f"❌ Ошибка вставки в PostgreSQL: {e}")
        return False

def main():
    """Основная функция"""
    print("🚀 Начало загрузки данных о колонках MS SQL в временную таблицу")
    
    # Подключения
    mssql_conn = connect_mssql()
    if not mssql_conn:
        sys.exit(1)
    
    postgres_conn = connect_postgres()
    if not postgres_conn:
        mssql_conn.close()
        sys.exit(1)
    
    try:
        # Получаем данные из MS SQL
        columns = get_mssql_columns(mssql_conn)
        if not columns:
            return
        
        # Вставляем в временную таблицу
        if insert_temp_columns(postgres_conn, columns):
            print("🎉 Загрузка завершена успешно!")
            
            # Проверяем количество записей
            cursor = postgres_conn.cursor()
            cursor.execute("SELECT COUNT(*) FROM mcl.temp_mssql_columns")
            count = cursor.fetchone()[0]
            cursor.close()
            
            print(f"📊 В временной таблице: {count} записей")
        else:
            print("❌ Загрузка не удалась")
    
    finally:
        mssql_conn.close()
        postgres_conn.close()
        print("🔌 Соединения закрыты")

if __name__ == "__main__":
    main()