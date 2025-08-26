#!/bin/bash

echo "🔧 НАСТРОЙКА POSTGRESQL ЧЕРЕЗ ПРЯМОЕ ПОДКЛЮЧЕНИЕ"
echo "==============================================="

echo "🔧 Подключение к PostgreSQL в контейнере..."
docker exec -it postgres-java-universal psql -U postgres -c "ALTER USER postgres PASSWORD 'postgres';"

echo "🔧 Создание базы данных vuege..."
docker exec -it postgres-java-universal psql -U postgres -c "CREATE DATABASE vuege;"

echo "🔧 Предоставление прав пользователю postgres..."
docker exec -it postgres-java-universal psql -U postgres -c "GRANT ALL PRIVILEGES ON DATABASE vuege TO postgres;"

echo "⏳ Ожидание применения изменений..."
sleep 5

echo "📋 Проверка подключения к базе данных..."
PGPASSWORD=postgres psql -h localhost -p 5432 -U postgres -d vuege -c "SELECT version();"