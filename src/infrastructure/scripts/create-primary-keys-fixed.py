#!/usr/bin/env python3
"""
Скрипт для создания первичных ключей в PostgreSQL
Использует правильные имена колонок из анализа структуры
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
log_file = f"{log_dir}/create-primary-keys-fixed-{datetime.now().strftime('%Y%m%d_%H%M%S')}.log"

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

def get_connection():
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

def get_table_primary_key_candidates():
    """Получение кандидатов для первичных ключей на основе анализа структуры"""
    # Основные таблицы с предполагаемыми первичными ключами
    candidates = {
        # Основные таблицы
        'org': ['org_key'],
        'cn': ['cn_key'],
        'cn_inv': ['cn_inv_key'],
        'cn_inv_dbt': ['cn_inv_dbt_key'],
        'cn_inv_dbt_upl': ['upl_key'],
        'cn_inv_doc': ['cn_inv_doc_key'],
        'cn_inv_pm': ['cn_inv_pm_key'],
        'cninvcmm': ['cninvcmm_key'],
        'cst': ['cst_key'],
        'cstag': ['cstag_key'],
        'cstagpn': ['cstagpn_key'],
        'inv': ['ikey'],
        'invdbtvalue': ['invdbtvalue_key'],
        'ipgutplpncostits': ['ipgutplpncostits_key'],
        'juundocchnggr': ['juundocchnggr_key'],
        'juundocchnggrrel': ['juundocchnggrrel_key'],
        'juundocprmrgrrel': ['juundocprmrgrrel_key'],
        'juundocside': ['juundocside_key'],
        'juundocsideorg': ['juundocsideorg_key'],
        'juundocsidetype': ['juundocsidetype_key'],
        'ogag': ['ogag_key'],
        'ra_period': ['ra_period_key'],
        'rgtaxreordivismerg': ['rgtaxreordivismerg_key'],
        'rgtaxreorseparmerg': ['rgtaxreorseparmerg_key'],
        
        # Дополнительные таблицы
        'accnt': ['account_key'],
        'cn_s': ['cn_s_key'],
        'cn_s_org': ['cn_s_org_key'],
        'cn_s_type': ['cn_s_type_key'],
        'cncs': ['cncs_key'],
        'cninv': ['cninv_key'],
        'cninvaccnt': ['cninvaccnt_key'],
        'cninvgr': ['cninvgr_key'],
        'cnnum': ['cnnum_key'],
        'cnnumtype': ['cnnumtype_key'],
        'cstagcs': ['cstagcs_key'],
        'cstagpnbranch': ['cstagpnbranch_key'],
        'cstagpncs': ['cstagpncs_key'],
        'dtqcontract': ['dtqcontract_key'],
        'dtqcounterparty': ['dtqcounterparty_key'],
        'dtqinvoice': ['dtqinvoice_key'],
        'dtqinvoicedbt': ['dtqinvoicedbt_key'],
        'impgr': ['impgr_key'],
        'invbranch_23q1': ['invbranch_key'],
        'invbranch_23q2': ['invbranch_key'],
        'invbranch_25q0': ['invbranch_key'],
        'invbranch_25q1': ['invbranch_key'],
        'invbranch_25q1_new': ['invbranch_key'],
        'invcs': ['invcs_key'],
        'invdbt': ['invdbt_key'],
        'invnum': ['invnum_key'],
        'invnumenum': ['invnumenum_key'],
        'ipg': ['ipg_key'],
        'ipgch': ['ipgch_key'],
        'ipgcostits': ['ipgcostits_key'],
        'ipgpn': ['ipgpn_key'],
        'ipgsh': ['ipgsh_key'],
        'ipgst': ['ipgst_key'],
        'ipgutpl': ['ipgutpl_key'],
        'ipgutplgr': ['ipgutplgr_key'],
        'ipgutplp': ['ipgutplp_key'],
        'juundoc': ['juundockey'],
        'juundocchng': ['juundocchng_key'],
        'juundocchngtype': ['juundocchngtype_key'],
        'juundocprmr': ['juundocprmr_key'],
        'juundocprmrtype': ['juundocprmrtype_key'],
        'juundocreg': ['juundocreg_key'],
        'juundocrelchng': ['juundocrelchng_key'],
        'juundoctype': ['juundoctype_key'],
        'og': ['og_key'],
        'ogagcs': ['ogagcs_key'],
        'ogagfee': ['ogagfee_key'],
        'ogagfeegr': ['ogagfeegr_key'],
        'ogagfeep': ['ogagfeep_key'],
        'ra': ['ra_key'],
        'ra_change': ['ra_change_key'],
        'ra_change_summ': ['ra_change_summ_key'],
        'ra_chcs': ['ra_chcs_key'],
        'ra_period': ['ra_period_key'],
        'ra_summ': ['ra_summ_key'],
        'ra_typegr': ['ra_typegr_key'],
        'racs': ['racs_key'],
        'ralp': ['ralp_key'],
        'ralpgr': ['ralpgr_key'],
        'ralpra': ['ralpra_key'],
        'rara_chsmlt': ['rara_chsmlt_key'],
        'rasmlt': ['rasmlt_key'],
        'ratime': ['ratime_key'],
        'ratimeag': ['ratimeag_key'],
        'rgtaxbuirg': ['rgtaxbuirg_key'],
        'rgtaxind': ['rgtaxind_key'],
        'rgtaxname': ['rgtaxname_key'],
        'rgtaxoffice': ['rgtaxoffice_key'],
        'rgtaxreason': ['rgtaxreason_key'],
        'rgtaxregion': ['rgtaxregion_key'],
        'rgtaxreoracqui': ['rgtaxreoracqui_key'],
        'rgtaxreordivis': ['rgtaxreordivis_key'],
        'rgtaxreordivisacqu': ['rgtaxreordivisacqu_key'],
        'rgtaxreormerge': ['rgtaxreormerge_key'],
        'rgtaxreorsepar': ['rgtaxreorsepar_key'],
        'rgtaxreorseparacqu': ['rgtaxreorseparacqu_key'],
        'rgtaxreortrans': ['rgtaxreortrans_key'],
        'rgtaxsubdivs': ['rgtaxsubdivs_key'],
        'rgtaxsubdivsbuirg': ['rgtaxsubdivsbuirg_key'],
        'rgtaxsubdivsname': ['rgtaxsubdivsname_key'],
        'rgtaxsubdivsreas': ['rgtaxsubdivsreas_key'],
        'rrclist': ['rrclist_key'],
        'rrcrslt': ['rrcrslt_key'],
        'rrctimelist': ['rrctimelist_key'],
        'st': ['st_key'],
        'stcost': ['stcost_key'],
        'stcostcs': ['stcostcs_key'],
        'stcostnm': ['stcostnm_key'],
        'stilim': ['stilim_key'],
        'stipg': ['stipg_key'],
        'stipgcs': ['stipgcs_key'],
        'stipgnm': ['stipgnm_key'],
        'stnet': ['stnet_key'],
        'stnetpn': ['stnetpn_key'],
        'strel': ['strel_key'],
        'sttype': ['sttype_key'],
        'timersltcap': ['timersltcap_key'],
        'timersltm': ['timersltm_key'],
        'timersltmrl': ['timersltmrl_key'],
        'timersltmrttl': ['timersltmrttl_key'],
        'yr': ['yr_key'],
        'yr_ctrl': ['yr_ctrl_key'],
        'yr_ctrl_cm': ['yr_ctrl_key'],
        'yr_ctrl_cm_21': ['yr_ctrl_key'],
        'yr_ctrl_cmacc21': ['yr_ctrl_key'],
        'yr_ctrl_cmacc21_06': ['yr_ctrl_key'],
        'yr_ctrlaccnt': ['yr_ctrl_key'],
        'yr_upl_p': ['yr_upl_p_key'],
        'yrcs': ['yrcs_key']
    }
    return candidates

def check_column_exists(conn, table_name, column_name):
    """Проверка существования колонки в таблице"""
    try:
        cursor = conn.cursor()
        
        query = """
        SELECT column_name
        FROM information_schema.columns
        WHERE table_schema = 'ags' 
        AND table_name = %s 
        AND column_name = %s
        """
        
        cursor.execute(query, (table_name, column_name))
        result = cursor.fetchone()
        
        return result is not None
        
    except Exception as e:
        logging.error(f"Ошибка проверки колонки {column_name} в таблице {table_name}: {e}")
        return False

def get_actual_primary_key_column(conn, table_name, candidates):
    """Получение фактической колонки для первичного ключа"""
    try:
        cursor = conn.cursor()
        
        # Получаем все колонки таблицы
        query = """
        SELECT column_name
        FROM information_schema.columns
        WHERE table_schema = 'ags' 
        AND table_name = %s
        ORDER BY ordinal_position
        """
        
        cursor.execute(query, (table_name,))
        columns = [row[0] for row in cursor.fetchall()]
        
        # Проверяем кандидатов
        for candidate in candidates:
            if candidate in columns:
                return candidate
        
        # Если кандидаты не найдены, ищем колонки с "key" в названии
        key_columns = [col for col in columns if 'key' in col.lower()]
        if key_columns:
            return key_columns[0]
        
        # Если нет колонок с "key", берем первую колонку
        if columns:
            return columns[0]
        
        return None
        
    except Exception as e:
        logging.error(f"Ошибка получения колонки для первичного ключа в таблице {table_name}: {e}")
        return None

def create_primary_key(conn, table_name, pk_column):
    """Создание первичного ключа в таблице"""
    try:
        cursor = conn.cursor()
        
        # Проверяем, есть ли уже первичный ключ
        query = """
        SELECT constraint_name
        FROM information_schema.table_constraints
        WHERE table_schema = 'ags' 
        AND table_name = %s 
        AND constraint_type = 'PRIMARY KEY'
        """
        
        cursor.execute(query, (table_name,))
        existing_pk = cursor.fetchone()
        
        if existing_pk:
            logging.info(f"Первичный ключ уже существует в таблице {table_name}")
            return True
        
        # Формируем имя первичного ключа
        pk_name = f"pk_{table_name}"
        
        # Создаем первичный ключ
        query = f"""
        ALTER TABLE ags.{table_name} 
        ADD CONSTRAINT {pk_name} PRIMARY KEY ({pk_column})
        """
        
        cursor.execute(query)
        conn.commit()
        
        logging.info(f"Создан первичный ключ {pk_name} в таблице {table_name}")
        return True
        
    except Exception as e:
        logging.error(f"Ошибка создания первичного ключа в таблице {table_name}: {e}")
        conn.rollback()
        return False

def main():
    """Основная функция"""
    logging.info("Начало создания первичных ключей")
    
    # Получение подключения
    conn = get_connection()
    if not conn:
        return
    
    # Получение кандидатов для первичных ключей
    candidates = get_table_primary_key_candidates()
    
    # Результаты
    results = {
        'processed_tables': 0,
        'successful_pks': 0,
        'failed_pks': 0,
        'errors': []
    }
    
    try:
        for table_name, pk_candidates in candidates.items():
            logging.info(f"Обработка таблицы: {table_name}")
            results['processed_tables'] += 1
            
            # Получаем фактическую колонку для первичного ключа
            pk_column = get_actual_primary_key_column(conn, table_name, pk_candidates)
            
            if pk_column:
                # Создаем первичный ключ
                if create_primary_key(conn, table_name, pk_column):
                    results['successful_pks'] += 1
                else:
                    results['failed_pks'] += 1
            else:
                logging.warning(f"Не найдена подходящая колонка для первичного ключа в таблице {table_name}")
                results['failed_pks'] += 1
    
    except Exception as e:
        logging.error(f"Ошибка в основной функции: {e}")
        results['errors'].append(str(e))
    
    finally:
        conn.close()
    
    # Создание отчета
    report = {
        'timestamp': datetime.now().isoformat(),
        'results': results,
        'log_file': log_file
    }
    
    # Сохранение отчета
    report_dir = "/home/alex/vuege/docs/infrastructure/reports"
    os.makedirs(report_dir, exist_ok=True)
    report_file = f"{report_dir}/create-primary-keys-fixed-report-{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
    
    with open(report_file, 'w', encoding='utf-8') as f:
        json.dump(report, f, ensure_ascii=False, indent=2)
    
    # Вывод результатов
    logging.info("=== РЕЗУЛЬТАТЫ СОЗДАНИЯ ПЕРВИЧНЫХ КЛЮЧЕЙ ===")
    logging.info(f"Обработано таблиц: {results['processed_tables']}")
    logging.info(f"Успешно создано первичных ключей: {results['successful_pks']}")
    logging.info(f"Ошибок создания: {results['failed_pks']}")
    
    if results['errors']:
        logging.error(f"Ошибки: {len(results['errors'])}")
        for error in results['errors']:
            logging.error(f"  - {error}")
    
    logging.info(f"Отчет сохранен: {report_file}")
    logging.info("Создание первичных ключей завершено")

if __name__ == "__main__":
    main()