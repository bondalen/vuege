#!/usr/bin/env python3
"""
Тестирование данных в SQL Server
"""

import pymssql

def test_mssql_data():
    try:
        # Подключение к SQL Server
        conn = pymssql.connect(
            server='localhost', 
            port=1433, 
            user='sa', 
            password='Vuege2024!', 
            database='Fish_Eye'
        )
        
        cursor = conn.cursor()
        
        # Основные таблицы для миграции
        tables = ['cn', 'org', 'cst', 'cn_PrDoc', 'cn_PrDocP', 'invNum']
        
        print('📊 Количество записей в основных таблицах:')
        print('=' * 50)
        
        total_records = 0
        for table in tables:
            try:
                cursor.execute(f'SELECT COUNT(*) FROM ags.{table}')
                result = cursor.fetchone()
                count = result[0] if result else 0
                print(f'   • {table}: {count:,} записей')
                total_records += count
            except Exception as e:
                print(f'   • {table}: Ошибка - {e}')
        
        print('=' * 50)
        print(f'📈 Общее количество записей: {total_records:,}')
        
        # Проверка структуры таблицы cn
        print('\n🔍 Структура таблицы cn:')
        print('=' * 50)
        try:
            cursor.execute("""
                SELECT column_name, data_type, is_nullable, column_default
                FROM information_schema.columns
                WHERE table_schema = 'ags' AND table_name = 'cn'
                ORDER BY ordinal_position
            """)
            
            columns = cursor.fetchall()
            for col in columns:
                print(f'   • {col[0]}: {col[1]} {"NULL" if col[2] == "YES" else "NOT NULL"}')
                
        except Exception as e:
            print(f'   Ошибка получения структуры: {e}')
        
        conn.close()
        print('\n✅ Тестирование завершено успешно!')
        
    except Exception as e:
        print(f'❌ Ошибка подключения: {e}')

if __name__ == "__main__":
    test_mssql_data()