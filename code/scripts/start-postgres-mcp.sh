#!/bin/bash

# Активация виртуального окружения
source venv/bin/activate

# Загрузка переменных окружения
if [ -f .env ]; then
    export $(cat .env | grep -v '^#' | xargs)
fi

# Запуск PostgreSQL MCP Server
exec /home/alex/projects/vuege/venv/bin/postgres-mcp --access-mode unrestricted postgresql://testuser:testpass@localhost:5432/testdb



