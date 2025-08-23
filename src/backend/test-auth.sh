#!/bin/bash

# Тестовый скрипт для проверки авторизации и JWT токенов
# Проверяет доступ к Actuator endpoints с разными ролями

BASE_URL="http://localhost:8082/api"
ACTUATOR_URL="http://localhost:8082/api/actuator"

echo "🔐 ТЕСТИРОВАНИЕ АВТОРИЗАЦИИ VUEGE"
echo "=================================="

# Проверка доступности сервера
echo "1. Проверка доступности сервера..."
curl -s -o /dev/null -w "HTTP Status: %{http_code}\n" "$BASE_URL/test/entities"

# Получение списка доступных пользователей
echo -e "\n2. Получение списка доступных пользователей..."
curl -s "$BASE_URL/auth/users" | jq '.'

# Тест 1: Попытка доступа к Actuator без токена (должен быть доступен только health и info)
echo -e "\n3. Тест доступа к Actuator без токена..."
echo "Health endpoint (должен быть доступен):"
curl -s "$ACTUATOR_URL/health" | jq '.'

echo -e "\nInfo endpoint (должен быть доступен):"
curl -s "$ACTUATOR_URL/info" | jq '.'

echo -e "\nMetrics endpoint (должен быть заблокирован):"
curl -s -w "HTTP Status: %{http_code}\n" "$ACTUATOR_URL/metrics"

# Тест 2: Аутентификация admin пользователя
echo -e "\n4. Аутентификация admin пользователя..."
ADMIN_RESPONSE=$(curl -s -X POST "$BASE_URL/auth/login" \
  -H "Content-Type: application/json" \
  -d '{"username":"admin","password":"admin123"}')

echo "Ответ аутентификации:"
echo "$ADMIN_RESPONSE" | jq '.'

ADMIN_TOKEN=$(echo "$ADMIN_RESPONSE" | jq -r '.accessToken')

if [ "$ADMIN_TOKEN" != "null" ] && [ "$ADMIN_TOKEN" != "" ]; then
    echo -e "\n5. Тест доступа к Actuator с admin токеном..."
    
    echo "Metrics endpoint (должен быть доступен):"
    curl -s -H "Authorization: Bearer $ADMIN_TOKEN" "$ACTUATOR_URL/metrics" | jq '.'
    
    echo -e "\nEnvironment endpoint (должен быть доступен):"
    curl -s -H "Authorization: Bearer $ADMIN_TOKEN" "$ACTUATOR_URL/env" | jq '.'
    
    echo -e "\nBeans endpoint (должен быть доступен):"
    curl -s -H "Authorization: Bearer $ADMIN_TOKEN" "$ACTUATOR_URL/beans" | jq '.'
else
    echo "❌ Ошибка получения admin токена"
fi

# Тест 3: Аутентификация monitor пользователя
echo -e "\n6. Аутентификация monitor пользователя..."
MONITOR_RESPONSE=$(curl -s -X POST "$BASE_URL/auth/login" \
  -H "Content-Type: application/json" \
  -d '{"username":"monitor","password":"monitor123"}')

echo "Ответ аутентификации:"
echo "$MONITOR_RESPONSE" | jq '.'

MONITOR_TOKEN=$(echo "$MONITOR_RESPONSE" | jq -r '.accessToken')

if [ "$MONITOR_TOKEN" != "null" ] && [ "$MONITOR_TOKEN" != "" ]; then
    echo -e "\n7. Тест доступа к Actuator с monitor токеном..."
    
    echo "Metrics endpoint (должен быть доступен):"
    curl -s -H "Authorization: Bearer $MONITOR_TOKEN" "$ACTUATOR_URL/metrics" | jq '.'
    
    echo -e "\nEnvironment endpoint (должен быть доступен):"
    curl -s -H "Authorization: Bearer $MONITOR_TOKEN" "$ACTUATOR_URL/env" | jq '.'
else
    echo "❌ Ошибка получения monitor токена"
fi

# Тест 4: Аутентификация обычного пользователя
echo -e "\n8. Аутентификация user пользователя..."
USER_RESPONSE=$(curl -s -X POST "$BASE_URL/auth/login" \
  -H "Content-Type: application/json" \
  -d '{"username":"user","password":"user123"}')

echo "Ответ аутентификации:"
echo "$USER_RESPONSE" | jq '.'

USER_TOKEN=$(echo "$USER_RESPONSE" | jq -r '.accessToken')

if [ "$USER_TOKEN" != "null" ] && [ "$USER_TOKEN" != "" ]; then
    echo -e "\n9. Тест доступа к Actuator с user токеном (должен быть заблокирован)..."
    
    echo "Metrics endpoint (должен быть заблокирован):"
    curl -s -H "Authorization: Bearer $USER_TOKEN" -w "HTTP Status: %{http_code}\n" "$ACTUATOR_URL/metrics"
else
    echo "❌ Ошибка получения user токена"
fi

# Тест 5: Неверные учетные данные
echo -e "\n10. Тест с неверными учетными данными..."
curl -s -X POST "$BASE_URL/auth/login" \
  -H "Content-Type: application/json" \
  -d '{"username":"admin","password":"wrongpassword"}' | jq '.'

echo -e "\n✅ ТЕСТИРОВАНИЕ ЗАВЕРШЕНО"