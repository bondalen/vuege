#!/bin/bash

echo "🧹 Очистка кэша Maven..."
mvn clean

echo "🔄 Очистка кэша Liquibase..."
rm -rf ~/.m2/repository/org/liquibase/

echo "🚀 Запуск Liquibase..."
mvn liquibase:update \
  -Dliquibase.url="jdbc:postgresql://localhost:5432/vuege" \
  -Dliquibase.username="postgres" \
  -Dliquibase.password="postgres" \
  -Dliquibase.driver="org.postgresql.Driver" \
  -Dliquibase.changeLogFile="backend/src/main/resources/db/changelog/db.changelog-master.xml"

echo "✅ Готово!"