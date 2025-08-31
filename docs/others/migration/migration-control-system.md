# Система контроля миграции

**Дата создания:** 31 августа 2025  
**Статус:** Активная  
**Версия:** 1.0

## 📋 Обзор

Система контроля миграции предназначена для детального учета и мониторинга процесса переноса объектов из SQL Server в PostgreSQL. Система включает схему `migration_control` с таблицами, представлениями и инструментами для отслеживания прогресса миграции.

## 🗄️ Структура системы

### Схема: `migration_control`

#### Таблица: `migration_tasks`
Таблица для учета задач миграции.

**Поля:**
- `id` (SERIAL PRIMARY KEY) - Уникальный идентификатор
- `description` (TEXT) - Описание задачи миграции
- `created_at` (TIMESTAMP) - Дата создания записи
- `updated_at` (TIMESTAMP) - Дата последнего обновления

#### Таблица: `objects`
Основная таблица для учета типов объектов миграции.

**Поля:**
- `id` (SERIAL PRIMARY KEY) - Уникальный идентификатор
- `task_id` (INTEGER) - Ссылка на таблицу migration_tasks
- `has_in_mssql` (BOOLEAN) - Наличие в MS SQL Server
- `has_in_postgres` (BOOLEAN) - Наличие в PostgreSQL
- `object_type` (VARCHAR(50)) - Тип объекта (TABLE, VIEW, FUNCTION, STORED_PROCEDURE, etc.)
- `name_in_mssql` (VARCHAR(255)) - Наименование в MS SQL Server
- `name_in_postgres` (VARCHAR(255)) - Наименование в PostgreSQL
- `created_at` (TIMESTAMP) - Дата создания записи
- `updated_at` (TIMESTAMP) - Дата последнего обновления

#### Таблица: `specific_objects`
Таблица для учета конкретных объектов с отношением один-ко-многим к таблице `objects`.

**Поля:**
- `id` (SERIAL PRIMARY KEY) - Уникальный идентификатор
- `object_id` (INTEGER) - Ссылка на таблицу `objects`
- `name_in_mssql` (VARCHAR(255)) - Наименование в MS SQL Server (заполняется при начале работы)
- `name_in_postgres` (VARCHAR(255)) - Наименование в PostgreSQL (NULL до определения в ходе работы)
- `migration_status` (VARCHAR(50)) - Статус миграции (pending, completed, failed)
- `migration_date` (TIMESTAMP) - Дата миграции
- `error_message` (TEXT) - Сообщение об ошибке
- `created_at` (TIMESTAMP) - Дата создания записи
- `updated_at` (TIMESTAMP) - Дата последнего обновления

### Представления

#### `migration_progress`
Представление для отображения прогресса миграции по типам объектов.

**Поля:**
- `object_type` - Тип объекта
- `has_in_mssql` - Наличие в MS SQL
- `has_in_postgres` - Наличие в PostgreSQL
- `total_objects` - Общее количество объектов
- `completed_objects` - Количество завершенных объектов
- `failed_objects` - Количество объектов с ошибками
- `pending_objects` - Количество объектов в ожидании
- `completion_percentage` - Процент завершения

#### `detailed_progress`
Представление для детального просмотра прогресса миграции.

**Поля:**
- `object_id` - ID типа объекта
- `object_type` - Тип объекта
- `object_name_mssql` - Имя объекта в MS SQL
- `object_name_postgres` - Имя объекта в PostgreSQL
- `has_in_mssql` - Наличие в MS SQL
- `has_in_postgres` - Наличие в PostgreSQL
- `specific_object_id` - ID конкретного объекта
- `specific_name_mssql` - Имя конкретного объекта в MS SQL
- `specific_name_postgres` - Имя конкретного объекта в PostgreSQL
- `migration_status` - Статус миграции
- `migration_date` - Дата миграции
- `error_message` - Сообщение об ошибке

## 📊 Текущий статус (31 августа 2025)

### Общая статистика
- **Типов объектов:** 6
- **Всего конкретных объектов:** 583
- **Завершено:** 236 (40.48%)
- **Ошибок:** 0
- **В ожидании:** 347 (59.52%)

### Прогресс по типам объектов

| Тип объекта | Всего | Завершено | Ошибок | Ожидает | Прогресс |
|-------------|-------|-----------|--------|---------|----------|
| TABLE | 371 | 236 | 0 | 135 | 63.61% |
| VIEW | 85 | 0 | 0 | 85 | 0.00% |
| FUNCTION | 47 | 0 | 0 | 47 | 0.00% |
| INLINE_FUNCTION | 28 | 0 | 0 | 28 | 0.00% |
| TABLE_FUNCTION | 29 | 0 | 0 | 29 | 0.00% |
| STORED_PROCEDURE | 23 | 0 | 0 | 23 | 0.00% |

## 🛠️ Порядок ведения таблиц

### 1. Инициализация системы

#### 1.1 Создание схемы и таблиц
```bash
# Запуск скрипта создания схемы
python3 src/infrastructure/scripts/create-migration-control-schema.py
```

#### 1.2 Первоначальное заполнение
```bash
# Запуск скрипта заполнения данными
python3 src/infrastructure/scripts/populate-migration-control-tables.py
```

### 2. Обновление статусов миграции

#### 2.1 При успешной миграции объекта
```sql
UPDATE migration_control.specific_objects 
SET migration_status = 'completed', 
    migration_date = CURRENT_TIMESTAMP,
    name_in_postgres = 'новое_имя_в_postgres'
WHERE name_in_mssql = 'имя_в_mssql';
```

#### 2.2 При ошибке миграции
```sql
UPDATE migration_control.specific_objects 
SET migration_status = 'failed', 
    migration_date = CURRENT_TIMESTAMP,
    error_message = 'описание_ошибки'
WHERE name_in_mssql = 'имя_в_mssql';
```

#### 2.3 При изменении типа объекта
```sql
UPDATE migration_control.objects 
SET has_in_postgres = true,
    name_in_postgres = 'новое_имя_типа'
WHERE object_type = 'тип_объекта';
```

### 3. Мониторинг прогресса

#### 3.1 Просмотр общего прогресса
```bash
# Запуск скрипта просмотра прогресса
python3 src/infrastructure/scripts/view-migration-progress.py
```

#### 3.2 SQL-запросы для мониторинга

**Общий прогресс:**
```sql
SELECT * FROM migration_control.migration_progress;
```

**Проблемные объекты:**
```sql
SELECT * FROM migration_control.detailed_progress 
WHERE migration_status IN ('failed', 'pending');
```

**Статистика по типам:**
```sql
SELECT object_type, 
       COUNT(*) as total,
       COUNT(CASE WHEN migration_status = 'completed' THEN 1 END) as completed,
       ROUND(COUNT(CASE WHEN migration_status = 'completed' THEN 1 END)::DECIMAL / COUNT(*)::DECIMAL * 100, 2) as percentage
FROM migration_control.objects o
JOIN migration_control.specific_objects so ON o.id = so.object_id
GROUP BY object_type
ORDER BY percentage DESC;
```

## 📋 Процедуры обновления

### Ежедневное обновление
1. **Запуск скрипта просмотра прогресса** для получения актуальной статистики
2. **Проверка проблемных объектов** и их статусов
3. **Обновление документации** с новыми данными

### После миграции объектов
1. **Обновление статусов** в таблице `specific_objects`
2. **Проверка целостности** данных
3. **Обновление отчетов** о прогрессе

### При выявлении ошибок
1. **Запись ошибки** в поле `error_message`
2. **Установка статуса** `failed`
3. **Анализ причин** и планирование исправления

## 🔧 Инструменты

### Скрипты управления

1. **`create-migration-control-schema.py`**
   - Создание схемы и всех объектов системы контроля

2. **`populate-migration-control-tables.py`**
   - Заполнение таблиц данными из SQL Server и PostgreSQL

3. **`view-migration-progress.py`**
   - Просмотр текущего прогресса миграции

### Дополнительные инструменты (планируются)

1. **`update-migration-status.py`**
   - Массовое обновление статусов миграции

2. **`generate-migration-report.py`**
   - Генерация детальных отчетов о миграции

3. **`validate-migration-data.py`**
   - Валидация данных в системе контроля

## 📈 Метрики и KPI

### Ключевые показатели
- **Общий прогресс миграции** (в процентах)
- **Прогресс по типам объектов** (в процентах)
- **Количество ошибок** миграции
- **Время выполнения** миграции объектов

### Целевые показатели
- **100% завершение** миграции таблиц
- **0 ошибок** в процессе миграции
- **Полная синхронизация** между SQL Server и PostgreSQL

## 🚨 Обработка проблем

### Типичные проблемы и решения

1. **Объект не найден в PostgreSQL**
   - Проверить правильность имени объекта
   - Убедиться в успешности миграции
   - Обновить статус на `failed` с описанием ошибки

2. **Несоответствие типов объектов**
   - Проверить классификацию объекта
   - Обновить тип в таблице `objects`
   - Пересчитать статистику

3. **Дублирование объектов**
   - Проверить уникальность имен
   - Очистить дубликаты
   - Обновить связи в таблицах

## 📚 Документация

### Связанные документы
- `views-migration-analysis-report.md` - Анализ мигрированных представлений
- `ags-migration-current-status.md` - Текущий статус миграции схемы AGS
- `changelog.md` - Журнал изменений проекта

### Диаграммы и схемы
- `docs/schemes/entity-relationship/` - Диаграммы сущность-связь системы контроля миграции
- `migration-control-system-schema.puml` - Основная схема данных
- `migration-functions-schema.puml` - Схема функций и триггеров
- `migration-process-flow.puml` - Диаграмма процесса миграции
- `migration-reporting-system.puml` - Схема системы отчетности

### Отчеты
- Ежедневные отчеты о прогрессе сохраняются в `docs/infrastructure/reports/`
- Логи выполнения скриптов в `docs/infrastructure/logs/`

---

**Автор:** AI Assistant  
**Последнее обновление:** 31 августа 2025  
**Статус:** Активная система контроля