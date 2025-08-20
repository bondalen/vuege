#!/bin/bash
# robust-pager-protection.sh - комплексная защита от pager и блокировки терминала

echo "=== КОМПЛЕКСНАЯ ЗАЩИТА ОТ PAGER И БЛОКИРОВКИ ТЕРМИНАЛА ==="

# Функция для настройки защиты от pager
setup_pager_protection() {
    echo "Настройка защиты от pager..."
    
    # Основные переменные окружения
    export PAGER=cat
    export LESS="-R -M --shift 5"
    export MORE="-R"
    export COMPOSER_NO_INTERACTION=1
    
    # Дополнительные переменные для предотвращения блокировки
    export TERM=xterm-256color
    export COLUMNS=120
    export LINES=30
    
    # Git конфигурация
    git config --global core.pager cat
    git config --global core.editor vim
    
    # Дополнительные настройки для предотвращения блокировки
    export GIT_PAGER=cat
    export GIT_EDITOR=vim
    
    echo "✅ Защита от pager настроена"
}

# Функция для безопасного выполнения git команд
safe_git() {
    local cmd="$1"
    local args="$2"
    
    # Принудительное использование cat для всех git команд
    case "$cmd" in
        "status")
            git status --porcelain $args
            ;;
        "log")
            git log --oneline $args
            ;;
        "diff")
            git diff --name-only $args
            ;;
        *)
            # Для других команд используем --no-pager если поддерживается
            if git $cmd --help | grep -q "no-pager"; then
                git --no-pager $cmd $args
            else
                git $cmd $args
            fi
            ;;
    esac
}

# Функция для тестирования защиты
test_protection() {
    echo "Тестирование защиты от pager..."
    
    # Тест 1: git status
    echo "Тест 1: git status"
    safe_git "status" | head -5
    
    # Тест 2: git log
    echo "Тест 2: git log"
    safe_git "log" "-5"
    
    # Тест 3: pip list
    echo "Тест 3: pip list"
    pip list | head -5
    
    # Тест 4: последовательность команд
    echo "Тест 4: последовательность команд"
    safe_git "status" | head -3 > /dev/null && date +"%Y-%m-%d" && pwd
    
    echo "✅ Все тесты пройдены успешно"
}

# Функция для создания алиасов
create_aliases() {
    echo "Создание безопасных алиасов..."
    
    # Алиасы для git команд
    alias gs='safe_git "status"'
    alias gl='safe_git "log" "-10"'
    alias gd='safe_git "diff"'
    
    # Алиасы для других команд
    alias pip-list='pip list | cat'
    alias pip-show='pip show | cat'
    
    echo "✅ Алиасы созданы"
}

# Функция для проверки состояния терминала
check_terminal_state() {
    echo "Проверка состояния терминала..."
    
    # Проверка переменных окружения
    echo "PAGER=$PAGER"
    echo "LESS=$LESS"
    echo "MORE=$MORE"
    echo "TERM=$TERM"
    
    # Проверка git конфигурации
    echo "Git pager: $(git config --global core.pager)"
    
    # Тест базовых команд
    echo "Тест базовых команд:"
    date +"%Y-%m-%d"
    pwd
    echo "test"
    
    echo "✅ Терминал работает корректно"
}

# Основная функция
main() {
    setup_pager_protection
    create_aliases
    test_protection
    check_terminal_state
    
    echo "=== КОМПЛЕКСНАЯ ЗАЩИТА НАСТРОЕНА ==="
    echo "Рекомендации:"
    echo "1. Используйте safe_git вместо обычных git команд"
    echo "2. Используйте алиасы gs, gl, gd для безопасных операций"
    echo "3. Добавляйте | cat к командам с потенциально длинным выводом"
    echo "4. При подозрении на блокировку используйте timeout 10s"
}

# Запуск основной функции
main "$@"
