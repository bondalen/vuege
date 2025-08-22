#!/bin/bash
# Скрипт для загрузки токенов MCP серверов
# Безопасная загрузка переменных окружения

MCP_ENV_FILE="$HOME/.cursor/mcp.env"

echo "🔐 Загрузка токенов MCP серверов..."

# Проверяем существование файла с токенами
if [ ! -f "$MCP_ENV_FILE" ]; then
    echo "❌ Файл токенов не найден: $MCP_ENV_FILE"
    echo "📝 Создайте файл с вашими токенами:"
    echo "   GITHUB_PERSONAL_ACCESS_TOKEN=ghp_your_actual_token"
    echo "   JIRA_API_KEY=your_actual_jira_key"
    exit 1
fi

# Загружаем переменные окружения
if source "$MCP_ENV_FILE"; then
    echo "✅ Токены загружены успешно"
    
    # Проверяем наличие токенов
    if [ -n "$GITHUB_PERSONAL_ACCESS_TOKEN" ] && [ "$GITHUB_PERSONAL_ACCESS_TOKEN" != "YOUR_ACTUAL_GITHUB_TOKEN_HERE" ]; then
        echo "✅ GitHub токен настроен"
    else
        echo "⚠️ GitHub токен не настроен или использует placeholder"
    fi
    
    if [ -n "$JIRA_API_KEY" ] && [ "$JIRA_API_KEY" != "your-actual-jira-api-key-here" ]; then
        echo "✅ JIRA токен настроен"
    else
        echo "⚠️ JIRA токен не настроен или использует placeholder"
    fi
    
    # Экспортируем переменные для текущей сессии
    export GITHUB_PERSONAL_ACCESS_TOKEN
    export JIRA_API_KEY
    
    echo "🚀 Токены готовы к использованию в MCP серверах"
else
    echo "❌ Ошибка загрузки токенов"
    exit 1
fi
