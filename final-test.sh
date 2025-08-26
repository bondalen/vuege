#!/bin/bash

echo "🧪 ФИНАЛЬНОЕ ТЕСТИРОВАНИЕ GRAPHQL API"
echo "====================================="

echo "⏳ Ожидание 90 секунд для полного запуска..."
sleep 90

echo "🔍 Проверка статуса приложения..."
curl -s http://localhost:8082/api/actuator/health | jq .

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
echo "🔍 Тестирование GraphQL API..."
curl -X POST http://localhost:8082/api/graphql \
  -H "Content-Type: application/json" \
  -d '{
    "query": "{ organizationalUnits { id name type status } }"
  }' | jq .

echo ""
echo "✅ Финальное тестирование завершено!"