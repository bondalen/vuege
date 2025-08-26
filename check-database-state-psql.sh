#!/bin/bash
echo "🔍 ПРОВЕРКА СОСТОЯНИЯ БАЗЫ ДАННЫХ (PSQL)"
echo "=========================================="

echo "🔍 Проверка таблицы historical_periods:"
echo "----------------------------------------"
PGPASSWORD=postgres psql -h localhost -U postgres -d vuege -c "SELECT id, name FROM historical_periods ORDER BY id;"

echo ""
echo "🔍 Проверка таблицы geo_points:"
echo "----------------------------------------"
PGPASSWORD=postgres psql -h localhost -U postgres -d vuege -c "SELECT id, latitude, longitude FROM geo_points ORDER BY id;"

echo ""
echo "✅ Проверка состояния базы данных завершена!"