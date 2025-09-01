# Система типов данных PostgreSQL в контроле миграции

## 📋 Обзор

Система типов данных PostgreSQL является аналогом системы типов данных MS SQL Server и предназначена для точного отслеживания всех типов полей в целевой базе данных PostgreSQL. Каждый тип PostgreSQL имеет обязательную и уникальную связь с соответствующим типом MS SQL Server.

## 🏗️ Структура системы

### 1. **Родительская таблица: `postgres_data_types`**

Базовая таблица для всех типов данных в PostgreSQL.

**Основные поля:**
- `id` - уникальный идентификатор
- `task_id` - ссылка на задачу миграции
- `source_data_type_id` - **ОБЯЗАТЕЛЬНАЯ И УНИКАЛЬНАЯ** ссылка на тип MS SQL
- `base_type_name` - базовое имя типа (например, VARCHAR)
- `type_category` - категория типа (CHARACTER, NUMERIC, DATETIME, etc.)
- `type_family` - семейство типа (STRING, INTEGER, DECIMAL, etc.)
- `is_user_defined` - пользовательский тип или системный
- `is_nullable` - поддерживает ли NULL значения
- `default_precision` - точность по умолчанию
- `default_scale` - масштаб по умолчанию
- `max_length` - максимальная длина
- `storage_size` - размер хранения в байтах

### 2. **Дочерняя таблица: `postgres_base_types`**

Основные типы данных PostgreSQL.

**Дополнительные поля:**
- `source_base_type_id` - **ОБЯЗАТЕЛЬНАЯ И УНИКАЛЬНАЯ** ссылка на базовый тип MS SQL
- `oid` - системный OID типа в PostgreSQL
- `typname` - имя типа в системном каталоге
- `typlen` - длина типа в байтах
- `typbyval` - передается ли по значению
- `typtype` - тип типа (b=base, c=composite, d=domain, e=enum, p=pseudo, r=range)
- `typcategory` - категория типа (A=array, B=boolean, C=composite, D=datetime, E=enum, G=geometric, I=network, N=numeric, P=pseudo, S=string, T=timespan, U=user, V=bit-string, X=unknown)
- `typispreferred` - предпочтительный тип в категории
- `typisdefined` - определен ли тип
- `typdelim` - разделитель для массивов
- `typrelid` - OID связанной таблицы
- `typelem` - OID элемента для массивов
- `typarray` - OID массива
- `typinput` - функция ввода
- `typoutput` - функция вывода
- `typreceive` - функция получения
- `typsend` - функция отправки
- `typmodin` - функция модификатора ввода
- `typmodout` - функция модификатора вывода
- `typanalyze` - функция анализа
- `typalign` - выравнивание (c=char, s=short, i=int, d=double)
- `typstorage` - стратегия хранения (p=plain, e=external, x=extended, m=main)
- `typnotnull` - NOT NULL ограничение
- `typbasetype` - базовый тип для доменов
- `typtypmod` - тип-модификатор
- `typndims` - количество измерений массива
- `typcollation` - OID сортировки
- `typdefaultbin` - бинарное представление значения по умолчанию
- `typdefault` - текстовое представление значения по умолчанию
- `typacl` - права доступа
- `migration_quality` - качество миграции (EXCELLENT, GOOD, FAIR, POOR)
- `performance_rating` - оценка производительности (HIGH, MEDIUM, LOW)
- `notes` - примечания

**Примеры записей:**
```
VARCHAR     - строковый тип переменной длины
INTEGER     - целочисленный тип
TIMESTAMP   - тип даты и времени
NUMERIC     - десятичный тип
BOOLEAN     - логический тип
```

### 3. **Дочерняя таблица: `postgres_derived_types`**

Производные типы данных PostgreSQL с конкретными параметрами.

**Дополнительные поля:**
- `source_derived_type_id` - **ОБЯЗАТЕЛЬНАЯ И УНИКАЛЬНАЯ** ссылка на производный тип MS SQL
- `base_type_id` - ссылка на базовый тип PostgreSQL
- `precision_value` - значение точности
- `scale_value` - значение масштаба
- `length_value` - значение длины
- `max_value` - максимальное значение
- `parameter_value` - дополнительный параметр
- `is_max_length` - максимальная длина
- `is_variable_length` - переменная длина
- `typmod` - тип-модификатор PostgreSQL
- `typname_with_params` - имя типа с параметрами
- `array_dimensions` - количество измерений массива
- `domain_name` - имя домена
- `domain_schema` - схема домена
- `check_constraints` - ограничения проверки
- `default_constraints` - ограничения по умолчанию
- `migration_quality` - качество миграции
- `performance_rating` - оценка производительности
- `validation_rules` - правила валидации
- `notes` - примечания

**Примеры записей:**
```
VARCHAR(255)   - VARCHAR с длиной 255
NUMERIC(18,2)  - NUMERIC с точностью 18 и масштабом 2
INTEGER        - INTEGER без параметров
TEXT           - TEXT без параметров
```

## 🔗 Связи с другими таблицами

### 1. **Связь с задачами миграции**
```sql
migration_tasks ||--o{ postgres_data_types : "task_id"
```

### 2. **Связь между базовыми и производными типами**
```sql
postgres_base_types ||--o{ postgres_derived_types : "base_type_id"
```

### 3. **Связь с колонками**
```sql
postgres_columns }o--|| postgres_data_types : "postgres_data_type_id"
```

### 4. **Связи с MS SQL типами (ОБЯЗАТЕЛЬНЫЕ И УНИКАЛЬНЫЕ)**
```sql
mssql_data_types ||--o| postgres_data_types : "source_data_type_id"
mssql_base_types ||--o| postgres_base_types : "source_base_type_id"
mssql_derived_types ||--o| postgres_derived_types : "source_derived_type_id"
```

## 📊 Примеры использования

### 1. **Получение всех типов PostgreSQL для задачи миграции**
```sql
SELECT 
    pdt.base_type_name,
    pdt.type_category,
    pdt.type_family,
    pdt.is_user_defined,
    pdt.is_nullable,
    pdt.default_precision,
    pdt.default_scale,
    pdt.max_length,
    pdt.storage_size,
    pdt.description,
    mdt.base_type_name as source_type_name
FROM postgres_data_types pdt
JOIN mssql_data_types mdt ON pdt.source_data_type_id = mdt.id
WHERE pdt.task_id = 1
ORDER BY pdt.base_type_name, pdt.type_category;
```

### 2. **Получение базовых типов PostgreSQL с их производными**
```sql
SELECT 
    pbt.base_type_name,
    pbt.type_category,
    pbt.typname,
    pbt.typlen,
    pbt.typcategory,
    pbt.migration_quality,
    pbt.performance_rating,
    COUNT(pdt.id) as derived_types_count
FROM postgres_base_types pbt
LEFT JOIN postgres_derived_types pdt ON pbt.id = pdt.base_type_id
WHERE pbt.task_id = 1
GROUP BY pbt.id, pbt.base_type_name, pbt.type_category, pbt.typname, pbt.typlen, pbt.typcategory, pbt.migration_quality, pbt.performance_rating
ORDER BY pbt.base_type_name;
```

### 3. **Получение производных типов PostgreSQL с параметрами**
```sql
SELECT 
    pdt.base_type_name,
    pdt.precision_value,
    pdt.scale_value,
    pdt.length_value,
    pdt.max_value,
    pdt.parameter_value,
    pdt.typmod,
    pdt.typname_with_params,
    pdt.migration_quality,
    pdt.performance_rating
FROM postgres_derived_types pdt
WHERE pdt.task_id = 1
ORDER BY pdt.base_type_name, pdt.precision_value, pdt.scale_value;
```

### 4. **Анализ качества миграции типов**
```sql
SELECT 
    migration_quality,
    COUNT(*) as type_count,
    ROUND(COUNT(*) * 100.0 / SUM(COUNT(*)) OVER (), 2) as percentage
FROM postgres_data_types
WHERE task_id = 1
GROUP BY migration_quality
ORDER BY type_count DESC;
```

### 5. **Сравнение типов MS SQL и PostgreSQL**
```sql
SELECT 
    mdt.base_type_name as mssql_type,
    mdt.type_category as mssql_category,
    pdt.base_type_name as postgres_type,
    pdt.type_category as postgres_category,
    pdt.migration_quality,
    pdt.performance_rating
FROM mssql_data_types mdt
JOIN postgres_data_types pdt ON mdt.id = pdt.source_data_type_id
WHERE mdt.task_id = 1
ORDER BY mdt.base_type_name;
```

## 🎯 Преимущества системы

### 1. **Точность соответствия**
- **Обязательные и уникальные связи** между типами MS SQL и PostgreSQL
- **Исключение дублирования** типов в PostgreSQL
- **Гарантия соответствия** каждому типу MS SQL

### 2. **Контроль качества**
- **Оценка качества миграции** типов
- **Оценка производительности** типов
- **Валидация соответствия** типов

### 3. **Аналитика и отчетность**
- **Статистика по типам** данных PostgreSQL
- **Анализ качества** миграции
- **Отслеживание производительности**

### 4. **Автоматизация**
- **Автоматическое создание** типов PostgreSQL
- **Валидация соответствия** с MS SQL типами
- **Генерация SQL** для создания типов

## 🔧 Практическое применение

### 1. **При создании таблиц в PostgreSQL**
```sql
-- Получение типов данных для создания таблицы
SELECT 
    pc.column_name,
    pc.ordinal_position,
    pc.is_nullable,
    pdt.base_type_name,
    pdt.precision_value,
    pdt.scale_value,
    pdt.length_value,
    pdt.typname_with_params,
    pdt.migration_quality
FROM postgres_columns pc
JOIN postgres_data_types pdt ON pc.postgres_data_type_id = pdt.id
WHERE pc.table_id = 123
ORDER BY pc.ordinal_position;
```

### 2. **При валидации миграции типов**
```sql
-- Проверка соответствия типов данных
SELECT 
    mc.column_name as mssql_column,
    mdt.base_type_name as mssql_type,
    pc.column_name as postgres_column,
    pdt.base_type_name as postgres_type,
    pdt.migration_quality,
    pdt.performance_rating
FROM mssql_columns mc
JOIN mssql_data_types mdt ON mc.data_type_id = mdt.id
JOIN postgres_columns pc ON mc.id = pc.source_column_id
JOIN postgres_data_types pdt ON pc.postgres_data_type_id = pdt.id
WHERE mc.table_id = 123;
```

### 3. **При анализе производительности**
```sql
-- Анализ производительности типов данных
SELECT 
    pdt.base_type_name,
    pdt.type_category,
    pdt.performance_rating,
    COUNT(pc.id) as column_count,
    AVG(pc.ordinal_position) as avg_position
FROM postgres_data_types pdt
JOIN postgres_columns pc ON pdt.id = pc.postgres_data_type_id
WHERE pdt.task_id = 1
GROUP BY pdt.base_type_name, pdt.type_category, pdt.performance_rating
ORDER BY column_count DESC;
```

## 📈 Метрики и KPI

### 1. **Качество миграции типов**
- Процент типов с качеством EXCELLENT/GOOD
- Количество типов с качеством FAIR/POOR
- Средняя оценка качества миграции

### 2. **Производительность типов**
- Процент типов с высокой производительностью
- Количество типов с низкой производительностью
- Средняя оценка производительности

### 3. **Соответствие типам MS SQL**
- Процент типов с установленными связями
- Количество типов без связей
- Точность соответствия типов

## 🔮 Будущие улучшения

### 1. **Автоматическая оценка качества**
- Алгоритмы машинного обучения для оценки качества
- Автоматические рекомендации по улучшению
- Предсказание проблем производительности

### 2. **Расширенная аналитика**
- Анализ использования типов в запросах
- Оптимизация типов данных
- Рекомендации по индексации

### 3. **Интеграция с мониторингом**
- Мониторинг производительности типов
- Алерты при проблемах
- Автоматическая оптимизация

---

**Система типов данных PostgreSQL обеспечивает точное соответствие типам MS SQL Server и контроль качества миграции.** 🎯