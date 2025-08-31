#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Запуск всех исправлений проблемных таблиц схемы AGS
Автор: AI Assistant
Дата: 30 августа 2025
"""

import subprocess
import logging
import sys
import os
from datetime import datetime

# Настройка логирования
def setup_logging():
    """Настройка логирования"""
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler(f'logs/run-all-fixes-{datetime.now().strftime("%Y%m%d_%H%M%S")}.log'),
            logging.StreamHandler(sys.stdout)
        ]
    )
    return logging.getLogger(__name__)

# Список исправляющих скриптов
FIX_SCRIPTS = [
    {
        'name': 'Исправление регистра имен колонок',
        'script': 'fix-column-case-issues.py',
        'description': 'Исправляет проблемы с регистром имен колонок (9 таблиц)'
    },
    {
        'name': 'Исправление UUID типов',
        'script': 'fix-uuid-issues.py',
        'description': 'Исправляет проблемы с UUID типами (3 таблицы)'
    },
    {
        'name': 'Исправление имен таблиц',
        'script': 'fix-table-name-issues.py',
        'description': 'Исправляет проблемы с именами таблиц (11 таблиц)'
    }
]

def run_script(script_path):
    """Запуск Python скрипта"""
    try:
        result = subprocess.run(
            [sys.executable, script_path],
            capture_output=True,
            text=True,
            cwd=os.path.dirname(os.path.abspath(__file__))
        )
        return result.returncode == 0, result.stdout, result.stderr
    except Exception as e:
        return False, "", str(e)

def main():
    """Основная функция"""
    logger = setup_logging()
    
    logging.info("🚀 ЗАПУСК ВСЕХ ИСПРАВЛЕНИЙ ПРОБЛЕМНЫХ ТАБЛИЦ")
    logging.info("=" * 80)
    
    # Проверяем наличие папки logs
    if not os.path.exists('logs'):
        os.makedirs('logs')
        logging.info("📁 Создана папка logs")
    
    success_count = 0
    error_count = 0
    
    for i, script_info in enumerate(FIX_SCRIPTS, 1):
        script_name = script_info['name']
        script_file = script_info['script']
        description = script_info['description']
        
        logging.info(f"📋 [{i}/{len(FIX_SCRIPTS)}] {script_name}")
        logging.info(f"   📝 {description}")
        logging.info(f"   🔧 Запуск скрипта: {script_file}")
        
        # Проверяем существование файла
        script_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), script_file)
        if not os.path.exists(script_path):
            logging.error(f"❌ Файл {script_path} не найден!")
            error_count += 1
            continue
        
        # Запускаем скрипт
        success, stdout, stderr = run_script(script_path)
        
        if success:
            logging.info(f"✅ {script_name} выполнен успешно")
            success_count += 1
        else:
            logging.error(f"❌ {script_name} завершился с ошибкой")
            if stderr:
                logging.error(f"   Ошибка: {stderr}")
            error_count += 1
        
        logging.info("-" * 60)
    
    # Итоговый отчет
    logging.info("=" * 80)
    logging.info("📊 ИТОГОВЫЙ ОТЧЕТ ВСЕХ ИСПРАВЛЕНИЙ")
    logging.info("=" * 80)
    logging.info(f"📋 Всего скриптов: {len(FIX_SCRIPTS)}")
    logging.info(f"✅ Успешно выполнено: {success_count}")
    logging.info(f"❌ Ошибки выполнения: {error_count}")
    logging.info(f"📈 Процент успеха: {(success_count/len(FIX_SCRIPTS)*100):.1f}%")
    
    if error_count == 0:
        logging.info("🎉 ВСЕ ИСПРАВЛЕНИЯ ВЫПОЛНЕНЫ УСПЕШНО!")
        logging.info("🚀 Готово к финальной проверке миграции")
    else:
        logging.warning(f"⚠️ Осталось {error_count} проблемных скриптов")
        logging.info("🔧 Требуется ручная проверка и исправление")
    
    return error_count == 0

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)