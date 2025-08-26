#!/bin/bash
echo "🔧 ИСПРАВЛЕНИЕ ФАЙЛА 010-TEST-DATA.XML (ДАТЫ)"
echo "=============================================="

cd /home/alex/vuege/src/app

echo "📁 Текущая директория: $(pwd)"

echo "📝 Создание исправленного файла 010-test-data.xml..."
cat > backend/src/main/resources/db/changelog/changes/010-test-data.xml << 'EOF'
<?xml version="1.0" encoding="UTF-8"?>
<databaseChangeLog
        xmlns="http://www.liquibase.org/xml/ns/dbchangelog"
        xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
        xsi:schemaLocation="http://www.liquibase.org/xml/ns/dbchangelog
        http://www.liquibase.org/xml/ns/dbchangelog/dbchangelog-4.20.xsd">

    <changeSet id="010-insert-test-data" author="vuege">
        
        <!-- Тестовые исторические периоды (исправленные даты) -->
        <insert tableName="historical_periods">
            <column name="name">Античность</column>
            <column name="start_date">-4712-01-01</column>
            <column name="end_date">0476-12-31</column>
            <column name="era">BCE</column>
            <column name="description">Период античной цивилизации</column>
        </insert>
        
        <insert tableName="historical_periods">
            <column name="name">Средневековье</column>
            <column name="start_date">0476-01-01</column>
            <column name="end_date">1492-12-31</column>
            <column name="era">CE</column>
            <column name="description">Период средневековой истории</column>
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
            <column name="end_date">NULL</column>
            <column name="era">CE</column>
            <column name="description">Период новейшей истории</column>
        </insert>
        
        <!-- Тестовые географические точки -->
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
        
        <!-- Тестовые организационные единицы -->
        <insert tableName="organizational_units">
            <column name="name">Римская империя</column>
            <column name="type">EMPIRE</column>
            <column name="description">Древнеримская империя</column>
            <column name="founded_date">-0027-01-01</column>
            <column name="dissolved_date">0476-12-31</column>
            <column name="historical_period_id">1</column>
            <column name="location_id">1</column>
        </insert>
        
        <insert tableName="organizational_units">
            <column name="name">Византийская империя</column>
            <column name="type">EMPIRE</column>
            <column name="description">Восточная Римская империя</column>
            <column name="founded_date">0395-01-01</column>
            <column name="dissolved_date">1453-12-31</column>
            <column name="historical_period_id">2</column>
            <column name="location_id">2</column>
        </insert>
        
        <!-- Тестовые должности -->
        <insert tableName="positions">
            <column name="title">Император</column>
            <column name="description">Верховный правитель империи</column>
            <column name="hierarchy">1</column>
            <column name="organization_id">1</column>
            <column name="created_date">-0027-01-01</column>
            <column name="abolished_date">0476-12-31</column>
        </insert>
        
        <insert tableName="positions">
            <column name="title">Консул</column>
            <column name="description">Высшая должность в Римской республике</column>
            <column name="hierarchy">2</column>
            <column name="organization_id">1</column>
            <column name="created_date">-0509-01-01</column>
            <column name="abolished_date">-0027-12-31</column>
        </insert>
        
        <!-- Тестовые люди -->
        <insert tableName="persons">
            <column name="first_name">Октавиан</column>
            <column name="last_name">Август</column>
            <column name="birth_date">-0063-09-23</column>
            <column name="death_date">0014-08-19</column>
            <column name="nationality">Римлянин</column>
            <column name="biography">Первый римский император</column>
            <column name="historical_period_id">1</column>
            <column name="is_fictional">false</column>
        </insert>
        
        <insert tableName="persons">
            <column name="first_name">Юлий</column>
            <column name="last_name">Цезарь</column>
            <column name="birth_date">-0100-07-12</column>
            <column name="death_date">-0044-03-15</column>
            <column name="nationality">Римлянин</column>
            <column name="biography">Римский диктатор и полководец</column>
            <column name="historical_period_id">1</column>
            <column name="is_fictional">false</column>
        </insert>
        
        <!-- Тестовые связи человек-должность -->
        <insert tableName="person_positions">
            <column name="person_id">1</column>
            <column name="position_id">1</column>
            <column name="start_date">-0027-01-01</column>
            <column name="end_date">0014-08-19</column>
            <column name="appointment_type">ELECTION</column>
            <column name="notes">Первый император Рима</column>
        </insert>
        
        <insert tableName="person_positions">
            <column name="person_id">2</column>
            <column name="position_id">2</column>
            <column name="start_date">-0059-01-01</column>
            <column name="end_date">-0044-03-15</column>
            <column name="appointment_type">ELECTION</column>
            <column name="notes">Консул и диктатор</column>
        </insert>
        
    </changeSet>

</databaseChangeLog>
EOF

echo "🔍 Проверка исправленных дат..."
echo "Строки 12-18:"
echo "----------------------------------------"
sed -n '12,18p' backend/src/main/resources/db/changelog/changes/010-test-data.xml
echo "----------------------------------------"

echo ""
echo "🚀 Запуск Liquibase с исправленными датами..."
echo ""

mvn liquibase:update \
  -Dliquibase.url="jdbc:postgresql://localhost:5432/vuege" \
  -Dliquibase.username="postgres" \
  -Dliquibase.password="postgres" \
  -Dliquibase.driver="org.postgresql.Driver" \
  -Dliquibase.changeLogFile="backend/src/main/resources/db/changelog/db.changelog-master.xml"

echo ""
echo "✅ Исправление тестовых данных завершено!"