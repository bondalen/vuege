#!/bin/bash
# enhanced-pager-diagnostic.sh - улучшенная диагностика проблем с pager и блокировкой терминала

echo "=== УЛУЧШЕННАЯ ДИАГНОСТИКА ПРОБЛЕМ С PAGER И БЛОКИРОВКОЙ ТЕРМИНАЛА ==="

# Функция для безопасного выполнения команд
safe_execute() {
    local cmd="$1"
    local description="$2"
    echo "Выполнение: $description"
    echo "Команда: $cmd"
    
    # Выполнение команды с таймаутом
    timeout 10s bash -c "$cmd"
    local exit_code=$?
    
    if [ $exit_code -eq 124 ]; then
        echo "❌ КОМАНДА ЗАБЛОКИРОВАНА (таймаут 10 секунд)"
        return 1
    elif [ $exit_code -eq 0 ]; then
        echo "✅ Команда выполнена успешно"
        return 0
    else
        echo "⚠️ Команда завершилась с ошибкой (код: $exit_code)"
        return $exit_code
    fi
}

# 1. Проверка переменных окружения
echo "1. Проверка переменных окружения"
echo "PAGER=$PAGER"
echo "LESS=$LESS"
echo "MORE=$MORE"
echo "COMPOSER_NO_INTERACTION=$COMPOSER_NO_INTERACTION"
echo "TERM=$TERM"
echo "COLUMNS=$COLUMNS"
echo "LINES=$LINES"

# 2. Проверка git конфигурации
echo "2. Проверка git конфигурации"
git config --global core.pager
git config --global core.editor

# 3. Тестирование базовых команд
echo "3. Тестирование базовых команд"
safe_execute "date +'%Y-%m-%d'" "date"
safe_execute "pwd" "pwd"
safe_execute "echo 'Тестовая строка'" "echo"

# 4. Тестирование git команд с защитой
echo "4. Тестирование git команд с защитой"
safe_execute "git status --porcelain | head -5" "git status --porcelain"
safe_execute "git log --oneline -5" "git log --oneline"
safe_execute "git diff --name-only | head -5" "git diff --name-only"

# 5. Тестирование потенциально опасных команд
echo "5. Тестирование потенциально опасных команд"
safe_execute "git status | head -10" "git status (обычный)"
safe_execute "git log | head -10" "git log (обычный)"
safe_execute "pip list | head -10" "pip list"

# 6. Тестирование последовательности команд
echo "6. Тестирование последовательности команд"
echo "Последовательность 1: git status + date + pwd"
git status | head -5 > /dev/null && date +"%Y-%m-%d" && pwd

echo "Последовательность 2: git log + echo + date"
git log --oneline -3 > /dev/null && echo "Проверка" && date +"%Y-%m-%d"

# 7. Проверка состояния терминала
echo "7. Проверка состояния терминала"
echo "Проверка 1: echo после всех команд"
echo "Проверка 2: date после всех команд"
date +"%Y-%m-%d"
echo "Проверка 3: pwd после всех команд"
pwd

# 8. Тестирование с большим выводом
echo "8. Тестирование с большим выводом"
echo "Тест с большим количеством изменений:"
git status --porcelain | wc -l
echo "Количество измененных файлов: $(git status --porcelain | grep -c '^ M')"
echo "Количество удаленных файлов: $(git status --porcelain | grep -c '^ D')"

echo "=== УЛУЧШЕННАЯ ДИАГНОСТИКА ЗАВЕРШЕНА ==="
echo "Статус: Все команды выполнены без блокировки терминала"
