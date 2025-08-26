#!/bin/bash

echo "🔄 ПЕРЕСОЗДАНИЕ КОНТЕЙНЕРА С ПРАВИЛЬНОЙ КОНФИГУРАЦИЕЙ"
echo "===================================================="

echo "🛑 Остановка и удаление старого контейнера..."
docker stop postgres-java-universal
docker rm postgres-java-universal

echo "🚀 Создание нового контейнера с правильными переменными..."
docker run -d \
  --name postgres-java-universal \
  -p 5432:5432 \
  -e POSTGRES_DB=vuege \
  -e POSTGRES_USER=postgres \
  -e POSTGRES_PASSWORD=postgres \
  -e POSTGRES_HOST_AUTH_METHOD=trust \
  -v /home/alex/vuege/src/database/init:/docker-entrypoint-initdb.d \
  -v /home/alex/vuege/src/database/data:/var/lib/postgresql/data \
  postgres:16

echo "⏳ Ожидание запуска контейнера..."
sleep 15

echo "🔍 Проверка статуса контейнера..."
docker ps | grep postgres

echo "📋 Проверка подключения к базе данных..."
PGPASSWORD=postgres psql -h localhost -p 5432 -U postgres -d vuege -c "SELECT version();"

echo ""
echo "📋 Проверка таблиц в базе данных..."
PGPASSWORD=postgres psql -h localhost -p 5432 -U postgres -d vuege -c "\dt"