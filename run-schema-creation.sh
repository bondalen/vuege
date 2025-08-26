#!/bin/bash

echo "🔄 СОЗДАНИЕ СХЕМЫ БАЗЫ ДАННЫХ VUEGE"
echo "===================================="

echo "📋 Создание схемы базы данных..."
PGPASSWORD=postgres psql -h localhost -p 5432 -U postgres -d vuege -f /home/alex/vuege/create-schema.sql

echo ""
echo "📋 Загрузка тестовых данных..."
PGPASSWORD=postgres psql -h localhost -p 5432 -U postgres -d vuege -f /home/alex/vuege/insert-test-data.sql

echo ""
echo "📋 Проверка созданных таблиц..."
PGPASSWORD=postgres psql -h localhost -p 5432 -U postgres -d vuege -c "\dt"

echo ""
echo "📋 Проверка данных в таблицах..."
PGPASSWORD=postgres psql -h localhost -p 5432 -U postgres -d vuege -c "SELECT COUNT(*) as organizational_units_count FROM organizational_units;"
PGPASSWORD=postgres psql -h localhost -p 5432 -U postgres -d vuege -c "SELECT COUNT(*) as persons_count FROM persons;"
PGPASSWORD=postgres psql -h localhost -p 5432 -U postgres -d vuege -c "SELECT COUNT(*) as positions_count FROM positions;"

echo ""
echo "📋 Проверка таблицы DATABASECHANGELOG..."
PGPASSWORD=postgres psql -h localhost -p 5432 -U postgres -d vuege -c "SELECT COUNT(*) as changelog_count FROM DATABASECHANGELOG;"

echo ""
echo "✅ Создание схемы завершено!"chmod +x /home/alex/vuege/run-schema-creation.sh
/home/alex/vuege/run-schema-creation.sh