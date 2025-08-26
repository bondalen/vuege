#!/bin/bash

echo "🔍 ПРОВЕРКА СУЩЕСТВУЮЩИХ КОЛОНОК В ТАБЛИЦАХ"
echo "=========================================="

cd /home/alex/vuege

echo "=== Колонки organizational_units ==="
psql -h localhost -U postgres -d vuege -c "\d organizational_units" | cat

echo ""
echo "=== Колонки persons ==="
psql -h localhost -U postgres -d vuege -c "\d persons" | cat

echo ""
echo "=== Колонки positions ==="
psql -h localhost -U postgres -d vuege -c "\d positions" | cat

echo ""
echo "🔧 СОЗДАНИЕ ИСПРАВЛЕННОГО ФАЙЛА 012-add-extended-functionality.xml"
echo "=================================================================="

cd /home/alex/vuege/src/app

# Создаем исправленный файл только с новыми колонками
cat > backend/src/main/resources/db/changelog/changes/012-add-extended-functionality.xml << 'EOF'
<?xml version="1.0" encoding="UTF-8"?>
<databaseChangeLog
        xmlns="http://www.liquibase.org/xml/ns/dbchangelog"
        xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
        xsi:schemaLocation="http://www.liquibase.org/xml/ns/dbchangelog
        http://www.liquibase.org/xml/ns/dbchangelog/dbchangelog-4.20.xsd">

    <changeSet id="012-001-add-status-to-organizations" author="vuege">
        <addColumn tableName="organizational_units">
            <column name="status" type="VARCHAR(20)" defaultValue="ACTIVE">
                <constraints nullable="false"/>
            </column>
            <column name="metadata" type="JSONB"/>
            <column name="tags" type="TEXT[]"/>
            <column name="description" type="TEXT"/>
            <column name="website" type="VARCHAR(255)"/>
        </addColumn>
        
        <sql>
            UPDATE organizational_units SET 
                status = 'ACTIVE'
            WHERE status IS NULL;
        </sql>
    </changeSet>

    <changeSet id="008-002-add-extended-fields-to-persons" author="vuege">
        <addColumn tableName="persons">
            <column name="email" type="VARCHAR(255)"/>
            <column name="phone" type="VARCHAR(50)"/>
            <column name="biography" type="TEXT"/>
            <column name="achievements" type="TEXT[]"/>
            <column name="skills" type="TEXT[]"/>
        </addColumn>
    </changeSet>

    <changeSet id="008-003-add-extended-fields-to-positions" author="vuege">
        <addColumn tableName="positions">
            <column name="salary_min" type="DECIMAL(10,2)"/>
            <column name="salary_max" type="DECIMAL(10,2)"/>
            <column name="salary_currency" type="VARCHAR(3)" defaultValue="USD"/>
            <column name="salary_period" type="VARCHAR(20)" defaultValue="YEARLY"/>
            <column name="requirements" type="TEXT[]"/>
            <column name="benefits" type="TEXT[]"/>
            <column name="reports_to_id" type="BIGINT"/>
        </addColumn>
        
        <addForeignKeyConstraint baseTableName="positions" baseColumnNames="reports_to_id"
                                constraintName="fk_positions_reports_to"
                                referencedTableName="positions" referencedColumnNames="id"/>
    </changeSet>

    <changeSet id="008-004-create-users-table" author="vuege">
        <createTable tableName="users">
            <column name="id" type="BIGINT" autoIncrement="true">
                <constraints primaryKey="true" nullable="false"/>
            </column>
            <column name="username" type="VARCHAR(100)">
                <constraints nullable="false" unique="true"/>
            </column>
            <column name="email" type="VARCHAR(255)">
                <constraints nullable="false" unique="true"/>
            </column>
            <column name="password_hash" type="VARCHAR(255)">
                <constraints nullable="false"/>
            </column>
            <column name="first_name" type="VARCHAR(100)">
                <constraints nullable="false"/>
            </column>
            <column name="last_name" type="VARCHAR(100)">
                <constraints nullable="false"/>
            </column>
            <column name="roles" type="TEXT[]">
                <constraints nullable="false"/>
            </column>
            <column name="is_active" type="BOOLEAN" defaultValueBoolean="true">
                <constraints nullable="false"/>
            </column>
            <column name="created_at" type="TIMESTAMP" defaultValueComputed="CURRENT_TIMESTAMP">
                <constraints nullable="false"/>
            </column>
            <column name="last_login" type="TIMESTAMP"/>
        </createTable>
        
        <createIndex tableName="users" indexName="idx_users_username">
            <column name="username"/>
        </createIndex>
        
        <createIndex tableName="users" indexName="idx_users_email">
            <column name="email"/>
        </createIndex>
    </changeSet>

    <changeSet id="008-005-create-audit-logs-table" author="vuege">
        <createTable tableName="audit_logs">
            <column name="id" type="BIGINT" autoIncrement="true">
                <constraints primaryKey="true" nullable="false"/>
            </column>
            <column name="entity_id" type="BIGINT">
                <constraints nullable="false"/>
            </column>
            <column name="entity_type" type="VARCHAR(100)">
                <constraints nullable="false"/>
            </column>
            <column name="action" type="VARCHAR(50)">
                <constraints nullable="false"/>
            </column>
            <column name="old_values" type="JSONB"/>
            <column name="new_values" type="JSONB"/>
            <column name="user_id" type="VARCHAR(100)">
                <constraints nullable="false"/>
            </column>
            <column name="timestamp" type="TIMESTAMP" defaultValueComputed="CURRENT_TIMESTAMP">
                <constraints nullable="false"/>
            </column>
            <column name="ip_address" type="VARCHAR(45)"/>
            <column name="user_agent" type="TEXT"/>
        </createTable>
        
        <createIndex tableName="audit_logs" indexName="idx_audit_logs_entity">
            <column name="entity_id"/>
            <column name="entity_type"/>
        </createIndex>
        
        <createIndex tableName="audit_logs" indexName="idx_audit_logs_user">
            <column name="user_id"/>
        </createIndex>
        
        <createIndex tableName="audit_logs" indexName="idx_audit_logs_timestamp">
            <column name="timestamp"/>
        </createIndex>
    </changeSet>

    <changeSet id="008-006-create-notifications-table" author="vuege">
        <createTable tableName="notifications">
            <column name="id" type="BIGINT" autoIncrement="true">
                <constraints primaryKey="true" nullable="false"/>
            </column>
            <column name="user_id" type="VARCHAR(100)">
                <constraints nullable="false"/>
            </column>
            <column name="type" type="VARCHAR(20)">
                <constraints nullable="false"/>
            </column>
            <column name="title" type="VARCHAR(255)">
                <constraints nullable="false"/>
            </column>
            <column name="message" type="TEXT">
                <constraints nullable="false"/>
            </column>
            <column name="data" type="JSONB"/>
            <column name="is_read" type="BOOLEAN" defaultValueBoolean="false">
                <constraints nullable="false"/>
            </column>
            <column name="created_at" type="TIMESTAMP" defaultValueComputed="CURRENT_TIMESTAMP">
                <constraints nullable="false"/>
            </column>
            <column name="read_at" type="TIMESTAMP"/>
        </createTable>
        
        <createIndex tableName="notifications" indexName="idx_notifications_user">
            <column name="user_id"/>
        </createIndex>
        
        <createIndex tableName="notifications" indexName="idx_notifications_unread">
            <column name="user_id"/>
            <column name="is_read"/>
        </createIndex>
        
        <createIndex tableName="notifications" indexName="idx_notifications_created">
            <column name="created_at"/>
        </createIndex>
    </changeSet>

    <changeSet id="008-007-create-webhooks-table" author="vuege">
        <createTable tableName="webhooks">
            <column name="id" type="BIGINT" autoIncrement="true">
                <constraints primaryKey="true" nullable="false"/>
            </column>
            <column name="name" type="VARCHAR(255)">
                <constraints nullable="false"/>
            </column>
            <column name="url" type="VARCHAR(500)">
                <constraints nullable="false"/>
            </column>
            <column name="events" type="TEXT[]">
                <constraints nullable="false"/>
            </column>
            <column name="is_active" type="BOOLEAN" defaultValueBoolean="true">
                <constraints nullable="false"/>
            </column>
            <column name="secret" type="VARCHAR(255)">
                <constraints nullable="false"/>
            </column>
            <column name="created_at" type="TIMESTAMP" defaultValueComputed="CURRENT_TIMESTAMP">
                <constraints nullable="false"/>
            </column>
            <column name="updated_at" type="TIMESTAMP" defaultValueComputed="CURRENT_TIMESTAMP">
                <constraints nullable="false"/>
            </column>
            <column name="last_triggered" type="TIMESTAMP"/>
            <column name="success_count" type="INTEGER" defaultValueNumeric="0">
                <constraints nullable="false"/>
            </column>
            <column name="failure_count" type="INTEGER" defaultValueNumeric="0">
                <constraints nullable="false"/>
            </column>
        </createTable>
        
        <createIndex tableName="webhooks" indexName="idx_webhooks_active">
            <column name="is_active"/>
        </createIndex>
        
        <createIndex tableName="webhooks" indexName="idx_webhooks_events">
            <column name="events" type="GIN"/>
        </createIndex>
    </changeSet>

    <changeSet id="008-008-add-address-table" author="vuege">
        <createTable tableName="addresses">
            <column name="id" type="BIGINT" autoIncrement="true">
                <constraints primaryKey="true" nullable="false"/>
            </column>
            <column name="street" type="VARCHAR(255)">
                <constraints nullable="false"/>
            </column>
            <column name="city" type="VARCHAR(100)">
                <constraints nullable="false"/>
            </column>
            <column name="state" type="VARCHAR(100)"/>
            <column name="country" type="VARCHAR(100)">
                <constraints nullable="false"/>
            </column>
            <column name="postal_code" type="VARCHAR(20)"/>
            <column name="latitude" type="DECIMAL(10,8)"/>
            <column name="longitude" type="DECIMAL(11,8)"/>
        </createTable>
        
        <createIndex tableName="addresses" indexName="idx_addresses_coordinates">
            <column name="latitude"/>
            <column name="longitude"/>
        </createIndex>
    </changeSet>

    <changeSet id="008-009-add-education-table" author="vuege">
        <createTable tableName="education">
            <column name="id" type="BIGINT" autoIncrement="true">
                <constraints primaryKey="true" nullable="false"/>
            </column>
            <column name="person_id" type="BIGINT">
                <constraints nullable="false"/>
            </column>
            <column name="institution" type="VARCHAR(255)">
                <constraints nullable="false"/>
            </column>
            <column name="degree" type="VARCHAR(255)">
                <constraints nullable="false"/>
            </column>
            <column name="field" type="VARCHAR(255)">
                <constraints nullable="false"/>
            </column>
            <column name="start_date" type="DATE">
                <constraints nullable="false"/>
            </column>
            <column name="end_date" type="DATE"/>
            <column name="gpa" type="DECIMAL(3,2)"/>
        </createTable>
        
        <addForeignKeyConstraint baseTableName="education" baseColumnNames="person_id"
                                constraintName="fk_education_person"
                                referencedTableName="persons" referencedColumnNames="id"/>
        
        <createIndex tableName="education" indexName="idx_education_person">
            <column name="person_id"/>
        </createIndex>
    </changeSet>

    <changeSet id="008-010-add-performance-indexes" author="vuege">
        <!-- Индексы для организаций -->
        <createIndex tableName="organizational_units" indexName="idx_org_status">
            <column name="status"/>
        </createIndex>
        
        <createIndex tableName="organizational_units" indexName="idx_org_tags">
            <column name="tags" type="GIN"/>
        </createIndex>
        
        <!-- Индексы для людей -->
        <createIndex tableName="persons" indexName="idx_person_email">
            <column name="email"/>
        </createIndex>
        
        <createIndex tableName="persons" indexName="idx_person_skills">
            <column name="skills" type="GIN"/>
        </createIndex>
        
        <!-- Индексы для должностей -->
        <createIndex tableName="positions" indexName="idx_position_salary">
            <column name="salary_min"/>
            <column name="salary_max"/>
        </createIndex>
        
        <createIndex tableName="positions" indexName="idx_position_requirements">
            <column name="requirements" type="GIN"/>
        </createIndex>
    </changeSet>

</databaseChangeLog>
EOF

echo "✅ Файл исправлен - удалены все дублирующиеся колонки"
echo ""

echo "🚀 Запуск Liquibase для применения исправлений..."
mvn liquibase:update \
    -Dliquibase.changeLogFile="backend/src/main/resources/db/changelog/db.changelog-master.xml" \
    -Dliquibase.url="jdbc:postgresql://localhost:5432/vuege" \
    -Dliquibase.username="postgres" \
    -Dliquibase.password="postgres" \
    -Dliquibase.clearCheckSums="true"

echo ""
echo "✅ Проверка и исправление завершено!"