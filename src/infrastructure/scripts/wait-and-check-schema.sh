#!/bin/bash

echo "⏳ ОЖИДАНИЕ СОЗДАНИЯ СХЕМЫ БАЗЫ ДАННЫХ..."
echo "========================================="

# Ждем 60 секунд для полного запуска и создания схемы
echo "⏰ Ожидание 60 секунд..."
sleep 60

echo "🔍 Проверка статуса приложения..."
curl -s http://localhost:8082/api/actuator/health

echo ""
echo "📋 Проверка таблиц в базе данных..."
PGPASSWORD=postgres psql -h localhost -p 5432 -U postgres -d vuege -c "\dt"

echo ""
echo "📋 Проверка схем в базе данных..."
PGPASSWORD=postgres psql -h localhost -p 5432 -U postgres -d vuege -c "\dn"

echo ""
echo "📋 Проверка данных в таблицах..."
PGPASSWORD=postgres psql -h localhost -p 5432 -U postgres -d vuege -c "SELECT COUNT(*) as organizational_units_count FROM organizational_units;" 2>/dev/null || echo "Таблица organizational_units не найдена"
PGPASSWORD=postgres psql -h localhost -p 5432 -U postgres -d vuege -c "SELECT COUNT(*) as persons_count FROM persons;" 2>/dev/null || echo "Таблица persons не найдена"

echo ""
echo "✅ Проверка завершена!"