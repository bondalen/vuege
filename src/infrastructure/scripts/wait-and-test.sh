#!/bin/bash

echo "⏳ ОЖИДАНИЕ ЗАПУСКА SPRING BOOT ПРИЛОЖЕНИЯ..."
echo "============================================="

# Ждем 30 секунд для полного запуска
echo "⏰ Ожидание 30 секунд..."
sleep 30

echo "🔍 Проверка статуса приложения..."

# Проверяем health endpoint
echo "📍 Health check: http://localhost:8082/api/actuator/health"
curl -s http://localhost:8082/api/actuator/health

echo ""
echo "🔍 Проверка GraphQL endpoint..."
echo "📍 URL: http://localhost:8082/api/graphql"

# Тестовый GraphQL запрос
curl -X POST http://localhost:8082/api/graphql \
  -H "Content-Type: application/json" \
  -d '{
    "query": "{ organizationalUnits { id name type status } }"
  }'

echo ""
echo "✅ Тестирование завершено!"