# Скрипты Backend

Эта папка содержит все shell скрипты для работы с backend модулем.

## Структура

### `database/` - Скрипты для работы с базой данных
- `fix-liquibase.sh` - Исправление проблем с Liquibase
- `force-migrate.sh` - Принудительная миграция БД

### `performance/` - Скрипты для тестирования производительности
- `run-performance-benchmark.sh` - Запуск бенчмарков производительности
- `run-performance-mode.sh` - Запуск в режиме производительности

### `testing/` - Скрипты для тестирования
- `test-actuator.sh` - Тестирование Actuator endpoints
- `test-auth.sh` - Тестирование аутентификации

## Использование

Все скрипты должны запускаться из корневой папки проекта (`/home/alex/vuege`).

Пример:
```bash
cd /home/alex/vuege
./src/backend/scripts/database/fix-liquibase.sh
```