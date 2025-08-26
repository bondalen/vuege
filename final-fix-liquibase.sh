#!/bin/bash
echo "🎯 ФИНАЛЬНОЕ ИСПРАВЛЕНИЕ LIQUIBASE (CDATA-ПОДХОД)"
echo "=================================================="

cd /home/alex/vuege/src/app

echo "📁 Текущая директория: $(pwd)"

echo "🗑️ Удаление проблемного файла..."
rm -f backend/src/main/resources/db/changelog/changes/008-geo-points-table.xml

echo "🧹 Очистка кэша Maven..."
mvn clean

echo "🔄 Очистка кэша Liquibase..."
rm -rf ~/.m2/repository/org/liquibase

echo "📝 Создание финального файла с CDATA-подходом..."
cat > backend/src/main/resources/db/changelog/changes/008-geo-points-table.xml << 'EOF'
<?xml version="1.0" encoding="UTF-8"?>
<databaseChangeLog
        xmlns="http://www.liquibase.org/xml/ns/dbchangelog"
        xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
        xsi:schemaLocation="http://www.liquibase.org/xml/ns/dbchangelog
        http://www.liquibase.org/xml/ns/dbchangelog/dbchangelog-4.20.xsd">

    <changeSet id="008-create-geo-points-table" author="vuege">
        <createTable tableName="geo_points">
            <column name="id" type="BIGSERIAL">
                <constraints primaryKey="true" nullable="false"/>
            </column>
            <column name="latitude" type="DOUBLE PRECISION">
                <constraints nullable="false"/>
            </column>
            <column name="longitude" type="DOUBLE PRECISION">
                <constraints nullable="false"/>
            </column>
            <column name="elevation" type="DOUBLE PRECISION">
                <constraints nullable="true"/>
            </column>
            <column name="accuracy" type="VARCHAR(20)">
                <constraints nullable="false"/>
            </column>
            <column name="created_at" type="TIMESTAMP" defaultValueComputed="CURRENT_TIMESTAMP">
                <constraints nullable="false"/>
            </column>
            <column name="updated_at" type="TIMESTAMP" defaultValueComputed="CURRENT_TIMESTAMP">
                <constraints nullable="false"/>
            </column>
        </createTable>
    </changeSet>

    <changeSet id="008-add-geo-points-constraints-sql" author="vuege">
        <sql><![CDATA[
            ALTER TABLE geo_points 
            ADD CONSTRAINT chk_latitude_range 
            CHECK (latitude >= -90 AND latitude <= 90);
            
            ALTER TABLE geo_points 
            ADD CONSTRAINT chk_longitude_range 
            CHECK (longitude >= -180 AND longitude <= 180);
        ]]></sql>
    </changeSet>

    <changeSet id="008-add-geo-points-indexes" author="vuege">
        <createIndex tableName="geo_points" indexName="idx_geo_points_coordinates">
            <column name="latitude"/>
            <column name="longitude"/>
        </createIndex>
        
        <createIndex tableName="geo_points" indexName="idx_geo_points_accuracy">
            <column name="accuracy"/>
        </createIndex>
    </changeSet>

</databaseChangeLog>
EOF

echo "🔍 Проверка созданного файла..."
echo "Строки 35-45:"
echo "----------------------------------------"
sed -n '35,45p' backend/src/main/resources/db/changelog/changes/008-geo-points-table.xml
echo "----------------------------------------"

echo ""
echo "🚀 Запуск Liquibase с CDATA-подходом..."
echo ""

mvn liquibase:update \
  -Dliquibase.url="jdbc:postgresql://localhost:5432/vuege" \
  -Dliquibase.username="postgres" \
  -Dliquibase.password="postgres" \
  -Dliquibase.driver="org.postgresql.Driver" \
  -Dliquibase.changeLogFile="backend/src/main/resources/db/changelog/db.changelog-master.xml"

echo ""
echo "✅ Финальное исправление завершено!"