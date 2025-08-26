#!/bin/bash
echo "🔧 ИСПРАВЛЕНИЕ ФАЙЛА 009-INDEXES-AND-CONSTRAINTS.XML"
echo "=================================================="

cd /home/alex/vuege/src/app

echo "📁 Текущая директория: $(pwd)"

echo "📝 Создание исправленного файла 009-indexes-and-constraints.xml..."
cat > backend/src/main/resources/db/changelog/changes/009-indexes-and-constraints.xml << 'EOF'
<?xml version="1.0" encoding="UTF-8"?>
<databaseChangeLog
        xmlns="http://www.liquibase.org/xml/ns/dbchangelog"
        xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
        xsi:schemaLocation="http://www.liquibase.org/xml/ns/dbchangelog
        http://www.liquibase.org/xml/ns/dbchangelog/dbchangelog-4.20.xsd">

    <changeSet id="009-additional-indexes" author="vuege">
        <!-- Дополнительные индексы для улучшения производительности -->
        
        <!-- Составные индексы для организационных единиц -->
        <createIndex tableName="organizational_units" indexName="idx_org_units_type_period">
            <column name="type"/>
            <column name="historical_period_id"/>
        </createIndex>
        
        <createIndex tableName="organizational_units" indexName="idx_org_units_founded_dissolved">
            <column name="founded_date"/>
            <column name="dissolved_date"/>
        </createIndex>
        
        <!-- Составные индексы для должностей -->
        <createIndex tableName="positions" indexName="idx_positions_org_hierarchy">
            <column name="organization_id"/>
            <column name="hierarchy"/>
        </createIndex>
        
        <createIndex tableName="positions" indexName="idx_positions_created_abolished">
            <column name="created_date"/>
            <column name="abolished_date"/>
        </createIndex>
        
        <!-- Составные индексы для людей -->
        <createIndex tableName="persons" indexName="idx_persons_birth_death">
            <column name="birth_date"/>
            <column name="death_date"/>
        </createIndex>
        
        <createIndex tableName="persons" indexName="idx_persons_period_fictional">
            <column name="historical_period_id"/>
            <column name="is_fictional"/>
        </createIndex>
        
        <!-- Составные индексы для связей человек-должность -->
        <createIndex tableName="person_positions" indexName="idx_person_positions_date_range">
            <column name="start_date"/>
            <column name="end_date"/>
        </createIndex>
        
        <createIndex tableName="person_positions" indexName="idx_person_positions_person_type">
            <column name="person_id"/>
            <column name="appointment_type"/>
        </createIndex>
    </changeSet>

    <changeSet id="009-additional-constraints" author="vuege">
        <!-- Дополнительные проверки -->
        <sql><![CDATA[
            ALTER TABLE persons 
            ADD CONSTRAINT chk_person_dates 
            CHECK ((birth_date IS NULL OR death_date IS NULL) OR (birth_date <= death_date));
            
            ALTER TABLE organizational_units 
            ADD CONSTRAINT chk_org_unit_dates 
            CHECK ((dissolved_date IS NULL) OR (founded_date <= dissolved_date));
            
            ALTER TABLE positions 
            ADD CONSTRAINT chk_position_dates 
            CHECK ((abolished_date IS NULL) OR (created_date <= abolished_date));
            
            ALTER TABLE person_positions 
            ADD CONSTRAINT chk_person_position_dates 
            CHECK ((end_date IS NULL) OR (start_date <= end_date));
            
            ALTER TABLE historical_periods 
            ADD CONSTRAINT chk_historical_period_dates 
            CHECK ((end_date IS NULL) OR (start_date <= end_date));
        ]]></sql>
    </changeSet>

</databaseChangeLog>
EOF

echo "🔍 Проверка созданного файла..."
echo "Строки 55-65:"
echo "----------------------------------------"
sed -n '55,65p' backend/src/main/resources/db/changelog/changes/009-indexes-and-constraints.xml
echo "----------------------------------------"

echo ""
echo "🚀 Запуск Liquibase с исправленным файлом..."
echo ""

mvn liquibase:update \
  -Dliquibase.url="jdbc:postgresql://localhost:5432/vuege" \
  -Dliquibase.username="postgres" \
  -Dliquibase.password="postgres" \
  -Dliquibase.driver="org.postgresql.Driver" \
  -Dliquibase.changeLogFile="backend/src/main/resources/db/changelog/db.changelog-master.xml"

echo ""
echo "✅ Исправление файла 009-indexes-and-constraints.xml завершено!"