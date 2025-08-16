# Исходный код проекта Vuege

Эта папка содержит **ИСПОЛНЕНИЕ** проекта - всю кодовую базу и ресурсы.

## Структура папок

### `backend/`
Backend код проекта на Spring Boot:
- Java 21 LTS
- Spring Boot 3.4.5
- GraphQL API
- R2DBC для работы с PostgreSQL
- Lombok для минимизации boilerplate кода

### `frontend/`
Frontend код проекта:
- Vue.js 3.4.21
- Quasar Framework 2.16.1
- TypeScript 5.4.0
- TanStack Router 1.16.0
- Apollo Client 3.13.5

### `infrastructure/`
Инфраструктурные файлы проекта:

#### `infrastructure/docker/`
- Dockerfile.postgres-java - универсальный контейнер PostgreSQL + Java
- README.md - документация по Docker

#### `infrastructure/scripts/`
- Скрипты автоматизации и настройки
- MCP серверы для Cursor IDE
- SSH настройка и управление
- Тестирование и отладка

#### `infrastructure/configs/`
- Конфигурационные файлы проекта
- Настройки для различных сред разработки

## Правила размещения файлов

1. **Новый код** размещается в соответствующих папках `backend/` или `frontend/`
2. **Инфраструктурные файлы** размещаются в `infrastructure/` с подразделением по типам
3. **Скрипты** добавляются в `infrastructure/scripts/`
4. **Конфигурации** добавляются в `infrastructure/configs/`
5. **Docker файлы** размещаются в `infrastructure/docker/`

---

*Структура соответствует архитектуре проекта, описанной в `docs/main/project.md`*
