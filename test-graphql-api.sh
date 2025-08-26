#!/bin/bash

echo "🧪 ТЕСТИРОВАНИЕ GRAPHQL API"
echo "=========================="

echo "🔍 Проверка доступности Spring Boot приложения..."
echo "📍 URL: http://localhost:8082/api/actuator/health"

# Проверка health endpoint
curl -s http://localhost:8082/api/actuator/health | jq .

echo ""
echo "🔍 Проверка GraphQL endpoint..."
echo "📍 URL: http://localhost:8082/api/graphql"

# Тестовый GraphQL запрос
curl -X POST http://localhost:8082/api/graphql \
  -H "Content-Type: application/json" \
  -d '{
    "query": "{ organizationalUnits { id name type status } }"
  }' | jq .

echo ""
echo "🔍 Проверка GraphiQL..."
echo "📍 URL: http://localhost:8082/api/graphiql"
echo "🌐 Откройте браузер и перейдите по ссылке для интерактивного тестирования"