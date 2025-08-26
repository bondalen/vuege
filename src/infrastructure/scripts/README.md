# Скрипты проекта Vuege

## Основные скрипты

### Управление проектом
- `sync-with-github.sh` - Синхронизация проекта с GitHub
- `update-node-maven.sh` - Обновление Node.js в Maven конфигурации
- `test-graphql-api.sh` - Тестирование GraphQL API

### Запуск сервисов
- `start-backend.sh` - Запуск Spring Boot приложения
- `start-postgresql.sh` - Запуск PostgreSQL контейнера

### Управление базой данных
- `check-database.sh` - Проверка состояния базы данных
- `clean-and-restart-liquibase.sh` - Очистка и перезапуск Liquibase
- `load-test-data.sh` - Загрузка тестовых данных

### Исправления и настройки
- `fix-*.sh` - Скрипты исправления различных проблем
- `setup-*.sh` - Скрипты настройки компонентов

## Использование

### Из корня проекта (через алиасы)
```bash
./run-sync-github.sh    # Синхронизация с GitHub
./run-update-node.sh    # Обновление Node.js
./run-test-api.sh       # Тестирование API
./run-backend.sh        # Запуск Backend
./run-postgresql.sh     # Запуск PostgreSQL
```

### Прямое использование
```bash
cd src/infrastructure/scripts/
./sync-with-github.sh
./start-backend.sh
```

## Структура

Все скрипты организованы в одной директории согласно правилам проекта:
- Основные скрипты управления проектом
- Скрипты запуска сервисов
- Скрипты работы с базой данных
- Скрипты исправления и настройки
- MCP серверы и обертки
