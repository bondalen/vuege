#!/bin/bash

echo "📋 ПРОВЕРКА ЛОГОВ КОНТЕЙНЕРА"
echo "============================"

echo "🔍 Логи контейнера postgres-java-universal:"
docker logs postgres-java-universal

echo ""
echo "⏳ Ожидание 30 секунд для полного запуска..."
sleep 30

echo "🔍 Повторная проверка подключения..."
PGPASSWORD=postgres psql -h localhost -p 5432 -U postgres -d vuege -c "SELECT version();"

echo ""
echo "📋 Проверка таблиц..."
PGPASSWORD=postgres psql -h localhost -p 5432 -U postgres -d vuege -c "\dt"