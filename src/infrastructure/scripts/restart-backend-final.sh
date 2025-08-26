#!/bin/bash

echo "🚀 ФИНАЛЬНЫЙ ЗАПУСК SPRING BOOT С АВТОМАТИЧЕСКИМИ МИГРАЦИЯМИ"
echo "=========================================================="

cd /home/alex/vuege/src/app

echo "📁 Текущая директория: $(pwd)"

echo "🛑 Остановка предыдущего процесса..."
pkill -f "spring-boot:run" || true

echo "🧹 Очистка и компиляция..."
mvn clean compile

echo "🚀 Запуск Spring Boot приложения с автоматическими миграциями..."
echo "📍 Порт: 8082"
echo "🌐 GraphQL endpoint: http://localhost:8082/api/graphql"
echo "🔧 GraphiQL: http://localhost:8082/api/graphiql"

# Запуск с автоматическими миграциями
mvn spring-boot:run -Dspring-boot.run.arguments="--server.port=8082 --spring.liquibase.enabled=true --spring.liquibase.change-log=classpath:db/changelog/db.changelog-master.xml"