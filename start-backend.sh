#!/bin/bash

echo "🚀 ЗАПУСК SPRING BOOT BACKEND"
echo "=============================="

cd /home/alex/vuege/src/app

echo "🔧 Сборка проекта..."
mvn clean compile

echo ""
echo "🚀 Запуск Spring Boot приложения на порту 8082..."
mvn spring-boot:run -Dspring-boot.run.jvmArguments="-Dserver.port=8082" &

# Ждем запуска приложения
echo "⏳ Ожидание запуска приложения..."
sleep 30

echo ""
echo "🔍 Проверка состояния приложения..."
curl -s http://localhost:8082/actuator/health | jq . 2>/dev/null || echo "Приложение еще запускается..."

echo ""
echo "📊 Проверка GraphQL endpoint..."
curl -s -X POST http://localhost:8082/api/graphql \
  -H "Content-Type: application/json" \
  -d '{"query":"{ organizationalUnits { id name type } }"}' | jq . 2>/dev/null || echo "GraphQL endpoint недоступен"

echo ""
echo "🌐 GraphiQL доступен по адресу: http://localhost:8082/api/graphiql"
echo "📡 GraphQL endpoint: http://localhost:8082/api/graphql"
echo ""
echo "✅ Backend запущен!"