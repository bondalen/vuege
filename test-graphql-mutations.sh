#!/bin/bash

echo "🧪 ТЕСТИРОВАНИЕ GRAPHQL МУТАЦИЙ VUEGE"
echo "======================================"

# URL GraphQL API
GRAPHQL_URL="http://localhost:8082/api/graphql"

# Проверка доступности сервера
echo "📡 Проверка доступности сервера..."
if curl -s "$GRAPHQL_URL" > /dev/null; then
    echo "✅ Сервер доступен"
else
    echo "❌ Сервер недоступен. Запустите приложение: ./run-backend.sh"
    exit 1
fi

echo ""
echo "🔍 Тест 1: Создание организационной единицы с корректными данными"
echo "------------------------------------------------------------"

# Тест с корректными данными
curl -X POST "$GRAPHQL_URL" \
  -H "Content-Type: application/json" \
  -d '{
    "query": "mutation { createOrganizationalUnit(input: { name: \"Тестовая организация\", type: EMPIRE, foundedDate: \"2024-01-01\", historicalPeriodId: 1, isFictional: false }) { id name type foundedDate } }"
  }' | jq '.'

echo ""
echo "🔍 Тест 2: Создание организационной единицы с null датой"
echo "--------------------------------------------------------"

# Тест с null датой
curl -X POST "$GRAPHQL_URL" \
  -H "Content-Type: application/json" \
  -d '{
    "query": "mutation { createOrganizationalUnit(input: { name: \"Тестовая организация 2\", type: EMPIRE, foundedDate: null, historicalPeriodId: 1, isFictional: false }) { id name type foundedDate } }"
  }' | jq '.'

echo ""
echo "🔍 Тест 3: Создание организационной единицы без обязательных полей"
echo "------------------------------------------------------------------"

# Тест без обязательных полей
curl -X POST "$GRAPHQL_URL" \
  -H "Content-Type: application/json" \
  -d '{
    "query": "mutation { createOrganizationalUnit(input: { name: \"\", type: null, foundedDate: null, historicalPeriodId: null, isFictional: false }) { id name type foundedDate } }"
  }' | jq '.'

echo ""
echo "🔍 Тест 4: Чтение всех организационных единиц"
echo "---------------------------------------------"

# Тест чтения
curl -X POST "$GRAPHQL_URL" \
  -H "Content-Type: application/json" \
  -d '{
    "query": "{ organizationalUnits { id name type foundedDate } }"
  }' | jq '.'

echo ""
echo "✅ Тестирование завершено!"