#!/bin/bash

echo "🔧 ПОЛНАЯ ПЕРЕЗАПИСЬ ТЕСТОВЫХ ДАННЫХ С ПРАВИЛЬНОЙ СХЕМОЙ"
echo "=========================================================="

cd /home/alex/vuege/src/app

# Создаем резервную копию
cp backend/src/main/resources/db/changelog/changes/010-test-data.xml backend/src/main/resources/db/changelog/changes/010-test-data.xml.backup4

# Полностью переписываем файл с правильными данными
cat > backend/src/main/resources/db/changelog/changes/010-test-data.xml << 'EOF'
<?xml version="1.0" encoding="UTF-8"?>
<databaseChangeLog
        xmlns="http://www.liquibase.org/xml/ns/dbchangelog"
        xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
        xsi:schemaLocation="http://www.liquibase.org/xml/ns/dbchangelog
        http://www.liquibase.org/xml/ns/dbchangelog/dbchangelog-4.20.xsd">

    <!-- ChangeSet 1: Исторические периоды -->
    <changeSet id="010-insert-historical-periods" author="vuege">
        <insert tableName="historical_periods">
            <column name="name">Раннее Средневековье</column>
            <column name="start_date">0476-01-01</column>
            <column name="end_date">1000-12-31</column>
            <column name="era">CE</column>
            <column name="description">Период раннего средневековья</column>
        </insert>
        
        <insert tableName="historical_periods">
            <column name="name">Высокое Средневековье</column>
            <column name="start_date">1000-01-01</column>
            <column name="end_date">1300-12-31</column>
            <column name="era">CE</column>
            <column name="description">Период высокого средневековья</column>
        </insert>
        
        <insert tableName="historical_periods">
            <column name="name">Позднее Средневековье</column>
            <column name="start_date">1300-01-01</column>
            <column name="end_date">1492-12-31</column>
            <column name="era">CE</column>
            <column name="description">Период позднего средневековья</column>
        </insert>
        
        <insert tableName="historical_periods">
            <column name="name">Новое время</column>
            <column name="start_date">1492-01-01</column>
            <column name="end_date">1789-12-31</column>
            <column name="era">CE</column>
            <column name="description">Период нового времени</column>
        </insert>
        
        <insert tableName="historical_periods">
            <column name="name">Новейшее время</column>
            <column name="start_date">1789-01-01</column>
            <column name="end_date">2025-12-31</column>
            <column name="era">CE</column>
            <column name="description">Период новейшей истории</column>
        </insert>
    </changeSet>

    <!-- ChangeSet 2: Географические точки -->
    <changeSet id="010-insert-geo-points" author="vuege">
        <insert tableName="geo_points">
            <column name="latitude">55.7558</column>
            <column name="longitude">37.6176</column>
            <column name="elevation">156</column>
            <column name="accuracy">EXACT</column>
        </insert>
        
        <insert tableName="geo_points">
            <column name="latitude">59.9311</column>
            <column name="longitude">30.3609</column>
            <column name="elevation">3</column>
            <column name="accuracy">EXACT</column>
        </insert>
    </changeSet>

    <!-- ChangeSet 3: Организационные единицы -->
    <changeSet id="010-insert-organizational-units" author="vuege">
        <insert tableName="organizational_units">
            <column name="name">Византийская империя</column>
            <column name="type">EMPIRE</column>
            <column name="founded_date">0395-01-01</column>
            <column name="dissolved_date">1453-12-31</column>
            <column name="historical_period_id">1</column>
            <column name="location_id">1</column>
            <column name="is_fictional">false</column>
        </insert>
        
        <insert tableName="organizational_units">
            <column name="name">Священная Римская империя</column>
            <column name="type">EMPIRE</column>
            <column name="founded_date">0800-01-01</column>
            <column name="dissolved_date">1806-08-06</column>
            <column name="historical_period_id">2</column>
            <column name="location_id">2</column>
            <column name="is_fictional">false</column>
        </insert>
    </changeSet>

    <!-- ChangeSet 4: Должности -->
    <changeSet id="010-insert-positions" author="vuege">
        <insert tableName="positions">
            <column name="title">Император</column>
            <column name="organization_id">1</column>
            <column name="hierarchy">1</column>
            <column name="created_date">0395-01-01</column>
            <column name="abolished_date">1453-12-31</column>
            <column name="is_active">false</column>
        </insert>
        
        <insert tableName="positions">
            <column name="title">Папа Римский</column>
            <column name="organization_id">2</column>
            <column name="hierarchy">1</column>
            <column name="created_date">0800-01-01</column>
            <column name="abolished_date">1806-08-06</column>
            <column name="is_active">false</column>
        </insert>
    </changeSet>

    <!-- ChangeSet 5: Персоны -->
    <changeSet id="010-insert-persons" author="vuege">
        <insert tableName="persons">
            <column name="name">Юстиниан I</column>
            <column name="birth_date">0482-05-11</column>
            <column name="death_date">0565-11-14</column>
            <column name="nationality">Византийская</column>
            <column name="historical_period_id">1</column>
            <column name="is_fictional">false</column>
        </insert>
        
        <insert tableName="persons">
            <column name="name">Карл Великий</column>
            <column name="birth_date">0742-04-02</column>
            <column name="death_date">0814-01-28</column>
            <column name="nationality">Франкская</column>
            <column name="historical_period_id">2</column>
            <column name="is_fictional">false</column>
        </insert>
    </changeSet>

    <!-- ChangeSet 6: Связи человек-должность -->
    <changeSet id="010-insert-person-positions" author="vuege">
        <insert tableName="person_positions">
            <column name="person_id">1</column>
            <column name="position_id">1</column>
            <column name="start_date">0527-08-01</column>
            <column name="end_date">0565-11-14</column>
            <column name="appointment_type">APPOINTED</column>
        </insert>
        
        <insert tableName="person_positions">
            <column name="person_id">2</column>
            <column name="position_id">2</column>
            <column name="start_date">0800-12-25</column>
            <column name="end_date">0814-01-28</column>
            <column name="appointment_type">APPOINTED</column>
        </insert>
    </changeSet>

</databaseChangeLog>
EOF

echo "✅ Файл переписан с правильной схемой"
echo ""

echo "🚀 Запуск Liquibase с сбросом контрольных сумм..."
mvn liquibase:update \
    -Dliquibase.changeLogFile="backend/src/main/resources/db/changelog/db.changelog-master.xml" \
    -Dliquibase.url="jdbc:postgresql://localhost:5432/vuege" \
    -Dliquibase.username="postgres" \
    -Dliquibase.password="postgres" \
    -Dliquibase.clearCheckSums="true"

echo ""
echo "🔍 Проверка данных после исправления..."
psql -h localhost -U postgres -d vuege -c "SELECT COUNT(*) as persons_count FROM persons;"
psql -h localhost -U postgres -d vuege -c "SELECT COUNT(*) as person_positions_count FROM person_positions;"

echo ""
echo "✅ Исправление завершено!"