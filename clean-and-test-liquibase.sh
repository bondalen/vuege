#!/bin/bash
echo "🧹 ОЧИСТКА КЭША И ТЕСТИРОВАНИЕ LIQUIBASE"
echo "=========================================="

cd /home/alex/vuege/src/app

echo "📁 Текущая директория: $(pwd)"

echo "🧹 Очистка кэша Maven..."
mvn clean

echo "🔄 Очистка кэша Liquibase..."
rm -rf ~/.m2/repository/org/liquibase

echo ""
echo "🔍 Проверка исправленного файла..."
echo "Строки 35-45 файла 008-geo-points-table.xml:"
echo "----------------------------------------"
sed -n '35,45p' backend/src/main/resources/db/changelog/changes/008-geo-points-table.xml
echo "----------------------------------------"

echo ""
echo "🚀 Запуск Liquibase с очищенным кэшем..."
echo ""

mvn liquibase:update \
  -Dliquibase.url="jdbc:postgresql://localhost:5432/vuege" \
  -Dliquibase.username="postgres" \
  -Dliquibase.password="postgres" \
  -Dliquibase.driver="org.postgresql.Driver" \
  -Dliquibase.changeLogFile="backend/src/main/resources/db/changelog/db.changelog-master.xml"

echo ""
echo "✅ Тестирование завершено!"