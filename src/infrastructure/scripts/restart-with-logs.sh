#!/bin/bash

echo "🚀 ПЕРЕЗАПУСК SPRING BOOT С ПОДРОБНЫМИ ЛОГАМИ"
echo "============================================="

cd /home/alex/vuege/src/app

echo "📁 Текущая директория: $(pwd)"

echo "🛑 Остановка предыдущих процессов..."
pkill -f "spring-boot:run" || true
pkill -f "java.*vuege" || true

echo "🧹 Очистка и компиляция..."
mvn clean compile

echo "🚀 Запуск Spring Boot с подробными логами..."
echo "📍 Порт: 8082"
echo "🌐 GraphQL endpoint: http://localhost:8082/api/graphql"

# Запуск с подробными логами Liquibase
mvn spring-boot:run \
  -Dspring-boot.run.arguments="--server.port=8082 --logging.level.liquibase=DEBUG --logging.level.org.springframework.liquibase=DEBUG" \
  -Dspring-boot.run.jvmArguments="-Dliquibase.debug=true"