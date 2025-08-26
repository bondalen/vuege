#!/bin/bash

echo "🧹 ПОЛНАЯ ОЧИСТКА БАЗЫ ДАННЫХ И ПЕРЕЗАПУСК LIQUIBASE"
echo "====================================================="
echo "📁 Текущая директория: $(pwd)"
echo ""

echo "🔍 Проверка текущего состояния базы данных..."
cd /home/alex/vuege/src/app
psql -h localhost -U postgres -d vuege -c "SELECT COUNT(*) as historical_periods_count FROM historical_periods;"
psql -h localhost -U postgres -d vuege -c "SELECT COUNT(*) as geo_points_count FROM geo_points;"
echo ""

echo "🗑️ Очистка всех таблиц Liquibase..."
mvn liquibase:dropAll \
    -Dliquibase.changeLogFile="backend/src/main/resources/db/changelog/db.changelog-master.xml" \
    -Dliquibase.url="jdbc:postgresql://localhost:5432/vuege" \
    -Dliquibase.username="postgres" \
    -Dliquibase.password="postgres"

echo ""
echo "✅ База данных очищена"
echo ""

echo "🔍 Проверка после очистки..."
psql -h localhost -U postgres -d vuege -c "SELECT COUNT(*) as historical_periods_count FROM historical_periods;" 2>/dev/null || echo "Таблица historical_periods не существует"
psql -h localhost -U postgres -d vuege -c "SELECT COUNT(*) as geo_points_count FROM geo_points;" 2>/dev/null || echo "Таблица geo_points не существует"
echo ""

echo "🚀 Полный перезапуск Liquibase..."
mvn liquibase:update \
    -Dliquibase.changeLogFile="backend/src/main/resources/db/changelog/db.changelog-master.xml" \
    -Dliquibase.url="jdbc:postgresql://localhost:5432/vuege" \
    -Dliquibase.username="postgres" \
    -Dliquibase.password="postgres"

echo ""
echo "🔍 Финальная проверка данных..."
psql -h localhost -U postgres -d vuege -c "SELECT COUNT(*) as historical_periods_count FROM historical_periods;"
psql -h localhost -U postgres -d vuege -c "SELECT COUNT(*) as geo_points_count FROM geo_points;"
psql -h localhost -U postgres -d vuege -c "SELECT COUNT(*) as organizational_units_count FROM organizational_units;"
psql -h localhost -U postgres -d vuege -c "SELECT COUNT(*) as positions_count FROM positions;"
psql -h localhost -U postgres -d vuege -c "SELECT COUNT(*) as persons_count FROM persons;"
psql -h localhost -U postgres -d vuege -c "SELECT COUNT(*) as person_positions_count FROM person_positions;"

echo ""
echo "✅ Полная очистка и перезапуск завершены!"