# Универсальный контейнер PostgreSQL 16 + Java 21 LTS

## Описание
Универсальный Docker контейнер, содержащий PostgreSQL 16 и Java 21 LTS (Eclipse Temurin) в одном образе.

## Компоненты

### PostgreSQL 16
- Версия: PostgreSQL 16.9
- Порт: 5432
- Пользователь: testuser
- База данных: testdb
- Пароль: testpass

### Java 21 LTS
- Версия: Eclipse Temurin 21
- JAVA_HOME: /usr/lib/jvm/temurin-21-jdk-amd64
- Тип: OpenJDK

## Установка и настройка

### 1. Сборка образа
```bash
./manage-universal-container.sh build
```

### 2. Запуск контейнера
```bash
./manage-universal-container.sh start
```

### 3. Настройка базы данных
```bash
./manage-universal-container.sh setup-db
```

### 4. Проверка работы
```bash
# Проверка Java
./manage-universal-container.sh java

# Проверка PostgreSQL
./manage-universal-container.sh postgres

# Статус контейнера
./manage-universal-container.sh status
```

## Управление контейнером

### Доступные команды:
- `build` - Собрать образ
- `start` - Запустить контейнер
- `stop` - Остановить контейнер
- `restart` - Перезапустить контейнер
- `status` - Показать статус
- `logs` - Показать логи
- `exec` - Подключиться к контейнеру
- `java` - Проверить Java
- `postgres` - Проверить PostgreSQL
- `setup-db` - Настроить базу данных
- `cleanup` - Очистить контейнер и образ

### Примеры использования:

```bash
# Полная настройка с нуля
./manage-universal-container.sh build
./manage-universal-container.sh start
./manage-universal-container.sh setup-db

# Проверка работы
./manage-universal-container.sh java
./manage-universal-container.sh postgres

# Подключение к контейнеру
./manage-universal-container.sh exec

# Очистка
./manage-universal-container.sh cleanup
```

## Подключение к PostgreSQL

### Параметры подключения:
- **Хост**: localhost
- **Порт**: 5432
- **База данных**: testdb
- **Пользователь**: testuser
- **Пароль**: testpass

### Строка подключения:
```
postgresql://testuser:testpass@localhost:5432/testdb
```

## Использование Java

### Переменные окружения:
- `JAVA_HOME=/usr/lib/jvm/temurin-21-jdk-amd64`
- `PATH` включает Java bin директорию

### Проверка Java:
```bash
docker exec postgres-java-universal java -version
docker exec postgres-java-universal javac -version
```

## Интеграция с MCP Server

После запуска универсального контейнера, MCP Server автоматически подключится к PostgreSQL:

1. Убедитесь, что контейнер запущен
2. Проверьте статус в Cursor MCP Tools
3. Зеленая точка означает успешное подключение

## Преимущества универсального контейнера

1. **Один контейнер** - PostgreSQL и Java в одном месте
2. **Простота управления** - единый скрипт для всех операций
3. **Изоляция** - все компоненты изолированы от хост-системы
4. **Портативность** - легко переносить между системами
5. **Версионирование** - четкие версии PostgreSQL и Java

## Устранение неполадок

### Контейнер не запускается:
```bash
./manage-universal-container.sh logs
```

### PostgreSQL недоступен:
```bash
./manage-universal-container.sh postgres
./manage-universal-container.sh setup-db
```

### Java не работает:
```bash
./manage-universal-container.sh java
```

### Очистка и пересборка:
```bash
./manage-universal-container.sh cleanup
./manage-universal-container.sh build
./manage-universal-container.sh start
```

