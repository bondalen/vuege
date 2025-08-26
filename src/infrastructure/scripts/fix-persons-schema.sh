#!/bin/bash

echo "🔧 ИСПРАВЛЕНИЕ СХЕМЫ ТАБЛИЦЫ persons В ТЕСТОВЫХ ДАННЫХ"
echo "========================================================"

cd /home/alex/vuege/src/app

# Создаем резервную копию
cp backend/src/main/resources/db/changelog/changes/010-test-data.xml backend/src/main/resources/db/changelog/changes/010-test-data.xml.backup2

# Исправляем файл - заменяем first_name, last_name на name и is_active на is_fictional
sed -i 's/first_name/name/g' backend/src/main/resources/db/changelog/changes/010-test-data.xml
sed -i 's/last_name/name/g' backend/src/main/resources/db/changelog/changes/010-test-data.xml
sed -i 's/is_active/is_fictional/g' backend/src/main/resources/db/changelog/changes/010-test-data.xml

# Удаляем дублирующиеся колонки name (оставляем только одну)
sed -i '/<column name="name">.*<\/column>/,+1d' backend/src/main/resources/db/changelog/changes/010-test-data.xml

echo "✅ Файл исправлен"
echo ""

echo "🚀 Запуск Liquibase с сбросом контрольных сумм..."
mvn liquibase:update \
    -Dliquibase.changeLogFile="backend/src/main/resources/db/changelog/db.changelog-master.xml" \
    -Dliquibase.url="jdbc:postgresql://localhost:5432/vuege" \
    -Dliquibase.username="postgres" \
    -Dliquibase.password="postgres" \
    -Dliquibase.clearCheckSums="true"

echo ""
echo "🔍 Проверка данных после исправления..."
psql -h localhost -U postgres -d vuege -c "SELECT COUNT(*) as persons_count FROM persons;"
psql -h localhost -U postgres -d vuege -c "SELECT COUNT(*) as person_positions_count FROM person_positions;"

echo ""
echo "✅ Исправление завершено!"