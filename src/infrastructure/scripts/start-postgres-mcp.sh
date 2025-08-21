#!/bin/bash

# @file: start-postgres-mcp.sh
# @description: Запуск PostgreSQL MCP сервера с защитой от pager
# @pager-protection: Встроенная защита от pager для предотвращения блокировки автоматизации
# @dependencies: postgres-mcp, docker
# @created: 2025-08-20

# Настройка защиты от pager
export PAGER=cat
export LESS="-R -M --shift 5"
export MORE="-R"
export COMPOSER_NO_INTERACTION=1
export TERM=xterm-256color
export COLUMNS=120
export LINES=30
export GIT_PAGER=cat
export GIT_EDITOR=vim

# Настройка git pager глобально
git config --global core.pager cat 2>/dev/null

# Активация виртуального окружения
source venv/bin/activate

# Загрузка переменных окружения
if [ -f .env ]; then
    export $(cat .env | grep -v '^#' | xargs)
fi

# Проверка доступности PostgreSQL
echo "🔍 Проверка доступности PostgreSQL..."
if ! timeout 5s docker ps | grep -q postgres; then
    echo "❌ PostgreSQL контейнер не запущен"
    echo "💡 Запустите контейнер: docker start postgres-java-universal"
    exit 1
fi

echo "✅ PostgreSQL контейнер запущен"

# Запуск PostgreSQL MCP Server
echo "🚀 Запуск PostgreSQL MCP Server..."
export PGPASSWORD=testpass
exec venv/bin/python src/infrastructure/scripts/postgres-mcp-wrapper.py



