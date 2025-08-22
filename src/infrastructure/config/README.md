# Infrastructure Configuration

## 📋 Описание

Конфигурационные файлы для инфраструктуры проекта.

## 📁 Файлы

### MCP Configuration:

1. **`mcp-config.json`** - Конфигурация MCP серверов для Cursor IDE
   - Настройки DBHub MCP сервера
   - Параметры подключения к PostgreSQL
   - Конфигурация транспорта (stdio)

## 🔧 Структура конфигурации

### DBHub MCP Server:
```json
{
  "mcpServers": {
    "dbhub": {
      "command": "node",
      "args": ["/home/alex/vuege/dbhub/dist/index.js", "--transport", "stdio", "--dsn", "postgres://testuser:testpass@localhost:5432/testdb?sslmode=disable"],
      "env": {
        "READONLY": "false"
      }
    }
  }
}
```

## 🚀 Использование

Конфигурация автоматически загружается Cursor IDE при запуске.

## 🔗 Связанные документы

- [MCP Management Scripts](../scripts/mcp-management/README.md)
- [DBHub Setup Guide](../../../docs/others/dbhub-setup.md)

---
**Создано**: 2025-08-21  
**Статус**: Активно  
**Версия**: 1.0