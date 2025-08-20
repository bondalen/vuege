#!/bin/bash

# @file: setup-ssh-agent.sh
# @description: Автоматическая настройка SSH агента для работы с GitHub
# @dependencies: SSH ключи в ~/.ssh/
# @created: 2025-01-27

echo "🔧 Настройка SSH агента для GitHub..."

# Функция для проверки работы SSH агента
check_ssh_agent() {
    if ssh-add -l &>/dev/null; then
        echo "✅ SSH агент уже запущен"
        return 0
    else
        echo "❌ SSH агент не запущен"
        return 1
    fi
}

# Функция для запуска SSH агента
start_ssh_agent() {
    echo "🚀 Запуск SSH агента..."
    eval "$(ssh-agent -s)"
    if [ $? -eq 0 ]; then
        echo "✅ SSH агент успешно запущен"
        return 0
    else
        echo "❌ Ошибка запуска SSH агента"
        return 1
    fi
}

# Функция для добавления SSH ключей
add_ssh_keys() {
    local keys_added=0
    
    # Добавляем GitHub ключ
    if [ -f ~/.ssh/id_ed25519_github ]; then
        echo "🔑 Добавление GitHub SSH ключа..."
        if ssh-add ~/.ssh/id_ed25519_github; then
            echo "✅ GitHub ключ добавлен"
            ((keys_added++))
        else
            echo "❌ Ошибка добавления GitHub ключа"
        fi
    fi
    
    # Добавляем авто ключ
    if [ -f ~/.ssh/id_ed25519_auto ]; then
        echo "🔑 Добавление авто SSH ключа..."
        if ssh-add ~/.ssh/id_ed25519_auto; then
            echo "✅ Авто ключ добавлен"
            ((keys_added++))
        else
            echo "❌ Ошибка добавления авто ключа"
        fi
    fi
    
    # Возвращаем true если хотя бы один ключ добавлен
    [ $keys_added -gt 0 ]
}

# Функция для тестирования подключения к GitHub
test_github_connection() {
    echo "🧪 Тестирование подключения к GitHub..."
    if ssh -T git@github.com 2>&1 | grep -q "successfully authenticated"; then
        echo "✅ Подключение к GitHub успешно"
        return 0
    else
        echo "❌ Ошибка подключения к GitHub"
        return 1
    fi
}

# Основная логика
main() {
    echo "=== Настройка SSH агента ==="
    
    # Проверяем SSH агент
    if ! check_ssh_agent; then
        if ! start_ssh_agent; then
            echo "❌ Не удалось запустить SSH агент"
            exit 1
        fi
    fi
    
    # Добавляем ключи
    if add_ssh_keys; then
        echo "✅ SSH ключи добавлены"
    else
        echo "❌ Не удалось добавить SSH ключи"
        exit 1
    fi
    
    # Тестируем подключение
    if test_github_connection; then
        echo "🎉 SSH агент настроен успешно!"
        echo "📋 Статус ключей:"
        ssh-add -l
    else
        echo "❌ Проблемы с подключением к GitHub"
        exit 1
    fi
}

# Запуск скрипта
main "$@"
