# Руководство по настройке токенов MCP серверов

## 🎯 Цель
Безопасная настройка токенов для MCP серверов без их попадания в git.

## 📋 Безопасный подход

### 1. Файл с токенами (НЕ в git)
Файл `~/.cursor/mcp.env` содержит реальные токены и НЕ попадает в git.

### 2. Конфигурация MCP (в git)
Файл `~/.cursor/mcp.json` содержит только placeholder токены.

## 🔧 Настройка токенов

### Шаг 1: Отредактируйте файл токенов
```bash
nano ~/.cursor/mcp.env
```

### Шаг 2: Замените placeholder на реальные токены
```bash
# GitHub Personal Access Token
GITHUB_PERSONAL_ACCESS_TOKEN=ghp_your_actual_token_here

# JIRA API Key  
JIRA_API_KEY=your_actual_jira_key_here
```

### Шаг 3: Загрузите токены в сессию
```bash
source ~/.cursor/mcp.env
```

## 🧪 Тестирование

### Запуск тестирования MCP серверов:
```bash
python src/infrastructure/scripts/test-mcp-servers.py
```

### Ожидаемый результат:
- ✅ Git MCP Server: Полностью работает
- ✅ GitHub MCP Server: Работает после настройки токена

## 🔒 Безопасность

### ✅ Правильно:
- Токены в `~/.cursor/mcp.env` (не в git)
- Placeholder в `~/.cursor/mcp.json` (в git)
- Файл `mcp.env` в `.gitignore`

### ❌ Неправильно:
- Реальные токены в git
- Токены в коде
- Токены в конфигурации MCP

## 📊 Статус

- **Git MCP Server**: ✅ Работает
- **GitHub MCP Server**: ⚠️ Требует токен
- **Desktop Commander MCP**: ✅ Работает
- **Безопасность**: ✅ Настроена

---

**Создано**: 2025-08-21  
**Статус**: Готово к использованию  
**Приоритет**: Высокий