#!/bin/bash

echo "Исправление проблем с Liquibase и датами..."

# Остановка приложения если запущено
echo "Остановка приложения..."
pkill -f "spring-boot:run" || true
sleep 3

# Очистка таблиц Liquibase для принудительного выполнения миграций
echo "Очистка таблиц Liquibase..."
PGPASSWORD=postgres psql -h localhost -U postgres -d vuege -c "DROP TABLE IF EXISTS databasechangelog CASCADE;" || true
PGPASSWORD=postgres psql -h localhost -U postgres -d vuege -c "DROP TABLE IF EXISTS databasechangeloglock CASCADE;" || true

# Перезапуск приложения с обновленной конфигурацией
echo "Запуск приложения с исправленной конфигурацией..."
cd /home/alex/vuege/src/backend
mvn spring-boot:run -Dspring.liquibase.enabled=true -Dspring.liquibase.drop-first=false