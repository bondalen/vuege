#!/bin/bash

echo "🔄 ПЕРЕЗАПУСК КОНТЕЙНЕРА БАЗЫ ДАННЫХ"
echo "===================================="

echo "🛑 Остановка контейнера..."
docker stop postgres-java-universal

echo "🧹 Удаление контейнера..."
docker rm postgres-java-universal

echo "🚀 Запуск нового контейнера..."
docker run -d \
  --name postgres-java-universal \
  -p 5432:5432 \
  -e POSTGRES_DB=vuege \
  -e POSTGRES_USER=postgres \
  -e POSTGRES_PASSWORD=postgres \
  -v /home/alex/vuege/src/database/init:/docker-entrypoint-initdb.d \
  -v /home/alex/vuege/src/database/data:/var/lib/postgresql/data \
  postgres-java-universal:latest

echo "⏳ Ожидание запуска контейнера..."
sleep 10

echo "🔍 Проверка статуса контейнера..."
docker ps | grep postgres-java-universal

echo "📋 Проверка подключения к базе данных..."
PGPASSWORD=postgres psql -h localhost -p 5432 -U postgres -d vuege -c "SELECT version();"