#!/bin/bash

echo "📋 ПРОВЕРКА ЛОГОВ SPRING BOOT ПРИЛОЖЕНИЯ"
echo "========================================"

echo "🔍 Поиск процесса Spring Boot..."
ps aux | grep "spring-boot:run" | grep -v grep

echo ""
echo "🔍 Проверка логов контейнера (если запущен в Docker)..."
docker logs postgres-java-universal 2>/dev/null || echo "Контейнер postgres-java-universal не найден"

echo ""
echo "🔍 Проверка доступности приложения..."
curl -s http://localhost:8082/api/actuator/health

echo ""
echo "🔍 Проверка статуса базы данных..."
PGPASSWORD=postgres psql -h localhost -p 5432 -U postgres -d vuege -c "SELECT version();"