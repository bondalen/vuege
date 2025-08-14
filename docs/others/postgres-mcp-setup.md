# PostgreSQL MCP Server - Установка и настройка

## Описание
PostgreSQL MCP Server предоставляет интеграцию с PostgreSQL базой данных в Cursor IDE через Model Context Protocol (MCP).

## Установленные компоненты

### 1. Виртуальное окружение Python
- Создано в директории `venv/`
- Активируется командой: `source venv/bin/activate`

### 2. PostgreSQL MCP Server
- Установлен пакет: `postgres-mcp`
- Версия: 0.3.0
- Путь к исполняемому файлу: `/home/alex/projects/vuege/venv/bin/postgres-mcp`

### 3. Конфигурационные файлы
- `~/.cursor/mcp/postgres-mcp.json` - конфигурация для Cursor
- `.env` - переменные окружения для подключения к БД
- `start-postgres-mcp.sh` - скрипт запуска сервера

## Настройка подключения к базе данных

### Шаг 1: Настройка PostgreSQL в Docker контейнере

PostgreSQL 16 установлен в контейнере `ubuntu-postgres-24.04`:

```bash
# Контейнер запущен с пробросом порта 5432
docker run -d --name ubuntu-postgres-24.04 -p 5432:5432 ubuntu:24.04 tail -f /dev/null

# Пользователь и база данных созданы:
# - Пользователь: testuser
# - Пароль: testpass
# - База данных: testdb
# - Порт: 5432
```

### Шаг 2: Параметры подключения

Файл `.env` настроен с реальными параметрами:

```bash
# PostgreSQL Configuration
POSTGRES_HOST=localhost
POSTGRES_PORT=5432
POSTGRES_DB=testdb
POSTGRES_USER=testuser
POSTGRES_PASSWORD=testpass

# PostgreSQL Database URI (формат для postgres-mcp)
DATABASE_URI=postgresql://testuser:testpass@localhost:5432/testdb
```

### Шаг 2: Убедитесь, что PostgreSQL сервер запущен
```bash
sudo systemctl status postgresql
```

### Шаг 3: Создайте базу данных (если не существует)
```bash
sudo -u postgres psql
CREATE DATABASE your_database_name;
CREATE USER your_username WITH PASSWORD 'your_password';
GRANT ALL PRIVILEGES ON DATABASE your_database_name TO your_username;
\q
```

## Тестирование подключения

### Проверка работы MCP Server
```bash
source venv/bin/activate
./start-postgres-mcp.sh --help
```

### Тест подключения к базе данных
```bash
source venv/bin/activate
export $(cat .env | grep -v '^#' | xargs)
postgres-mcp --database-uri $DATABASE_URI
```

## Использование в Cursor

После настройки подключения к базе данных:

1. Перезапустите Cursor
2. MCP Server автоматически подключится к PostgreSQL
3. Используйте команды для работы с базой данных:
   - Выполнение SQL запросов
   - Просмотр структуры таблиц
   - Управление схемой базы данных

## Устранение проблем с отображением в Cursor

### Проблема: PostgreSQL MCP Server не появляется в панели MCP Tools

**Возможные причины и решения:**

1. **Неправильный путь к конфигурации**
   - Проверьте, что файл создан в `~/.cursor/mcp.json`
   - Альтернативно: создайте в `.cursor/mcp.json` в корне проекта

2. **Неправильный формат конфигурации**
   ```json
   {
     "mcpServers": {
       "postgres-mcp": {
         "command": "/полный/путь/к/postgres-mcp",
         "args": ["--access-mode", "unrestricted"],
         "env": {},
         "description": "PostgreSQL MCP Server"
       }
     }
   }
   ```

3. **Проблемы с правами доступа**
   - Убедитесь, что скрипт исполняемый: `chmod +x venv/bin/postgres-mcp`
   - Проверьте права на конфигурационный файл

4. **Проблемы с виртуальным окружением**
   - Активируйте виртуальное окружение: `source venv/bin/activate`
   - Проверьте установку: `pip list | grep postgres-mcp`

5. **Логи Cursor**
   - Проверьте логи Cursor для диагностики ошибок
   - Запустите Cursor из терминала для просмотра ошибок

## Доступные функции MCP Server

- `sql_query` - выполнение SQL запросов
- `list_tables` - список таблиц в базе данных
- `describe_table` - описание структуры таблицы
- `list_schemas` - список схем
- `list_databases` - список баз данных

## Безопасность

- Файл `.env` содержит чувствительные данные и не должен попадать в систему контроля версий
- Добавьте `.env` в `.gitignore`
- Используйте переменные окружения для продакшн окружения

## Устранение неполадок

### Ошибка подключения к базе данных
1. Проверьте, что PostgreSQL сервер запущен
2. Убедитесь в правильности параметров подключения в `.env`
3. Проверьте права доступа пользователя к базе данных

### MCP Server не запускается
1. Активируйте виртуальное окружение: `source venv/bin/activate`
2. Проверьте установку: `pip list | grep postgres-mcp`
3. Проверьте права на исполнение скрипта: `ls -la start-postgres-mcp.sh`

