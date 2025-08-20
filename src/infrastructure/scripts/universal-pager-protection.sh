#!/bin/bash
# universal-pager-protection.sh - универсальная защита от блокировки терминала pager'ом

# Настройка защиты от pager
export PAGER=cat
export LESS="-R -M --shift 5"
export MORE="-R"
export COMPOSER_NO_INTERACTION=1
export GIT_PAGER=cat
export GIT_TERMINAL_PROGRESS=0

# Настройка git pager глобально
git config --global core.pager cat 2>/dev/null

# Функция для безопасного выполнения команд с таймаутом
safe_cmd() {
    local cmd="$1"
    local timeout_seconds="${2:-10}"
    local description="${3:-"Команда"}"
    
    echo "🔒 Выполняется: $description"
    echo "   Команда: $cmd"
    
    # Выполнение команды с таймаутом
    timeout ${timeout_seconds}s bash -c "$cmd" 2>&1
    local exit_code=$?
    
    case $exit_code in
        0)
            echo "✅ $description выполнена успешно"
            return 0
            ;;
        124)
            echo "❌ $description ЗАБЛОКИРОВАНА (таймаут ${timeout_seconds} секунд)"
            return 1
            ;;
        *)
            echo "⚠️ $description завершилась с ошибкой (код: $exit_code)"
            return $exit_code
            ;;
    esac
}

# Функция для безопасного git status
safe_git_status() {
    local porcelain="${1:-true}"
    
    if [ "$porcelain" = "true" ]; then
        echo "🔒 Безопасный git status (--porcelain)"
        git status --porcelain
    else
        echo "⚠️ Обычный git status (может заблокировать терминал)"
        safe_cmd "git status --no-pager" 15 "Git status"
    fi
}

# Функция для безопасного git log
safe_git_log() {
    local lines="${1:-10}"
    echo "🔒 Безопасный git log (--oneline, ограниченный вывод)"
    git log --oneline -${lines}
}

# Функция для безопасного git diff
safe_git_diff() {
    local porcelain="${1:-true}"
    
    if [ "$porcelain" = "true" ]; then
        echo "🔒 Безопасный git diff (--name-only)"
        git diff --name-only
    else
        echo "⚠️ Обычный git diff (может заблокировать терминал)"
        safe_cmd "git diff --no-pager | head -20" 15 "Git diff"
    fi
}

# Функция для диагностики состояния терминала
diagnose_terminal() {
    echo "=== ДИАГНОСТИКА СОСТОЯНИЯ ТЕРМИНАЛА ==="
    
    echo "1. Переменные окружения:"
    echo "   PAGER=$PAGER"
    echo "   LESS=$LESS"
    echo "   MORE=$MORE"
    echo "   COMPOSER_NO_INTERACTION=$COMPOSER_NO_INTERACTION"
    
    echo "2. Git конфигурация:"
    git config --global core.pager 2>/dev/null || echo "   core.pager не настроен"
    
    echo "3. Тестирование базовых команд:"
    safe_cmd "date +'%Y-%m-%d %H:%M:%S'" 5 "Команда date"
    safe_cmd "pwd" 5 "Команда pwd"
    safe_cmd "echo 'Терминал работает'" 5 "Команда echo"
    
    echo "4. Тестирование git команд:"
    safe_cmd "git status --porcelain | head -3" 10 "Git status --porcelain"
    safe_cmd "git log --oneline -3" 10 "Git log --oneline"
    
    echo "=== ДИАГНОСТИКА ЗАВЕРШЕНА ==="
}

# Функция для восстановления терминала
recover_terminal() {
    echo "=== ВОССТАНОВЛЕНИЕ ТЕРМИНАЛА ==="
    
    echo "1. Убийство процессов pager:"
    pkill -f "less" 2>/dev/null && echo "   Процессы less остановлены"
    pkill -f "more" 2>/dev/null && echo "   Процессы more остановлены"
    
    echo "2. Сброс переменных окружения:"
    export PAGER=cat
    export LESS="-R -M --shift 5"
    export MORE="-R"
    export COMPOSER_NO_INTERACTION=1
    
    echo "3. Настройка git pager:"
    git config --global core.pager cat
    
    echo "4. Тестирование восстановления:"
    safe_cmd "date +'%Y-%m-%d %H:%M:%S'" 5 "Проверка работы терминала"
    
    echo "=== ВОССТАНОВЛЕНИЕ ЗАВЕРШЕНО ==="
}

# Основная функция
main() {
    local action="${1:-diagnose}"
    
    case $action in
        "diagnose")
            diagnose_terminal
            ;;
        "recover")
            recover_terminal
            ;;
        "status")
            safe_git_status "${2:-true}"
            ;;
        "log")
            safe_git_log "${2:-10}"
            ;;
        "diff")
            safe_git_diff "${2:-true}"
            ;;
        "safe")
            safe_cmd "${2}" "${3:-10}" "${4:-"Команда"}"
            ;;
        *)
            echo "Использование: $0 [действие] [параметры]"
            echo ""
            echo "Действия:"
            echo "  diagnose                    - диагностика состояния терминала"
            echo "  recover                     - восстановление терминала"
            echo "  status [porcelain]          - безопасный git status (porcelain=true/false)"
            echo "  log [lines]                 - безопасный git log (количество строк)"
            echo "  diff [porcelain]            - безопасный git diff (porcelain=true/false)"
            echo "  safe <команда> [таймаут] [описание] - безопасное выполнение команды"
            echo ""
            echo "Примеры:"
            echo "  $0 diagnose"
            echo "  $0 status true"
            echo "  $0 log 5"
            echo "  $0 safe 'git log --oneline -10' 15 'Git log'"
            ;;
    esac
}

# Запуск основной функции с переданными параметрами
main "$@"
