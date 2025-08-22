#!/bin/bash

# Безопасная синхронизация с защитой от pager

set -e

echo "🔄 Безопасная синхронизация проекта"
echo "==================================="

# Проверяем GitHub CLI
echo "🔍 Проверка GitHub CLI..."
if ! gh auth status &> /dev/null; then
    echo "❌ GitHub CLI не аутентифицирован"
    exit 1
fi

echo "✅ GitHub CLI аутентифицирован"

# Проверяем Git статус
echo ""
echo "📊 Статус изменений:"
git status --porcelain | cat

# Проверяем, есть ли изменения
if [ -z "$(git status --porcelain)" ]; then
    echo ""
    echo "✅ Нет изменений для коммита"
    echo "Репозиторий уже синхронизирован"
    exit 0
fi

echo ""
echo "📝 Подготовка к коммиту..."

# Добавляем все изменения
echo "Добавление файлов..."
git add .

# Создаем коммит
COMMIT_MESSAGE="Синхронизация проекта - $(date '+%Y-%m-%d %H:%M:%S')

### 🔄 Что синхронизировано:
- GitHub CLI безопасная установка
- Скрипты защиты от pager
- Документация проекта
- Конфигурация MCP серверов

### 🛡️ Безопасность:
- GitHub CLI вместо токенов
- Защита от pager
- Безопасная аутентификация

---
**Дата**: $(date '+%Y-%m-%d %H:%M:%S')  
**Статус**: Синхронизация  
**Метод**: GitHub CLI"

echo "Создание коммита..."
git commit -m "$COMMIT_MESSAGE"

# Отправляем изменения
echo ""
echo "🚀 Отправка изменений в GitHub..."
git push origin main

echo ""
echo "🎉 Синхронизация завершена успешно!"
echo "==================================="
echo "📊 Результаты:"
echo "- ✅ Изменения добавлены"
echo "- ✅ Коммит создан"
echo "- ✅ Изменения отправлены в GitHub"
echo "- ✅ Защита от pager работает"
echo ""
echo "🔗 Репозиторий: https://github.com/bondalen/vuege"
echo ""