#!/bin/bash
# advanced-pager-diagnostic.sh - расширенная диагностика проблем с pager и блокировкой терминала

echo "=== РАСШИРЕННАЯ ДИАГНОСТИКА ПРОБЛЕМ С PAGER И БЛОКИРОВКОЙ ТЕРМИНАЛА ==="

# Функция для безопасного выполнения команд
safe_execute() {
    local cmd="$1"
    local description="$2"
    echo "--- $description ---"
    echo "Выполняется: $cmd"
    
    # Выполнение команды с таймаутом
    timeout 10s bash -c "$cmd" 2>&1
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

# 1. Проверка системной информации
echo "1. СИСТЕМНАЯ ИНФОРМАЦИЯ"
echo "ОС: $(uname -a)"
echo "Shell: $SHELL"
echo "Terminal: $TERM"
echo "TZ: $TZ"

# 2. Проверка переменных окружения
echo "2. ПЕРЕМЕННЫЕ ОКРУЖЕНИЯ"
echo "PAGER=$PAGER"
echo "LESS=$LESS"
echo "MORE=$MORE"
echo "COMPOSER_NO_INTERACTION=$COMPOSER_NO_INTERACTION"
echo "GIT_PAGER=$GIT_PAGER"
echo "GIT_TERMINAL_PROGRESS=$GIT_TERMINAL_PROGRESS"

# 3. Проверка git конфигурации
echo "3. GIT КОНФИГУРАЦИЯ"
safe_execute "git config --global core.pager" "Git core.pager"
safe_execute "git config --global core.editor" "Git core.editor"
safe_execute "git config --list | grep -E '(pager|editor|terminal)'" "Git pager/editor/terminal настройки"

# 4. Тестирование базовых команд
echo "4. ТЕСТИРОВАНИЕ БАЗОВЫХ КОМАНД"
safe_execute "date +'%Y-%m-%d %H:%M:%S'" "Команда date"
safe_execute "pwd" "Команда pwd"
safe_execute "echo 'Тестовая строка'" "Команда echo"
safe_execute "whoami" "Команда whoami"

# 5. Тестирование git команд с защитой
echo "5. ТЕСТИРОВАНИЕ GIT КОМАНД С ЗАЩИТОЙ"
safe_execute "git status --porcelain | head -5" "Git status --porcelain"
safe_execute "git log --oneline -5" "Git log --oneline"
safe_execute "git diff --name-only | head -5" "Git diff --name-only"

# 6. Тестирование потенциально опасных команд
echo "6. ТЕСТИРОВАНИЕ ПОТЕНЦИАЛЬНО ОПАСНЫХ КОМАНД"
echo "ВНИМАНИЕ: Следующие команды могут заблокировать терминал!"

# Тест 1: Обычный git status
echo "--- Тест 1: Обычный git status (ограниченный вывод) ---"
timeout 15s bash -c "git status --no-pager | head -10" 2>&1
if [ $? -eq 124 ]; then
    echo "❌ GIT STATUS ЗАБЛОКИРОВАН (таймаут 15 секунд)"
else
    echo "✅ Git status выполнен успешно"
fi

# Тест 2: Git log без ограничений
echo "--- Тест 2: Git log без ограничений ---"
timeout 15s bash -c "git log --no-pager | head -10" 2>&1
if [ $? -eq 124 ]; then
    echo "❌ GIT LOG ЗАБЛОКИРОВАН (таймаут 15 секунд)"
else
    echo "✅ Git log выполнен успешно"
fi

# 7. Тестирование последовательности команд
echo "7. ТЕСТИРОВАНИЕ ПОСЛЕДОВАТЕЛЬНОСТИ КОМАНД"
echo "--- Последовательность 1: Безопасные команды ---"
safe_execute "git status --porcelain | wc -l" "Количество изменений"
safe_execute "date +'%Y-%m-%d %H:%M:%S'" "Время после git status"
safe_execute "echo 'Проверка работы терминала'" "Проверка терминала"

echo "--- Последовательность 2: После потенциально опасной команды ---"
echo "Выполняется git status --no-pager | head -5"
timeout 10s bash -c "git status --no-pager | head -5" > /dev/null 2>&1
if [ $? -eq 124 ]; then
    echo "❌ ПОСЛЕДОВАТЕЛЬНОСТЬ ЗАБЛОКИРОВАНА"
else
    echo "✅ Git status выполнен, проверяем последующие команды"
    safe_execute "date +'%Y-%m-%d %H:%M:%S'" "Время после git status"
    safe_execute "echo 'Проверка работы терминала'" "Проверка терминала"
fi

# 8. Проверка процессов
echo "8. ПРОВЕРКА ПРОЦЕССОВ"
safe_execute "ps aux | grep -E '(less|more|git)' | grep -v grep" "Активные процессы less/more/git"

# 9. Рекомендации
echo "9. РЕКОМЕНДАЦИИ"
echo "Для предотвращения блокировки терминала:"
echo "1. Всегда используйте git status --porcelain вместо git status"
echo "2. Добавляйте | cat к командам с потенциальным pager"
echo "3. Используйте --no-pager флаг для git команд"
echo "4. Ограничивайте вывод команд с помощью head/tail"
echo "5. Используйте таймауты для потенциально опасных команд"

echo "=== РАСШИРЕННАЯ ДИАГНОСТИКА ЗАВЕРШЕНА ==="
