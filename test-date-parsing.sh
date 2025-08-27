#!/bin/bash

echo "🧪 ТЕСТИРОВАНИЕ ПАРСИНГА ДАТ В GRAPHQL"
echo "======================================"

# URL GraphQL API
GRAPHQL_URL="http://localhost:8082/api/graphql"

echo ""
echo "🔍 Тест 1: Проверка парсинга даты в GraphQL"
echo "-------------------------------------------"

# Тест с разными форматами дат
curl -X POST "$GRAPHQL_URL" \
  -H "Content-Type: application/json" \
  -d '{
    "query": "mutation { createOrganizationalUnit(input: { name: \"Тест даты\", type: STATE, foundedDate: \"2024-01-01\", historicalPeriodId: 1, isFictional: false }) { id name type foundedDate } }"
  }' | jq '.'

echo ""
echo "🔍 Тест 2: Проверка с датой до нашей эры"
echo "----------------------------------------"

# Тест с датой до нашей эры
curl -X POST "$GRAPHQL_URL" \
  -H "Content-Type: application/json" \
  -d '{
    "query": "mutation { createOrganizationalUnit(input: { name: \"Тест даты до н.э.\", type: STATE, foundedDate: \"-0100-01-01\", historicalPeriodId: 1, isFictional: false }) { id name type foundedDate } }"
  }' | jq '.'

echo ""
echo "🔍 Тест 3: Проверка с простой датой"
echo "-----------------------------------"

# Тест с простой датой
curl -X POST "$GRAPHQL_URL" \
  -H "Content-Type: application/json" \
  -d '{
    "query": "mutation { createOrganizationalUnit(input: { name: \"Простая дата\", type: STATE, foundedDate: \"2024-01-01\", historicalPeriodId: 1, isFictional: false }) { id name type foundedDate } }"
  }' | jq '.'

echo ""
echo "✅ Тестирование завершено!"