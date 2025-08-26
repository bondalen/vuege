#!/bin/bash

echo "🔄 ЗАПУСК LIQUIBASE С ПАРАМЕТРАМИ ПОДКЛЮЧЕНИЯ"
echo "============================================="

cd /home/alex/vuege/src/app

echo "📁 Текущая директория: $(pwd)"

echo "🔧 Запуск Liquibase update с параметрами..."
mvn liquibase:update \
  -Dliquibase.url="jdbc:postgresql://localhost:5432/vuege" \
  -Dliquibase.username="postgres" \
  -Dliquibase.password="postgres" \
  -Dliquibase.driver="org.postgresql.Driver"

echo "⏳ Ожидание завершения..."
sleep 10

echo "📋 Проверка созданных таблиц..."
PGPASSWORD=postgres psql -h localhost -p 5432 -U postgres -d vuege -c "\dt"

echo ""
echo "📋 Проверка схем в базе данных..."
PGPASSWORD=postgres psql -h localhost -p 5432 -U postgres -d vuege -c "\dn"

echo ""
echo "📋 Проверка данных в таблицах..."
PGPASSWORD=postgres psql -h localhost -p 5432 -U postgres -d vuege -c "SELECT COUNT(*) as organizational_units_count FROM organizational_units;" 2>/dev/null || echo "Таблица organizational_units не найдена"
PGPASSWORD=postgres psql -h localhost -p 5432 -U postgres -d vuege -c "SELECT COUNT(*) as persons_count FROM persons;" 2>/dev/null || echo "Таблица persons не найдена"

echo ""
echo "✅ Liquibase выполнен!"