#!/bin/bash

echo "🔧 Финальное исправление путей Liquibase..."

# Переходим в корневую директорию проекта
cd /home/alex/vuege/src/app

echo "📁 Текущая директория: $(pwd)"

# Запускаем Liquibase с правильным путем
mvn liquibase:update \
  -Dliquibase.url="jdbc:postgresql://localhost:5432/vuege" \
  -Dliquibase.username="postgres" \
  -Dliquibase.password="postgres" \
  -Dliquibase.driver="org.postgresql.Driver" \
  -Dliquibase.changeLogFile="db/changelog/db.changelog-master.xml" \
  -Dliquibase.searchPath="backend/src/main/resources"

echo "✅ Готово!"