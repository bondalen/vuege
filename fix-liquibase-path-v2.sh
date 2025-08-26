#!/bin/bash

echo "🔧 Исправление путей Liquibase (версия 2)..."

# Переходим в корневую директорию проекта
cd /home/alex/vuege/src/app

echo "📁 Текущая директория: $(pwd)"

# Запускаем Liquibase с правильными путями
mvn liquibase:update \
  -Dliquibase.url="jdbc:postgresql://localhost:5432/vuege" \
  -Dliquibase.username="postgres" \
  -Dliquibase.password="postgres" \
  -Dliquibase.driver="org.postgresql.Driver" \
  -Dliquibase.changeLogFile="backend/src/main/resources/db/changelog/db.changelog-master.xml"

echo "✅ Готово!"