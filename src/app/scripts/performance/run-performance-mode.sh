#!/bin/bash

# Скрипт для запуска приложения в режиме производительности

set -e

echo "🚀 Запуск Vuege в режиме производительности"
echo "=========================================="

# JVM оптимизации для производительности
export JAVA_OPTS="-Xms512m -Xmx2g -XX:+UseG1GC -XX:MaxGCPauseMillis=200 -XX:+UseStringDeduplication -XX:+OptimizeStringConcat -XX:+UseCompressedOops -XX:+UseCompressedClassPointers"

# Проверка наличия PostgreSQL
if ! pg_isready -h localhost -p 5432 &> /dev/null; then
    echo "❌ PostgreSQL не доступен. Запустите PostgreSQL перед запуском приложения."
    exit 1
fi

echo "✅ PostgreSQL доступен"

# Сборка проекта
echo "📦 Сборка проекта..."
cd /home/alex/vuege/src/app
mvn clean package -DskipTests

# Запуск приложения с профилем производительности
echo "🏃 Запуск приложения с оптимизированными настройками..."
java $JAVA_OPTS -jar target/vuege-0.1.0.jar --spring.profiles.active=performance

echo "✅ Приложение запущено в режиме производительности"
echo ""
echo "📊 Доступные эндпоинты:"
echo "- GraphQL API: http://localhost:8082/api/graphql"
echo "- Actuator: http://localhost:8082/api/actuator"
echo "- Health: http://localhost:8082/api/actuator/health"
echo "- Metrics: http://localhost:8082/api/actuator/metrics"