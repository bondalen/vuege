# MCP Management - Скрипты управления

## 📋 Описание

Набор скриптов для управления MCP серверами и их конфигурацией.

## 🛠️ Файлы

### Основные скрипты:

1. **`manage-dbhub.sh`** - Скрипт управления DBHub MCP сервером
   - Запуск/остановка сервера
   - Проверка статуса
   - Тестирование API
   - Просмотр логов

2. **`cleanup_mcp_backups.py`** - Python скрипт очистки MCP бэкапов
   - Безопасное удаление резервных копий
   - Решение проблемы P250821-01 с блокировкой терминала
   - Автоматическая очистка старых файлов

## 🚀 Использование

### Управление DBHub:
```bash
./manage-dbhub.sh start    # Запуск сервера
./manage-dbhub.sh stop     # Остановка сервера
./manage-dbhub.sh restart  # Перезапуск
./manage-dbhub.sh status   # Статус
./manage-dbhub.sh test     # Тестирование API
./manage-dbhub.sh logs     # Просмотр логов
```

### Очистка бэкапов:
```bash
python3 cleanup_mcp_backups.py
```

## 📁 Конфигурация

Конфигурация MCP серверов находится в:
`../config/mcp-config.json`

## 🔗 Связанные документы

- [DBHub MCP Server Setup](../../../docs/others/dbhub-setup.md)
- [MCP Configuration Guide](../../../docs/others/mcp-configuration.md)

---
**Создано**: 2025-08-21  
**Статус**: Активно  
**Версия**: 1.0