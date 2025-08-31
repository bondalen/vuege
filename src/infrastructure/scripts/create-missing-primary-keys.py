#!/usr/bin/env python3
"""
Скрипт для создания первичных ключей в таблицах, где они отсутствуют
Использует анализ структуры таблиц для определения потенциальных PK
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
log_file = f'{log_dir}/create-missing-primary-keys-{datetime.now().strftime("%Y%m%d_%H%M%S")}.log'

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

def get_tables_without_pk(conn):
    """Получение списка таблиц без первичных ключей"""
    cursor = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
    
    try:
        cursor.execute("""
            SELECT t.table_name
            FROM information_schema.tables t
            LEFT JOIN information_schema.table_constraints tc 
                ON t.table_name = tc.table_name 
                AND tc.constraint_type = 'PRIMARY KEY'
                AND tc.table_schema = t.table_schema
            WHERE t.table_schema = %s
                AND t.table_type = 'BASE TABLE'
                AND tc.constraint_name IS NULL
            ORDER BY t.table_name
        """, (PG_SCHEMA,))
        
        tables = [row['table_name'] for row in cursor.fetchall()]
        return tables
        
    except Exception as e:
        logging.error(f"Ошибка получения списка таблиц: {e}")
        return []
    finally:
        cursor.close()

def get_table_columns(conn, table_name):
    """Получение списка колонок таблицы"""
    cursor = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
    
    try:
        cursor.execute("""
            SELECT 
                column_name,
                data_type,
                is_nullable,
                ordinal_position
            FROM information_schema.columns
            WHERE table_schema = %s AND table_name = %s
            ORDER BY ordinal_position
        """, (PG_SCHEMA, table_name))
        
        columns = cursor.fetchall()
        return [dict(col) for col in columns]
        
    except Exception as e:
        logging.error(f"Ошибка получения колонок таблицы {table_name}: {e}")
        return []
    finally:
        cursor.close()

def check_column_uniqueness(conn, table_name, column_name):
    """Проверка уникальности колонки"""
    cursor = conn.cursor()
    
    try:
        cursor.execute(f"""
            SELECT COUNT(*) as total, COUNT(DISTINCT "{column_name}") as unique_count
            FROM {PG_SCHEMA}."{table_name}"
        """)
        
        result = cursor.fetchone()
        total_records = result[0]
        unique_records = result[1]
        
        if total_records == 0:
            return True, 100.0  # Пустая таблица - считаем уникальной
        
        uniqueness_percentage = (unique_records / total_records) * 100
        is_unique = total_records == unique_records
        
        return is_unique, uniqueness_percentage
        
    except Exception as e:
        logging.error(f"Ошибка проверки уникальности колонки {column_name} в таблице {table_name}: {e}")
        return False, 0.0
    finally:
        cursor.close()

def find_potential_pk_columns(conn, table_name):
    """Поиск потенциальных колонок для первичного ключа"""
    columns = get_table_columns(conn, table_name)
    
    if not columns:
        return []
    
    potential_pk_columns = []
    
    # Приоритетные типы данных для PK
    pk_priority_types = ['integer', 'bigint', 'smallint', 'uuid', 'character varying', 'text']
    
    for column in columns:
        col_name = column['column_name']
        data_type = column['data_type']
        is_nullable = column['is_nullable'] == 'YES'
        
        # Пропускаем nullable колонки
        if is_nullable:
            continue
        
        # Проверяем уникальность
        is_unique, uniqueness_percentage = check_column_uniqueness(conn, table_name, col_name)
        
        if is_unique:
            priority_score = pk_priority_types.index(data_type) if data_type in pk_priority_types else 999
            potential_pk_columns.append({
                'column_name': col_name,
                'data_type': data_type,
                'uniqueness_percentage': uniqueness_percentage,
                'priority_score': priority_score
            })
    
    # Сортируем по приоритету
    potential_pk_columns.sort(key=lambda x: x['priority_score'])
    
    return potential_pk_columns

def create_primary_key(conn, table_name, pk_columns):
    """Создание первичного ключа для таблицы"""
    cursor = conn.cursor()
    
    try:
        # Проверяем, что все колонки существуют
        cursor.execute(f"""
            SELECT column_name 
            FROM information_schema.columns 
            WHERE table_schema = %s AND table_name = %s
        """, (PG_SCHEMA, table_name))
        
        existing_columns = [row[0] for row in cursor.fetchall()]
        
        # Проверяем, что все колонки PK существуют
        missing_columns = [col for col in pk_columns if col not in existing_columns]
        if missing_columns:
            logging.warning(f"⚠️ Таблица {table_name}: отсутствуют колонки {missing_columns}")
            return {
                'table_name': table_name,
                'pk_columns': pk_columns,
                'status': 'error',
                'error': f'Missing columns: {missing_columns}'
            }
        
        # Проверяем уникальность данных
        pk_columns_str = ', '.join([f'"{col}"' for col in pk_columns])
        cursor.execute(f"""
            SELECT COUNT(*) as total, COUNT(DISTINCT ({pk_columns_str})) as unique_count
            FROM {PG_SCHEMA}."{table_name}"
        """)
        
        result = cursor.fetchone()
        total_records = result[0]
        unique_records = result[1]
        
        if total_records != unique_records:
            logging.warning(f"⚠️ Таблица {table_name}: дубли в PK колонках ({total_records} записей, {unique_records} уникальных)")
            return {
                'table_name': table_name,
                'pk_columns': pk_columns,
                'status': 'error',
                'error': f'Duplicate data: {total_records} total, {unique_records} unique'
            }
        
        # Создаем первичный ключ
        constraint_name = f"pk_{table_name}"
        cursor.execute(f"""
            ALTER TABLE {PG_SCHEMA}."{table_name}" 
            ADD CONSTRAINT {constraint_name} PRIMARY KEY ({pk_columns_str})
        """)
        
        logging.info(f"✅ Создан первичный ключ для таблицы {table_name}: {pk_columns_str}")
        
        return {
            'table_name': table_name,
            'pk_columns': pk_columns,
            'total_records': total_records,
            'status': 'success'
        }
        
    except Exception as e:
        logging.error(f"❌ Ошибка создания PK для таблицы {table_name}: {e}")
        return {
            'table_name': table_name,
            'pk_columns': pk_columns,
            'status': 'error',
            'error': str(e)
        }

def main():
    """Основная функция"""
    logging.info("🚀 Начало создания первичных ключей")
    
    conn = connect_to_postgres()
    if not conn:
        return
    
    try:
        # Получаем таблицы без первичных ключей
        tables_without_pk = get_tables_without_pk(conn)
        
        logging.info(f"📋 Найдено {len(tables_without_pk)} таблиц без первичных ключей")
        
        results = []
        successful_creations = 0
        
        # Обрабатываем каждую таблицу
        for table_name in tables_without_pk:
            logging.info(f"🔍 Анализ таблицы {table_name}...")
            
            # Ищем потенциальные колонки для PK
            potential_pk_columns = find_potential_pk_columns(conn, table_name)
            
            if not potential_pk_columns:
                logging.info(f"  ❌ Не найдены подходящие колонки для PK в таблице {table_name}")
                results.append({
                    'table_name': table_name,
                    'pk_columns': [],
                    'status': 'no_candidates',
                    'error': 'No suitable columns found'
                })
                continue
            
            # Берем первую (лучшую) колонку для PK
            best_column = potential_pk_columns[0]
            pk_column = best_column['column_name']
            
            logging.info(f"  🎯 Выбрана колонка {pk_column} для PK (тип: {best_column['data_type']}, уникальность: {best_column['uniqueness_percentage']:.1f}%)")
            
            # Создаем первичный ключ
            result = create_primary_key(conn, table_name, [pk_column])
            results.append(result)
            
            if result['status'] == 'success':
                successful_creations += 1
                conn.commit()
                logging.info(f"  ✅ Первичный ключ создан успешно")
            else:
                conn.rollback()
                logging.info(f"  ❌ Ошибка создания первичного ключа: {result.get('error', 'Unknown error')}")
        
        # Создаем отчет
        report = {
            'timestamp': datetime.now().isoformat(),
            'total_tables_processed': len(results),
            'successful_creations': successful_creations,
            'failed_creations': len([r for r in results if r['status'] == 'error']),
            'no_candidates': len([r for r in results if r['status'] == 'no_candidates']),
            'results': results
        }
        
        # Сохраняем отчет
        report_dir = '/home/alex/vuege/docs/infrastructure/reports'
        os.makedirs(report_dir, exist_ok=True)
        report_file = f'{report_dir}/missing-primary-keys-creation-report-{datetime.now().strftime("%Y%m%d_%H%M%S")}.json'
        
        with open(report_file, 'w', encoding='utf-8') as f:
            json.dump(report, f, ensure_ascii=False, indent=2)
        
        logging.info(f"📄 Отчет сохранен: {report_file}")
        
        # Итоговая статистика
        failed = len([r for r in results if r['status'] == 'error'])
        no_candidates = len([r for r in results if r['status'] == 'no_candidates'])
        
        logging.info(f"🎉 Создание первичных ключей завершено!")
        logging.info(f"✅ Успешно создано: {successful_creations}/{len(results)} первичных ключей")
        logging.info(f"❌ Ошибки: {failed}")
        logging.info(f"⚠️ Нет кандидатов: {no_candidates}")
        
        if successful_creations > 0:
            logging.info("🔄 Теперь можно создать внешние ключи")
        
    except Exception as e:
        logging.error(f"❌ Критическая ошибка: {e}")
        conn.rollback()
    finally:
        conn.close()

if __name__ == "__main__":
    main()