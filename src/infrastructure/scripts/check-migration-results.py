#!/usr/bin/env python3
"""
Проверка результатов миграции
"""

import psycopg2
import pymssql

def check_migration_results():
    print("📊 ПРОВЕРКА РЕЗУЛЬТАТОВ МИГРАЦИИ")
    print("=" * 50)
    
    # Подключение к PostgreSQL
    pg_conn = psycopg2.connect('postgresql://postgres:postgres@localhost:5432/vuege')
    pg_cursor = pg_conn.cursor()
    
    # Подключение к SQL Server
    mssql_conn = pymssql.connect(
        server='localhost',
        port=1433,
        user='sa',
        password='Vuege2024!',
        database='Fish_Eye'
    )
    mssql_cursor = mssql_conn.cursor()
    
    # Таблицы для проверки
    tables = ['cn', 'org', 'cst', 'cn_PrDocP']
    
    print("📋 Сравнение количества записей:")
    print("-" * 50)
    
    total_pg = 0
    total_mssql = 0
    
    for table in tables:
        try:
            # PostgreSQL
            pg_cursor.execute(f"SELECT COUNT(*) FROM ags.{table}")
            pg_count = pg_cursor.fetchone()[0]
            
            # SQL Server
            mssql_cursor.execute(f"SELECT COUNT(*) FROM ags.{table}")
            mssql_count = mssql_cursor.fetchone()[0]
            
            status = "✅" if pg_count == mssql_count else "⚠️"
            print(f"{status} {table}:")
            print(f"   PostgreSQL: {pg_count:,} записей")
            print(f"   SQL Server: {mssql_count:,} записей")
            print(f"   Разница: {abs(pg_count - mssql_count):,}")
            print()
            
            total_pg += pg_count
            total_mssql += mssql_count
            
        except Exception as e:
            print(f"❌ {table}: Ошибка - {e}")
            print()
    
    print("=" * 50)
    print(f"📈 ИТОГО:")
    print(f"   PostgreSQL: {total_pg:,} записей")
    print(f"   SQL Server: {total_mssql:,} записей")
    print(f"   Разница: {abs(total_pg - total_mssql):,}")
    
    # Проверка структуры таблиц
    print("\n🔍 СТРУКТУРА ТАБЛИЦ:")
    print("-" * 50)
    
    for table in tables:
        try:
            print(f"\n📋 Таблица: {table}")
            
            # PostgreSQL структура
            pg_cursor.execute(f"""
                SELECT column_name, data_type, is_nullable
                FROM information_schema.columns
                WHERE table_schema = 'ags' AND table_name = '{table}'
                ORDER BY ordinal_position
            """)
            
            pg_columns = pg_cursor.fetchall()
            print("   PostgreSQL:")
            for col in pg_columns[:5]:  # Показываем первые 5 колонок
                print(f"     • {col[0]}: {col[1]} ({col[2]})")
            
            if len(pg_columns) > 5:
                print(f"     ... и еще {len(pg_columns) - 5} колонок")
            
        except Exception as e:
            print(f"   ❌ Ошибка получения структуры: {e}")
    
    pg_conn.close()
    mssql_conn.close()
    
    print("\n✅ Проверка завершена!")

if __name__ == "__main__":
    check_migration_results()