#!/bin/bash

echo "🚀 ЗАПУСК SPRING BOOT С СОЗДАНИЕМ СХЕМЫ"
echo "======================================="

cd /home/alex/vuege/src/app

echo "📁 Текущая директория: $(pwd)"
echo "🔍 Проверка Maven..."
mvn --version

echo "🧹 Очистка и компиляция..."
mvn clean compile

echo "🚀 Запуск Spring Boot приложения с автоматическим созданием схемы..."
echo "📍 Порт: 8082"
echo "🌐 GraphQL endpoint: http://localhost:8082/api/graphql"
echo "🔧 GraphiQL: http://localhost:8082/api/graphiql"

# Запуск с автоматическим созданием схемы
mvn spring-boot:run -Dspring-boot.run.arguments="--server.port=8082 --spring.liquibase.enabled=true"