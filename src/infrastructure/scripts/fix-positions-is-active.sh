#!/bin/bash

echo "🔧 ИСПРАВЛЕНИЕ КОЛОНКИ is_fictional -> is_active В ТАБЛИЦЕ positions"
echo "====================================================================="

cd /home/alex/vuege/src/app

# Создаем резервную копию
cp backend/src/main/resources/db/changelog/changes/010-test-data.xml backend/src/main/resources/db/changelog/changes/010-test-data.xml.backup

# Исправляем файл
sed -i 's/is_fictional/is_active/g' backend/src/main/resources/db/changelog/changes/010-test-data.xml

echo "✅ Файл исправлен"
echo ""

echo "🚀 Запуск Liquibase для применения исправлений..."
mvn liquibase:update \
    -Dliquibase.changeLogFile="backend/src/main/resources/db/changelog/db.changelog-master.xml" \
    -Dliquibase.url="jdbc:postgresql://localhost:5432/vuege" \
    -Dliquibase.username="postgres" \
    -Dliquibase.password="postgres"

echo ""
echo "🔍 Проверка данных после исправления..."
psql -h localhost -U postgres -d vuege -c "SELECT COUNT(*) as positions_count FROM positions;"
psql -h localhost -U postgres -d vuege -c "SELECT COUNT(*) as persons_count FROM persons;"
psql -h localhost -U postgres -d vuege -c "SELECT COUNT(*) as person_positions_count FROM person_positions;"

echo ""
echo "✅ Исправление завершено!"