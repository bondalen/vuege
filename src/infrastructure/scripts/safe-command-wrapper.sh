#!/bin/bash

# Safe Command Wrapper
# Автоматически добавляет защиту от pager к командам
# Использование: ./safe-command-wrapper.sh "команда"

set -e

# Функция для добавления защиты от pager
add_pager_protection() {
    local cmd="$1"
    
    # Команды, которые могут вызвать pager
    local pager_commands=(
        "git log" "git diff" "git show" "git status"
        "pip list" "pip show" "pip search"
        "python -m" "python --help"
        "less" "more" "man"
        "curl" "wget"
        "find" "grep" "cat"
    )
    
    # Проверяем, содержит ли команда потенциально проблемные части
    for pager_cmd in "${pager_commands[@]}"; do
        if [[ "$cmd" == *"$pager_cmd"* ]]; then
            # Если команда уже содержит | cat, не добавляем повторно
            if [[ "$cmd" != *"| cat"* ]]; then
                echo "$cmd | cat"
                return 0
            fi
        fi
    done
    
    # Если команда не содержит проблемных частей, возвращаем как есть
    echo "$cmd"
}

# Функция для проверки и настройки git pager
setup_git_pager() {
    local current_pager=$(git config --global core.pager 2>/dev/null || echo "")
    
    if [[ "$current_pager" != "cat" ]]; then
        echo "Настройка git pager..."
        git config --global core.pager cat
        echo "✅ Git pager настроен на 'cat'"
    else
        echo "✅ Git pager уже настроен правильно"
    fi
}

# Функция для проверки переменных окружения
check_environment() {
    # Проверяем переменные, которые могут влиять на pager
    local env_vars=("PAGER" "LESS" "MORE")
    
    for var in "${env_vars[@]}"; do
        if [[ -n "${!var}" ]]; then
            echo "⚠️  Переменная $var установлена: ${!var}"
        fi
    done
    
    # Рекомендуемые настройки
    echo "Рекомендуемые настройки для предотвращения pager:"
    echo "export PAGER=cat"
    echo "export LESS=-R"
    echo "export MORE=-R"
}

# Основная логика
main() {
    echo "🔧 Safe Command Wrapper"
    echo "========================"
    
    # Настройка git pager
    setup_git_pager
    
    # Проверка окружения
    check_environment
    
    # Если передана команда, обрабатываем её
    if [[ $# -gt 0 ]]; then
        local original_cmd="$*"
        local safe_cmd=$(add_pager_protection "$original_cmd")
        
        echo ""
        echo "Исходная команда: $original_cmd"
        echo "Безопасная команда: $safe_cmd"
        echo ""
        echo "Выполнение команды..."
        echo "========================"
        
        # Выполняем команду
        eval "$safe_cmd"
    else
        echo ""
        echo "Использование: $0 \"команда\""
        echo "Пример: $0 \"git log --oneline\""
        echo ""
        echo "Или запустите без параметров для настройки окружения"
    fi
}

# Запуск основной функции
main "$@"
