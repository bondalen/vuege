#!/bin/bash
# scripts/start-services.sh

set -e

echo "🚀 Starting Vuege services..."

# Запуск Redis
echo "🔴 Starting Redis..."
redis-server --daemonize yes --dir /var/lib/redis

# Функция для ожидания готовности Redis
wait_for_redis() {
    echo "⏳ Waiting for Redis..."
    until redis-cli ping; do
        sleep 1
    done
    echo "✅ Redis is ready"
}

# Ожидание готовности Redis
wait_for_redis

# Запуск Spring Boot приложения с H2 базой данных
echo "☕ Starting Spring Boot application..."
exec java -Xms512m -Xmx1g \
    -Dspring.profiles.active=production \
    -Dspring.datasource.url="jdbc:h2:mem:vuege;DB_CLOSE_DELAY=-1;DB_CLOSE_ON_EXIT=FALSE" \
    -Dspring.datasource.driver-class-name=org.h2.Driver \
    -Dspring.datasource.username=sa \
    -Dspring.datasource.password="" \
    -Dspring.h2.console.enabled=true \
    -Dspring.redis.host=localhost \
    -Dspring.redis.port=6379 \
    -jar /app/app.jar