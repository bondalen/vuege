#!/bin/bash

# Тестовый скрипт для проверки Spring Boot Actuator endpoints
# Проект: Vuege

echo "🔍 Тестирование Spring Boot Actuator endpoints"
echo "=============================================="
echo ""

BASE_URL="http://localhost:8082/api/actuator"

# Функция для проверки endpoint
check_endpoint() {
    local endpoint=$1
    local description=$2
    
    echo "📋 Проверка: $description"
    echo "URL: $BASE_URL$endpoint"
    
    response=$(curl -s -w "%{http_code}" "$BASE_URL$endpoint")
    http_code="${response: -3}"
    body="${response%???}"
    
    if [ "$http_code" -eq 200 ]; then
        echo "✅ Статус: $http_code (OK)"
        if [ -n "$body" ]; then
            echo "📄 Ответ:"
            echo "$body" | jq . 2>/dev/null || echo "$body"
        fi
    else
        echo "❌ Статус: $http_code (ERROR)"
        echo "📄 Ответ: $body"
    fi
    echo ""
}

# Проверяем основные endpoints
echo "🏥 Health Check"
check_endpoint "/health" "Состояние приложения"

echo "ℹ️  Info"
check_endpoint "/info" "Информация о приложении"

echo "📊 Metrics"
check_endpoint "/metrics" "Метрики приложения"

echo "🌍 Environment"
check_endpoint "/env" "Переменные окружения"

echo "⚙️  Configuration Properties"
check_endpoint "/configprops" "Конфигурационные свойства"

echo "🫘 Beans"
check_endpoint "/beans" "Spring Beans"

echo "🧵 Thread Dump"
check_endpoint "/threaddump" "Информация о потоках"

echo "💾 Heap Dump"
check_endpoint "/heapdump" "Дамп памяти"

echo "📋 Список всех endpoints"
check_endpoint "/" "Доступные endpoints"

echo "✅ Тестирование завершено!"
echo ""
echo "💡 Для просмотра в браузере откройте:"
echo "   http://localhost:8082/api/actuator/health"
echo "   http://localhost:8082/api/actuator/info"
echo "   http://localhost:8082/api/actuator/metrics"