#!/bin/bash

echo "Принудительное выполнение Liquibase миграций..."

# Очистка таблицы changelog если существует
PGPASSWORD=postgres psql -h localhost -U postgres -d vuege -c "DROP TABLE IF EXISTS databasechangelog CASCADE;"
PGPASSWORD=postgres psql -h localhost -U postgres -d vuege -c "DROP TABLE IF EXISTS databasechangeloglock CASCADE;"

# Запуск приложения с принудительным выполнением миграций
echo "Запуск приложения с миграциями..."
mvn spring-boot:run -Dspring.liquibase.enabled=true