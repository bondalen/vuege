#!/bin/bash

# @file: setup-pager-protection.sh
# @description: Автоматическая настройка защиты от pager для предотвращения блокировки автоматизации
# @dependencies: git, bash
# @created: 2025-01-27

echo "🔧 Настройка защиты от pager..."

# Функция для проверки текущих настроек pager
check_pager_settings() {
    local issues=0
    
    echo "📋 Проверка текущих настроек pager..."
    
    # Проверяем git pager
    local git_pager=$(git config --global core.pager 2>/dev/null)
    if [ "$git_pager" != "cat" ]; then
        echo "❌ Git pager не настроен на cat (текущее значение: $git_pager)"
        ((issues++))
    else
        echo "✅ Git pager настроен на cat"
    fi
    
    # Проверяем переменные окружения
    if [ "$PAGER" != "cat" ]; then
        echo "❌ PAGER не установлен в cat (текущее значение: $PAGER)"
        ((issues++))
    else
        echo "✅ PAGER установлен в cat"
    fi
    
    if [ "$LESS" != "-R -M --shift 5" ]; then
        echo "❌ LESS не настроен корректно (текущее значение: $LESS)"
        ((issues++))
    else
        echo "✅ LESS настроен корректно"
    fi
    
    if [ "$MORE" != "-R" ]; then
        echo "❌ MORE не настроен корректно (текущее значение: $MORE)"
        ((issues++))
    else
        echo "✅ MORE настроен корректно"
    fi
    
    if [ "$COMPOSER_NO_INTERACTION" != "1" ]; then
        echo "❌ COMPOSER_NO_INTERACTION не установлен в 1 (текущее значение: $COMPOSER_NO_INTERACTION)"
        ((issues++))
    else
        echo "✅ COMPOSER_NO_INTERACTION установлен в 1"
    fi
    
    return $issues
}

# Функция для настройки git pager
setup_git_pager() {
    echo "🔧 Настройка git pager..."
    if git config --global core.pager cat; then
        echo "✅ Git pager настроен на cat"
        return 0
    else
        echo "❌ Ошибка настройки git pager"
        return 1
    fi
}

# Функция для настройки переменных окружения
setup_environment_variables() {
    echo "🔧 Настройка переменных окружения..."
    
    # Устанавливаем переменные для текущей сессии
    export PAGER=cat
    export LESS="-R -M --shift 5"
    export MORE="-R"
    export COMPOSER_NO_INTERACTION=1
    
    echo "✅ Переменные окружения установлены для текущей сессии"
    
    # Добавляем в ~/.bashrc для постоянного эффекта
    local bashrc="$HOME/.bashrc"
    local added=0
    
    # Проверяем и добавляем PAGER
    if ! grep -q "export PAGER=cat" "$bashrc" 2>/dev/null; then
        echo 'export PAGER=cat' >> "$bashrc"
        ((added++))
    fi
    
    # Проверяем и добавляем LESS
    if ! grep -q 'export LESS="-R -M --shift 5"' "$bashrc" 2>/dev/null; then
        echo 'export LESS="-R -M --shift 5"' >> "$bashrc"
        ((added++))
    fi
    
    # Проверяем и добавляем MORE
    if ! grep -q 'export MORE="-R"' "$bashrc" 2>/dev/null; then
        echo 'export MORE="-R"' >> "$bashrc"
        ((added++))
    fi
    
    # Проверяем и добавляем COMPOSER_NO_INTERACTION
    if ! grep -q "export COMPOSER_NO_INTERACTION=1" "$bashrc" 2>/dev/null; then
        echo 'export COMPOSER_NO_INTERACTION=1' >> "$bashrc"
        ((added++))
    fi
    
    if [ $added -gt 0 ]; then
        echo "✅ Добавлено $added настроек в ~/.bashrc"
    else
        echo "✅ Все настройки уже присутствуют в ~/.bashrc"
    fi
    
    return 0
}

# Функция для тестирования настроек
test_pager_protection() {
    echo "🧪 Тестирование защиты от pager..."
    
    local tests_passed=0
    local total_tests=3
    
    # Тест 1: git log
    echo "  Тест 1: git log --oneline -5"
    if timeout 10s git log --oneline -5 >/dev/null 2>&1; then
        echo "    ✅ git log работает без блокировки"
        ((tests_passed++))
    else
        echo "    ❌ git log заблокирован"
    fi
    
    # Тест 2: pip list
    echo "  Тест 2: pip list"
    if timeout 10s pip list >/dev/null 2>&1; then
        echo "    ✅ pip list работает без блокировки"
        ((tests_passed++))
    else
        echo "    ❌ pip list заблокирован"
    fi
    
    # Тест 3: man --help
    echo "  Тест 3: man --help"
    if timeout 10s man --help >/dev/null 2>&1; then
        echo "    ✅ man --help работает без блокировки"
        ((tests_passed++))
    else
        echo "    ❌ man --help заблокирован"
    fi
    
    echo "📊 Результаты тестирования: $tests_passed/$total_tests тестов прошли"
    
    if [ $tests_passed -eq $total_tests ]; then
        echo "🎉 Все тесты прошли успешно!"
        return 0
    else
        echo "⚠️ Некоторые тесты не прошли"
        return 1
    fi
}

# Функция для создания функции bash
create_bash_function() {
    echo "🔧 Создание функции bash для автоматической защиты..."
    
    local bashrc="$HOME/.bashrc"
    local function_name="safe_cmd"
    
    # Проверяем, есть ли уже функция
    if grep -q "function $function_name" "$bashrc" 2>/dev/null; then
        echo "✅ Функция $function_name уже существует"
        return 0
    fi
    
    # Добавляем функцию
    cat >> "$bashrc" << 'EOF'

# Функция для безопасного выполнения команд с защитой от pager
safe_cmd() {
    local cmd="$*"
    if [[ "$cmd" == *"git log"* ]] || [[ "$cmd" == *"git diff"* ]] || [[ "$cmd" == *"git show"* ]] || \
       [[ "$cmd" == *"pip list"* ]] || [[ "$cmd" == *"pip show"* ]] || [[ "$cmd" == *"man"* ]] || \
       [[ "$cmd" == *"less"* ]] || [[ "$cmd" == *"more"* ]]; then
        echo "🔒 Выполняю команду с защитой от pager: $cmd"
        eval "$cmd | cat"
    else
        eval "$cmd"
    fi
}
EOF
    
    echo "✅ Функция $function_name добавлена в ~/.bashrc"
    echo "💡 Использование: safe_cmd 'git log --oneline'"
    
    return 0
}

# Основная логика
main() {
    echo "=== Настройка защиты от pager ==="
    
    # Проверяем текущие настройки
    local issues=0
    check_pager_settings
    issues=$?
    
    if [ $issues -eq 0 ]; then
        echo "✅ Все настройки pager уже корректны"
    else
        echo "🔧 Требуется настройка $issues параметров"
        
        # Настраиваем git pager
        if ! setup_git_pager; then
            echo "❌ Не удалось настроить git pager"
            exit 1
        fi
        
        # Настраиваем переменные окружения
        if ! setup_environment_variables; then
            echo "❌ Не удалось настроить переменные окружения"
            exit 1
        fi
        
        # Создаем функцию bash
        if ! create_bash_function; then
            echo "❌ Не удалось создать функцию bash"
            exit 1
        fi
        
        echo "✅ Настройка завершена"
    fi
    
    # Тестируем настройки
    if test_pager_protection; then
        echo "🎉 Защита от pager настроена успешно!"
        echo ""
        echo "📋 Краткая справка:"
        echo "  • Git pager: git config --global core.pager cat"
        echo "  • Переменные: PAGER=cat, LESS=\"-R -M --shift 5\", MORE=\"-R\""
        echo "  • Функция: safe_cmd 'команда' для автоматической защиты"
        echo "  • Перезапуск терминала: source ~/.bashrc"
    else
        echo "⚠️ Настройка завершена с предупреждениями"
        echo "💡 Рекомендуется перезапустить терминал: source ~/.bashrc"
    fi
}

# Запуск скрипта
main "$@"
