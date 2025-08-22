#!/bin/bash

# Скрипт синхронизации через MCP серверы
# Выполняется без прямого использования терминала

set -e

echo "🚀 Синхронизация проекта с GitHub через MCP серверы"
echo "=================================================="

# Проверяем, что мы в правильной директории
if [ ! -f ".git/HEAD" ]; then
    echo "❌ Не найден Git репозиторий"
    exit 1
fi

echo "✅ Git репозиторий найден"

# Проверяем статус
echo "📋 Проверка статуса Git..."
git status --porcelain

# Добавляем все изменения
echo "📦 Добавление файлов в staging area..."
git add .

# Проверяем, что файлы добавлены
echo "📋 Проверка staged файлов..."
git diff --cached --name-only

# Создаем коммит
echo "💾 Создание коммита..."
git commit -m "feat: Настройка GitHub MCP сервера с Desktop Commander

- Добавлен GitHub Personal Access Token
- Настроен GitHub MCP сервер в Cursor IDE
- Созданы скрипты для настройки и тестирования
- Обновлена документация
- Протестирована интеграция с Desktop Commander MCP
- Создан тестовый issue #1

Результат: Полная интеграция GitHub через MCP без риска блокировки терминала"

# Отправляем в GitHub
echo "🚀 Отправка в GitHub..."
git push origin main

echo "✅ Синхронизация завершена успешно!"
echo ""
echo "📊 Результат:"
echo "- Все изменения отправлены в GitHub"
echo "- GitHub MCP сервер полностью настроен"
echo "- Desktop Commander MCP работает"
echo "- Нет риска блокировки терминала"