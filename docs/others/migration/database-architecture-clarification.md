# 🗄️ Архитектура баз данных проекта Vuege - УТОЧНЕНИЕ

**Дата создания:** 2 сентября 2025  
**Статус:** Актуально  
**Версия:** 1.0

## 🚨 КРИТИЧЕСКОЕ УТОЧНЕНИЕ

**В проекте Vuege используются ДВЕ РАЗНЫЕ базы данных PostgreSQL с РАЗНЫМИ целями!**

## 📊 СТРУКТУРА БАЗ ДАННЫХ

### 🎯 База данных `vuege` (Основная)
- **Назначение**: Основная база данных проекта Vuege
- **Контейнер**: postgres-java-universal:5432
- **Пользователь**: testuser (основной), postgres (админ)
- **Схемы**:
  - `public` - Основные таблицы приложения (14 таблиц)
  - `ags` - Схема для бизнес-логики (236 таблиц - уже мигрированы!)
  - `gis` - Географические данные
  - `history` - Исторические данные
  - `migration_control` - Базовая система контроля миграции (3 таблицы)
  - `vuege` - Служебные таблицы

### 🚀 База данных `Fish_Eye` (Миграция)
- **Назначение**: Целевая база для миграции MS SQL → PostgreSQL
- **Контейнер**: postgres-java-universal:5432
- **Пользователь**: postgres
- **Схемы**:
  - `ags` - Пуста (готово для миграции данных из MS SQL)
  - `mcl` - Продвинутая система контроля миграции (26 таблиц)
  - `public` - Системные таблицы

## 🔍 ТЕКУЩЕЕ СОСТОЯНИЕ

### ✅ Что уже готово:
1. **База `vuege`**: Полностью функциональна с 236 таблицами в схеме ags
2. **База `Fish_Eye`**: Система контроля миграции готова (166 таблиц MS SQL зарегистрированы)
3. **Схема `mcl`**: 26 таблиц с полной функциональностью контроля миграции

### 🔄 Что нужно сделать:
1. **Мигрировать данные** из MS SQL Server в базу `Fish_Eye`, схема `ags`
2. **Обновить статусы** в таблицах `mcl.mssql_tables` и `mcl.postgres_tables`
3. **Валидировать** перенесенные данные

## 🛠️ КОМАНДЫ ДЛЯ РАБОТЫ

### Подключение к базе `vuege`:
```bash
docker exec postgres-java-universal psql -U testuser -d vuege
```

### Подключение к базе `Fish_Eye`:
```bash
docker exec postgres-java-universal psql -U postgres -d Fish_Eye
```

### Проверка статуса миграции:
```bash
# Количество таблиц MS SQL
docker exec postgres-java-universal psql -U postgres -d Fish_Eye -c "SELECT COUNT(*) FROM mcl.mssql_tables WHERE schema_name = 'ags';"

# Статус миграции
docker exec postgres-java-universal psql -U postgres -d Fish_Eye -c "SELECT migration_status, COUNT(*) FROM mcl.mssql_tables WHERE schema_name = 'ags' GROUP BY migration_status;"

# Количество мигрированных таблиц
docker exec postgres-java-universal psql -U postgres -d Fish_Eye -c "SELECT COUNT(*) FROM mcl.postgres_tables;"
```

## 📋 СИСТЕМА КОНТРОЛЯ МИГРАЦИИ (mcl)

### 🎯 Основные таблицы:
- **migration_tasks** - Задачи миграции
- **migration_problems** - Проблемы миграции
- **mssql_objects** - Базовые объекты MS SQL
- **mssql_tables** - Таблицы MS SQL (наследует от mssql_objects)
- **postgres_objects** - Базовые объекты PostgreSQL
- **postgres_tables** - Таблицы PostgreSQL (наследует от postgres_objects)

### 🔧 Вспомогательные таблицы:
- **mssql_columns** - Колонки таблиц MS SQL
- **postgres_columns** - Колонки таблиц PostgreSQL
- **mssql_data_types** - Типы данных MS SQL
- **postgres_data_types** - Типы данных PostgreSQL
- **table_migration_problems** - Проблемы миграции таблиц
- **column_migration_problems** - Проблемы миграции колонок

## ⚠️ ВАЖНЫЕ ЗАМЕЧАНИЯ

1. **НЕ ПУТАТЬ** базы `vuege` и `Fish_Eye` - это разные базы с разными целями
2. **База `vuege`** уже содержит мигрированные данные в схеме ags
3. **База `Fish_Eye`** предназначена для новой миграции с использованием системы mcl
4. **Система mcl** в базе `Fish_Eye` более продвинутая, чем `migration_control` в базе `vuege`

## 🎯 СЛЕДУЮЩИЕ ШАГИ

1. **Завершить миграцию** данных из MS SQL в базу `Fish_Eye`
2. **Обновить документацию** проекта с учетом двух баз данных
3. **Интегрировать** систему mcl с основным приложением
4. **Тестировать** работу с мигрированными данными

## 📞 ПОДДЕРЖКА

При возникновении путаницы с базами данных:
1. Проверьте название базы в команде подключения
2. Убедитесь, что используете правильную схему
3. Обратитесь к данной документации
4. Проверьте статус миграции через систему mcl