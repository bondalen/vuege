#!/bin/bash

echo "📊 ЗАГРУЗКА ТЕСТОВЫХ ДАННЫХ В БАЗУ"
echo "=================================="

echo "📋 Проверка наличия SQL файлов..."
ls -la /home/alex/vuege/src/database/init/

echo ""
echo "📋 Загрузка схемы базы данных..."
PGPASSWORD=postgres psql -h localhost -p 5432 -U postgres -d vuege -f /home/alex/vuege/src/database/init/01-schema.sql

echo ""
echo "📋 Загрузка тестовых данных..."
PGPASSWORD=postgres psql -h localhost -p 5432 -U postgres -d vuege -f /home/alex/vuege/src/database/init/02-test-data.sql

echo ""
echo "📋 Проверка загруженных данных..."
PGPASSWORD=postgres psql -h localhost -p 5432 -U postgres -d vuege -c "SELECT COUNT(*) as organizational_units_count FROM organizational_units;"
PGPASSWORD=postgres psql -h localhost -p 5432 -U postgres -d vuege -c "SELECT COUNT(*) as persons_count FROM persons;"

echo ""
echo "📋 Проверка таблиц в базе данных..."
PGPASSWORD=postgres psql -h localhost -p 5432 -U postgres -d vuege -c "\dt"