#!/bin/bash

echo "🔍 ПРОВЕРКА СТАТУСА БАЗЫ ДАННЫХ"
echo "==============================="

echo "📋 Проверка контейнера postgres-java-universal..."
docker ps | grep postgres-java-universal

echo ""
echo "📋 Проверка подключения к PostgreSQL..."
echo "📍 Host: localhost"
echo "📍 Port: 5432"
echo "📍 Database: vuege"
echo "📍 User: postgres"

# Проверка подключения к базе данных
PGPASSWORD=postgres psql -h localhost -p 5432 -U postgres -d vuege -c "SELECT version();"

echo ""
echo "📋 Проверка таблиц в базе данных..."
PGPASSWORD=postgres psql -h localhost -p 5432 -U postgres -d vuege -c "\dt"

echo ""
echo "📋 Проверка данных в таблицах..."
PGPASSWORD=postgres psql -h localhost -p 5432 -U postgres -d vuege -c "SELECT COUNT(*) as organizational_units_count FROM organizational_units;"
PGPASSWORD=postgres psql -h localhost -p 5432 -U postgres -d vuege -c "SELECT COUNT(*) as persons_count FROM persons;"