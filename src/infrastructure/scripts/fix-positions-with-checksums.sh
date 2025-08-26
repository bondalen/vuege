#!/bin/bash

echo "🔧 ИСПРАВЛЕНИЕ КОЛОНКИ is_fictional -> is_active С СБРОСОМ CHECKSUMS"
echo "======================================================================"

cd /home/alex/vuege/src/app

echo "🚀 Запуск Liquibase с сбросом контрольных сумм..."
mvn liquibase:update \
    -Dliquibase.changeLogFile="backend/src/main/resources/db/changelog/db.changelog-master.xml" \
    -Dliquibase.url="jdbc:postgresql://localhost:5432/vuege" \
    -Dliquibase.username="postgres" \
    -Dliquibase.password="postgres" \
    -Dliquibase.clearCheckSums="true"

echo ""
echo "🔍 Проверка данных после исправления..."
psql -h localhost -U postgres -d vuege -c "SELECT COUNT(*) as positions_count FROM positions;"
psql -h localhost -U postgres -d vuege -c "SELECT COUNT(*) as persons_count FROM persons;"
psql -h localhost -U postgres -d vuege -c "SELECT COUNT(*) as person_positions_count FROM person_positions;"

echo ""
echo "✅ Исправление завершено!"