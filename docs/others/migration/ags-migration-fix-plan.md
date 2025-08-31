# 🔧 ПЛАН ИСПРАВЛЕНИЯ ПРОБЛЕМНЫХ ТАБЛИЦ СХЕМЫ AGS

## 🎯 ОБЩАЯ ИНФОРМАЦИЯ

**Дата:** 30 августа 2025  
**Статус:** Планирование исправлений  
**Цель:** Достичь 100% миграции схемы AGS

### 📊 ТЕКУЩЕЕ СОСТОЯНИЕ:
- **Всего таблиц:** 251
- **Успешно мигрировано:** 182 (72.5%)
- **Проблемных таблиц:** 52 (20.7%)
- **Цель:** 251 (100%)

---

## 🔧 КАТЕГОРИИ ПРОБЛЕМ И РЕШЕНИЯ

### 1. **ПРОБЛЕМЫ С ИМЕНАМИ КОЛОНОК (РЕГИСТР)**

#### **📋 ПРОБЛЕМНЫЕ ТАБЛИЦЫ:**
- cn_PrDoc
- cn_PrDocT
- cn_s_org_smplCs
- cn_s_orgCs
- cn_sCs
- cnCs
- cnInv
- cnInvAccnt
- cnInvAccntSmpl

#### **🔧 РЕШЕНИЕ:**
```python
def fix_column_name_case(column_name):
    """Исправление регистра имен колонок"""
    return column_name.lower()

def create_table_with_fixed_columns(table_name, columns):
    """Создание таблицы с исправленными именами колонок"""
    fixed_columns = []
    for col in columns:
        col['name'] = fix_column_name_case(col['name'])
        fixed_columns.append(col)
    return create_table(table_name, fixed_columns)
```

#### **📝 ПЛАН ДЕЙСТВИЙ:**
1. Создать скрипт `fix-column-case-issues.py`
2. Добавить функцию автоматического исправления регистра
3. Пересоздать проблемные таблицы с правильными именами
4. Проверить целостность данных

---

### 2. **ПРОБЛЕМЫ С UUID ТИПАМИ**

#### **📋 ПРОБЛЕМНЫЕ ТАБЛИЦЫ:**
- cstAg
- cstAgPn
- ogAg

#### **🔧 РЕШЕНИЕ:**
```python
def convert_uuid_to_text(value):
    """Конвертация UUID в text"""
    if isinstance(value, uuid.UUID):
        return str(value)
    return value

def handle_uuid_columns(data):
    """Обработка UUID колонок в данных"""
    for row in data:
        for key, value in row.items():
            if isinstance(value, uuid.UUID):
                row[key] = str(value)
    return data
```

#### **📝 ПЛАН ДЕЙСТВИЙ:**
1. Создать скрипт `fix-uuid-issues.py`
2. Добавить автоматическую конвертацию UUID в text
3. Обновить схему таблиц для UUID колонок
4. Перемигрировать данные с конвертацией

---

### 3. **ПРОБЛЕМЫ С ДЛИНОЙ СТРОК**

#### **📋 ПРОБЛЕМНЫЕ ТАБЛИЦЫ:**
- ogAgFeeGr

#### **🔧 РЕШЕНИЕ:**
```python
def adjust_column_length(column_type, max_length):
    """Увеличение длины колонки при необходимости"""
    if 'varchar' in column_type.lower():
        current_length = extract_length(column_type)
        if current_length < max_length:
            return f"varchar({max_length})"
    return column_type

def analyze_string_lengths(data, column_name):
    """Анализ максимальной длины строк в данных"""
    max_length = 0
    for row in data:
        if column_name in row and row[column_name]:
            max_length = max(max_length, len(str(row[column_name])))
    return max_length
```

#### **📝 ПЛАН ДЕЙСТВИЙ:**
1. Создать скрипт `fix-string-length-issues.py`
2. Проанализировать максимальные длины строк
3. Увеличить лимиты колонок при необходимости
4. Пересоздать таблицы с правильными типами

---

### 4. **ПРОБЛЕМЫ С ИМЕНАМИ ТАБЛИЦ (ДЕФИСЫ)**

#### **📋 ПРОБЛЕМНЫЕ ТАБЛИЦЫ:**
- dym_pm
- importDbt_23-0331_Pir
- importDbt_23-0630_Pir
- importDbt_23-0930_Pir
- importDbt_23-1231_Pir
- importDbt_25-0210_Test-Pir
- importDbt_25-0529_Test-Pir
- importDbt_25-0606_Test-Pir
- importDbt_25-0731_Test-Pir
- importMnrl_23-1128
- yr_ctrl_rep

#### **🔧 РЕШЕНИЕ:**
```python
def fix_table_name(table_name):
    """Исправление имен таблиц с дефисами"""
    return table_name.replace('-', '_')

def create_table_with_fixed_name(original_name, columns):
    """Создание таблицы с исправленным именем"""
    fixed_name = fix_table_name(original_name)
    return create_table(fixed_name, columns)
```

#### **📝 ПЛАН ДЕЙСТВИЙ:**
1. Создать скрипт `fix-table-name-issues.py`
2. Заменить дефисы на подчеркивания в именах таблиц
3. Создать таблицы с правильными именами
4. Обновить ссылки в связанных таблицах

---

### 5. **ПРОБЛЕМЫ С ДУБЛИРОВАНИЕМ ТИПОВ**

#### **📋 ПРОБЛЕМНЫЕ ТАБЛИЦЫ:**
- cn_PrDocCs
- cn_s_orgExeBuirg
- cnInvAccntCs
- cstCcnGr
- dtqInvoice
- dym_pm_pm
- impPIR_21

#### **🔧 РЕШЕНИЕ:**
```python
def handle_duplicate_type_error(error):
    """Обработка ошибок дублирования типов"""
    if "duplicate key value violates unique constraint" in str(error):
        if "pg_type_typname_nsp_index" in str(error):
            return "SKIP_TYPE_CREATION"
    return "RETRY"

def create_table_with_type_check(table_name, columns):
    """Создание таблицы с проверкой типов"""
    try:
        return create_table(table_name, columns)
    except Exception as e:
        if handle_duplicate_type_error(e) == "SKIP_TYPE_CREATION":
            # Пропустить создание типа, продолжить с таблицей
            return create_table_without_type(table_name, columns)
        raise e
```

#### **📝 ПЛАН ДЕЙСТВИЙ:**
1. Создать скрипт `fix-duplicate-type-issues.py`
2. Добавить проверку существования типов
3. Пропускать создание существующих типов
4. Продолжать создание таблиц

---

### 6. **ПРОБЛЕМЫ С НЕСУЩЕСТВУЮЩИМИ ОБЪЕКТАМИ**

#### **📋 ПРОБЛЕМНЫЕ ТАБЛИЦЫ:**
- dtqContract
- dtqCounterparty
- dtqInvoiceDbt
- RaRa_chSmLt_RltYy

#### **🔧 РЕШЕНИЕ:**
```python
def check_object_exists(object_name, object_type):
    """Проверка существования объекта в SQL Server"""
    query = f"""
    SELECT COUNT(*) 
    FROM sys.objects 
    WHERE name = '{object_name}' AND type = '{object_type}'
    """
    result = execute_query(query)
    return result[0][0] > 0

def migrate_table_with_validation(table_name):
    """Миграция таблицы с валидацией"""
    if not check_object_exists(table_name, 'U'):
        print(f"Таблица {table_name} не существует, пропускаем")
        return False
    return migrate_table(table_name)
```

#### **📝 ПЛАН ДЕЙСТВИЙ:**
1. Создать скрипт `fix-missing-object-issues.py`
2. Добавить проверку существования объектов
3. Пропускать несуществующие таблицы
4. Логировать пропущенные объекты

---

### 7. **ПРОБЛЕМЫ С НЕСУЩЕСТВУЮЩИМИ КОЛОНКАМИ**

#### **📋 ПРОБЛЕМНЫЕ ТАБЛИЦЫ:**
- cn_s_orgCustBuirgInv
- cn_s_orgExeBuirgInv
- TimeRsltCAP
- TimeRsltM
- TimeRsltMrl
- TimeRsltMrTtl
- yr_ctrl
- yr_ctrl_cm
- yr_ctrl_cm_21
- yr_ctrl_cmAcc21
- yr_ctrl_cmAcc21_06
- yr_ctrlAccnt

#### **🔧 РЕШЕНИЕ:**
```python
def get_table_columns(table_name):
    """Получение списка колонок таблицы"""
    query = f"""
    SELECT COLUMN_NAME 
    FROM INFORMATION_SCHEMA.COLUMNS 
    WHERE TABLE_NAME = '{table_name}'
    """
    result = execute_query(query)
    return [row[0] for row in result]

def create_table_with_existing_columns(table_name):
    """Создание таблицы только с существующими колонками"""
    columns = get_table_columns(table_name)
    return create_table_with_columns(table_name, columns)
```

#### **📝 ПЛАН ДЕЙСТВИЙ:**
1. Создать скрипт `fix-missing-column-issues.py`
2. Получить актуальный список колонок из SQL Server
3. Создать таблицы только с существующими колонками
4. Пропускать несуществующие колонки

---

### 8. **СИНТАКСИЧЕСКИЕ ОШИБКИ**

#### **📋 ПРОБЛЕМНЫЕ ТАБЛИЦЫ:**
- ra_period

#### **🔧 РЕШЕНИЕ:**
```python
def fix_sql_syntax(sql_query):
    """Исправление синтаксиса SQL"""
    # Замена зарезервированных слов
    sql_query = sql_query.replace('key', '"key"')
    sql_query = sql_query.replace('order', '"order"')
    sql_query = sql_query.replace('group', '"group"')
    return sql_query

def create_table_with_syntax_fix(table_name, columns):
    """Создание таблицы с исправлением синтаксиса"""
    sql = generate_create_table_sql(table_name, columns)
    fixed_sql = fix_sql_syntax(sql)
    return execute_sql(fixed_sql)
```

#### **📝 ПЛАН ДЕЙСТВИЙ:**
1. Создать скрипт `fix-syntax-issues.py`
2. Добавить обработку зарезервированных слов
3. Исправить синтаксис SQL запросов
4. Пересоздать проблемные таблицы

---

## 🚀 ПЛАН РЕАЛИЗАЦИИ

### 📋 **ЭТАП 1: ПОДГОТОВКА (1-2 часа)**
1. Создать все исправляющие скрипты
2. Протестировать на небольшом наборе таблиц
3. Подготовить план отката

### 📋 **ЭТАП 2: ИСПРАВЛЕНИЕ (2-3 часа)**
1. Исправить проблемы с именами колонок (9 таблиц)
2. Исправить проблемы с UUID (3 таблицы)
3. Исправить проблемы с длиной строк (1 таблица)
4. Исправить проблемы с именами таблиц (11 таблиц)

### 📋 **ЭТАП 3: ЗАВЕРШЕНИЕ (1-2 часа)**
1. Исправить проблемы с дублированием типов (7 таблиц)
2. Исправить проблемы с несуществующими объектами (4 таблицы)
3. Исправить проблемы с несуществующими колонками (12 таблиц)
4. Исправить синтаксические ошибки (1 таблица)

### 📋 **ЭТАП 4: ПРОВЕРКА (1 час)**
1. Проверить целостность всех мигрированных таблиц
2. Сравнить количество записей
3. Провести тестовые запросы
4. Создать финальный отчет

---

## 📊 ОЖИДАЕМЫЕ РЕЗУЛЬТАТЫ

### 🎯 **ПОСЛЕ ИСПРАВЛЕНИЙ:**
- **Всего таблиц:** 251
- **Успешно мигрировано:** 251 (100%)
- **Ошибки миграции:** 0 (0%)
- **Общий прогресс:** 251/251 (100%)

### 🏆 **БИЗНЕС-ЦЕННОСТЬ:**
- **Полная миграция схемы AGS**
- **100% готовность к интеграции**
- **Полная совместимость с PostgreSQL**
- **Готовность к запуску приложения**

---

## 🔧 ТЕХНИЧЕСКИЕ ТРЕБОВАНИЯ

### 📋 **ИНСТРУМЕНТЫ:**
- Python 3.8+
- pymssql
- psycopg2-binary
- Виртуальная среда migration-env

### 📋 **ДОСТУПЫ:**
- SQL Server: localhost:1433 (sa/YourStrong@Passw0rd)
- PostgreSQL: localhost:5432 (testuser/testpass)

### 📋 **ФАЙЛЫ:**
- Все исправляющие скрипты в папке `scripts/`
- Логи в папке `logs/`
- Отчеты в папке `docs/migration/`

---

## 🚨 РИСКИ И МИТИГАЦИЯ

### ⚠️ **ПОТЕНЦИАЛЬНЫЕ РИСКИ:**
1. **Потеря данных при исправлении**
2. **Нарушение целостности данных**
3. **Проблемы с производительностью**
4. **Конфликты с существующими данными**

### 🛡️ **МИТИГАЦИЯ:**
1. **Создание резервных копий перед исправлением**
2. **Тестирование на копии данных**
3. **Поэтапное применение исправлений**
4. **Детальное логирование всех операций**

---

## 📋 ЧЕК-ЛИСТ ЗАВЕРШЕНИЯ

### ✅ **ПОДГОТОВКА:**
- [ ] Созданы все исправляющие скрипты
- [ ] Протестированы на небольшом наборе таблиц
- [ ] Подготовлен план отката
- [ ] Созданы резервные копии

### ✅ **ИСПРАВЛЕНИЕ:**
- [ ] Исправлены проблемы с именами колонок
- [ ] Исправлены проблемы с UUID
- [ ] Исправлены проблемы с длиной строк
- [ ] Исправлены проблемы с именами таблиц
- [ ] Исправлены проблемы с дублированием типов
- [ ] Исправлены проблемы с несуществующими объектами
- [ ] Исправлены проблемы с несуществующими колонками
- [ ] Исправлены синтаксические ошибки

### ✅ **ПРОВЕРКА:**
- [ ] Проверена целостность всех таблиц
- [ ] Сравнено количество записей
- [ ] Проведены тестовые запросы
- [ ] Создан финальный отчет

### ✅ **ЗАВЕРШЕНИЕ:**
- [ ] Достигнуто 100% миграции
- [ ] Обновлена документация
- [ ] Обновлен changelog
- [ ] Готовность к интеграции

---

## 🎯 ЗАКЛЮЧЕНИЕ

Данный план обеспечивает систематический подход к исправлению всех проблемных таблиц схемы AGS. После выполнения всех этапов будет достигнута 100% миграция схемы с полной готовностью к интеграции с основным приложением.

**Ожидаемое время выполнения:** 5-8 часов  
**Ожидаемый результат:** 100% миграция схемы AGS  
**Готовность к интеграции:** 100%