# SQL файлы Backend

Эта папка содержит все SQL файлы для работы с базой данных.

## Структура

### `migrations/` - Файлы миграций
- `force-liquibase-migration.sql` - Принудительная миграция через Liquibase
- `manual-migrate.sql` - Ручная миграция БД
- `move-tables.sql` - Перемещение таблиц

### `data/` - Файлы с данными
- `insert-person-positions.sql` - Вставка связей персон и позиций
- `insert-test-data-fixed.sql` - Исправленные тестовые данные
- `insert-test-data.sql` - Тестовые данные

## Использование

### Миграции
Файлы миграций выполняются автоматически через Liquibase или вручную через psql.

### Тестовые данные
Файлы с данными используются для заполнения БД тестовыми данными.

Пример выполнения:
```bash
psql -d your_database -f sql/data/insert-test-data.sql
```