#!/bin/bash

# Git SSH Wrapper - Автоматическая проверка SSH-агента перед git-командами
# Автор: Александр
# Дата: 2025-08-15

# Цвета для вывода
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Функция для цветного вывода
print_status() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

print_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# Функция для автоматической проверки SSH-агента
check_ssh_agent() {
    if [ -z "$SSH_AUTH_SOCK" ] || ! ssh-add -l &>/dev/null; then
        print_warning "SSH-агент не работает, запускаем автоматическую настройку..."
        if [ -f "./setup-ssh-agent.sh" ]; then
            ./setup-ssh-agent.sh
            return $?
        else
            print_error "Скрипт setup-ssh-agent.sh не найден"
            return 1
        fi
    fi
    return 0
}

# Основная функция для выполнения git-команд с проверкой SSH-агента
git_with_ssh_check() {
    # Проверяем SSH-агент перед выполнением git-команды
    if ! check_ssh_agent; then
        print_error "Не удалось настроить SSH-агент"
        return 1
    fi
    
    # Выполняем git-команду
    print_status "Выполняем git-команду: $*"
    git "$@"
    return $?
}

# Если скрипт вызван напрямую
if [[ "${BASH_SOURCE[0]}" == "${0}" ]]; then
    if [ $# -eq 0 ]; then
        echo "Использование: $0 <git-команда> [аргументы]"
        echo "Пример: $0 push origin main"
        exit 1
    fi
    
    git_with_ssh_check "$@"
fi

# Экспортируем функцию для использования в других скриптах
export -f check_ssh_agent
export -f git_with_ssh_check
