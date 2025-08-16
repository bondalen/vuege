#!/bin/bash

# Автоматическая настройка SSH-агента для проекта Vuege
# Автор: Александр
# Дата: 2024-12-19

set -e  # Остановка при ошибке

echo "=== Настройка SSH-агента для проекта Vuege ==="
echo

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
        "$0"
        return $?
    fi
    return 0
}

# Проверка существования SSH-ключа
SSH_KEY="$HOME/.ssh/id_ed25519_github"

if [ ! -f "$SSH_KEY" ]; then
    print_error "SSH-ключ не найден: $SSH_KEY"
    echo "Создайте SSH-ключ командой:"
    echo "ssh-keygen -t ed25519 -C 'your_email@example.com' -f ~/.ssh/id_ed25519_github"
    exit 1
fi

print_success "SSH-ключ найден: $SSH_KEY"

# Проверка прав доступа к SSH-ключу
if [ "$(stat -c %a "$SSH_KEY")" != "600" ]; then
    print_warning "Исправление прав доступа к SSH-ключу..."
    chmod 600 "$SSH_KEY"
    print_success "Права доступа исправлены"
fi

# Проверка и запуск SSH-агента
print_status "Проверка SSH-агента..."

if [ -z "$SSH_AUTH_SOCK" ]; then
    print_status "SSH-агент не запущен. Запускаем..."
    eval "$(ssh-agent -s)" > /dev/null
    print_success "SSH-агент запущен"
else
    print_success "SSH-агент уже запущен: $SSH_AUTH_SOCK"
fi

# Проверка добавленных ключей
print_status "Проверка добавленных ключей..."

if ssh-add -l 2>/dev/null | grep -q "id_ed25519_github"; then
    print_success "SSH-ключ уже добавлен в агент"
else
    print_status "Добавление SSH-ключа в агент..."
    
    # Попытка добавить ключ без passphrase (если уже добавлен ранее)
    if ssh-add "$SSH_KEY" 2>/dev/null; then
        print_success "SSH-ключ добавлен без запроса passphrase"
    else
        print_warning "Требуется ввод passphrase для SSH-ключа"
        echo "Введите passphrase для ключа $SSH_KEY:"
        if ssh-add "$SSH_KEY"; then
            print_success "SSH-ключ успешно добавлен"
            # Настройка персистентного хранения для текущей сессии
            print_status "Настройка персистентного хранения ключа..."
            ssh-add -K "$SSH_KEY" 2>/dev/null || ssh-add "$SSH_KEY" 2>/dev/null
            print_success "Ключ настроен для персистентного хранения"
        else
            print_error "Не удалось добавить SSH-ключ"
            exit 1
        fi
    fi
fi

# Проверка подключения к GitHub
print_status "Проверка подключения к GitHub..."

if ssh -T git@github.com 2>&1 | grep -q "successfully authenticated"; then
    print_success "Подключение к GitHub работает"
else
    print_error "Не удалось подключиться к GitHub"
    echo "Проверьте:"
    echo "1. SSH-ключ добавлен в GitHub аккаунт"
    echo "2. Правильность passphrase"
    exit 1
fi

# Проверка git-операций
print_status "Проверка git-операций..."

if git remote -v | grep -q "github.com"; then
    print_success "GitHub remote настроен"
    
    # Тест git fetch (безопасная операция)
    if git fetch --dry-run 2>/dev/null; then
        print_success "Git-операции работают корректно"
    else
        print_warning "Git-операции могут требовать дополнительной настройки"
    fi
else
    print_warning "GitHub remote не настроен"
fi

# Настройка автоматического запуска
print_status "Настройка автоматического запуска SSH-агента..."

BASH_RC="$HOME/.bashrc"
SSH_SETUP_LINE="# SSH-агент для проекта Vuege"

if ! grep -q "$SSH_SETUP_LINE" "$BASH_RC" 2>/dev/null; then
    print_status "Добавление автоматического запуска в $BASH_RC"
    
    cat >> "$BASH_RC" << 'EOF'

# SSH-агент для проекта Vuege
if [ -z "$SSH_AUTH_SOCK" ]; then
    eval "$(ssh-agent -s)" > /dev/null
    ssh-add ~/.ssh/id_ed25519_github 2>/dev/null
fi
EOF
    
    print_success "Автоматический запуск SSH-агента настроен"
    print_warning "Перезапустите терминал или выполните: source ~/.bashrc"
else
    print_success "Автоматический запуск SSH-агента уже настроен"
fi

echo
print_success "=== Настройка SSH-агента завершена успешно ==="
echo
echo "Проверка статуса:"
echo "  SSH-агент: $(ssh-add -l | wc -l) ключей добавлено"
echo "  GitHub: $(ssh -T git@github.com 2>&1 | grep -o 'successfully authenticated' || echo 'не подключен')"
echo
echo "Для проверки выполните:"
echo "  ssh-add -l"
echo "  ssh -T git@github.com"
echo "  git fetch --dry-run"
