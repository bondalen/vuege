#!/bin/bash
echo "🔍 ПРОВЕРКА СОСТОЯНИЯ БАЗЫ ДАННЫХ"
echo "=================================="

cd /home/alex/vuege/src/app

echo "📁 Текущая директория: $(pwd)"

echo ""
echo "🔍 Проверка таблицы historical_periods:"
echo "----------------------------------------"
mvn liquibase:executeSql \
  -Dliquibase.url="jdbc:postgresql://localhost:5432/vuege" \
  -Dliquibase.username="postgres" \
  -Dliquibase.password="postgres" \
  -Dliquibase.driver="org.postgresql.Driver" \
  -Dliquibase.sql="SELECT id, name FROM historical_periods ORDER BY id;"

echo ""
echo "🔍 Проверка таблицы geo_points:"
echo "----------------------------------------"
mvn liquibase:executeSql \
  -Dliquibase.url="jdbc:postgresql://localhost:5432/vuege" \
  -Dliquibase.username="postgres" \
  -Dliquibase.password="postgres" \
  -Dliquibase.driver="org.postgresql.Driver" \
  -Dliquibase.sql="SELECT id, latitude, longitude FROM geo_points ORDER BY id;"

echo ""
echo "✅ Проверка состояния базы данных завершена!"