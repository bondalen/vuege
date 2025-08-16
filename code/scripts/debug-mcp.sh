#!/bin/bash

echo "=== Диагностика PostgreSQL MCP Server ==="
echo

echo "1. Проверка Docker контейнера..."
if docker ps | grep -q ubuntu-postgres-24.04; then
    echo "✅ Контейнер ubuntu-postgres-24.04 запущен"
else
    echo "❌ Контейнер ubuntu-postgres-24.04 не найден"
    exit 1
fi

echo
echo "2. Проверка PostgreSQL в контейнере..."
if docker exec ubuntu-postgres-24.04 service postgresql status | grep -q "online"; then
    echo "✅ PostgreSQL работает"
else
    echo "❌ PostgreSQL не работает"
    exit 1
fi

echo
echo "3. Проверка виртуального окружения..."
if [ -f "venv/bin/activate" ]; then
    echo "✅ Виртуальное окружение найдено"
    source venv/bin/activate
else
    echo "❌ Виртуальное окружение не найдено"
    exit 1
fi

echo
echo "4. Проверка MCP Server..."
if command -v postgres-mcp &> /dev/null; then
    echo "✅ postgres-mcp установлен: $(which postgres-mcp)"
else
    echo "❌ postgres-mcp не найден"
    exit 1
fi

echo
echo "5. Тестирование подключения к базе данных..."
if timeout 5s postgres-mcp postgresql://testuser:testpass@localhost:5432/testdb &> /dev/null; then
    echo "✅ Подключение к базе данных успешно"
else
    echo "❌ Ошибка подключения к базе данных"
fi

echo
echo "6. Проверка конфигурационных файлов..."
if [ -f "~/.cursor/mcp.json" ]; then
    echo "✅ Конфигурация найдена в ~/.cursor/mcp.json"
else
    echo "❌ Конфигурация не найдена в ~/.cursor/mcp.json"
fi

if [ -f ".cursor/mcp.json" ]; then
    echo "✅ Конфигурация найдена в .cursor/mcp.json"
else
    echo "❌ Конфигурация не найдена в .cursor/mcp.json"
fi

echo
echo "=== Рекомендации ==="
echo "1. Перезапустите Cursor"
echo "2. Проверьте логи Cursor (Help > Toggle Developer Tools > Console)"
echo "3. Убедитесь, что порт 5432 не занят другими процессами"
echo "4. Проверьте, что контейнер PostgreSQL доступен по localhost:5432"

