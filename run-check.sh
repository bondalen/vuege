#!/bin/bash

echo "🔍 ПРОВЕРКА ТЕКУЩЕГО СОСТОЯНИЯ"
echo "=============================="

echo "📋 Проверка процессов Spring Boot..."
ps aux | grep "spring-boot:run" | grep -v grep

echo ""
echo "📋 Проверка статуса приложения..."
curl -s http://localhost:8082/api/actuator/health 2>/dev/null || echo "Приложение не отвечает"

echo ""
echo "📋 Проверка таблиц в базе данных..."
PGPASSWORD=postgres psql -h localhost -p 5432 -U postgres -d vuege -c "\dt"

echo ""
echo "📋 Проверка таблицы DATABASECHANGELOG..."
PGPASSWORD=postgres psql -h localhost -p 5432 -U postgres -d vuege -c "SELECT * FROM DATABASECHANGELOG;" 2>/dev/null || echo "Таблица DATABASECHANGELOG не найдена"