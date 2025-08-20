#!/bin/bash

"""
@file: chat-reminder-analysis.sh
@description: Диагностический скрипт для анализа проблемы с автоматическими напоминаниями в новых чатах
@pager-protection: Встроенная защита от pager для предотвращения блокировки автоматизации
@dependencies: bash, grep, find
@created: 2025-08-20
"""

echo "=== АНАЛИЗ ПРОБЛЕМЫ С АВТОМАТИЧЕСКИМИ НАПОМИНАНИЯМИ ==="

# Настройка защиты от pager
export PAGER=cat
export LESS="-R -M --shift 5"
export MORE="-R"
export COMPOSER_NO_INTERACTION=1
export TERM=xterm-256color
export COLUMNS=120
export LINES=30
export GIT_PAGER=cat
export GIT_EDITOR=vim

git config --global core.pager cat

echo "=== ТЕСТ 1: ПРОВЕРКА НАЛИЧИЯ КРИТИЧЕСКИХ НАПОМИНАНИЙ ==="
echo "Поиск критических напоминаний в .cursorrules:"
grep -n "КРИТИЧЕСКОЕ НАПОМИНАНИЕ" .cursorrules
grep -n "ПЕРЕД началом работы" .cursorrules
grep -n "robust-pager-protection" .cursorrules

echo "=== ТЕСТ 2: АНАЛИЗ СТРУКТУРЫ ПРАВИЛ ==="
echo "Количество строк в .cursorrules:"
wc -l .cursorrules

echo "Позиция критических напоминаний:"
grep -n "## 🚨 КРИТИЧЕСКОЕ НАПОМИНАНИЕ" .cursorrules

echo "=== ТЕСТ 3: ПРОВЕРКА ДОСТУПНОСТИ СКРИПТОВ ==="
echo "Проверка наличия скриптов защиты:"
ls -la src/infrastructure/scripts/robust-pager-protection.sh
ls -la src/infrastructure/scripts/setup-pager-protection.sh
ls -la src/infrastructure/scripts/enhanced-pager-diagnostic.sh

echo "=== ТЕСТ 4: АНАЛИЗ ПРОБЛЕМЫ НЕПРИМЕНЕНИЯ ПРАВИЛ ==="
echo "Возможные причины неприменения правил:"
echo "1. Правила находятся в конце файла .cursorrules"
echo "2. Cursor IDE не читает весь файл .cursorrules"
echo "3. Правила не имеют правильного форматирования"
echo "4. Отсутствует принудительное напоминание в начале чата"

echo "=== ТЕСТ 5: ПРОВЕРКА РАЗМЕРА ФАЙЛА .cursorrules ==="
echo "Размер файла .cursorrules:"
ls -lh .cursorrules

echo "=== ТЕСТ 6: АНАЛИЗ СОДЕРЖИМОГО ПРАВИЛ ==="
echo "Первые 20 строк .cursorrules:"
head -20 .cursorrules

echo "Последние 20 строк .cursorrules:"
tail -20 .cursorrules

echo "=== ТЕСТ 7: ПОИСК КЛЮЧЕВЫХ СЛОВ ==="
echo "Поиск ключевых слов в правилах:"
grep -i "напоминание\|reminder\|критич\|critical" .cursorrules | head -10

echo "=== ТЕСТ 8: ПРЕДЛОЖЕНИЯ ПО РЕШЕНИЮ ==="
echo "Предложения по решению проблемы:"
echo "1. Переместить критические напоминания в начало файла"
echo "2. Создать отдельный файл с критическими правилами"
echo "3. Добавить принудительное напоминание в первые сообщения чата"
echo "4. Создать автоматический скрипт проверки правил"
echo "5. Добавить визуальные маркеры для привлечения внимания"

echo "=== АНАЛИЗ ЗАВЕРШЕН ==="
