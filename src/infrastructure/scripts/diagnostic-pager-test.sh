#!/bin/bash
# diagnostic-pager-test.sh - диагностика проблем с pager и блокировкой терминала

echo "=== ДИАГНОСТИКА ПРОБЛЕМ С PAGER И БЛОКИРОВКОЙ ТЕРМИНАЛА ==="

# 1. Проверка переменных окружения
echo "1. Проверка переменных окружения"
echo "PAGER=$PAGER"
echo "LESS=$LESS"
echo "MORE=$MORE"
echo "COMPOSER_NO_INTERACTION=$COMPOSER_NO_INTERACTION"

# 2. Проверка git конфигурации
echo "2. Проверка git конфигурации"
git config --global core.pager

# 3. Тестирование базовых команд
echo "3. Тестирование базовых команд"
echo "Команда 1: date"
date +"%Y-%m-%d"
echo "Команда 2: pwd"
pwd
echo "Команда 3: echo"
echo "Тестовая строка"

# 4. Тестирование git status с --porcelain
echo "4. Тестирование git status --porcelain (безопасная версия)"
git status --porcelain | head -5

# 5. Тестирование обычного git status
echo "5. Тестирование обычного git status (ПОТЕНЦИАЛЬНО ОПАСНО)"
echo "ВНИМАНИЕ: Эта команда может заблокировать терминал!"
git status --no-pager | head -10

# 6. Тестирование последующих команд
echo "6. Тестирование последующих команд после git status"
echo "Команда после git status 1: date"
date +"%Y-%m-%d"
echo "Команда после git status 2: pwd"
pwd
echo "Команда после git status 3: echo"
echo "Проверка работы терминала"

echo "=== ДИАГНОСТИКА ЗАВЕРШЕНА ==="
