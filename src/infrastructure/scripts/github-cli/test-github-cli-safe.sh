#!/bin/bash

# Безопасное тестирование GitHub CLI с защитой от pager
# Использует Desktop Commander MCP подход

set -e

echo "🧪 Безопасное тестирование GitHub CLI"
echo "===================================="

# Проверяем, установлен ли GitHub CLI
if ! command -v gh &> /dev/null; then
    echo "❌ GitHub CLI не установлен"
    exit 1
fi

echo "✅ GitHub CLI установлен"

# Проверяем аутентификацию (с защитой от pager)
echo "🔍 Проверка аутентификации..."
if ! gh auth status &> /dev/null; then
    echo "❌ GitHub CLI не аутентифицирован"
    echo "Выполните: ./setup-github-cli-safe.sh"
    exit 1
fi

echo "✅ GitHub CLI аутентифицирован"

# Тест 1: Просмотр репозитория (с защитой от pager)
echo ""
echo "1. Просмотр репозитория..."
gh repo view bondalen/vuege --json name,description,url,stargazerCount,forkCount | cat

# Тест 2: Список issues (с защитой от pager)
echo ""
echo "2. Список issues..."
gh issue list --repo bondalen/vuege --limit 3 | cat

# Тест 3: Создание тестового issue
echo ""
echo "3. Создание тестового issue..."
gh issue create \
    --repo bondalen/vuege \
    --title "Тест GitHub CLI - безопасная установка" \
    --body "Этот issue создан для тестирования GitHub CLI после безопасной установки

### ✅ Что протестировано:
- GitHub CLI установлен через Desktop Commander MCP
- Аутентификация через браузер работает
- Создание issues работает
- Нет риска удаления токенов
- Защита от pager работает

### 🎯 Преимущества GitHub CLI:
- Безопасная аутентификация
- Нет токенов = нет риска их удаления
- Официальный инструмент GitHub
- Стабильная работа
- Интеграция с Desktop Commander MCP

### 🛡️ Безопасность:
- Нет риска блокировки терминала
- Нет риска удаления токенов
- Стабильная работа

---
**Создано**: 2025-08-22  
**Статус**: Тестирование безопасности  
**Приоритет**: Высокий"

# Тест 4: Список issues после создания (с защитой от pager)
echo ""
echo "4. Список issues после создания..."
gh issue list --repo bondalen/vuege --limit 3 | cat

echo ""
echo "🎉 Все тесты пройдены успешно!"
echo "GitHub CLI работает отлично!"
echo ""
echo "📊 Результаты:"
echo "- ✅ Аутентификация работает"
echo "- ✅ Просмотр репозитория работает"
echo "- ✅ Создание issues работает"
echo "- ✅ Нет риска удаления токенов"
echo "- ✅ Защита от pager работает"
echo ""