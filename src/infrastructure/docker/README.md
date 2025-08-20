# Docker образ с PostgreSQL LTS и Java LTS

Этот Docker образ содержит:
- **PostgreSQL 15** (Long Term Support) - стабильная версия СУБД
- **Java 17** (Long Term Support) - Eclipse Temurin JDK

## Быстрый старт

### Использование docker-compose (рекомендуется)

```bash
# Сборка и запуск
cd docker
docker-compose up -d

# Проверка статуса
docker-compose ps

# Просмотр логов
docker-compose logs -f postgres-java
```

### Использование Docker напрямую

```bash
# Сборка образа
cd docker
docker build -t postgres-java-lts .

# Запуск контейнера
docker run -d \
  --name postgres-java-lts \
  -e POSTGRES_DB=postgres \
  -e POSTGRES_USER=postgres \
  -e POSTGRES_PASSWORD=postgres \
  -p 5432:5432 \
  -v postgres_data:/var/lib/postgresql/data \
  postgres-java-lts
```

## Подключение к PostgreSQL

```bash
# Через psql в контейнере
docker exec -it postgres-java-lts psql -U postgres

# Через внешний клиент
psql -h localhost -p 5432 -U postgres -d postgres
```

## Проверка Java

```bash
# Проверка версии Java
docker exec -it postgres-java-lts java -version

# Проверка компилятора
docker exec -it postgres-java-lts javac -version
```

## Переменные окружения

- `POSTGRES_DB` - имя базы данных (по умолчанию: postgres)
- `POSTGRES_USER` - пользователь PostgreSQL (по умолчанию: postgres)
- `POSTGRES_PASSWORD` - пароль PostgreSQL (по умолчанию: postgres)
- `JAVA_HOME` - путь к Java (автоматически устанавливается)

## Порты

- `5432` - PostgreSQL

## Тома

- `postgres_data` - данные PostgreSQL
- `./init-scripts` - скрипты инициализации БД

## Остановка

```bash
# Остановка docker-compose
docker-compose down

# Остановка контейнера
docker stop postgres-java-lts
docker rm postgres-java-lts
```
