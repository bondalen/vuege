#!/bin/bash

# Безопасная настройка GitHub Personal Access Token
# Включает мониторинг и проверки безопасности

set -e

echo "🛡️ Безопасная настройка GitHub Personal Access Token"
echo "=================================================="

# Цвета для вывода
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Функции логирования
log_info() {
    echo -e "${GREEN}ℹ️  $1${NC}"
}

log_warning() {
    echo -e "${YELLOW}⚠️  $1${NC}"
}

log_error() {
    echo -e "${RED}❌ $1${NC}"
}

# Проверка существующего токена
check_existing_token() {
    log_info "Проверка существующего токена..."
    
    if [ -n "$GITHUB_PERSONAL_ACCESS_TOKEN" ]; then
        log_info "Токен найден в переменной окружения"
        
        # Проверка валидности
        RESPONSE=$(curl -s -H "Authorization: token $GITHUB_PERSONAL_ACCESS_TOKEN" \
            https://api.github.com/user)
        
        if echo "$RESPONSE" | grep -q "Bad credentials"; then
            log_warning "Токен невалиден (возможно, истек или отозван)"
            return 1
        else
            log_info "Токен валиден"
            return 0
        fi
    else
        log_warning "Токен не найден в переменной окружения"
        return 1
    fi
}

# Создание лог файла
setup_logging() {
    LOG_FILE="$HOME/.github-api.log"
    log_info "Настройка логирования в $LOG_FILE"
    
    # Создаем лог файл если не существует
    if [ ! -f "$LOG_FILE" ]; then
        touch "$LOG_FILE"
        echo "$(date): Лог файл создан" >> "$LOG_FILE"
    fi
    
    # Ограничиваем размер лога
    if [ $(wc -l < "$LOG_FILE") -gt 1000 ]; then
        tail -500 "$LOG_FILE" > "$LOG_FILE.tmp" && mv "$LOG_FILE.tmp" "$LOG_FILE"
        log_info "Лог файл обрезан до 500 строк"
    fi
}

# Проверка прав токена
check_token_permissions() {
    log_info "Проверка прав токена..."
    
    RESPONSE=$(curl -s -H "Authorization: token $GITHUB_PERSONAL_ACCESS_TOKEN" \
        https://api.github.com/user)
    
    if echo "$RESPONSE" | grep -q "Bad credentials"; then
        log_error "Токен невалиден"
        return 1
    fi
    
    # Проверяем доступ к репозиторию
    REPO_RESPONSE=$(curl -s -H "Authorization: token $GITHUB_PERSONAL_ACCESS_TOKEN" \
        https://api.github.com/repos/bondalen/vuege)
    
    if echo "$REPO_RESPONSE" | grep -q "Not Found"; then
        log_warning "Нет доступа к репозиторию bondalen/vuege"
        return 1
    else
        log_info "Доступ к репозиторию подтвержден"
    fi
    
    # Логируем проверку
    echo "$(date): Проверка прав токена - OK" >> "$HOME/.github-api.log"
}

# Настройка переменной окружения
setup_environment() {
    log_info "Настройка переменной окружения..."
    
    # Добавляем в .bashrc если еще нет
    if ! grep -q "GITHUB_PERSONAL_ACCESS_TOKEN" ~/.bashrc; then
        echo "" >> ~/.bashrc
        echo "# GitHub Personal Access Token" >> ~/.bashrc
        echo 'export GITHUB_PERSONAL_ACCESS_TOKEN="YOUR_NEW_TOKEN_HERE"' >> ~/.bashrc
        log_info "Переменная добавлена в ~/.bashrc"
    else
        log_info "Переменная уже настроена в ~/.bashrc"
    fi
    
    # Обновляем .env файл
    if [ -f ".env" ]; then
        sed -i 's/GITHUB_PERSONAL_ACCESS_TOKEN=.*/GITHUB_PERSONAL_ACCESS_TOKEN=YOUR_NEW_TOKEN_HERE/' .env
        log_info "Файл .env обновлен"
    fi
}

# Тестирование токена
test_token() {
    log_info "Тестирование токена..."
    
    # Тест 1: Получение информации о пользователе
    USER_RESPONSE=$(curl -s -H "Authorization: token $GITHUB_PERSONAL_ACCESS_TOKEN" \
        https://api.github.com/user)
    
    if echo "$USER_RESPONSE" | grep -q "login"; then
        USER_LOGIN=$(echo "$USER_RESPONSE" | grep -o '"login":"[^"]*"' | cut -d'"' -f4)
        log_info "Пользователь: $USER_LOGIN"
    else
        log_error "Не удалось получить информацию о пользователе"
        return 1
    fi
    
    # Тест 2: Создание тестового issue
    log_info "Создание тестового issue..."
    ISSUE_DATA='{"title":"Тест безопасности токена","body":"Этот issue создан для тестирования безопасности токена"}'
    
    ISSUE_RESPONSE=$(curl -s -X POST \
        -H "Authorization: token $GITHUB_PERSONAL_ACCESS_TOKEN" \
        -H "Accept: application/vnd.github.v3+json" \
        -d "$ISSUE_DATA" \
        https://api.github.com/repos/bondalen/vuege/issues)
    
    if echo "$ISSUE_RESPONSE" | grep -q "number"; then
        ISSUE_NUMBER=$(echo "$ISSUE_RESPONSE" | grep -o '"number":[0-9]*' | cut -d':' -f2)
        log_info "Создан тестовый issue #$ISSUE_NUMBER"
        
        # Закрываем тестовый issue
        CLOSE_DATA='{"state":"closed"}'
        curl -s -X PATCH \
            -H "Authorization: token $GITHUB_PERSONAL_ACCESS_TOKEN" \
            -H "Accept: application/vnd.github.v3+json" \
            -d "$CLOSE_DATA" \
            https://api.github.com/repos/bondalen/vuege/issues/$ISSUE_NUMBER > /dev/null
        
        log_info "Тестовый issue #$ISSUE_NUMBER закрыт"
    else
        log_error "Не удалось создать тестовый issue"
        return 1
    fi
    
    # Логируем тестирование
    echo "$(date): Тестирование токена - OK" >> "$HOME/.github-api.log"
}

# Основная функция
main() {
    log_info "Начало безопасной настройки GitHub токена"
    
    # Настройка логирования
    setup_logging
    
    # Проверка существующего токена
    if check_existing_token; then
        log_info "Существующий токен валиден"
        
        # Проверка прав
        if check_token_permissions; then
            log_info "Права токена в порядке"
            
            # Тестирование
            if test_token; then
                log_info "🎉 Токен полностью функционален!"
                return 0
            fi
        fi
    fi
    
    log_warning "Требуется новый токен"
    log_info "Инструкции по созданию нового токена:"
    echo ""
    echo "1. Перейдите на https://github.com/settings/tokens"
    echo "2. Нажмите 'Generate new token (classic)'"
    echo "3. Настройте права:"
    echo "   - repo (только для bondalen/vuege)"
    echo "   - user (только чтение)"
    echo "4. Скопируйте токен"
    echo "5. Замените YOUR_NEW_TOKEN_HERE в ~/.bashrc и .env"
    echo "6. Запустите этот скрипт снова"
    echo ""
    
    # Настройка переменной окружения
    setup_environment
    
    log_info "Настройка завершена. Создайте новый токен и обновите конфигурацию."
}

# Запуск основной функции
main "$@"