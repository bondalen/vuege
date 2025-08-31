#!/usr/bin/env python3
"""
Скрипт для пересоздания первичных ключей в PostgreSQL
Создает первичные ключи для всех таблиц, где они отсутствуют
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
log_file = f'{log_dir}/recreate-primary-keys-{datetime.now().strftime("%Y%m%d_%H%M%S")}.log'

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
            SELECT 
                t.table_name,
                c.column_name,
                c.data_type,
                c.character_maximum_length,
                c.is_nullable
            FROM information_schema.tables t
            LEFT JOIN information_schema.table_constraints tc 
                ON t.table_name = tc.table_name 
                AND tc.constraint_type = 'PRIMARY KEY'
                AND tc.table_schema = t.table_schema
            JOIN information_schema.columns c 
                ON t.table_name = c.table_name 
                AND t.table_schema = c.table_schema
            WHERE t.table_schema = %s
                AND t.table_type = 'BASE TABLE'
                AND tc.constraint_name IS NULL
            ORDER BY t.table_name, c.ordinal_position
        """, (PG_SCHEMA,))
        
        tables = {}
        for row in cursor.fetchall():
            table_name = row['table_name']
            if table_name not in tables:
                tables[table_name] = []
            tables[table_name].append({
                'column_name': row['column_name'],
                'data_type': row['data_type'],
                'character_maximum_length': row['character_maximum_length'],
                'is_nullable': row['is_nullable']
            })
        
        return tables
        
    except Exception as e:
        logging.error(f"Ошибка получения списка таблиц: {e}")
        return {}
    finally:
        cursor.close()

def get_pk_info_from_sqlserver():
    """Получение информации о первичных ключах из SQL Server"""
    # Здесь должна быть логика подключения к SQL Server
    # Пока используем статический список на основе предыдущего анализа
    
    pk_info = {
        'org': ['ogkey'],
        'cn': ['cnkey'],
        'cn_inv': ['cnkey', 'invkey'],
        'cn_inv_dbt': ['cnkey', 'invkey', 'dbtkey'],
        'cn_inv_dbt_upl': ['cnkey', 'invkey', 'dbtkey', 'uplkey'],
        'cn_inv_dbt_upl_g_p': ['cnkey', 'invkey', 'dbtkey', 'uplkey', 'gkey', 'pkey'],
        'cn_inv_doc': ['cnkey', 'invkey', 'dockey'],
        'cn_inv_pm': ['cnkey', 'invkey', 'pmkey'],
        'cninvcmm': ['cnkey', 'invkey', 'cmmkey'],
        'cst': ['cstkey'],
        'cstag': ['cstkey', 'agkey'],
        'cstagpn': ['cstkey', 'agkey', 'pnkey'],
        'inv': ['invkey'],
        'invdbtvalue': ['invkey', 'dbtkey', 'valuekey'],
        'ipgutplpncostits': ['ipgkey', 'utkey', 'plkey', 'pnkey', 'costkey', 'itkey', 'skey'],
        'juundocchnggr': ['juundockey', 'chngkey', 'grkey'],
        'juundocchnggrrel': ['juundockey', 'chngkey', 'grkey', 'relkey'],
        'juundocprmrgrrel': ['juundockey', 'prmrkey', 'grkey', 'relkey'],
        'juundocside': ['juundockey', 'sidekey'],
        'juundocsideorg': ['juundockey', 'sidekey', 'orgkey'],
        'juundocsidetype': ['juundockey', 'sidekey', 'typekey'],
        'ogag': ['ogkey', 'agkey'],
        'ra_period': ['rakey', 'periodkey'],
        'rgtaxreordivismerg': ['rgkey', 'taxkey', 'reorkey', 'diviskey', 'mergkey'],
        'rgtaxreorseparmerg': ['rgkey', 'taxkey', 'reorkey', 'separkey', 'mergkey']
    }
    
    return pk_info

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
    logging.info("🚀 Начало пересоздания первичных ключей")
    
    conn = connect_to_postgres()
    if not conn:
        return
    
    try:
        # Получаем информацию о первичных ключах из SQL Server
        pk_info = get_pk_info_from_sqlserver()
        
        logging.info(f"📋 Найдено {len(pk_info)} таблиц с первичными ключами")
        
        results = []
        
        # Создаем первичные ключи для каждой таблицы
        for table_name, pk_columns in pk_info.items():
            logging.info(f"🔑 Создание PK для таблицы {table_name}...")
            
            result = create_primary_key(conn, table_name, pk_columns)
            results.append(result)
            
            # Коммитим изменения для каждой таблицы
            if result['status'] == 'success':
                conn.commit()
            else:
                conn.rollback()
        
        # Создаем отчет
        report = {
            'timestamp': datetime.now().isoformat(),
            'total_tables_processed': len(results),
            'successful_pks': len([r for r in results if r['status'] == 'success']),
            'failed_pks': len([r for r in results if r['status'] == 'error']),
            'results': results
        }
        
        # Сохраняем отчет
        report_dir = '/home/alex/vuege/docs/infrastructure/reports'
        os.makedirs(report_dir, exist_ok=True)
        report_file = f'{report_dir}/primary-keys-recreation-report-{datetime.now().strftime("%Y%m%d_%H%M%S")}.json'
        
        with open(report_file, 'w', encoding='utf-8') as f:
            json.dump(report, f, ensure_ascii=False, indent=2)
        
        logging.info(f"📄 Отчет сохранен: {report_file}")
        
        # Итоговая статистика
        successful = len([r for r in results if r['status'] == 'success'])
        failed = len([r for r in results if r['status'] == 'error'])
        
        logging.info(f"🎉 Пересоздание первичных ключей завершено!")
        logging.info(f"✅ Успешно создано: {successful}/{len(results)} первичных ключей")
        logging.info(f"❌ Ошибки: {failed}/{len(results)}")
        
        if successful > 0:
            logging.info("🔄 Теперь можно создать внешние ключи")
        
    except Exception as e:
        logging.error(f"❌ Критическая ошибка: {e}")
        conn.rollback()
    finally:
        conn.close()

if __name__ == "__main__":
    main()