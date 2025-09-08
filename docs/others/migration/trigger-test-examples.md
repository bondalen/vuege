# Примеры тестирования триггера check_table_problem_uniqueness

## 🎯 **ЦЕЛЬ ТРИГГЕРА**

**Контроль уникальности связи между исходной таблицей и проблемой:**
- Одна таблица не должна быть связана с одной проблемой дважды
- Даже если используются разные способы решения
- Промежуточная таблица `problems_tb_slt_mp` связывает таблицы со способами решения
- Через способ решения определяется проблема

## 📊 **АРХИТЕКТУРА СВЯЗЕЙ**

```
mcl.mssql_tables (исходные таблицы)
    ↓ table_id
mcl.problems_tb_slt_mp (связи)
    ↓ solution_id  
mcl.problems_tb_slt (способы решения)
    ↓ problem_id
mcl.problems_tb (проблемы)
```

## 🔍 **ТЕКУЩЕЕ СОСТОЯНИЕ**

### **Проблема заглавных букв (ID=1):**
- **Способ решения**: "Способ решения не определен" (ID=4)
- **Связанные таблицы**: 135 таблиц с заглавными буквами

### **Пример существующих связей:**
```sql
-- Таблица cnInv связана с проблемой заглавных букв
cnInv → "Способ решения не определен" → "Проблема заглавных букв"
```

## ✅ **ТЕСТЫ ДЛЯ ТРИГГЕРА**

### **Тест 1: Попытка дублирования связи таблица-проблема**
```sql
-- Попытка связать таблицу cnInv с той же проблемой через тот же способ
INSERT INTO mcl.problems_tb_slt_mp (table_id, solution_id, solution_status)
VALUES (1524, 4, 'active');
-- Ожидается: ОШИБКА - таблица уже связана с этой проблемой
```

### **Тест 2: Попытка дублирования через другой способ решения**
```sql
-- Создаем новый способ решения для той же проблемы
INSERT INTO mcl.problems_tb_slt (
    solution_name, solution_description, problem_id
) VALUES (
    'Альтернативный способ', 'Другой способ решения', 1
) RETURNING id;

-- Попытка связать ту же таблицу с той же проблемой через новый способ
INSERT INTO mcl.problems_tb_slt_mp (table_id, solution_id, solution_status)
VALUES (1524, [новый_id], 'active');
-- Ожидается: ОШИБКА - таблица уже связана с этой проблемой
```

### **Тест 3: Валидная операция - новая таблица с той же проблемой**
```sql
-- Связываем другую таблицу с той же проблемой
INSERT INTO mcl.problems_tb_slt_mp (table_id, solution_id, solution_status)
VALUES (1525, 4, 'active');  -- cnInvAccnt
-- Ожидается: УСПЕХ - таблица еще не связана с этой проблемой
```

### **Тест 4: Валидная операция - та же таблица с другой проблемой**
```sql
-- Создаем новую проблему
INSERT INTO mcl.problems_tb (
    problem_name, problem_description, problem_category
) VALUES (
    'Проблема длинных имен', 'Имена таблиц слишком длинные', 'naming_convention'
) RETURNING id;

-- Создаем способ решения для новой проблемы
INSERT INTO mcl.problems_tb_slt (
    solution_name, solution_description, problem_id
) VALUES (
    'Сокращение имен', 'Сократить имена таблиц', [новая_проблема_id]
) RETURNING id;

-- Связываем ту же таблицу с новой проблемой
INSERT INTO mcl.problems_tb_slt_mp (table_id, solution_id, solution_status)
VALUES (1524, [новый_способ_id], 'active');
-- Ожидается: УСПЕХ - таблица связана с другой проблемой
```

## 🚨 **ОЖИДАЕМЫЕ ОШИБКИ**

### **Ошибка дублирования связи таблица-проблема:**
```
ERROR: Таблица 1524 уже связана с проблемой 1 (через другой способ решения)
```

### **Ошибка несуществующего способа решения:**
```
ERROR: Способ решения с ID 999 не существует
```

### **Ошибка несуществующей таблицы:**
```
ERROR: Таблица с ID 9999 не существует
```

## 📋 **ПРОВЕРОЧНЫЕ ЗАПРОСЫ**

### **Проверка существующих связей таблица-проблема:**
```sql
SELECT 
    m.object_name as table_name,
    p.problem_name,
    COUNT(*) as solution_count,
    STRING_AGG(s.solution_name, ', ') as solutions
FROM mcl.problems_tb_slt_mp mp
INNER JOIN mcl.mssql_tables m ON mp.table_id = m.id
INNER JOIN mcl.problems_tb_slt s ON mp.solution_id = s.id
INNER JOIN mcl.problems_tb p ON s.problem_id = p.id
WHERE m.schema_name = 'ags'
GROUP BY m.object_name, p.problem_name
ORDER BY m.object_name, p.problem_name;
```

### **Поиск дублирующих связей:**
```sql
SELECT 
    m.object_name as table_name,
    p.problem_name,
    COUNT(*) as duplicate_count
FROM mcl.problems_tb_slt_mp mp
INNER JOIN mcl.mssql_tables m ON mp.table_id = m.id
INNER JOIN mcl.problems_tb_slt s ON mp.solution_id = s.id
INNER JOIN mcl.problems_tb p ON s.problem_id = p.id
WHERE m.schema_name = 'ags'
GROUP BY m.object_name, p.problem_name
HAVING COUNT(*) > 1
ORDER BY COUNT(*) DESC;
```

## 🎯 **ОЖИДАЕМЫЕ РЕЗУЛЬТАТЫ**

### **После восстановления триггера:**
1. **Невозможность дублирования** связей таблица-проблема
2. **Корректные сообщения об ошибках** при попытке дублирования
3. **Валидация существования** таблиц и способов решения
4. **Сохранение целостности** системы контроля миграции

### **Преимущества:**
- **Уникальность проблем** для каждой таблицы
- **Корректная отчетность** по проблемам миграции
- **Предотвращение ошибок** в процессе миграции
- **Четкая структура** связей в системе

---

**Автор**: AI Assistant  
**Дата**: 6 сентября 2025  
**Версия**: 1.0  
**Статус**: Готово к тестированию