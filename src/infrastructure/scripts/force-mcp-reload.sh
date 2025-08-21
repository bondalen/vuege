#!/bin/bash
"""
@file: force-mcp-reload.sh
@description: Скрипт для принудительного обновления конфигурации MCP серверов
@created: 2025-01-27
"""

echo "🔄 Принудительное обновление конфигурации MCP серверов..."

# Очистка возможных кэшей
echo "🧹 Очистка кэшей..."
rm -rf ~/.cursor/mcp/ 2>/dev/null

# Проверка и исправление прав доступа
echo "🔧 Проверка прав доступа..."
chmod 644 ~/.cursor/mcp.json

# Проверка конфигурации
echo "📋 Проверка конфигурации..."
if [ -f ~/.cursor/mcp.json ]; then
    echo "✅ Файл конфигурации найден"
    echo "📊 Размер файла: $(wc -c < ~/.cursor/mcp.json) байт"
else
    echo "❌ Файл конфигурации не найден"
    exit 1
fi

# Проверка оберток
echo "🔍 Проверка оберток..."
WRAPPERS=(
    "postgres-mcp-wrapper.py"
    "git-mcp-wrapper.py"
    "docker-mcp-wrapper.py"
    "terminal-controller-wrapper.py"
)

for wrapper in "${WRAPPERS[@]}"; do
    if [ -f "src/infrastructure/scripts/$wrapper" ]; then
        echo "✅ $wrapper найден"
        chmod +x "src/infrastructure/scripts/$wrapper"
    else
        echo "❌ $wrapper не найден"
    fi
done

# Проверка Python в виртуальном окружении
echo "🐍 Проверка Python..."
if [ -f "venv/bin/python" ]; then
    echo "✅ Python в venv найден"
    venv/bin/python --version
else
    echo "❌ Python в venv не найден"
fi

echo "✅ Обновление завершено"
echo "💡 Перезапустите Cursor IDE для применения изменений"


