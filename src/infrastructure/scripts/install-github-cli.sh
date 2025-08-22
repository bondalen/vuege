#!/bin/bash

# Скрипт установки GitHub CLI
# Использует Desktop Commander MCP для безопасной установки

set -e

echo "🔧 Установка GitHub CLI"
echo "======================"

# Проверяем, установлен ли уже GitHub CLI
if command -v gh &> /dev/null; then
    echo "✅ GitHub CLI уже установлен"
    gh --version
    exit 0
fi

echo "📦 Установка GitHub CLI..."

# Добавляем репозиторий GitHub CLI
echo "Добавление репозитория GitHub CLI..."
curl -fsSL https://cli.github.com/packages/githubcli-archive-keyring.gpg | sudo dd of=/usr/share/keyrings/githubcli-archive-keyring.gpg

echo "deb [arch=$(dpkg --print-architecture) signed-by=/usr/share/keyrings/githubcli-archive-keyring.gpg] https://cli.github.com/packages stable main" | sudo tee /etc/apt/sources.list.d/github-cli.list > /dev/null

# Обновляем пакеты
echo "Обновление пакетов..."
sudo apt update

# Устанавливаем GitHub CLI
echo "Установка GitHub CLI..."
sudo apt install gh -y

# Проверяем установку
if command -v gh &> /dev/null; then
    echo "✅ GitHub CLI успешно установлен"
    gh --version
else
    echo "❌ Ошибка установки GitHub CLI"
    exit 1
fi

echo ""
echo "🎉 GitHub CLI готов к использованию!"
echo ""
echo "Следующие шаги:"
echo "1. gh auth login - аутентификация"
echo "2. gh auth status - проверка статуса"
echo "3. gh repo view - просмотр репозитория"
echo ""