#!/usr/bin/env python3
"""
Проверка прогресса миграции схемы ags
"""

import psycopg2
import pymssql
from datetime import datetime

def check_migration_progress():
    print("📊 ПРОВЕРКА ПРОГРЕССА МИГРАЦИИ СХЕМЫ AGS")
    print("=" * 60)
    
    try:
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
        
        # Получение списка таблиц из SQL Server
        mssql_cursor.execute("""
            SELECT table_name 
            FROM information_schema.tables 
            WHERE table_schema = 'ags' 
            ORDER BY table_name
        """)
        mssql_tables = [row[0] for row in mssql_cursor.fetchall()]
        
        # Получение списка таблиц из PostgreSQL
        pg_cursor.execute("""
            SELECT table_name 
            FROM information_schema.tables 
            WHERE table_schema = 'ags' 
            ORDER BY table_name
        """)
        pg_tables = [row[0] for row in pg_cursor.fetchall()]
        
        print(f"📋 Всего таблиц в SQL Server: {len(mssql_tables)}")
        print(f"📋 Мигрировано в PostgreSQL: {len(pg_tables)}")
        print(f"📈 Прогресс: {len(pg_tables)}/{len(mssql_tables)} ({len(pg_tables)/len(mssql_tables)*100:.1f}%)")
        
        # Проверка количества записей в ключевых таблицах
        key_tables = ['cn', 'org', 'cst', 'cn_PrDoc', 'cn_PrDocP', 'invNum', 'inv', 'cn_inv_doc']
        
        print("\n📊 Количество записей в ключевых таблицах:")
        print("-" * 60)
        
        for table in key_tables:
            if table in mssql_tables:
                try:
                    # SQL Server
                    mssql_cursor.execute(f"SELECT COUNT(*) FROM ags.{table}")
                    mssql_count = mssql_cursor.fetchone()[0]
                    
                    # PostgreSQL
                    if table in pg_tables:
                        pg_cursor.execute(f"SELECT COUNT(*) FROM ags.{table}")
                        pg_count = pg_cursor.fetchone()[0]
                        status = "✅" if mssql_count == pg_count else "⚠️"
                        print(f"{status} {table}: SQL Server {mssql_count:,} → PostgreSQL {pg_count:,}")
                    else:
                        print(f"❌ {table}: SQL Server {mssql_count:,} → Не мигрирована")
                        
                except Exception as e:
                    print(f"❌ {table}: Ошибка проверки - {e}")
        
        # Последние мигрированные таблицы
        print(f"\n📋 Последние мигрированные таблицы:")
        print("-" * 60)
        for table in pg_tables[-10:]:
            print(f"   • {table}")
        
        # Ожидающие миграции таблицы
        remaining_tables = [t for t in mssql_tables if t not in pg_tables]
        print(f"\n⏳ Ожидающие миграции таблицы (первые 10):")
        print("-" * 60)
        for table in remaining_tables[:10]:
            print(f"   • {table}")
        if len(remaining_tables) > 10:
            print(f"   ... и еще {len(remaining_tables) - 10} таблиц")
        
        print(f"\n🎯 Осталось мигрировать: {len(remaining_tables)} таблиц")
        
    except Exception as e:
        print(f"❌ Ошибка проверки прогресса: {e}")
    finally:
        if 'pg_conn' in locals():
            pg_conn.close()
        if 'mssql_conn' in locals():
            mssql_conn.close()

if __name__ == "__main__":
    check_migration_progress()