#!/bin/bash

echo "🚀 ПЕРЕЗАПУСК SPRING BOOT ПРИЛОЖЕНИЯ"
echo "==================================="

cd /home/alex/vuege/src/app

echo "📁 Текущая директория: $(pwd)"
echo "🔍 Проверка Maven..."
mvn --version

echo "🧹 Очистка и компиляция с обновленным Node.js..."
mvn clean compile

echo "🚀 Запуск Spring Boot приложения на порту 8082..."
echo "📍 Порт: 8082"
echo "🌐 GraphQL endpoint: http://localhost:8082/api/graphql"
echo "🔧 GraphiQL: http://localhost:8082/api/graphiql"

mvn spring-boot:run -Dspring-boot.run.arguments="--server.port=8082"