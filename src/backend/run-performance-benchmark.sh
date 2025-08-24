#!/bin/bash

# Скрипт для запуска бенчмарков производительности GraphQL API

set -e

echo "🚀 Запуск бенчмарков производительности GraphQL API"
echo "=================================================="

# Проверка наличия Maven
if ! command -v mvn &> /dev/null; then
    echo "❌ Maven не найден. Установите Maven для запуска бенчмарков."
    exit 1
fi

# Проверка наличия Java
if ! command -v java &> /dev/null; then
    echo "❌ Java не найдена. Установите Java для запуска бенчмарков."
    exit 1
fi

echo "✅ Зависимости проверены"

# Сборка проекта
echo "📦 Сборка проекта..."
mvn clean compile test-compile

# Запуск бенчмарков
echo "🏃 Запуск бенчмарков производительности..."
mvn test -Dtest=GraphQLPerformanceBenchmark

echo "✅ Бенчмарки завершены"
echo ""
echo "📊 Результаты бенчмарков:"
echo "- Проверьте вывод выше для детальных результатов"
echo "- Целевые показатели:"
echo "  * Время отклика: < 100ms"
echo "  * Throughput: > 10 requests/sec"
echo "  * Memory usage: < 100MB"
echo "  * Concurrent throughput: > 50 requests/sec"

# Проверка метрик через Actuator (если приложение запущено)
echo ""
echo "📈 Проверка метрик производительности:"
echo "curl -u admin:admin123 http://localhost:8082/api/actuator/metrics"
echo "curl -u admin:admin123 http://localhost:8082/api/actuator/health"
echo "curl -u admin:admin123 http://localhost:8082/api/actuator/info"