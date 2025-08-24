# Синхронизация проекта с GitHub

## 🎯 Цель
Безопасная и автоматизированная синхронизация проекта Vuege с GitHub репозиторием.

## 🚨 Проблемы и решения

### Проблема P250817-02: Блокировка терминала pager
**Решение**: Использование Desktop Commander MCP для всех Git операций

### Проблема с GitHub токенами
**Решение**: Использование GitHub CLI вместо токенов

### Проблема с реорганизацией файлов
**Решение**: Обновление путей в скриптах и документации

## 🔧 Методы синхронизации

### 1. Автоматическая синхронизация (РЕКОМЕНДУЕТСЯ)

#### Через GitHub CLI:
```bash
# Безопасная синхронизация
./src/infrastructure/scripts/github-cli/sync-safe.sh
```

#### Через Python скрипт:
```bash
# Синхронизация через API
python3 src/infrastructure/scripts/github-sync.py
```

### 2. Ручная синхронизация

#### Проверка статуса:
```bash
# Безопасная проверка статуса
git status --porcelain
```

#### Добавление изменений:
```bash
git add .
```

#### Создание коммита:
```bash
git commit -m "feat: Описание изменений

- Детальное описание изменений
- Список новых функций
- Исправленные проблемы

Дата: $(date '+%Y-%m-%d %H:%M:%S')"
```

#### Отправка в GitHub:
```bash
git push origin main
```

## 🛡️ Безопасность

### Защита от pager:
- ✅ Использование `--porcelain` для статуса
- ✅ Использование `--no-pager` для логов
- ✅ Desktop Commander MCP для всех операций

### Аутентификация:
- ✅ GitHub CLI вместо токенов
- ✅ Браузерная аутентификация
- ✅ Безопасное хранение учетных данных

## 📋 Процесс синхронизации

### 1. Подготовка
```bash
# Проверка аутентификации
gh auth status

# Проверка статуса репозитория
git status --porcelain
```

### 2. Добавление изменений
```bash
# Добавление всех изменений
git add .

# Проверка добавленных файлов
git diff --cached --name-only
```

### 3. Создание коммита
```bash
# Создание коммита с описанием
git commit -m "feat: Этап 6 - Интеграция с базой данных

- GraphQL API интегрирован с PostgreSQL
- Liquibase миграции настроены
- R2DBC репозитории работают
- Исправлены проблемы с парсингом дат
- Добавлены тестовые страницы
- Actuator мониторинг настроен

Результаты тестирования:
- ТЕСТ 1 (чтение): ✅ ПРОЙДЕН
- ТЕСТ 2 (создание): ✅ ПРОЙДЕН
- Actuator: ✅ ПРОЙДЕН

Статус: Этап 6 полностью завершен

Дата: $(date '+%Y-%m-%d %H:%M:%S')"
```

### 4. Отправка в GitHub
```bash
# Отправка в основной репозиторий
git push origin main

# Проверка результата
gh repo view bondalen/vuege
```

## 🔍 Мониторинг

### Проверка статуса:
```bash
# Статус GitHub CLI
gh auth status

# Статус репозитория
git status --porcelain

# Последние коммиты
git log --oneline -5
```

### Логирование:
```bash
# Логи синхронизации
tail -f ~/.github-sync.log

# Логи GitHub CLI
gh api rate_limit
```

## 🚨 Устранение проблем

### Проблема: "gh: command not found"
**Решение:**
```bash
# Установка GitHub CLI
./src/infrastructure/scripts/install-github-cli.sh
```

### Проблема: "not authenticated"
**Решение:**
```bash
# Повторная аутентификация
gh auth login
```

### Проблема: "pager blocks terminal"
**Решение:**
```bash
# Использование Desktop Commander MCP
# Или настройка pager
export PAGER=cat
git config --global core.pager cat
```

### Проблема: "push rejected"
**Решение:**
```bash
# Получение изменений с GitHub
git fetch origin
git pull origin main

# Повторная отправка
git push origin main
```

## 📊 Автоматизация

### Скрипт автоматической синхронизации:
```bash
#!/bin/bash
# Автоматическая синхронизация

echo "🔄 Автоматическая синхронизация проекта"
echo "======================================"

# Проверка аутентификации
if ! gh auth status &> /dev/null; then
    echo "❌ GitHub CLI не аутентифицирован"
    exit 1
fi

# Проверка изменений
if [ -z "$(git status --porcelain)" ]; then
    echo "✅ Нет изменений для синхронизации"
    exit 0
fi

# Синхронизация
git add .
git commit -m "feat: Автоматическая синхронизация - $(date '+%Y-%m-%d %H:%M:%S')"
git push origin main

echo "✅ Синхронизация завершена"
```

## 🔄 Последние изменения (2025-08-24)

### Реорганизация структуры backend:
- **Создана структура папок**: `scripts/`, `sql/`, `config/`
- **Перемещены SQL файлы**: в `sql/migrations/` и `sql/data/`
- **Перемещены shell скрипты**: в `scripts/database/`, `scripts/performance/`, `scripts/testing/`
- **Перемещен конфигурационный файл**: в `config/`
- **Созданы README.md файлы**: для каждой папки
- **Обновлены пути в скриптах**: для работы из новой структуры

### Новые файлы и изменения:
- **Новые сущности**: AuditLog, Notification, Webhook, User
- **Новые enum типы**: StatusType, NotificationType, AuditActionType, UserRole
- **Новые резолверы**: ExtendedQueryResolver, AuthResolver, WebhookResolver, AuditResolver, NotificationResolver
- **Новые сервисы**: ExtendedQueryService, AuthService, JwtService
- **Новые конфигурации**: WebSocketConfig, SecurityConfig, RateLimitConfig
- **Новые миграции**: для расширенной функциональности
- **Новые тесты**: интеграционные тесты для ExtendedQueryResolver

### Исправленные проблемы:
- **Этап 8 завершен**: Все 22 проблемы компиляции решены
- **GraphQL схема**: Расширена до 685 строк
- **Тесты**: Все тесты проходят успешно
- **Документация**: Обновлена changelog.md

## 🎯 Результат

После успешной синхронизации:
- ✅ Все изменения сохранены в GitHub
- ✅ История коммитов обновлена
- ✅ Проект доступен в репозитории
- ✅ Безопасность обеспечена
- ✅ Автоматизация настроена

---
**Создано**: 2025-08-24  
**Статус**: Актуально  
**Приоритет**: Высокий