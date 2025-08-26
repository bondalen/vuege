#!/bin/bash

echo "🔧 Исправление путей Liquibase с searchPath..."

# Переходим в корневую директорию проекта
cd /home/alex/vuege/src/app

echo "📁 Текущая директория: $(pwd)"

# Запускаем Liquibase с searchPath
mvn liquibase:update \
  -Dliquibase.url="jdbc:postgresql://localhost:5432/vuege" \
  -Dliquibase.username="postgres" \
  -Dliquibase.password="postgres" \
  -Dliquibase.driver="org.postgresql.Driver" \
  -Dliquibase.changeLogFile="backend/src/main/resources/db/changelog/db.changelog-master.xml" \
  -Dliquibase.searchPath="backend/src/main/resources"

echo "✅ Готово!"