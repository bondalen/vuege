#!/bin/bash

# @file: ensure-postgres-running.sh
# @description: Обеспечение запуска PostgreSQL в контейнере
# @pager-protection: Встроенная защита от pager для предотвращения блокировки автоматизации
# @dependencies: docker, postgres-java-universal
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

echo "🔍 Проверка статуса PostgreSQL контейнера..."

# Проверяем, запущен ли контейнер
if ! docker ps | grep -q postgres-java-universal; then
    echo "❌ Контейнер postgres-java-universal не запущен"
    echo "💡 Запускаем контейнер..."
    docker start postgres-java-universal
    sleep 5
fi

echo "✅ Контейнер postgres-java-universal запущен"

# Проверяем статус PostgreSQL внутри контейнера
echo "🔍 Проверка статуса PostgreSQL внутри контейнера..."
if docker exec postgres-java-universal pg_isready -U testuser -d testdb >/dev/null 2>&1; then
    echo "✅ PostgreSQL работает корректно"
else
    echo "⚠️ PostgreSQL не отвечает, запускаем..."
    docker exec postgres-java-universal service postgresql start
    sleep 3
    
    # Проверяем еще раз
    if docker exec postgres-java-universal pg_isready -U testuser -d testdb >/dev/null 2>&1; then
        echo "✅ PostgreSQL успешно запущен"
    else
        echo "❌ Не удалось запустить PostgreSQL"
        exit 1
    fi
fi

echo "🎉 PostgreSQL готов к работе!"
echo "📊 База данных: postgresql://testuser:testpass@localhost:5432/testdb"

