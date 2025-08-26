#!/bin/bash

echo "🔧 ИСПРАВЛЕНИЕ ВСЕХ НЕСООТВЕТСТВИЙ СХЕМ В ТЕСТОВЫХ ДАННЫХ"
echo "============================================================="

cd /home/alex/vuege/src/app

# Создаем резервную копию
cp backend/src/main/resources/db/changelog/changes/010-test-data.xml backend/src/main/resources/db/changelog/changes/010-test-data.xml.backup3

# Исправляем organizational_units: is_active -> is_fictional
sed -i 's/is_active/is_fictional/g' backend/src/main/resources/db/changelog/changes/010-test-data.xml

# Исправляем persons: объединяем first_name и last_name в name, исправляем is_active -> is_fictional
# Создаем временный файл с исправленными данными persons
cat > /tmp/fixed-persons.xml << 'EOF'
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
EOF

# Заменяем секцию persons в основном файле
sed -i '/<!-- ChangeSet 5: Персоны -->/,/<!-- ChangeSet 6: Связи человек-должность -->/c\' backend/src/main/resources/db/changelog/changes/010-test-data.xml
sed -i '/<!-- ChangeSet 5: Персоны -->/r /tmp/fixed-persons.xml' backend/src/main/resources/db/changelog/changes/010-test-data.xml

echo "✅ Файл исправлен"
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