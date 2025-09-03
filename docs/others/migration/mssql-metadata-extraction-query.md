# Запрос для извлечения метаданных таблиц MS SQL Server

## **Описание**

Этот запрос является **образцом для миграций с использованием системы контроля** и предназначен для извлечения детальной информации о таблицах из MS SQL Server для последующего заполнения системы контроля миграции.

## **SQL Запрос (ИСПРАВЛЕННЫЙ - БЕЗ ДУБЛИРОВАНИЯ)**

```sql
SELECT DISTINCT
    t.TABLE_SCHEMA,
    t.TABLE_NAME,
    t.TABLE_TYPE,
    p.rows AS ROW_COUNT,
    CAST(ROUND(((SUM(a.total_pages) * 8) / 1024.00), 2) AS DECIMAL(18,2)) AS SIZE_MB,
    c.COLUMN_COUNT,
    pk.PRIMARY_KEY_COUNT,
    fk.FOREIGN_KEY_COUNT,
    idx.INDEX_COUNT,
    t.TABLE_CATALOG,
    -- Описание объекта (комментарий)
    ISNULL(ep.value, 'Описание отсутствует') AS TABLE_DESCRIPTION,
    -- Дополнительная информация об объекте
    o.create_date AS CREATION_DATE,
    o.modify_date AS MODIFICATION_DATE,
    -- Статус объекта
    CASE 
        WHEN o.is_ms_shipped = 1 THEN 'Системный объект'
        ELSE 'Пользовательский объект'
    END AS OBJECT_TYPE_DESCRIPTION,
    -- Количество триггеров
    (SELECT COUNT(*) FROM sys.triggers tr 
     WHERE tr.parent_id = OBJECT_ID(t.TABLE_SCHEMA + '.' + t.TABLE_NAME)) AS TRIGGER_COUNT,
    -- Максимальная длина колонки
    (SELECT MAX(CHARACTER_MAXIMUM_LENGTH) 
     FROM INFORMATION_SCHEMA.COLUMNS col 
     WHERE col.TABLE_SCHEMA = t.TABLE_SCHEMA 
       AND col.TABLE_NAME = t.TABLE_NAME) AS MAX_COLUMN_LENGTH,
    -- ID объекта в MS SQL
    OBJECT_ID(t.TABLE_SCHEMA + '.' + t.TABLE_NAME) AS MS_SQL_OBJECT_ID
FROM INFORMATION_SCHEMA.TABLES t
-- Основная информация о таблице (только одна запись)
INNER JOIN sys.partitions p ON p.object_id = OBJECT_ID(t.TABLE_SCHEMA + '.' + t.TABLE_NAME)
    AND p.index_id IN (0, 1)  -- Только heap и clustered index
-- Размер таблицы
LEFT JOIN sys.allocation_units a ON a.container_id = p.hobt_id
-- Описание объекта
LEFT JOIN sys.extended_properties ep ON ep.major_id = OBJECT_ID(t.TABLE_SCHEMA + '.' + t.TABLE_NAME)
    AND ep.minor_id = 0
    AND ep.name = 'MS_Description'
-- Метаданные объекта
LEFT JOIN sys.objects o ON o.object_id = OBJECT_ID(t.TABLE_SCHEMA + '.' + t.TABLE_NAME)
-- Количество колонок
LEFT JOIN (
    SELECT 
        TABLE_SCHEMA, 
        TABLE_NAME, 
        COUNT(*) AS COLUMN_COUNT
    FROM INFORMATION_SCHEMA.COLUMNS 
    WHERE TABLE_SCHEMA = 'ags'
    GROUP BY TABLE_SCHEMA, TABLE_NAME
) c ON c.TABLE_SCHEMA = t.TABLE_SCHEMA AND c.TABLE_NAME = t.TABLE_NAME
-- Количество первичных ключей
LEFT JOIN (
    SELECT 
        TABLE_SCHEMA, 
        TABLE_NAME, 
        COUNT(*) AS PRIMARY_KEY_COUNT
    FROM INFORMATION_SCHEMA.KEY_COLUMN_USAGE 
    WHERE CONSTRAINT_NAME LIKE '%PK%'
        AND TABLE_SCHEMA = 'ags'
    GROUP BY TABLE_SCHEMA, TABLE_NAME
) pk ON pk.TABLE_SCHEMA = t.TABLE_SCHEMA AND pk.TABLE_NAME = t.TABLE_NAME
-- Количество внешних ключей
LEFT JOIN (
    SELECT 
        TABLE_SCHEMA, 
        TABLE_NAME, 
        COUNT(*) AS FOREIGN_KEY_COUNT
    FROM INFORMATION_SCHEMA.KEY_COLUMN_USAGE 
    WHERE CONSTRAINT_NAME LIKE '%FK%'
        AND TABLE_SCHEMA = 'ags'
    GROUP BY TABLE_SCHEMA, TABLE_NAME
) fk ON fk.TABLE_SCHEMA = t.TABLE_SCHEMA AND fk.TABLE_NAME = t.TABLE_NAME
-- Количество индексов
LEFT JOIN (
    SELECT 
        OBJECT_SCHEMA_NAME(object_id) AS TABLE_SCHEMA,
        OBJECT_NAME(object_id) AS TABLE_NAME,
        COUNT(*) AS INDEX_COUNT
    FROM sys.indexes 
    WHERE type > 0
        AND OBJECT_SCHEMA_NAME(object_id) = 'ags'
    GROUP BY object_id
) idx ON idx.TABLE_SCHEMA = t.TABLE_SCHEMA AND idx.TABLE_NAME = t.TABLE_NAME
WHERE t.TABLE_TYPE = 'BASE TABLE'
    AND t.TABLE_SCHEMA = 'ags'
GROUP BY 
    t.TABLE_SCHEMA, t.TABLE_NAME, t.TABLE_TYPE, p.rows, t.TABLE_CATALOG,
    c.COLUMN_COUNT, pk.PRIMARY_KEY_COUNT, fk.FOREIGN_KEY_COUNT, idx.INDEX_COUNT,
    ep.value, o.create_date, o.modify_date, o.is_ms_shipped
ORDER BY t.TABLE_NAME;
```

## **Ключевые особенности запроса**

### **Фильтрация объектов:**
- `t.TABLE_TYPE = 'BASE TABLE'` - только пользовательские таблицы
- `t.TABLE_SCHEMA = 'ags'` - конкретная схема
- `p.index_id IN (0, 1)` - таблицы с валидными разделами (heap и clustered index)

### **Извлекаемые метаданные:**
- **Базовая информация**: схема, имя, тип, каталог
- **Размер и объем**: количество строк, размер в МБ
- **Структура**: количество колонок, ключей, индексов, триггеров
- **Описания**: комментарии, даты создания/изменения
- **Статус**: системный/пользовательский объект
- **Дополнительно**: максимальная длина колонки, ID объекта MS SQL

### **JOIN операции:**
- `sys.partitions` - информация о разделах и строках (INNER JOIN для уникальности)
- `sys.allocation_units` - размер таблицы
- `sys.extended_properties` - описания объектов
- `sys.objects` - метаданные объектов
- `INFORMATION_SCHEMA.COLUMNS` - количество колонок
- `INFORMATION_SCHEMA.KEY_COLUMN_USAGE` - ключи
- `sys.indexes` - индексы
- `sys.triggers` - количество триггеров (подзапрос)

## **Использование в системе контроля миграции**

### **1. Выполнение запроса:**
- Выполнить в DBeaver или другом клиенте MS SQL Server
- Сохранить результаты в CSV или Excel файл
- **Результат**: ровно 166 уникальных таблиц без дублирования

### **2. Заполнение системы контроля:**
```sql
-- Вставка в mssql_objects
INSERT INTO mcl.mssql_objects (task_id, object_name, object_type, schema_name, migration_status, object_type_description, object_description, create_date, modify_date, object_id)
VALUES (?, ?, ?, ?, 'pending', ?, ?, ?, ?, ?);

-- Вставка в mssql_tables  
INSERT INTO mcl.mssql_tables (task_id, object_name, object_type, schema_name, migration_status, object_type_description, object_description, table_catalog, row_count, table_size, primary_key_count, foreign_key_count, index_count, column_count, trigger_count, max_column_length)
VALUES (?, ?, ?, ?, 'pending', ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?);
```

### **3. Маппинг полей:**
| **MS SQL Запрос** | **PostgreSQL Таблица** | **Поле** |
|-------------------|------------------------|----------|
| `TABLE_SCHEMA` | `mssql_objects` | `schema_name` |
| `TABLE_NAME` | `mssql_objects` | `object_name` |
| `TABLE_TYPE` | `mssql_objects` | `object_type` |
| `TABLE_CATALOG` | `mssql_tables` | `table_catalog` |
| `ROW_COUNT` | `mssql_tables` | `row_count` |
| `SIZE_MB` | `mssql_tables` | `table_size` |
| `COLUMN_COUNT` | `mssql_tables` | `column_count` |
| `PRIMARY_KEY_COUNT` | `mssql_tables` | `primary_key_count` |
| `FOREIGN_KEY_COUNT` | `mssql_tables` | `foreign_key_count` |
| `INDEX_COUNT` | `mssql_tables` | `index_count` |
| `TRIGGER_COUNT` | `mssql_tables` | `trigger_count` |
| `MAX_COLUMN_LENGTH` | `mssql_tables` | `max_column_length` |
| `MS_SQL_OBJECT_ID` | `mssql_objects` | `object_id` |
| `OBJECT_TYPE_DESCRIPTION` | `mssql_objects` | `object_type_description` |
| `TABLE_DESCRIPTION` | `mssql_objects` | `object_description` |
| `CREATION_DATE` | `mssql_objects` | `create_date` |
| `MODIFICATION_DATE` | `mssql_objects` | `modify_date` |

## **Преимущества данного запроса**

### **1. Точность:**
- Показывает только валидные пользовательские таблицы
- Исключает системные и проблемные объекты
- Фильтрует таблицы без корректных разделов
- **НЕ ДУБЛИРУЕТ** записи благодаря DISTINCT и INNER JOIN

### **2. Полнота:**
- Извлекает все необходимые метаданные
- Включает описания и комментарии
- Содержит информацию о размере и структуре
- **17 полей** для полного заполнения системы контроля

### **3. Совместимость:**
- Работает с системой контроля миграции
- Поля запроса соответствуют структуре PostgreSQL
- Поддерживает все типы объектов
- Готов для автоматического импорта

## **Применение в проекте Vuege**

### **Текущий статус:**
- ✅ Запрос протестирован на базе Fish_Eye
- ✅ Возвращает ровно 166 уникальных таблиц схемы ags
- ✅ **ИСПРАВЛЕНА ПРОБЛЕМА ДУБЛИРОВАНИЯ**
- ✅ Готов для использования в системе контроля миграции

### **Следующие шаги:**
1. ✅ Выполнить запрос в DBeaver (166 таблиц)
2. 🔄 Обновить Python скрипт для обработки 17 полей
3. 🔄 Заполнить систему контроля миграции
4. 🔄 Начать процесс миграции таблиц

---

**Дата создания**: 2025-09-02  
**Дата исправления**: 2025-09-02  
**Версия**: 2.0 (ИСПРАВЛЕННАЯ)  
**Статус**: ✅ Протестирован, исправлен и готов к использованию  
**Проект**: Vuege - Модульная система миграции данных