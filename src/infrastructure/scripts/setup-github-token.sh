#!/bin/bash

# Скрипт настройки GitHub Personal Access Token для MCP сервера
# Решает проблему настройки токена для github-mcp-server

set -e

echo "🔧 Настройка GitHub Personal Access Token для MCP сервера"
echo "=================================================="

# Проверяем, есть ли уже токен
if [ -n "$GITHUB_PERSONAL_ACCESS_TOKEN" ]; then
    echo "✅ GitHub токен уже настроен в переменной окружения"
    echo "Токен: ${GITHUB_PERSONAL_ACCESS_TOKEN:0:10}..."
else
    echo "⚠️  GitHub токен не найден в переменной окружения"
fi

# Проверяем токен в .env файле
if [ -f ".env" ]; then
    if grep -q "GITHUB_PERSONAL_ACCESS_TOKEN" .env; then
        echo "✅ GitHub токен найден в .env файле"
        TOKEN_IN_ENV=$(grep "GITHUB_PERSONAL_ACCESS_TOKEN" .env | cut -d'=' -f2)
        if [ "$TOKEN_IN_ENV" != "YOUR_GITHUB_TOKEN_HERE" ]; then
            echo "✅ Токен в .env файле настроен"
        else
            echo "⚠️  Токен в .env файле не настроен (placeholder)"
        fi
    else
        echo "❌ GitHub токен не найден в .env файле"
    fi
else
    echo "❌ Файл .env не найден"
fi

echo ""
echo "📋 Инструкция по настройке токена:"
echo "1. Перейдите на https://github.com/settings/tokens"
echo "2. Нажмите 'Generate new token (classic)'"
echo "3. Настройте права доступа:"
echo "   - repo (Full control of private repositories)"
echo "   - workflow (Update GitHub Action workflows)"
echo "   - notifications (Access notifications)"
echo "   - user (Update all user data)"
echo "4. Скопируйте токен"
echo ""
echo "5. Выполните одну из команд:"
echo ""
echo "   Вариант 1 - Временная настройка:"
echo "   export GITHUB_PERSONAL_ACCESS_TOKEN='ghp_your_token_here'"
echo ""
echo "   Вариант 2 - Постоянная настройка в .env:"
echo "   sed -i 's/YOUR_GITHUB_TOKEN_HERE/ghp_your_token_here/' .env"
echo ""
echo "   Вариант 3 - Добавить в ~/.bashrc:"
echo "   echo 'export GITHUB_PERSONAL_ACCESS_TOKEN=\"ghp_your_token_here\"' >> ~/.bashrc"
echo "   source ~/.bashrc"
echo ""

# Проверяем конфигурацию MCP
if [ -f "$HOME/.cursor/mcp.json" ]; then
    echo "✅ Конфигурация MCP найдена"
    if grep -q "github-mcp-server" "$HOME/.cursor/mcp.json"; then
        echo "✅ GitHub MCP сервер настроен в конфигурации"
    else
        echo "❌ GitHub MCP сервер не найден в конфигурации"
    fi
else
    echo "❌ Конфигурация MCP не найдена"
fi

echo ""
echo "🧪 Тестирование после настройки:"
echo "1. Перезапустите Cursor IDE"
echo "2. Проверьте наличие GitHub MCP сервера в панели MCP Tools"
echo "3. Выполните тестовую команду через MCP"
echo ""

echo "🎯 Настройка завершена!"
echo "Следующий шаг: создайте токен на GitHub и настройте его"