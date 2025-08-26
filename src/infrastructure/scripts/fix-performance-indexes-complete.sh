#!/bin/bash

echo "🔧 ПОЛНОЕ ИСПРАВЛЕНИЕ ДУБЛИРУЮЩИХСЯ И НЕСУЩЕСТВУЮЩИХ ИНДЕКСОВ"
echo "==============================================================="

cd /home/alex/vuege/src/app

# Создаем резервную копию
cp backend/src/main/resources/db/changelog/changes/011-add-performance-indexes.xml backend/src/main/resources/db/changelog/changes/011-add-performance-indexes.xml.backup3

# Создаем исправленный файл без дублирующихся и несуществующих индексов
cat > backend/src/main/resources/db/changelog/changes/011-add-performance-indexes.xml << 'EOF'
<?xml version="1.0" encoding="UTF-8"?>
<databaseChangeLog
        xmlns="http://www.liquibase.org/xml/ns/dbchangelog"
        xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
        xsi:schemaLocation="http://www.liquibase.org/xml/ns/dbchangelog
        http://www.liquibase.org/xml/ns/dbchangelog/dbchangelog-4.20.xsd">

    <changeSet id="011-add-performance-indexes" author="bondalen">
        <comment>Добавление дополнительных индексов для оптимизации производительности</comment>

        <!-- Дополнительные индексы для organizational_units (удалены дублирующиеся) -->
        <createIndex tableName="organizational_units" indexName="idx_org_units_historical_period">
            <column name="historical_period_id"/>
        </createIndex>

        <createIndex tableName="organizational_units" indexName="idx_org_units_location">
            <column name="location_id"/>
        </createIndex>

        <!-- Составной индекс для часто используемых запросов -->
        <createIndex tableName="organizational_units" indexName="idx_org_units_type_fictional">
            <column name="type"/>
            <column name="is_fictional"/>
        </createIndex>

        <!-- Индексы для persons (удалены дублирующиеся - уже созданы в 005-persons-table.xml) -->
        <createIndex tableName="persons" indexName="idx_persons_historical_period">
            <column name="historical_period_id"/>
        </createIndex>

        <!-- Индексы для person_positions -->
        <createIndex tableName="person_positions" indexName="idx_person_positions_start_date">
            <column name="start_date"/>
        </createIndex>

        <createIndex tableName="person_positions" indexName="idx_person_positions_end_date">
            <column name="end_date"/>
        </createIndex>

        <!-- Составной индекс для активных должностей -->
        <createIndex tableName="person_positions" indexName="idx_person_positions_active">
            <column name="person_id"/>
            <column name="start_date"/>
            <column name="end_date"/>
        </createIndex>

        <!-- Индексы для historical_periods (удалены дублирующиеся) -->
        <createIndex tableName="historical_periods" indexName="idx_historical_periods_period">
            <column name="start_date"/>
            <column name="end_date"/>
        </createIndex>

    </changeSet>

</databaseChangeLog>
EOF

echo "✅ Файл исправлен - удалены все дублирующиеся и несуществующие индексы"
echo ""

echo "🚀 Запуск Liquibase для применения исправлений..."
mvn liquibase:update \
    -Dliquibase.changeLogFile="backend/src/main/resources/db/changelog/db.changelog-master.xml" \
    -Dliquibase.url="jdbc:postgresql://localhost:5432/vuege" \
    -Dliquibase.username="postgres" \
    -Dliquibase.password="postgres" \
    -Dliquibase.clearCheckSums="true"

echo ""
echo "🔍 Проверка всех индексов после исправления..."
echo "=== Индексы organizational_units ==="
psql -h localhost -U postgres -d vuege -c "SELECT indexname FROM pg_indexes WHERE tablename = 'organizational_units' ORDER BY indexname;"

echo ""
echo "=== Индексы persons ==="
psql -h localhost -U postgres -d vuege -c "SELECT indexname FROM pg_indexes WHERE tablename = 'persons' ORDER BY indexname;"

echo ""
echo "=== Индексы positions ==="
psql -h localhost -U postgres -d vuege -c "SELECT indexname FROM pg_indexes WHERE tablename = 'positions' ORDER BY indexname;"

echo ""
echo "=== Индексы person_positions ==="
psql -h localhost -U postgres -d vuege -c "SELECT indexname FROM pg_indexes WHERE tablename = 'person_positions' ORDER BY indexname;"

echo ""
echo "=== Индексы historical_periods ==="
psql -h localhost -U postgres -d vuege -c "SELECT indexname FROM pg_indexes WHERE tablename = 'historical_periods' ORDER BY indexname;"

echo ""
echo "✅ Полное исправление завершено!"