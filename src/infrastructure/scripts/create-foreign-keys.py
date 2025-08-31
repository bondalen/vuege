#!/usr/bin/env python3
"""
Скрипт для создания внешних ключей в PostgreSQL
Создает внешние ключи на основе существующих первичных ключей
"""

import psycopg2
import psycopg2.extras
import logging
from datetime import datetime
import json
import os

# Настройки подключения к PostgreSQL
PG_HOST = 'localhost'
PG_DB = 'vuege'
PG_USER = 'postgres'
PG_PASSWORD = 'testpass'
PG_SCHEMA = 'ags'

# Настройка логирования
log_dir = '/home/alex/vuege/docs/infrastructure/logs'
os.makedirs(log_dir, exist_ok=True)
log_file = f'{log_dir}/create-foreign-keys-{datetime.now().strftime("%Y%m%d_%H%M%S")}.log'

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(log_file, encoding='utf-8'),
        logging.StreamHandler()
    ]
)

def connect_to_postgres():
    """Подключение к PostgreSQL"""
    try:
        conn = psycopg2.connect(
            host=PG_HOST,
            database=PG_DB,
            user=PG_USER,
            password=PG_PASSWORD
        )
        conn.autocommit = False
        return conn
    except Exception as e:
        logging.error(f"Ошибка подключения к PostgreSQL: {e}")
        return None

def get_tables_with_pk(conn):
    """Получение списка таблиц с первичными ключами"""
    cursor = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
    
    try:
        cursor.execute("""
            SELECT 
                tc.table_name,
                kcu.column_name as pk_column,
                c.data_type
            FROM information_schema.table_constraints tc
            JOIN information_schema.key_column_usage kcu 
                ON tc.constraint_name = kcu.constraint_name
            JOIN information_schema.columns c 
                ON kcu.table_name = c.table_name 
                AND kcu.column_name = c.column_name
                AND c.table_schema = tc.table_schema
            WHERE tc.constraint_type = 'PRIMARY KEY'
                AND tc.table_schema = %s
            ORDER BY tc.table_name
        """, (PG_SCHEMA,))
        
        tables = cursor.fetchall()
        return [dict(table) for table in tables]
        
    except Exception as e:
        logging.error(f"Ошибка получения таблиц с PK: {e}")
        return []
    finally:
        cursor.close()

def get_potential_foreign_keys(conn):
    """Поиск потенциальных внешних ключей"""
    cursor = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
    
    try:
        # Получаем все колонки всех таблиц
        cursor.execute("""
            SELECT 
                t.table_name,
                c.column_name,
                c.data_type,
                c.character_maximum_length
            FROM information_schema.tables t
            JOIN information_schema.columns c 
                ON t.table_name = c.table_name 
                AND t.table_schema = c.table_schema
            WHERE t.table_schema = %s
                AND t.table_type = 'BASE TABLE'
            ORDER BY t.table_name, c.ordinal_position
        """, (PG_SCHEMA,))
        
        all_columns = cursor.fetchall()
        
        # Получаем таблицы с первичными ключами
        tables_with_pk = get_tables_with_pk(conn)
        pk_columns = {table['table_name']: table['pk_column'] for table in tables_with_pk}
        
        potential_fks = []
        
        # Анализируем каждую таблицу
        for table_name in set([col['table_name'] for col in all_columns]):
            table_columns = [col for col in all_columns if col['table_name'] == table_name]
            
            # Пропускаем таблицы, которые уже имеют первичный ключ
            if table_name in pk_columns:
                continue
            
            for column in table_columns:
                col_name = column['column_name']
                col_type = column['data_type']
                
                # Ищем таблицы с первичными ключами, которые могут быть связаны
                for pk_table, pk_column in pk_columns.items():
                    # Проверяем соответствие типов данных
                    pk_table_info = next((t for t in tables_with_pk if t['table_name'] == pk_table), None)
                    if not pk_table_info:
                        continue
                    
                    pk_type = pk_table_info['data_type']
                    
                    # Проверяем соответствие типов
                    if col_type == pk_type:
                        # Проверяем, есть ли данные в колонке
                        cursor.execute(f"""
                            SELECT COUNT(*) as total, COUNT(DISTINCT "{col_name}") as unique_count
                            FROM {PG_SCHEMA}."{table_name}"
                            WHERE "{col_name}" IS NOT NULL
                        """)
                        
                        result = cursor.fetchone()
                        if result and result['total'] > 0:
                            potential_fks.append({
                                'table_name': table_name,
                                'column_name': col_name,
                                'column_type': col_type,
                                'referenced_table': pk_table,
                                'referenced_column': pk_column,
                                'referenced_type': pk_type,
                                'total_records': result['total'],
                                'unique_values': result['unique_count']
                            })
        
        return potential_fks
        
    except Exception as e:
        logging.error(f"Ошибка поиска потенциальных FK: {e}")
        return []
    finally:
        cursor.close()

def create_foreign_key(conn, fk_info):
    """Создание внешнего ключа"""
    cursor = conn.cursor()
    
    try:
        table_name = fk_info['table_name']
        column_name = fk_info['column_name']
        referenced_table = fk_info['referenced_table']
        referenced_column = fk_info['referenced_column']
        
        # Проверяем, что внешний ключ еще не существует
        cursor.execute("""
            SELECT COUNT(*) 
            FROM information_schema.table_constraints tc
            JOIN information_schema.key_column_usage kcu 
                ON tc.constraint_name = kcu.constraint_name
            WHERE tc.table_schema = %s
                AND tc.table_name = %s
                AND kcu.column_name = %s
                AND tc.constraint_type = 'FOREIGN KEY'
        """, (PG_SCHEMA, table_name, column_name))
        
        if cursor.fetchone()[0] > 0:
            return {
                'table_name': table_name,
                'column_name': column_name,
                'referenced_table': referenced_table,
                'referenced_column': referenced_column,
                'status': 'already_exists',
                'error': 'Foreign key already exists'
            }
        
        # Проверяем целостность данных
        cursor.execute(f"""
            SELECT COUNT(*) 
            FROM {PG_SCHEMA}."{table_name}" t1
            LEFT JOIN {PG_SCHEMA}."{referenced_table}" t2 
                ON t1."{column_name}" = t2."{referenced_column}"
            WHERE t1."{column_name}" IS NOT NULL 
                AND t2."{referenced_column}" IS NULL
        """)
        
        orphaned_records = cursor.fetchone()[0]
        if orphaned_records > 0:
            return {
                'table_name': table_name,
                'column_name': column_name,
                'referenced_table': referenced_table,
                'referenced_column': referenced_column,
                'status': 'data_integrity_error',
                'error': f'{orphaned_records} orphaned records found'
            }
        
        # Создаем внешний ключ
        constraint_name = f"fk_{table_name}_{column_name}_{referenced_table}"
        cursor.execute(f"""
            ALTER TABLE {PG_SCHEMA}."{table_name}" 
            ADD CONSTRAINT {constraint_name} 
            FOREIGN KEY ("{column_name}") 
            REFERENCES {PG_SCHEMA}."{referenced_table}" ("{referenced_column}")
        """)
        
        logging.info(f"✅ Создан внешний ключ: {table_name}.{column_name} → {referenced_table}.{referenced_column}")
        
        return {
            'table_name': table_name,
            'column_name': column_name,
            'referenced_table': referenced_table,
            'referenced_column': referenced_column,
            'status': 'success'
        }
        
    except Exception as e:
        logging.error(f"❌ Ошибка создания FK {table_name}.{column_name}: {e}")
        return {
            'table_name': table_name,
            'column_name': column_name,
            'referenced_table': referenced_table,
            'referenced_column': referenced_column,
            'status': 'error',
            'error': str(e)
        }

def main():
    """Основная функция"""
    logging.info("🚀 Начало создания внешних ключей")
    
    conn = connect_to_postgres()
    if not conn:
        return
    
    try:
        # Получаем таблицы с первичными ключами
        tables_with_pk = get_tables_with_pk(conn)
        logging.info(f"📋 Найдено {len(tables_with_pk)} таблиц с первичными ключами")
        
        # Ищем потенциальные внешние ключи
        logging.info("🔍 Поиск потенциальных внешних ключей...")
        potential_fks = get_potential_foreign_keys(conn)
        
        logging.info(f"🎯 Найдено {len(potential_fks)} потенциальных внешних ключей")
        
        if not potential_fks:
            logging.info("❌ Потенциальные внешние ключи не найдены")
            return
        
        # Сортируем по количеству записей (от большего к меньшему)
        potential_fks.sort(key=lambda x: x['total_records'], reverse=True)
        
        results = []
        successful_creations = 0
        
        # Создаем внешние ключи
        for fk_info in potential_fks:
            logging.info(f"🔗 Создание FK: {fk_info['table_name']}.{fk_info['column_name']} → {fk_info['referenced_table']}.{fk_info['referenced_column']}")
            
            result = create_foreign_key(conn, fk_info)
            results.append(result)
            
            if result['status'] == 'success':
                successful_creations += 1
                conn.commit()
                logging.info(f"  ✅ Внешний ключ создан успешно")
            else:
                conn.rollback()
                logging.info(f"  ❌ Ошибка: {result.get('error', 'Unknown error')}")
        
        # Создаем отчет
        report = {
            'timestamp': datetime.now().isoformat(),
            'total_potential_fks': len(potential_fks),
            'successful_creations': successful_creations,
            'failed_creations': len([r for r in results if r['status'] == 'error']),
            'already_exists': len([r for r in results if r['status'] == 'already_exists']),
            'data_integrity_errors': len([r for r in results if r['status'] == 'data_integrity_error']),
            'results': results
        }
        
        # Сохраняем отчет
        report_dir = '/home/alex/vuege/docs/infrastructure/reports'
        os.makedirs(report_dir, exist_ok=True)
        report_file = f'{report_dir}/foreign-keys-creation-report-{datetime.now().strftime("%Y%m%d_%H%M%S")}.json'
        
        with open(report_file, 'w', encoding='utf-8') as f:
            json.dump(report, f, ensure_ascii=False, indent=2)
        
        logging.info(f"📄 Отчет сохранен: {report_file}")
        
        # Итоговая статистика
        failed = len([r for r in results if r['status'] == 'error'])
        already_exists = len([r for r in results if r['status'] == 'already_exists'])
        data_integrity_errors = len([r for r in results if r['status'] == 'data_integrity_error'])
        
        logging.info(f"🎉 Создание внешних ключей завершено!")
        logging.info(f"✅ Успешно создано: {successful_creations}/{len(potential_fks)} внешних ключей")
        logging.info(f"❌ Ошибки: {failed}")
        logging.info(f"⚠️ Уже существуют: {already_exists}")
        logging.info(f"🔍 Ошибки целостности данных: {data_integrity_errors}")
        
    except Exception as e:
        logging.error(f"❌ Критическая ошибка: {e}")
        conn.rollback()
    finally:
        conn.close()

if __name__ == "__main__":
    main()