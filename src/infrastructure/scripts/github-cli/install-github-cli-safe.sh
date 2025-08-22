#!/bin/bash

# Безопасная установка GitHub CLI с защитой от pager
# Использует Desktop Commander MCP подход

set -e

echo "🔧 Безопасная установка GitHub CLI"
echo "=================================="

# Проверяем, установлен ли уже GitHub CLI
if command -v gh &> /dev/null; then
    echo "✅ GitHub CLI уже установлен"
    gh --version | cat
    exit 0
fi

echo "📦 Установка GitHub CLI..."

# Добавляем репозиторий GitHub CLI
echo "Добавление репозитория GitHub CLI..."
curl -fsSL https://cli.github.com/packages/githubcli-archive-keyring.gpg | sudo dd of=/usr/share/keyrings/githubcli-archive-keyring.gpg

echo "deb [arch=$(dpkg --print-architecture) signed-by=/usr/share/keyrings/githubcli-archive-keyring.gpg] https://cli.github.com/packages stable main" | sudo tee /etc/apt/sources.list.d/github-cli.list > /dev/null

# Обновляем пакеты (с защитой от pager)
echo "Обновление пакетов..."
sudo apt update | cat

# Устанавливаем GitHub CLI
echo "Установка GitHub CLI..."
sudo apt install gh -y | cat

# Проверяем установку
if command -v gh &> /dev/null; then
    echo "✅ GitHub CLI успешно установлен"
    gh --version | cat
else
    echo "❌ Ошибка установки GitHub CLI"
    exit 1
fi

echo ""
echo "🎉 GitHub CLI готов к использованию!"
echo ""
echo "Следующие шаги:"
echo "1. ./setup-github-cli-safe.sh - аутентификация"
echo "2. ./test-github-cli-safe.sh - тестирование"
echo ""