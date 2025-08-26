#!/bin/bash
echo "🔧 ПРОСТОЕ ИСПРАВЛЕНИЕ ТЕСТОВЫХ ДАННЫХ (БЕЗ ВНЕШНИХ КЛЮЧЕЙ)"
echo "============================================================="

cd /home/alex/vuege/src/app

echo "📁 Текущая директория: $(pwd)"

echo "📝 Создание простого файла 010-test-data.xml..."
cat > backend/src/main/resources/db/changelog/changes/010-test-data.xml << 'EOF'
<?xml version="1.0" encoding="UTF-8"?>
<databaseChangeLog
        xmlns="http://www.liquibase.org/xml/ns/dbchangelog"
        xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
        xsi:schemaLocation="http://www.liquibase.org/xml/ns/dbchangelog
        http://www.liquibase.org/xml/ns/dbchangelog/dbchangelog-4.20.xsd">

    <changeSet id="010-insert-test-data" author="vuege">
        
        <!-- Тестовые исторические периоды (только наша эра) -->
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
        
        <!-- Тестовые организационные единицы (БЕЗ location_id) -->
        <insert tableName="organizational_units">
            <column name="name">Византийская империя</column>
            <column name="type">EMPIRE</column>
            <column name="founded_date">0395-01-01</column>
            <column name="dissolved_date">1453-12-31</column>
            <column name="historical_period_id">1</column>
            <column name="location_id">NULL</column>
            <column name="is_fictional">false</column>
        </insert>
        
        <insert tableName="organizational_units">
            <column name="name">Священная Римская империя</column>
            <column name="type">EMPIRE</column>
            <column name="founded_date">0800-01-01</column>
            <column name="dissolved_date">1806-12-31</column>
            <column name="historical_period_id">2</column>
            <column name="location_id">NULL</column>
            <column name="is_fictional">false</column>
        </insert>
        
        <!-- Тестовые должности -->
        <insert tableName="positions">
            <column name="title">Император Византии</column>
            <column name="description">Верховный правитель Византийской империи</column>
            <column name="hierarchy">1</column>
            <column name="organization_id">1</column>
            <column name="created_date">0395-01-01</column>
            <column name="abolished_date">1453-12-31</column>
        </insert>
        
        <insert tableName="positions">
            <column name="title">Император Священной Римской империи</column>
            <column name="description">Верховный правитель Священной Римской империи</column>
            <column name="hierarchy">1</column>
            <column name="organization_id">2</column>
            <column name="created_date">0800-01-01</column>
            <column name="abolished_date">1806-12-31</column>
        </insert>
        
        <!-- Тестовые люди -->
        <insert tableName="persons">
            <column name="first_name">Юстиниан</column>
            <column name="last_name">I</column>
            <column name="birth_date">0482-05-11</column>
            <column name="death_date">0565-11-14</column>
            <column name="nationality">Византиец</column>
            <column name="biography">Византийский император, известный своими реформами</column>
            <column name="historical_period_id">1</column>
            <column name="is_fictional">false</column>
        </insert>
        
        <insert tableName="persons">
            <column name="first_name">Карл</column>
            <column name="last_name">Великий</column>
            <column name="birth_date">0742-04-02</column>
            <column name="death_date">0814-01-28</column>
            <column name="nationality">Франк</column>
            <column name="biography">Король франков и первый император Священной Римской империи</column>
            <column name="historical_period_id">2</column>
            <column name="is_fictional">false</column>
        </insert>
        
        <!-- Тестовые связи человек-должность -->
        <insert tableName="person_positions">
            <column name="person_id">1</column>
            <column name="position_id">1</column>
            <column name="start_date">0527-08-01</column>
            <column name="end_date">0565-11-14</column>
            <column name="appointment_type">INHERITANCE</column>
            <column name="notes">Император Византии</column>
        </insert>
        
        <insert tableName="person_positions">
            <column name="person_id">2</column>
            <column name="position_id">2</column>
            <column name="start_date">0800-12-25</column>
            <column name="end_date">0814-01-28</column>
            <column name="appointment_type">CORONATION</column>
            <column name="notes">Первый император Священной Римской империи</column>
        </insert>
        
    </changeSet>

</databaseChangeLog>
EOF

echo "🔍 Проверка простого файла..."
echo "Строки 45-55 (organizational_units):"
echo "----------------------------------------"
sed -n '45,55p' backend/src/main/resources/db/changelog/changes/010-test-data.xml
echo "----------------------------------------"

echo ""
echo "🚀 Запуск Liquibase с простыми тестовыми данными..."
echo ""

mvn liquibase:update \
  -Dliquibase.url="jdbc:postgresql://localhost:5432/vuege" \
  -Dliquibase.username="postgres" \
  -Dliquibase.password="postgres" \
  -Dliquibase.driver="org.postgresql.Driver" \
  -Dliquibase.changeLogFile="backend/src/main/resources/db/changelog/db.changelog-master.xml"

echo ""
echo "✅ Простое исправление тестовых данных завершено!"