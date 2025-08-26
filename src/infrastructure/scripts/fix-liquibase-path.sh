#!/bin/bash

echo "🔧 Исправление путей Liquibase..."

# Переходим в директорию backend
cd /home/alex/vuege/src/app/backend

echo "📁 Текущая директория: $(pwd)"

# Запускаем Liquibase с правильными путями
mvn liquibase:update \
  -Dliquibase.url="jdbc:postgresql://localhost:5432/vuege" \
  -Dliquibase.username="postgres" \
  -Dliquibase.password="postgres" \
  -Dliquibase.driver="org.postgresql.Driver" \
  -Dliquibase.changeLogFile="src/main/resources/db/changelog/db.changelog-master.xml"

echo "✅ Готово!"