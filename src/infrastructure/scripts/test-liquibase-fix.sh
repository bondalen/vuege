#!/bin/bash
echo "🧪 ТЕСТИРОВАНИЕ ИСПРАВЛЕНИЙ LIQUIBASE"
echo "======================================"

cd /home/alex/vuege/src/app

echo "📁 Текущая директория: $(pwd)"
echo "🔍 Проверка структуры файлов..."

# Проверяем, что файлы существуют
if [ -f "backend/src/main/resources/db/changelog/db.changelog-master.xml" ]; then
    echo "✅ db.changelog-master.xml найден"
else
    echo "❌ db.changelog-master.xml НЕ НАЙДЕН"
    exit 1
fi

if [ -f "backend/src/main/resources/db/changelog/changes/008-geo-points-table.xml" ]; then
    echo "✅ 008-geo-points-table.xml найден"
else
    echo "❌ 008-geo-points-table.xml НЕ НАЙДЕН"
    exit 1
fi

echo ""
echo "🚀 Запуск Liquibase с исправленными файлами..."
echo ""

mvn liquibase:update \
  -Dliquibase.url="jdbc:postgresql://localhost:5432/vuege" \
  -Dliquibase.username="postgres" \
  -Dliquibase.password="postgres" \
  -Dliquibase.driver="org.postgresql.Driver" \
  -Dliquibase.changeLogFile="backend/src/main/resources/db/changelog/db.changelog-master.xml"

echo ""
echo "✅ Тестирование завершено!"