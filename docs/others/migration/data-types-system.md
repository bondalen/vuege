# Система типов данных в контроле миграции

## 📋 Обзор

Система типов данных предназначена для точного отслеживания всех типов полей в исходной базе данных MS SQL Server и их корректного маппинга в PostgreSQL. Это позволяет обеспечить целостность данных и качество миграции.

## 🏗️ Структура системы

### 1. **Родительская таблица: `mssql_data_types`**

Базовая таблица для всех типов данных в MS SQL Server.

**Основные поля:**
- `id` - уникальный идентификатор
- `task_id` - ссылка на задачу миграции
- `base_type_name` - базовое имя типа (например, NVARCHAR)
- `type_category` - категория типа (CHARACTER, NUMERIC, DATETIME, etc.)
- `type_family` - семейство типа (STRING, INTEGER, DECIMAL, etc.)
- `is_user_defined` - пользовательский тип или системный
- `is_nullable` - поддерживает ли NULL значения
- `default_precision` - точность по умолчанию
- `default_scale` - масштаб по умолчанию
- `max_length` - максимальная длина
- `storage_size` - размер хранения в байтах

### 2. **Дочерняя таблица: `mssql_base_types`**

Основные типы данных, определенные в базе данных.

**Дополнительные поля:**
- `system_type_id` - системный ID типа
- `user_type_id` - пользовательский ID типа
- `is_assembly_type` - тип сборки
- `is_table_type` - табличный тип
- `is_computed` - вычисляемый тип
- `collation_name` - имя сортировки
- `xml_collection_id` - ID XML коллекции
- `postgres_equivalent_type` - эквивалентный тип в PostgreSQL
- `migration_complexity` - сложность миграции (LOW, MEDIUM, HIGH)
- `notes` - примечания

**Примеры записей:**
```
NVARCHAR    - строковый тип переменной длины
INT         - целочисленный тип
DATETIME    - тип даты и времени
DECIMAL     - десятичный тип
BIT         - битовый тип
```

### 3. **Дочерняя таблица: `mssql_derived_types`**

Производные типы данных с конкретными параметрами.

**Дополнительные поля:**
- `base_type_id` - ссылка на базовый тип
- `precision_value` - значение точности
- `scale_value` - значение масштаба
- `length_value` - значение длины
- `max_value` - максимальное значение (например, MAX)
- `parameter_value` - дополнительный параметр
- `is_max_length` - максимальная длина
- `is_variable_length` - переменная длина
- `postgres_equivalent_type` - эквивалентный тип в PostgreSQL
- `postgres_parameters` - параметры для PostgreSQL
- `migration_complexity` - сложность миграции
- `validation_rules` - правила валидации
- `notes` - примечания

**Примеры записей:**
```
NVARCHAR(255)   - NVARCHAR с длиной 255
NVARCHAR(MAX)   - NVARCHAR с максимальной длиной
DECIMAL(18,2)   - DECIMAL с точностью 18 и масштабом 2
INT             - INT без параметров
```

## 🔗 Связи с другими таблицами

### 1. **Связь с задачами миграции**
```sql
migration_tasks ||--o{ mssql_data_types : "task_id"
```

### 2. **Связь между базовыми и производными типами**
```sql
mssql_base_types ||--o{ mssql_derived_types : "base_type_id"
```

### 3. **Связь с колонками**
```sql
mssql_columns }o--|| mssql_data_types : "data_type_id"
postgres_columns }o--|| mssql_data_types : "data_type_id"
```

## 📊 Примеры использования

### 1. **Получение всех типов данных для задачи миграции**
```sql
SELECT 
    dt.base_type_name,
    dt.type_category,
    dt.type_family,
    dt.is_user_defined,
    dt.is_nullable,
    dt.default_precision,
    dt.default_scale,
    dt.max_length,
    dt.storage_size,
    dt.description
FROM mssql_data_types dt
WHERE dt.task_id = 1
ORDER BY dt.base_type_name, dt.type_category;
```

### 2. **Получение базовых типов с их производными**
```sql
SELECT 
    bt.base_type_name,
    bt.type_category,
    bt.postgres_equivalent_type,
    bt.migration_complexity,
    COUNT(dt.id) as derived_types_count
FROM mssql_base_types bt
LEFT JOIN mssql_derived_types dt ON bt.id = dt.base_type_id
WHERE bt.task_id = 1
GROUP BY bt.id, bt.base_type_name, bt.type_category, bt.postgres_equivalent_type, bt.migration_complexity
ORDER BY bt.base_type_name;
```

### 3. **Получение производных типов с параметрами**
```sql
SELECT 
    dt.base_type_name,
    dt.precision_value,
    dt.scale_value,
    dt.length_value,
    dt.max_value,
    dt.parameter_value,
    dt.postgres_equivalent_type,
    dt.postgres_parameters,
    dt.migration_complexity
FROM mssql_derived_types dt
WHERE dt.task_id = 1
ORDER BY dt.base_type_name, dt.precision_value, dt.scale_value;
```

### 4. **Анализ сложности миграции типов**
```sql
SELECT 
    migration_complexity,
    COUNT(*) as type_count,
    ROUND(COUNT(*) * 100.0 / SUM(COUNT(*)) OVER (), 2) as percentage
FROM mssql_data_types
WHERE task_id = 1
GROUP BY migration_complexity
ORDER BY type_count DESC;
```

## 🎯 Преимущества системы

### 1. **Точность маппинга**
- Каждый тип данных точно отслеживается
- Параметры типов сохраняются
- Эквиваленты в PostgreSQL определяются заранее

### 2. **Контроль качества**
- Сложность миграции оценивается
- Правила валидации определяются
- Примечания и рекомендации сохраняются

### 3. **Аналитика и отчетность**
- Статистика по типам данных
- Анализ сложности миграции
- Отслеживание прогресса

### 4. **Автоматизация**
- Автоматическое определение эквивалентов
- Генерация SQL для создания типов
- Валидация соответствия типов

## 🔧 Практическое применение

### 1. **При миграции таблиц**
```sql
-- Получение типов данных для конкретной таблицы
SELECT 
    c.column_name,
    c.ordinal_position,
    c.is_nullable,
    dt.base_type_name,
    dt.precision_value,
    dt.scale_value,
    dt.length_value,
    dt.postgres_equivalent_type,
    dt.postgres_parameters
FROM mssql_columns c
JOIN mssql_data_types dt ON c.data_type_id = dt.id
WHERE c.table_id = 123
ORDER BY c.ordinal_position;
```

### 2. **При создании колонок в PostgreSQL**
```sql
-- Генерация SQL для создания колонки
SELECT 
    c.column_name,
    CASE 
        WHEN dt.is_nullable THEN 'NULL'
        ELSE 'NOT NULL'
    END as nullability,
    dt.postgres_equivalent_type as data_type,
    dt.postgres_parameters as parameters
FROM mssql_columns c
JOIN mssql_data_types dt ON c.data_type_id = dt.id
WHERE c.table_id = 123;
```

### 3. **При валидации миграции**
```sql
-- Проверка соответствия типов данных
SELECT 
    mc.column_name as mssql_column,
    mc.data_type_id as mssql_type_id,
    pc.column_name as postgres_column,
    pc.data_type_id as postgres_type_id,
    dt.postgres_equivalent_type as expected_type
FROM mssql_columns mc
JOIN postgres_columns pc ON mc.id = pc.source_column_id
JOIN mssql_data_types dt ON mc.data_type_id = dt.id
WHERE mc.table_id = 123;
```

## 📈 Метрики и KPI

### 1. **Покрытие типов данных**
- Процент типов с определенными эквивалентами в PostgreSQL
- Количество типов без эквивалентов
- Сложность миграции типов

### 2. **Качество маппинга**
- Точность соответствия типов
- Количество предупреждений
- Процент успешных миграций

### 3. **Производительность**
- Время анализа типов данных
- Время генерации SQL
- Время валидации

## 🔮 Будущие улучшения

### 1. **Автоматическое определение эквивалентов**
- Машинное обучение для определения соответствий
- База знаний типов данных
- Рекомендации по маппингу

### 2. **Расширенная валидация**
- Проверка совместимости типов
- Валидация ограничений
- Проверка производительности

### 3. **Интеграция с инструментами**
- Подключение к DBeaver
- Интеграция с pgAdmin
- API для внешних систем

---

**Система типов данных обеспечивает точный контроль и качество миграции данных между MS SQL Server и PostgreSQL.** 🎯