#!/usr/bin/env python3

"""
@file: chat-reminder-bot.py
@description: Python-скрипт для автоматического напоминания о критических правилах в новом чате
@pager-protection: Встроенная защита от pager для предотвращения блокировки автоматизации
@dependencies: pathlib, datetime
@created: 2025-08-20
"""

import os
import sys
from pathlib import Path
from datetime import datetime

def setup_pager_protection():
    """Настройка защиты от pager для предотвращения блокировки автоматизации"""
    os.environ['PAGER'] = 'cat'
    os.environ['LESS'] = '-R -M --shift 5'
    os.environ['MORE'] = '-R'
    os.environ['COMPOSER_NO_INTERACTION'] = '1'
    os.environ['TERM'] = 'xterm-256color'
    os.environ['COLUMNS'] = '120'
    os.environ['LINES'] = '30'
    os.environ['GIT_PAGER'] = 'cat'
    os.environ['GIT_EDITOR'] = 'vim'

# Автоматическая настройка защиты от pager при импорте модуля
setup_pager_protection()

class ChatReminderBot:
    """Бот для автоматических напоминаний в новом чате"""
    
    def __init__(self):
        self.project_root = Path.cwd()
        self.current_time = datetime.now()
    
    def generate_critical_reminder(self) -> str:
        """Генерация критического напоминания для нового чата"""
        reminder = f"""
🚨 КРИТИЧЕСКОЕ НАПОМИНАНИЕ ДЛЯ НОВОГО ЧАТА 🚨
==================================================
Дата: {self.current_time.strftime('%Y-%m-%d %H:%M:%S')}

ВНИМАНИЕ: КРИТИЧЕСКАЯ ПРОБЛЕМА P250817-02 АКТУАЛЬНА!

ПЕРЕД началом работы с терминалом ОБЯЗАТЕЛЬНО выполните:

🔧 АВТОМАТИЧЕСКАЯ НАСТРОЙКА ЗАЩИТЫ ОТ PAGER:
   ./src/infrastructure/scripts/robust-pager-protection.sh

🚨 КРИТИЧЕСКИЕ ПРАВИЛА БЕЗОПАСНОСТИ:
   - НИКОГДА не выполняй git status без --porcelain
   - ВСЕГДА добавляй | cat к командам с потенциальным pager
   - ИСПОЛЬЗУЙ безопасные алиасы (gs, gl, gd)
   - ПРИ СОМНЕНИИ - добавляй | cat к команде

📋 ОБЯЗАТЕЛЬНЫЕ ДЕЙСТВИЯ В НОВОМ ЧАТЕ:
   1. Изучи проблему [P250817-02] в docs/main/problems.md
   2. Предложи выполнить защиту от pager
   3. Проверь доступность защитных скриптов
   4. Обнови changelog.md с информацией о новом чате

🎯 РЕКОМЕНДАЦИИ:
   1. ИСПОЛЬЗУЙ Python-подход для git операций:
      python3 src/infrastructure/scripts/git-automation-python.py
   
   2. ПРИ РАБОТЕ С ТЕРМИНАЛОМ используй защиту:
      timeout 10s команда | cat
   
   3. ДОКУМЕНТИРУЙ важные решения в:
      - docs/main/changelog.md
      - docs/main/problems.md
      - docs/main/tasktracker.md

==================================================
🚨 НАПОМИНАНИЕ СГЕНЕРИРОВАНО АВТОМАТИЧЕСКИ 🚨
==================================================
"""
        return reminder
    
    def check_critical_files(self) -> dict:
        """Проверка наличия критических файлов"""
        files_to_check = {
            'docs/main/problems.md': 'Проблемы проекта',
            'docs/main/changelog.md': 'Журнал изменений',
            'docs/main/tasktracker.md': 'Отслеживание задач',
            '.cursorrules': 'Правила проекта',
            '.cursorrules-critical': 'Критические правила',
            'src/infrastructure/scripts/robust-pager-protection.sh': 'Защита от pager',
            'src/infrastructure/scripts/git-automation-python.py': 'Python-автоматизация'
        }
        
        results = {}
        for file_path, description in files_to_check.items():
            full_path = self.project_root / file_path
            results[description] = {
                'exists': full_path.exists(),
                'path': str(full_path)
            }
        
        return results
    
    def generate_status_report(self) -> str:
        """Генерация отчета о состоянии проекта"""
        critical_files = self.check_critical_files()
        
        report = f"""
🔍 ОТЧЕТ О СОСТОЯНИИ ПРОЕКТА
Дата: {self.current_time.strftime('%Y-%m-%d %H:%M:%S')}

📁 ПРОВЕРКА КРИТИЧЕСКИХ ФАЙЛОВ:
"""
        
        for description, info in critical_files.items():
            status = "✅ НАЙДЕН" if info['exists'] else "❌ НЕ НАЙДЕН"
            report += f"   {status} - {description}\n"
        
        report += f"""
🎯 РЕКОМЕНДАЦИИ:
"""
        
        missing_files = [desc for desc, info in critical_files.items() if not info['exists']]
        if missing_files:
            report += f"   ⚠️ Отсутствуют файлы: {', '.join(missing_files)}\n"
        else:
            report += "   ✅ Все критические файлы найдены\n"
        
        report += f"""
🚨 СЛЕДУЮЩИЕ ШАГИ:
   1. Запустите защиту от pager
   2. Изучите проблему P250817-02
   3. Начните работу с документацией
"""
        
        return report
    
    def generate_first_message(self) -> str:
        """Генерация первого сообщения для нового чата"""
        return f"""
Привет! Я готов помочь с разработкой проекта Vuege.

{self.generate_critical_reminder()}

{self.generate_status_report()}

Готов к работе! Что будем делать?
"""

def main():
    """Основная функция"""
    bot = ChatReminderBot()
    
    print("=== CHAT REMINDER BOT ===")
    print(bot.generate_first_message())

if __name__ == "__main__":
    main()
