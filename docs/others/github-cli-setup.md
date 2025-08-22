# GitHub CLI - Установка и настройка

## 🎯 Цель
Настроить GitHub CLI для безопасной работы с GitHub без использования токенов.

## 🚨 Проблема с GitHub MCP Server

### Что произошло:
- GitHub MCP Server **удаляет токены** после использования
- Два токена исчезли после работы с MCP Server
- Это системная проблема, а не случайность

### Решение:
**Использовать GitHub CLI вместо GitHub MCP Server**

## 🔧 Установка GitHub CLI

### Автоматическая установка:
```bash
# Установка GitHub CLI
./src/infrastructure/scripts/install-github-cli.sh

# Настройка аутентификации
./src/infrastructure/scripts/setup-github-cli.sh

# Тестирование
./src/infrastructure/scripts/test-github-cli.sh
```

### Ручная установка:
```bash
# Добавление репозитория
curl -fsSL https://cli.github.com/packages/githubcli-archive-keyring.gpg | sudo dd of=/usr/share/keyrings/githubcli-archive-keyring.gpg

echo "deb [arch=$(dpkg --print-architecture) signed-by=/usr/share/keyrings/githubcli-archive-keyring.gpg] https://cli.github.com/packages stable main" | sudo tee /etc/apt/sources.list.d/github-cli.list > /dev/null

# Установка
sudo apt update
sudo apt install gh -y
```

## 🔐 Аутентификация

### Интерактивная настройка:
```bash
gh auth login
```

### Выборы при настройке:
1. **GitHub.com** - основной сервис
2. **HTTPS** - безопасное соединение
3. **Yes** - аутентификация через браузер
4. **Следовать инструкциям** в браузере

### Проверка статуса:
```bash
gh auth status
```

## 🚀 Основные команды

### Репозитории:
```bash
# Просмотр репозитория
gh repo view bondalen/vuege

# Клонирование репозитория
gh repo clone bondalen/vuege

# Создание репозитория
gh repo create my-new-repo --public
```

### Issues:
```bash
# Список issues
gh issue list

# Создание issue
gh issue create --title "Новый issue" --body "Описание"

# Просмотр issue
gh issue view 1

# Закрытие issue
gh issue close 1
```

### Pull Requests:
```bash
# Список PR
gh pr list

# Создание PR
gh pr create --title "Новый PR" --body "Описание"

# Просмотр PR
gh pr view 1

# Слияние PR
gh pr merge 1
```

### Рабочие процессы:
```bash
# Список workflows
gh workflow list

# Запуск workflow
gh workflow run build.yml

# Просмотр runs
gh run list
```

## 🛡️ Преимущества GitHub CLI

### ✅ Безопасность:
- **Нет токенов** = нет риска их удаления
- **Аутентификация через браузер** - безопасно
- **Официальный инструмент** GitHub

### ✅ Стабильность:
- **Проверенный временем** инструмент
- **Хорошая документация**
- **Активная поддержка**

### ✅ Функциональность:
- **Все основные операции** с GitHub
- **Интеграция с Git**
- **Автоматизация** через скрипты

## 🔧 Интеграция с MCP экосистемой

### Desktop Commander MCP:
```bash
# Выполнение команд через Desktop Commander MCP
gh issue create --title "Issue через MCP" --body "Описание"
gh pr list --repo bondalen/vuege
gh repo view bondalen/vuege
```

### Автоматизация:
```bash
# Создание issue через скрипт
gh issue create \
    --repo bondalen/vuege \
    --title "Автоматический issue" \
    --body "Создан автоматически"

# Список issues в JSON
gh issue list --repo bondalen/vuege --json number,title,state
```

## 📊 Мониторинг и логирование

### Логирование команд:
```bash
# Добавить в скрипты
echo "$(date): GitHub CLI command: $*" >> ~/.github-cli.log
gh "$@"
```

### Проверка статуса:
```bash
# Проверка аутентификации
gh auth status

# Проверка версии
gh --version

# Проверка доступных команд
gh help
```

## 🚨 Устранение проблем

### Проблема: "gh: command not found"
**Решение:**
```bash
# Переустановка
sudo apt remove gh
sudo apt install gh
```

### Проблема: "not authenticated"
**Решение:**
```bash
# Повторная аутентификация
gh auth logout
gh auth login
```

### Проблема: "rate limit exceeded"
**Решение:**
```bash
# Проверка лимитов
gh api rate_limit

# Ожидание сброса лимитов
```

## 🎯 Результат

После настройки GitHub CLI:
- ✅ **Безопасная работа** без токенов
- ✅ **Полная функциональность** GitHub
- ✅ **Интеграция с MCP** экосистемой
- ✅ **Стабильная работа** без рисков

---
**Создано**: 2025-08-22  
**Статус**: Готово к использованию  
**Приоритет**: Высокий