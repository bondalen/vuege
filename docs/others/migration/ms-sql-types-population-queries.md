# Запросы для заполнения таблиц типов данных MS SQL

**Дата создания:** 4 сентября 2025  
**Статус:** Активные  
**Версия:** 1.0

## 🎯 Обзор

Документ содержит реальные SQL запросы, которые были успешно выполнены для заполнения таблиц типов данных MS SQL в системе контроля миграции `mcl`.

## 📊 Результаты заполнения

### **Таблица mssql_base_types**
- **Количество записей**: 13 базовых типов
- **Статус**: ✅ Полностью заполнена
- **Дата заполнения**: 4 сентября 2025

### **Таблица mssql_derived_types**
- **Количество записей**: 70 производных типов
- **Статус**: ✅ Полностью заполнена
- **Дата заполнения**: 4 сентября 2025
- **Связь с задачей**: task_id = 2

## 🔧 Запросы для заполнения

### **1. Заполнение базовых типов (mssql_base_types)**

#### **Описание запроса:**
Запрос извлекает уникальные базовые типы данных из схемы `ags` MS SQL Server, категоризирует их и подсчитывает количество таблиц, использующих каждый тип.

#### **SQL запрос:**
```sql
-- Запрос для заполнения mssql_base_types (должно получиться 13 записей)
SELECT DISTINCT
    c.data_type as base_type_name,
    CASE
        WHEN c.data_type IN ('int', 'bigint', 'smallint', 'tinyint') THEN 'integer'
        WHEN c.data_type IN ('decimal', 'numeric', 'money', 'smallmoney') THEN 'decimal'
        WHEN c.data_type IN ('float', 'real') THEN 'float'
        WHEN c.data_type IN ('char', 'varchar', 'nchar', 'nvarchar', 'text', 'ntext') THEN 'string'
        WHEN c.data_type IN ('date', 'datetime', 'datetime2', 'smalldatetime') THEN 'datetime'
        WHEN c.data_type IN ('bit') THEN 'boolean'
        WHEN c.data_type IN ('binary', 'varbinary', 'image') THEN 'binary'
        WHEN c.data_type IN ('uniqueidentifier') THEN 'uuid'
        ELSE 'other'
    END as type_category,
    CASE
        WHEN c.data_type IN ('int', 'bigint', 'smallint', 'tinyint') THEN 'integer'
        WHEN c.data_type IN ('decimal', 'numeric', 'money', 'smallmoney') THEN 'decimal'
        WHEN c.data_type IN ('float', 'real') THEN 'float'
        WHEN c.data_type IN ('char', 'varchar', 'nchar', 'nvarchar', 'text', 'ntext') THEN 'string'
        WHEN c.data_type IN ('date', 'datetime', 'datetime2', 'smalldatetime') THEN 'datetime'
        WHEN c.data_type IN ('bit') THEN 'boolean'
        WHEN c.data_type IN ('binary', 'varbinary', 'image') THEN 'binary'
        WHEN c.data_type IN ('uniqueidentifier') THEN 'uuid'
        ELSE 'other'
    END as type_family,
    'false' as is_user_defined,
    'Базовый тип данных MS SQL Server: ' + c.data_type as description,
    COUNT(DISTINCT c.table_name) as table_usage_count
FROM INFORMATION_SCHEMA.COLUMNS c
INNER JOIN INFORMATION_SCHEMA.TABLES t
    ON c.table_name = t.table_name
    AND c.table_schema = t.table_schema
WHERE c.table_schema = 'ags'
    AND t.table_type = 'BASE TABLE'
GROUP BY c.data_type
ORDER BY COUNT(DISTINCT c.table_name) DESC, c.data_type;
```

#### **Результаты выполнения:**
| ID | base_type_name | type_category | type_family | table_usage_count |
|----|----------------|---------------|-------------|-------------------|
| 1 | int | integer | integer | 141 |
| 2 | nvarchar | string | string | 111 |
| 3 | date | datetime | datetime | 38 |
| 4 | char | string | string | 29 |
| 5 | datetime | datetime | datetime | 26 |
| 6 | money | decimal | decimal | 19 |
| 7 | decimal | decimal | decimal | 9 |
| 8 | float | float | float | 5 |
| 9 | tinyint | integer | integer | 4 |
| 10 | uniqueidentifier | uuid | uuid | 4 |
| 11 | smallint | integer | integer | 2 |
| 12 | varchar | string | string | 2 |
| 13 | bigint | integer | integer | 1 |

### **2. Заполнение производных типов (mssql_derived_types)**

#### **Описание запроса:**
Запрос извлекает производные типы данных с их параметрами (длина, точность, масштаб, nullable) и создает уникальные комбинации для каждого типа.

#### **SQL запрос:**
```sql
-- Запрос для заполнения mssql_derived_types (должно получиться 70 записей)
SELECT 
    c.data_type as base_type_name,
    c.character_maximum_length as length_value,
    c.numeric_precision as precision_value,
    c.numeric_scale as scale_value,
    c.is_nullable,
    CASE 
        WHEN c.character_maximum_length = -1 THEN 'max'
        WHEN c.character_maximum_length IS NULL THEN NULL
        ELSE CAST(c.character_maximum_length AS varchar)
    END as max_value,
    CASE 
        WHEN c.character_maximum_length = -1 THEN 1
        ELSE 0
    END as is_max_length,
    CASE 
        WHEN c.data_type IN ('varchar', 'nvarchar', 'char', 'nchar', 'binary', 'varbinary') THEN 1
        ELSE 0
    END as is_variable_length,
    c.data_type as parameter_value,
    c.collation_name,
    CASE 
        WHEN c.data_type IN ('varchar', 'nvarchar', 'char', 'nchar') AND c.character_maximum_length = -1 
            THEN c.data_type + '(max)'
        WHEN c.data_type IN ('varchar', 'nvarchar', 'char', 'nchar') AND c.character_maximum_length IS NOT NULL
            THEN c.data_type + '(' + CAST(c.character_maximum_length AS varchar) + ')'
        WHEN c.data_type IN ('decimal', 'numeric') AND c.numeric_precision IS NOT NULL AND c.numeric_scale IS NOT NULL
            THEN c.data_type + '(' + CAST(c.numeric_precision AS varchar) + ',' + CAST(c.numeric_scale AS varchar) + ')'
        WHEN c.data_type IN ('decimal', 'numeric') AND c.numeric_precision IS NOT NULL
            THEN c.data_type + '(' + CAST(c.numeric_precision AS varchar) + ')'
        WHEN c.data_type IN ('float') AND c.numeric_precision IS NOT NULL
            THEN c.data_type + '(' + CAST(c.numeric_precision AS varchar) + ')'
        ELSE c.data_type
    END as derived_type_description,
    COUNT(*) as usage_count
FROM INFORMATION_SCHEMA.COLUMNS c
INNER JOIN INFORMATION_SCHEMA.TABLES t
    ON c.table_name = t.table_name
    AND c.table_schema = t.table_schema
WHERE c.table_schema = 'ags'
    AND t.table_type = 'BASE TABLE'
GROUP BY 
    c.data_type,
    c.character_maximum_length,
    c.numeric_precision,
    c.numeric_scale,
    c.is_nullable,
    c.collation_name
ORDER BY 
    c.data_type,
    c.character_maximum_length,
    c.numeric_precision,
    c.numeric_scale,
    c.is_nullable;
```

#### **Статистика по базовым типам:**
| Базовый тип | Количество производных типов | Примеры производных типов |
|-------------|------------------------------|---------------------------|
| nvarchar | 21 | nvarchar(255), nvarchar(max), nvarchar(50) |
| char | 19 | char(13), char(2), char(3), char(4) |
| decimal | 14 | decimal(18,8), decimal(23,8), decimal(24,8) |
| int | 2 | int (nullable), int (not nullable) |
| date | 2 | date (nullable), date (not nullable) |
| datetime | 2 | datetime (nullable), datetime (not nullable) |
| money | 2 | money (nullable), money (not nullable) |
| smallint | 2 | smallint (nullable), smallint (not nullable) |
| varchar | 2 | varchar(3), varchar(12) |
| float | 1 | float(53) |
| tinyint | 1 | tinyint(3) |
| uniqueidentifier | 1 | uniqueidentifier |
| bigint | 1 | bigint(19) |

## 🔍 Особенности выполнения запросов

### **Критические моменты:**
1. **Фильтрация по BASE TABLE** - исключает представления и другие объекты
2. **Группировка по параметрам** - создает уникальные производные типы
3. **Обработка max длины** - `character_maximum_length = -1` → `'max'`
4. **Логические флаги** - `is_max_length`, `is_variable_length`
5. **Описания типов** - автоматическое формирование с параметрами
6. **Подсчет использований** - количество колонок каждого типа

### **Важные детали:**
- **Пустые строки в запросах** могут вызывать ошибки в DBeaver/MS SQL Server
- **Автоинкремент** должен быть настроен для таблиц PostgreSQL
- **Внешние ключи** должны быть созданы после заполнения данных
- **Связи с задачами** должны соответствовать текущей задаче миграции

## 🛠️ Скрипты автоматизации

### **Python скрипты для заполнения:**

#### **1. get-base-types.py**
- **Назначение**: Получение базовых типов из MS SQL Server
- **Результат**: 13 базовых типов с категоризацией
- **Файл**: `scripts/get-base-types.py`

#### **2. insert-base-types.py**
- **Назначение**: Вставка базовых типов в PostgreSQL
- **Результат**: Заполнение таблицы `mcl.mssql_base_types`
- **Файл**: `scripts/insert-base-types.py`

#### **3. get-derived-types.py**
- **Назначение**: Получение производных типов из MS SQL Server
- **Результат**: 70 производных типов с параметрами
- **Файл**: `scripts/get-derived-types.py`

#### **4. insert-derived-types.py**
- **Назначение**: Вставка производных типов в PostgreSQL
- **Результат**: Заполнение таблицы `mcl.mssql_derived_types`
- **Файл**: `scripts/insert-derived-types.py`

## 📋 Следующие шаги

### **Завершенные этапы:**
1. ✅ **Заполнение базовых типов** - 13 типов
2. ✅ **Заполнение производных типов** - 70 типов
3. ✅ **Настройка автоинкремента** - последовательности созданы
4. ✅ **Исправление task_id** - связь с задачей ID = 2

### **Следующие этапы:**
1. 🔄 **Обновление связей** - `mssql_columns.data_type_id`
2. 🔄 **Заполнение PostgreSQL типов** - `postgres_derived_types`
3. 🔄 **Тестирование системы связей** - валидация целостности
4. 🔄 **Заполнение оставшихся полей** - `postgres_equivalent_type`, `migration_complexity`

## 📚 Связанная документация

### **Правила проекта:**
- `.cursorrules-core/migration.md` - Основные правила миграции
- `.cursorrules` - Главные правила проекта

### **Документация миграции:**
- `database-architecture-clarification.md` - Архитектура баз данных
- `current-migration-status-report.md` - Текущий статус миграции
- `mssql-to-postgres-migration-plan.md` - План миграции

### **Диаграммы процесса:**
- `table-migration-detailed-process.puml` - Детальный процесс миграции
- `table-migration-subprocess.puml` - Подпроцесс миграции

---

**Автор:** AI Assistant  
**Последнее обновление:** 4 сентября 2025  
**Статус:** Активный документ  
**Версия:** 1.0 - Создан документ с реальными запросами для заполнения таблиц типов