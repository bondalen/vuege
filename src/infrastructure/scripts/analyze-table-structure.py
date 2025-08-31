#!/usr/bin/env python3
"""
Скрипт для анализа структуры таблиц в PostgreSQL
Получает информацию о колонках и существующих первичных ключах
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
log_file = f'{log_dir}/analyze-table-structure-{datetime.now().strftime("%Y%m%d_%H%M%S")}.log'

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

def analyze_table_structure(conn):
    """Анализ структуры всех таблиц"""
    cursor = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
    
    try:
        # Получаем список всех таблиц
        cursor.execute("""
            SELECT table_name
            FROM information_schema.tables
            WHERE table_schema = %s AND table_type = 'BASE TABLE'
            ORDER BY table_name
        """, (PG_SCHEMA,))
        
        tables = [row['table_name'] for row in cursor.fetchall()]
        logging.info(f"📋 Найдено {len(tables)} таблиц в схеме {PG_SCHEMA}")
        
        table_analysis = {}
        
        for table_name in tables:
            logging.info(f"🔍 Анализ таблицы {table_name}...")
            
            # Получаем информацию о колонках
            cursor.execute("""
                SELECT 
                    column_name,
                    data_type,
                    character_maximum_length,
                    is_nullable,
                    column_default,
                    ordinal_position
                FROM information_schema.columns
                WHERE table_schema = %s AND table_name = %s
                ORDER BY ordinal_position
            """, (PG_SCHEMA, table_name))
            
            columns = cursor.fetchall()
            
            # Получаем информацию о первичных ключах
            cursor.execute("""
                SELECT 
                    kcu.column_name,
                    tc.constraint_name
                FROM information_schema.table_constraints tc
                JOIN information_schema.key_column_usage kcu 
                    ON tc.constraint_name = kcu.constraint_name
                WHERE tc.table_schema = %s 
                    AND tc.table_name = %s
                    AND tc.constraint_type = 'PRIMARY KEY'
                ORDER BY kcu.ordinal_position
            """, (PG_SCHEMA, table_name))
            
            primary_keys = [row['column_name'] for row in cursor.fetchall()]
            
            # Получаем количество записей
            cursor.execute(f'SELECT COUNT(*) as record_count FROM {PG_SCHEMA}."{table_name}"')
            record_count = cursor.fetchone()['record_count']
            
            # Получаем информацию о внешних ключах
            cursor.execute("""
                SELECT 
                    tc.constraint_name,
                    kcu.column_name,
                    ccu.table_name AS foreign_table_name,
                    ccu.column_name AS foreign_column_name
                FROM information_schema.table_constraints tc
                JOIN information_schema.key_column_usage kcu 
                    ON tc.constraint_name = kcu.constraint_name
                JOIN information_schema.constraint_column_usage ccu 
                    ON ccu.constraint_name = tc.constraint_name
                WHERE tc.table_schema = %s 
                    AND tc.table_name = %s
                    AND tc.constraint_type = 'FOREIGN KEY'
                ORDER BY kcu.ordinal_position
            """, (PG_SCHEMA, table_name))
            
            foreign_keys = cursor.fetchall()
            
            table_analysis[table_name] = {
                'columns': [dict(col) for col in columns],
                'primary_keys': primary_keys,
                'foreign_keys': [dict(fk) for fk in foreign_keys],
                'record_count': record_count,
                'has_primary_key': len(primary_keys) > 0,
                'has_foreign_keys': len(foreign_keys) > 0
            }
            
            logging.info(f"  📊 {len(columns)} колонок, {len(primary_keys)} PK, {len(foreign_keys)} FK, {record_count} записей")
        
        return table_analysis
        
    except Exception as e:
        logging.error(f"Ошибка анализа структуры таблиц: {e}")
        return {}
    finally:
        cursor.close()

def analyze_potential_pk_columns(conn, table_analysis):
    """Анализ потенциальных колонок для первичных ключей"""
    cursor = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
    
    potential_pks = {}
    
    for table_name, analysis in table_analysis.items():
        if analysis['has_primary_key']:
            continue
            
        logging.info(f"🔍 Поиск потенциальных PK для таблицы {table_name}...")
        
        potential_columns = []
        
        for column in analysis['columns']:
            col_name = column['column_name']
            
            # Проверяем уникальность колонки
            try:
                cursor.execute(f"""
                    SELECT COUNT(*) as total, COUNT(DISTINCT "{col_name}") as unique_count
                    FROM {PG_SCHEMA}."{table_name}"
                """)
                
                result = cursor.fetchone()
                total_records = result['total']
                unique_records = result['unique_count']
                
                if total_records > 0 and total_records == unique_records:
                    potential_columns.append({
                        'column_name': col_name,
                        'data_type': column['data_type'],
                        'is_nullable': column['is_nullable'],
                        'total_records': total_records,
                        'unique_records': unique_records,
                        'uniqueness_percentage': 100.0
                    })
                    logging.info(f"  ✅ {col_name}: уникальная колонка ({total_records} записей)")
                elif total_records > 0:
                    uniqueness_percentage = (unique_records / total_records) * 100
                    if uniqueness_percentage > 95:  # Высокая уникальность
                        potential_columns.append({
                            'column_name': col_name,
                            'data_type': column['data_type'],
                            'is_nullable': column['is_nullable'],
                            'total_records': total_records,
                            'unique_records': unique_records,
                            'uniqueness_percentage': uniqueness_percentage
                        })
                        logging.info(f"  ⚠️ {col_name}: высокая уникальность ({uniqueness_percentage:.1f}%)")
                        
            except Exception as e:
                logging.warning(f"  ❌ Ошибка проверки колонки {col_name}: {e}")
        
        if potential_columns:
            potential_pks[table_name] = potential_columns
    
    cursor.close()
    return potential_pks

def main():
    """Основная функция"""
    logging.info("🚀 Начало анализа структуры таблиц")
    
    conn = connect_to_postgres()
    if not conn:
        return
    
    try:
        # Анализ структуры таблиц
        table_analysis = analyze_table_structure(conn)
        
        if not table_analysis:
            logging.error("❌ Не удалось получить анализ структуры таблиц")
            return
        
        # Анализ потенциальных первичных ключей
        potential_pks = analyze_potential_pk_columns(conn, table_analysis)
        
        # Создаем отчет
        report = {
            'timestamp': datetime.now().isoformat(),
            'schema': PG_SCHEMA,
            'total_tables': len(table_analysis),
            'tables_with_pk': len([t for t in table_analysis.values() if t['has_primary_key']]),
            'tables_without_pk': len([t for t in table_analysis.values() if not t['has_primary_key']]),
            'tables_with_fk': len([t for t in table_analysis.values() if t['has_foreign_keys']]),
            'total_records': sum([t['record_count'] for t in table_analysis.values()]),
            'table_analysis': table_analysis,
            'potential_primary_keys': potential_pks
        }
        
        # Сохраняем отчет
        report_dir = '/home/alex/vuege/docs/infrastructure/reports'
        os.makedirs(report_dir, exist_ok=True)
        report_file = f'{report_dir}/table-structure-analysis-{datetime.now().strftime("%Y%m%d_%H%M%S")}.json'
        
        with open(report_file, 'w', encoding='utf-8') as f:
            json.dump(report, f, ensure_ascii=False, indent=2)
        
        logging.info(f"📄 Отчет сохранен: {report_file}")
        
        # Итоговая статистика
        tables_with_pk = len([t for t in table_analysis.values() if t['has_primary_key']])
        tables_without_pk = len([t for t in table_analysis.values() if not t['has_primary_key']])
        total_records = sum([t['record_count'] for t in table_analysis.values()])
        
        logging.info(f"🎉 Анализ структуры завершен!")
        logging.info(f"📊 Всего таблиц: {len(table_analysis)}")
        logging.info(f"🔑 С первичными ключами: {tables_with_pk}")
        logging.info(f"❌ Без первичных ключей: {tables_without_pk}")
        logging.info(f"📝 Общий объем данных: {total_records:,} записей")
        logging.info(f"🎯 Потенциальных PK найдено: {len(potential_pks)}")
        
    except Exception as e:
        logging.error(f"❌ Критическая ошибка: {e}")
    finally:
        conn.close()

if __name__ == "__main__":
    main()