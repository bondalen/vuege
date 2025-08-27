#!/bin/bash

echo "🧪 ПОЛНОЕ ТЕСТИРОВАНИЕ CRUD ОПЕРАЦИЙ VUEGE"
echo "============================================"

# URL GraphQL API
GRAPHQL_URL="http://localhost:8082/api/graphql"

echo ""
echo "🔍 Тест 1: Создание новой организационной единицы"
echo "------------------------------------------------"

# Создание новой записи
CREATE_RESPONSE=$(curl -s -X POST "$GRAPHQL_URL" \
  -H "Content-Type: application/json" \
  -d '{
    "query": "mutation { createOrganizationalUnit(input: { name: \"Тест CRUD\", type: STATE, foundedDate: \"2024-01-01\", historicalPeriodId: 1, isFictional: false }) { id name type foundedDate } }"
  }')

echo "$CREATE_RESPONSE" | jq '.'

# Извлекаем ID созданной записи
NEW_ID=$(echo "$CREATE_RESPONSE" | jq -r '.data.createOrganizationalUnit.id')
echo "Создана запись с ID: $NEW_ID"

echo ""
echo "🔍 Тест 2: Чтение созданной записи"
echo "----------------------------------"

# Чтение созданной записи
curl -X POST "$GRAPHQL_URL" \
  -H "Content-Type: application/json" \
  -d "{
    \"query\": \"{ organizationalUnit(id: \\\"$NEW_ID\\\") { id name type foundedDate } }\"
  }" | jq '.'

echo ""
echo "🔍 Тест 3: Обновление записи"
echo "----------------------------"

# Обновление записи
curl -X POST "$GRAPHQL_URL" \
  -H "Content-Type: application/json" \
  -d "{
    \"query\": \"mutation { updateOrganizationalUnit(id: \\\"$NEW_ID\\\", input: { name: \\\"Обновленная тестовая организация\\\", type: EMPIRE, foundedDate: \\\"2024-02-01\\\", historicalPeriodId: 1, isFictional: true }) { id name type foundedDate } }\"
  }" | jq '.'

echo ""
echo "🔍 Тест 4: Проверка обновления"
echo "------------------------------"

# Проверка обновления
curl -X POST "$GRAPHQL_URL" \
  -H "Content-Type: application/json" \
  -d "{
    \"query\": \"{ organizationalUnit(id: \\\"$NEW_ID\\\") { id name type foundedDate } }\"
  }" | jq '.'

echo ""
echo "🔍 Тест 5: Удаление записи"
echo "--------------------------"

# Удаление записи
curl -X POST "$GRAPHQL_URL" \
  -H "Content-Type: application/json" \
  -d "{
    \"query\": \"mutation { deleteOrganizationalUnit(id: \\\"$NEW_ID\\\") }\"
  }" | jq '.'

echo ""
echo "🔍 Тест 6: Проверка удаления"
echo "----------------------------"

# Проверка удаления
curl -X POST "$GRAPHQL_URL" \
  -H "Content-Type: application/json" \
  -d "{
    \"query\": \"{ organizationalUnit(id: \\\"$NEW_ID\\\") { id name type foundedDate } }\"
  }" | jq '.'

echo ""
echo "🔍 Тест 7: Финальная проверка всех записей"
echo "------------------------------------------"

# Финальная проверка
curl -X POST "$GRAPHQL_URL" \
  -H "Content-Type: application/json" \
  -d '{
    "query": "{ organizationalUnits { id name type foundedDate } }"
  }' | jq '.'

echo ""
echo "✅ Полное тестирование CRUD завершено!"