#!/bin/bash

echo "🚀 ЗАПУСК POSTGRESQL В КОНТЕЙНЕРЕ"
echo "================================="

echo "🔧 Запуск PostgreSQL сервиса в контейнере..."
docker exec postgres-java-universal service postgresql start

echo "⏳ Ожидание запуска PostgreSQL..."
sleep 10

echo "🔍 Проверка статуса PostgreSQL..."
docker exec postgres-java-universal service postgresql status

echo "📋 Проверка подключения к базе данных..."
PGPASSWORD=postgres psql -h localhost -p 5432 -U postgres -d vuege -c "SELECT version();"

echo ""
echo "📋 Проверка таблиц в базе данных..."
PGPASSWORD=postgres psql -h localhost -p 5432 -U postgres -d vuege -c "\dt"

echo ""
echo "📋 Проверка данных..."
PGPASSWORD=postgres psql -h localhost -p 5432 -U postgres -d vuege -c "SELECT COUNT(*) as organizational_units_count FROM organizational_units;"
PGPASSWORD=postgres psql -h localhost -p 5432 -U postgres -d vuege -c "SELECT COUNT(*) as persons_count FROM persons;"