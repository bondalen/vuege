# Vuege

CRUD веб-сервис для учета организационных единиц с исторической перспективой и ГИС-функциональностью.

## Описание

Vuege - это современное веб-приложение, разработанное с использованием Spring Boot и Vue.js для учета организационных единиц, включающий государства, государственные и коммерческие организации, должности и людей, занимавших эти должности. Система обеспечивает учет в исторической перспективе с привязкой к географической позиции через ГИС-функциональность.

### Ключевые особенности
- **Исторический охват**: от 4000 лет до нашей эры до настоящего времени
- **ГИС-интеграция**: географическая привязка через PostGIS
- **Реактивная архитектура**: Spring Boot + Vue.js + GraphQL
- **Многоплатформенность**: Web/Desktop/Mobile через Quasar Framework
- **Отчётность**: генерация отчётов в множественных форматах (PDF, HTML, JSON, Excel, CSV, XML) с возможностью скачивания и отправки по email

## Технологии

### Backend
- **Spring Boot 3.4.5** - основной фреймворк
- **Java 21 LTS** - язык программирования
- **GraphQL** - API интерфейс
- **R2DBC** - реактивный доступ к базе данных
- **PostgreSQL 16 + PostGIS** - база данных с ГИС-функциональностью
- **Liquibase** - управление миграциями БД
- **Lombok** - минимизация boilerplate кода
- **Spring Boot Actuator** - мониторинг и метрики

### Frontend (в разработке)
- **Vue.js 3.4.21** - основной фреймворк
- **Quasar 2.16.1** - UI библиотека
- **TypeScript 5.4.0** - язык программирования
- **TanStack Router 1.16.0** - роутинг
- **Apollo Client 3.13.5** - GraphQL клиент

### Infrastructure
- **Docker** - контейнеризация
- **Maven** - управление зависимостями Java
- **npm** - управление зависимостями JavaScript

## Структура проекта

```
vuege/
├── src/
│   ├── backend/                    # Spring Boot приложение
│   │   ├── src/main/java/
│   │   │   └── io/github/bondalen/
│   │   │       ├── VuegeApplication.java
│   │   │       ├── domain/         # Доменная модель
│   │   │       ├── repository/     # Репозитории
│   │   │       ├── service/        # Сервисы
│   │   │       ├── controller/     # Контроллеры
│   │   │       └── config/         # Конфигурация
│   │   ├── src/main/resources/
│   │   │   ├── application.yml     # Конфигурация
│   │   │   ├── graphql/            # GraphQL схемы
│   │   │   └── db/changelog/       # Liquibase миграции
│   │   └── pom.xml                 # Maven конфигурация
│   ├── frontend/                   # Vue.js приложение (в разработке)
│   └── infrastructure/             # Инфраструктурные скрипты
├── docs/                           # Документация проекта
│   ├── main/                       # Основная документация
│   ├── others/                     # Вспомогательная документация
│   └── schemes/                    # Диаграммы и схемы
└── README.md                       # Этот файл
```

## Быстрый старт

### Предварительные требования

1. **Java 21 LTS** (Eclipse Temurin)
2. **Maven 3.8+**
3. **Docker** с контейнером `postgres-java-universal`
4. **Node.js 20.12.0 LTS** (для frontend)

### Запуск Backend

1. **Проверка контейнера PostgreSQL:**
   ```bash
   docker ps | grep postgres-java-universal
   ```

2. **Компиляция и запуск:**
   ```bash
   cd src/backend
   mvn clean compile
   mvn spring-boot:run
   ```

3. **Проверка работы:**
   - GraphQL Playground: http://localhost:8080/api/graphiql
   - Health Check: http://localhost:8080/api/actuator/health

### Запуск Frontend (в разработке)

```bash
cd src/frontend
npm install
npm run dev
```

## API Endpoints

### GraphQL
- **GraphQL Playground**: `/api/graphiql`
- **GraphQL Endpoint**: `/api/graphql`

### REST API
- **Health Check**: `/api/actuator/health`
- **Info**: `/api/actuator/info`
- **Metrics**: `/api/actuator/metrics`
- **Environment**: `/api/actuator/env`
- **Configuration Properties**: `/api/actuator/configprops`
- **Beans**: `/api/actuator/beans`
- **Thread Dump**: `/api/actuator/threaddump`
- **Heap Dump**: `/api/actuator/heapdump`

## Мониторинг

### Spring Boot Actuator
Приложение включает полноценную систему мониторинга через Spring Boot Actuator:

- **Health Checks**: Автоматическая проверка состояния компонентов
- **Метрики**: Сбор производительности JVM, HTTP, базы данных
- **Диагностика**: Информация о конфигурации и состоянии приложения
- **Prometheus**: Экспорт метрик для внешних систем мониторинга

### Health Checks
- **R2DBC**: Подключение к PostgreSQL
- **Disk Space**: Доступное место на диске
- **SSL**: Состояние сертификатов
- **Ping**: Доступность приложения

Подробная документация: [docs/monitoring/actuator-guide.md](docs/monitoring/actuator-guide.md)

## База данных

### Схемы
- **vuege** - основные таблицы
- **gis** - ГИС данные
- **history** - исторические данные

### Миграции
Миграции управляются через Liquibase в папке `src/backend/src/main/resources/db/changelog/`.

### PostGIS
Расширение PostGIS установлено для поддержки геопространственных данных.

## Разработка

### Backend разработка

Подробная информация в [src/backend/README.md](src/backend/README.md)

### Frontend разработка

Подробная информация будет добавлена по мере развития проекта.

## Документация

- **[Основная документация](docs/main/)** - полное руководство по проекту
- **[Дневник разработки](docs/main/diary.md)** - хронология разработки
- **[Журнал изменений](docs/main/changelog.md)** - история изменений
- **[Трекер задач](docs/main/tasktracker.md)** - управление задачами
- **[Проблемы](docs/main/problems.md)** - долгосрочные проблемы

## Лицензия

MIT
# Тест SSH-агента
