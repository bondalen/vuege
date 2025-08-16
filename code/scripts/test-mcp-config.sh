#!/bin/bash

echo "=== Тестирование конфигурации PostgreSQL MCP Server ==="
echo

echo "1. Проверка виртуального окружения..."
if [ -f "venv/bin/activate" ]; then
    echo "✅ Виртуальное окружение найдено"
else
    echo "❌ Виртуальное окружение не найдено"
    exit 1
fi

echo
echo "2. Проверка установки postgres-mcp..."
source venv/bin/activate
if command -v postgres-mcp &> /dev/null; then
    echo "✅ postgres-mcp установлен: $(which postgres-mcp)"
else
    echo "❌ postgres-mcp не найден"
    exit 1
fi

echo
echo "3. Проверка конфигурационных файлов..."
if [ -f "~/.cursor/mcp/postgres-mcp.json" ]; then
    echo "✅ Конфигурация найдена в ~/.cursor/mcp/postgres-mcp.json"
else
    echo "❌ Конфигурация не найдена в ~/.cursor/mcp/postgres-mcp.json"
fi

if [ -f "~/.config/cursor/mcp/postgres-mcp.json" ]; then
    echo "✅ Конфигурация найдена в ~/.config/cursor/mcp/postgres-mcp.json"
else
    echo "❌ Конфигурация не найдена в ~/.config/cursor/mcp/postgres-mcp.json"
fi

echo
echo "4. Тестирование запуска MCP Server..."
if timeout 5s postgres-mcp --help &> /dev/null; then
    echo "✅ MCP Server запускается корректно"
else
    echo "❌ Ошибка запуска MCP Server"
fi

echo
echo "=== Рекомендации ==="
echo "1. Перезапустите Cursor"
echo "2. Проверьте Settings > Tools & Integrations > MCP Tools"
echo "3. Если сервер не появился, проверьте логи Cursor"



