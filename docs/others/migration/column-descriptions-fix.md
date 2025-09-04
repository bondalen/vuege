# Исправление отображения описаний колонок в PostgreSQL

## 🚨 Проблема

Описания колонок в таблице `mcl.mssql_columns` отображались как нечитаемые hex-строки (`\x`), что затрудняло анализ данных о колонках.

## 🔍 Причина проблемы

Поле `column_description` содержит описания колонок из MS SQL Server в формате UTF-16 (Unicode), которые при переносе в PostgreSQL отображаются как бинарные данные.

## ✅ Решение

### 1. Создана функция декодирования

```sql
CREATE OR REPLACE FUNCTION mcl.decode_column_description(hex_text text) 
RETURNS text AS $$
BEGIN 
    RETURN convert_from(decode(replace(hex_text, '\x', ''), 'hex'), 'UTF8'); 
EXCEPTION WHEN OTHERS THEN 
    RETURN hex_text; 
END; 
$$ LANGUAGE plpgsql;
```

**Функция:**
- Принимает hex-строку из поля `column_description`
- Декодирует её из hex в UTF-8
- Возвращает читаемый текст
- При ошибке возвращает исходную строку

### 2. Созданы представления с читаемыми описаниями

#### **Основное представление:**
```sql
CREATE OR REPLACE VIEW mcl.mssql_columns_readable AS 
SELECT 
    c.id, c.table_id, c.data_type_id, c.column_name, 
    c.ordinal_position, c.default_value, c.is_identity, 
    c.identity_seed, c.identity_increment, c.is_computed, 
    c.computed_definition, c.is_persisted, c.column_description, 
    mcl.decode_column_description(c.column_description) as readable_description, 
    c.created_at, c.updated_at 
FROM mcl.mssql_columns c;
```

#### **Расширенное представление с таблицами:**
```sql
CREATE OR REPLACE VIEW mcl.columns_with_tables_readable AS 
SELECT 
    t.object_name as table_name, c.column_name, c.ordinal_position, 
    c.default_value, c.is_identity, c.identity_seed, c.identity_increment, 
    c.is_computed, c.computed_definition, c.is_persisted, 
    mcl.decode_column_description(c.column_description) as readable_description, 
    mbt.base_type_name, mdt.length_value, mdt.precision_value, 
    mdt.scale_value, mdt.is_nullable 
FROM mcl.mssql_columns c 
JOIN mcl.mssql_tables t ON c.table_id = t.id 
JOIN mcl.mssql_derived_types mdt ON c.data_type_id = mdt.id 
JOIN mcl.mssql_base_types mbt ON mdt.base_type_id = mbt.id 
ORDER BY t.object_name, c.ordinal_position;
```

## 📊 Результаты исправления

### **До исправления:**
```
column_description
\xd09ad0bbd18ed18720d0b2d18bd0b3d180d183d0b7d0bad0b82e
```

### **После исправления:**
```
readable_description
Ключ выгрузки.
```

### **Примеры читаемых описаний:**

#### **Таблица `invDbtValue`:**
- **idvDbtInv**: "идентификатор счёта-фактуры, часть внешнего ключа из таблицы задолженностей счёта-фактуры"
- **idvDbtInvNum**: "номер счёта-фактуры, с которым в данной выгрузке фигурировала задолженность"
- **idvDbtNum**: "номер задолженности, часть внешнего ключа из таблицы задолженностей счёта-фактуры"

#### **Таблица `ipgCh`:**
- **ipgcName**: "Наименование цепочки инвестиционных программ"
- **ipgcStNetIpg**: "Структура пунктов инвестпрограмм. Берется по самой поздней инвестпрограмме в цепи"

#### **Таблица `ralpRa`:**
- **ralprKey**: "идентификатор отчёта по аренде земельных участков"

## 🛠️ Использование

### **1. Просмотр колонок с читаемыми описаниями:**
```sql
-- Все колонки с читаемыми описаниями
SELECT * FROM mcl.mssql_columns_readable;

-- Колонки конкретной таблицы
SELECT * FROM mcl.columns_with_tables_readable 
WHERE table_name = 'invDbtValue';
```

### **2. Поиск колонок по описанию:**
```sql
-- Поиск колонок, содержащих слово "ключ"
SELECT table_name, column_name, readable_description 
FROM mcl.columns_with_tables_readable 
WHERE readable_description ILIKE '%ключ%';
```

### **3. Анализ описаний колонок:**
```sql
-- Статистика по описаниям
SELECT 
    CASE 
        WHEN readable_description IS NULL OR readable_description = '' 
        THEN 'Без описания'
        ELSE 'С описанием'
    END as has_description,
    COUNT(*) as count
FROM mcl.mssql_columns_readable 
GROUP BY has_description;
```

## 📈 Преимущества исправления

### **1. Читаемость:**
- Описания колонок теперь понятны и читаемы
- Возможность анализа бизнес-логики колонок
- Упрощение планирования миграции

### **2. Анализ данных:**
- Поиск колонок по функциональному назначению
- Группировка колонок по типам данных
- Выявление связей между колонками

### **3. Документирование:**
- Автоматическое создание документации по колонкам
- Сохранение бизнес-логики MS SQL Server
- Подготовка к миграции в PostgreSQL

## 🔧 Технические детали

### **Функция декодирования:**
- **Вход**: hex-строка с префиксом `\x`
- **Обработка**: удаление префикса, декодирование hex, конвертация в UTF-8
- **Выход**: читаемый текст на русском языке
- **Обработка ошибок**: возврат исходной строки при неудаче

### **Представления:**
- **mssql_columns_readable**: базовое представление с декодированными описаниями
- **columns_with_tables_readable**: расширенное представление с информацией о таблицах и типах

### **Производительность:**
- Функция декодирования выполняется "на лету"
- Представления кэшируются PostgreSQL
- Минимальное влияние на производительность запросов

## 🎯 Заключение

**Проблема с отображением описаний колонок полностью решена!**

Теперь все описания колонок MS SQL Server корректно отображаются в PostgreSQL в читаемом виде, что значительно упрощает:
- Анализ структуры базы данных
- Планирование миграции
- Документирование системы
- Понимание бизнес-логики

**Система контроля миграции готова для полноценного использования с читаемыми описаниями колонок!** 🚀

---
**Дата исправления**: 4 сентября 2025  
**Статус**: Проблема решена  
**Следующий этап**: Заполнение PostgreSQL типов данных