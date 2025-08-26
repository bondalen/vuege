#!/bin/bash

echo "🧪 ТЕСТИРОВАНИЕ ИСПРАВЛЕННОГО LIQUIBASE"
echo "========================================"

cd /home/alex/vuege/src/app

echo "📁 Текущая директория: $(pwd)"

echo "🔧 Проверка структуры changelog файлов..."
ls -la backend/src/main/resources/db/changelog/changes/

echo ""
echo "🔧 Запуск Liquibase update..."
mvn liquibase:update \
  -Dliquibase.url="jdbc:postgresql://localhost:5432/vuege" \
  -Dliquibase.username="postgres" \
  -Dliquibase.password="postgres" \
  -Dliquibase.driver="org.postgresql.Driver" \
  -Dliquibase.changeLogFile="backend/src/main/resources/db/changelog/db.changelog-master.xml"

echo ""
echo "📋 Проверка созданных таблиц..."
PGPASSWORD=postgres psql -h localhost -p 5432 -U postgres -d vuege -c "\dt"

echo ""
echo "📋 Проверка таблицы DATABASECHANGELOG..."
PGPASSWORD=postgres psql -h localhost -p 5432 -U postgres -d vuege -c "SELECT COUNT(*) as changelog_count FROM DATABASECHANGELOG;"

echo ""
echo "✅ Тестирование завершено!"chmod +x /home/alex/vuege/execute-test.sh
/home/alex/vuege/execute-test.sh