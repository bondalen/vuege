#!/bin/bash

# Скрипт настройки GitHub CLI
# Безопасная аутентификация без токенов

set -e

echo "🔧 Настройка GitHub CLI"
echo "======================"

# Проверяем, установлен ли GitHub CLI
if ! command -v gh &> /dev/null; then
    echo "❌ GitHub CLI не установлен"
    echo "Сначала выполните: ./src/infrastructure/scripts/install-github-cli.sh"
    exit 1
fi

echo "✅ GitHub CLI установлен"

# Проверяем статус аутентификации
echo "🔍 Проверка статуса аутентификации..."
if gh auth status &> /dev/null; then
    echo "✅ GitHub CLI уже аутентифицирован"
    gh auth status
    exit 0
fi

echo "🔐 Настройка аутентификации GitHub CLI..."

# Запускаем интерактивную аутентификацию
echo ""
echo "📋 Инструкции по аутентификации:"
echo "1. Выберите 'GitHub.com'"
echo "2. Выберите 'HTTPS'"
echo "3. Выберите 'Yes' для аутентификации через браузер"
echo "4. Следуйте инструкциям в браузере"
echo ""

# Запускаем аутентификацию
gh auth login

# Проверяем результат
if gh auth status &> /dev/null; then
    echo ""
    echo "🎉 GitHub CLI успешно настроен!"
    echo ""
    echo "Доступные команды:"
    echo "- gh repo view - просмотр репозитория"
    echo "- gh issue list - список issues"
    echo "- gh issue create - создание issue"
    echo "- gh pr list - список pull requests"
    echo "- gh pr create - создание pull request"
    echo ""
else
    echo "❌ Ошибка аутентификации GitHub CLI"
    exit 1
fi