#!/usr/bin/env python3
"""
Скрипт для просмотра прогресса миграции через созданные представления
"""

import psycopg2
import psycopg2.extras
import logging
from datetime import datetime
import json
import os

# Настройка логирования
log_dir = "/home/alex/vuege/docs/infrastructure/logs"
os.makedirs(log_dir, exist_ok=True)
log_file = f"{log_dir}/view-migration-progress-{datetime.now().strftime('%Y%m%d_%H%M%S')}.log"

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(log_file, encoding='utf-8'),
        logging.StreamHandler()
    ]
)

# Параметры подключения к PostgreSQL
PG_HOST = "localhost"
PG_PORT = 5432
PG_DB = "vuege"
PG_USER = "postgres"
PG_PASSWORD = "testpass"

def get_pg_connection():
    """Создание подключения к PostgreSQL"""
    try:
        conn = psycopg2.connect(
            host=PG_HOST,
            port=PG_PORT,
            database=PG_DB,
            user=PG_USER,
            password=PG_PASSWORD
        )
        return conn
    except Exception as e:
        logging.error(f"Ошибка подключения к PostgreSQL: {e}")
        return None

def get_migration_progress(pg_conn):
    """Получение прогресса миграции"""
    try:
        cursor = pg_conn.cursor()
        
        query = """
        SELECT 
            object_type,
            has_in_mssql,
            has_in_postgres,
            total_objects,
            completed_objects,
            failed_objects,
            pending_objects,
            completion_percentage
        FROM migration_control.migration_progress
        ORDER BY object_type;
        """
        
        cursor.execute(query)
        results = cursor.fetchall()
        
        return results
        
    except Exception as e:
        logging.error(f"Ошибка получения прогресса миграции: {e}")
        return []

def get_detailed_progress(pg_conn, object_type=None):
    """Получение детального прогресса миграции"""
    try:
        cursor = pg_conn.cursor()
        
        if object_type:
            query = """
            SELECT 
                object_type,
                object_name_mssql,
                object_name_postgres,
                has_in_mssql,
                has_in_postgres,
                specific_name_mssql,
                specific_name_postgres,
                migration_status,
                migration_date,
                error_message
            FROM migration_control.detailed_progress
            WHERE object_type = %s
            ORDER BY object_name_mssql, specific_name_mssql;
            """
            cursor.execute(query, (object_type,))
        else:
            query = """
            SELECT 
                object_type,
                object_name_mssql,
                object_name_postgres,
                has_in_mssql,
                has_in_postgres,
                specific_name_mssql,
                specific_name_postgres,
                migration_status,
                migration_date,
                error_message
            FROM migration_control.detailed_progress
            ORDER BY object_type, object_name_mssql, specific_name_mssql;
            """
            cursor.execute(query)
        
        results = cursor.fetchall()
        
        return results
        
    except Exception as e:
        logging.error(f"Ошибка получения детального прогресса: {e}")
        return []

def get_summary_statistics(pg_conn):
    """Получение сводной статистики"""
    try:
        cursor = pg_conn.cursor()
        
        # Общая статистика
        summary_query = """
        SELECT 
            COUNT(DISTINCT o.id) as total_object_types,
            COUNT(so.id) as total_specific_objects,
            COUNT(CASE WHEN so.migration_status = 'completed' THEN 1 END) as completed_objects,
            COUNT(CASE WHEN so.migration_status = 'failed' THEN 1 END) as failed_objects,
            COUNT(CASE WHEN so.migration_status = 'pending' THEN 1 END) as pending_objects,
            CASE 
                WHEN COUNT(so.id) > 0 THEN 
                    ROUND((COUNT(CASE WHEN so.migration_status = 'completed' THEN 1 END)::DECIMAL / COUNT(so.id)::DECIMAL) * 100, 2)
                ELSE 0 
            END as overall_completion_percentage
        FROM migration_control.objects o
        LEFT JOIN migration_control.specific_objects so ON o.id = so.object_id;
        """
        
        cursor.execute(summary_query)
        summary = cursor.fetchone()
        
        return summary
        
    except Exception as e:
        logging.error(f"Ошибка получения сводной статистики: {e}")
        return None

def main():
    """Основная функция"""
    logging.info("Начало просмотра прогресса миграции")
    
    # Получение подключения
    pg_conn = get_pg_connection()
    if not pg_conn:
        return
    
    try:
        # Получение сводной статистики
        summary = get_summary_statistics(pg_conn)
        if summary:
            logging.info("=== СВОДНАЯ СТАТИСТИКА МИГРАЦИИ ===")
            logging.info(f"Типов объектов: {summary[0]}")
            logging.info(f"Всего конкретных объектов: {summary[1]}")
            logging.info(f"Завершено: {summary[2]}")
            logging.info(f"Ошибок: {summary[3]}")
            logging.info(f"В ожидании: {summary[4]}")
            logging.info(f"Общий прогресс: {summary[5]}%")
        
        # Получение прогресса по типам объектов
        progress = get_migration_progress(pg_conn)
        if progress:
            logging.info("")
            logging.info("=== ПРОГРЕСС ПО ТИПАМ ОБЪЕКТОВ ===")
            logging.info(f"{'Тип объекта':<20} {'Всего':<8} {'Завершено':<10} {'Ошибок':<8} {'Ожидает':<8} {'Прогресс':<10}")
            logging.info("-" * 70)
            
            for row in progress:
                object_type, has_mssql, has_pg, total, completed, failed, pending, percentage = row
                logging.info(f"{object_type:<20} {total:<8} {completed:<10} {failed:<8} {pending:<8} {percentage:<10}%")
        
        # Получение детального прогресса для проблемных объектов
        logging.info("")
        logging.info("=== ДЕТАЛЬНЫЙ ПРОГРЕСС (ПРОБЛЕМНЫЕ ОБЪЕКТЫ) ===")
        
        detailed_progress = get_detailed_progress(pg_conn)
        if detailed_progress:
            # Показываем только объекты с ошибками или в ожидании
            problem_objects = [row for row in detailed_progress if row[7] in ['failed', 'pending']]
            
            if problem_objects:
                logging.info(f"{'Тип':<15} {'Имя в MSSQL':<25} {'Статус':<10} {'Дата':<20} {'Ошибка':<30}")
                logging.info("-" * 100)
                
                for row in problem_objects[:20]:  # Показываем первые 20 проблемных объектов
                    object_type, obj_mssql, obj_pg, has_mssql, has_pg, spec_mssql, spec_pg, status, date, error = row
                    name = spec_mssql if spec_mssql else obj_mssql
                    error_msg = error[:27] + "..." if error and len(error) > 30 else error or ""
                    date_str = date.strftime('%Y-%m-%d %H:%M') if date else ""
                    
                    logging.info(f"{object_type:<15} {name:<25} {status:<10} {date_str:<20} {error_msg:<30}")
                
                if len(problem_objects) > 20:
                    logging.info(f"... и еще {len(problem_objects) - 20} проблемных объектов")
            else:
                logging.info("Проблемных объектов не найдено!")
        
        # Создание отчета
        report = {
            'timestamp': datetime.now().isoformat(),
            'summary': {
                'total_object_types': summary[0] if summary else 0,
                'total_specific_objects': summary[1] if summary else 0,
                'completed_objects': summary[2] if summary else 0,
                'failed_objects': summary[3] if summary else 0,
                'pending_objects': summary[4] if summary else 0,
                'overall_completion_percentage': summary[5] if summary else 0
            },
            'progress_by_type': [
                {
                    'object_type': row[0],
                    'has_in_mssql': row[1],
                    'has_in_postgres': row[2],
                    'total_objects': row[3],
                    'completed_objects': row[4],
                    'failed_objects': row[5],
                    'pending_objects': row[6],
                    'completion_percentage': row[7]
                }
                for row in progress
            ],
            'problem_objects': [
                {
                    'object_type': row[0],
                    'object_name_mssql': row[1],
                    'specific_name_mssql': row[5],
                    'migration_status': row[7],
                    'migration_date': row[8].isoformat() if row[8] else None,
                    'error_message': row[9]
                }
                for row in detailed_progress if row[7] in ['failed', 'pending']
            ],
            'log_file': log_file
        }
        
        # Сохранение отчета
        report_dir = "/home/alex/vuege/docs/infrastructure/reports"
        os.makedirs(report_dir, exist_ok=True)
        report_file = f"{report_dir}/view-migration-progress-report-{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        
        with open(report_file, 'w', encoding='utf-8') as f:
            json.dump(report, f, ensure_ascii=False, indent=2)
        
        logging.info(f"Отчет сохранен: {report_file}")
        
    except Exception as e:
        logging.error(f"Ошибка в основной функции: {e}")
    
    finally:
        if pg_conn:
            pg_conn.close()
    
    logging.info("Просмотр прогресса миграции завершен")

if __name__ == "__main__":
    main()