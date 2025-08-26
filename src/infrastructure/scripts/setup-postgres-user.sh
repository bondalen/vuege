#!/bin/bash

echo "🔧 НАСТРОЙКА ПОЛЬЗОВАТЕЛЯ POSTGRESQL"
echo "===================================="

echo "🔧 Создание пользователя postgres в контейнере..."
docker exec postgres-java-universal bash -c "
sudo -u postgres psql -c \"ALTER USER postgres PASSWORD 'postgres';\"
sudo -u postgres psql -c \"CREATE DATABASE vuege;\"
sudo -u postgres psql -c \"GRANT ALL PRIVILEGES ON DATABASE vuege TO postgres;\"
"

echo "⏳ Ожидание применения изменений..."
sleep 5

echo "📋 Проверка подключения к базе данных..."
PGPASSWORD=postgres psql -h localhost -p 5432 -U postgres -d vuege -c "SELECT version();"

echo ""
echo "📋 Проверка таблиц в базе данных..."
PGPASSWORD=postgres psql -h localhost -p 5432 -U postgres -d vuege -c "\dt"