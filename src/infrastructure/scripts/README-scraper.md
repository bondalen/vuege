# Cursor Directory Scraper

Скрипт для автоматизации поиска MCP серверов на [cursor.directory](https://cursor.directory/mcp).

## Описание

Этот скрипт решает проблему [P250817-03] - невозможность прямого доступа к API cursor.directory из-за клиентского рендеринга Next.js. Использует Playwright для автоматизации браузера и извлечения данных о MCP серверах.

## Установка

1. Установите зависимости:
```bash
pip install -r requirements-scraper.txt
```

2. Установите браузеры для Playwright:
```bash
playwright install
```

## Использование

### Поиск MCP серверов
```bash
python cursor-directory-scraper.py search terminal
python cursor-directory-scraper.py search java
python cursor-directory-scraper.py search database
```

### Получение выделенных серверов
```bash
python cursor-directory-scraper.py featured
```

### Управление кэшем
```bash
# Просмотр сохраненных запросов
python cursor-directory-scraper.py cache

# Статистика кэша
python cursor-directory-scraper.py stats
```

## Возможности

- ✅ Поиск MCP серверов по ключевым словам
- ✅ Получение выделенных (featured) серверов
- ✅ Кэширование результатов для ускорения работы
- ✅ Извлечение метаданных: название, описание, ссылка, иконка
- ✅ Статистика использования кэша

## Структура кэша

Результаты сохраняются в папку `mcp_cache/`:
- `{query}.json` - результаты поиска по запросу
- `featured.json` - выделенные серверы
- Статистика использования

## Примеры использования

### Поиск терминальных серверов
```bash
python cursor-directory-scraper.py search terminal
```

### Поиск серверов для работы с базами данных
```bash
python cursor-directory-scraper.py search database
```

### Получение всех выделенных серверов
```bash
python cursor-directory-scraper.py featured
```

## Технические детали

- **Технология**: Playwright для автоматизации браузера
- **Язык**: Python 3.8+
- **Кэширование**: Локальные JSON файлы
- **Обработка ошибок**: Graceful handling с логированием
- **Производительность**: Асинхронная обработка

## Связь с проблемой [P250817-03]

Этот скрипт является решением проблемы невозможности прямого доступа к API cursor.directory. Он обходит ограничения клиентского рендеринга Next.js, используя браузерную автоматизацию для извлечения данных о MCP серверах.

## Планы развития

1. Добавление поддержки фильтрации по категориям
2. Интеграция с альтернативными источниками (GitHub, npm)
3. Создание веб-интерфейса для управления поиском
4. Автоматическая установка найденных MCP серверов
5. Экспорт данных в различные форматы (CSV, YAML)
