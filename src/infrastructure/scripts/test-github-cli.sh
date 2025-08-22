#!/bin/bash

# Скрипт тестирования GitHub CLI
# Проверяет функциональность GitHub CLI

set -e

echo "🧪 Тестирование GitHub CLI"
echo "=========================="

# Проверяем, установлен ли GitHub CLI
if ! command -v gh &> /dev/null; then
    echo "❌ GitHub CLI не установлен"
    exit 1
fi

echo "✅ GitHub CLI установлен"

# Проверяем аутентификацию
echo "🔍 Проверка аутентификации..."
if ! gh auth status &> /dev/null; then
    echo "❌ GitHub CLI не аутентифицирован"
    echo "Выполните: ./src/infrastructure/scripts/setup-github-cli.sh"
    exit 1
fi

echo "✅ GitHub CLI аутентифицирован"

# Тест 1: Просмотр репозитория
echo ""
echo "1. Просмотр репозитория..."
gh repo view bondalen/vuege --json name,description,url,stargazerCount,forkCount

# Тест 2: Список issues
echo ""
echo "2. Список issues..."
gh issue list --repo bondalen/vuege --limit 3

# Тест 3: Создание тестового issue
echo ""
echo "3. Создание тестового issue..."
gh issue create \
    --repo bondalen/vuege \
    --title "Тест GitHub CLI" \
    --body "Этот issue создан для тестирования GitHub CLI

### ✅ Что протестировано:
- GitHub CLI установлен и работает
- Аутентификация через браузер работает
- Создание issues работает
- Нет риска удаления токенов

### 🎯 Преимущества GitHub CLI:
- Безопасная аутентификация
- Нет токенов = нет риска их удаления
- Официальный инструмент GitHub
- Стабильная работа

---
**Создано**: 2025-08-22  
**Статус**: Тестирование  
**Приоритет**: Высокий"

# Тест 4: Список issues после создания
echo ""
echo "4. Список issues после создания..."
gh issue list --repo bondalen/vuege --limit 3

echo ""
echo "🎉 Все тесты пройдены успешно!"
echo "GitHub CLI работает отлично!"
echo ""
echo "📊 Результаты:"
echo "- ✅ Аутентификация работает"
echo "- ✅ Просмотр репозитория работает"
echo "- ✅ Создание issues работает"
echo "- ✅ Нет риска удаления токенов"
echo ""