# Vuege - Система учета организационных единиц и исторических данных

## Описание проекта

Vuege - это CRUD веб-сервис для учета организационных единиц, включающий государства, государственные и коммерческие организации, должности и людей, занимавших эти должности. Система обеспечивает учет в исторической перспективе с привязкой к географической позиции через ГИС-функциональность.

### Ключевые особенности
- **Исторический охват**: от 4000 лет до нашей эры до настоящего времени
- **ГИС-интеграция**: географическая привязка всех объектов
- **Жизненный цикл**: отслеживание создания, трансформаций и ликвидации
- **Типы объектов**: фактически существовавшие, планируемые и вымышленные
- **Реактивная архитектура**: полностью реактивный стек от БД до UI

## Архитектура системы

### Общая архитектура
```
┌─────────────────────────────────────────────────────────────┐
│                    Vuege Application                        │
│                     (Quasar Framework)                      │
├─────────────────────────────────────────────────────────────┤
│  Frontend (Vue.js + Quasar + TanStack Router + Apollo)     │
│  ├── Web (SPA/PWA/SSR)                                     │
│  ├── Mobile (iOS/Android via Capacitor)                    │
│  └── Desktop (Windows/macOS/Linux via Electron)            │
├─────────────────────────────────────────────────────────────┤
│  Backend (Spring Boot + GraphQL + R2DBC)                   │
│  Database (PostgreSQL 16 + PostGIS)                        │
└─────────────────────────────────────────────────────────────┘
```

### Технологический стек

#### Backend
- **Spring Boot**: 3.4.5
- **Java**: 21 LTS (Eclipse Temurin)
- **GraphQL**: Spring GraphQL
- **Database Access**: R2DBC (реактивный)
- **Database**: PostgreSQL 16 + PostGIS
- **Migrations**: Liquibase
- **Server**: Tomcat (вместо Netty)

#### Frontend
- **Framework**: Vue.js 3.4.21
- **UI Library**: Quasar 2.16.1 (поддержка Web/Mobile/Desktop)
- **Router**: TanStack Router 1.16.0
- **GraphQL Client**: Apollo Client 3.13.5
- **Language**: TypeScript 5.4.0
- **Build Tool**: Vite
- **Deployment**: SPA (разработка), PWA/SSR (Web), Capacitor (Mobile), Electron (Desktop)

#### Infrastructure
- **Container**: postgres-java-universal (PostgreSQL 16 + Java 21)
- **Deployment**: Единый JAR-артефакт
- **Node.js**: v20.12.0 LTS
- **Package Manager**: npm 10.8.0

## Доменная модель

### Основные сущности

#### OrganizationalUnit (Организационная единица)
```typescript
interface OrganizationalUnit {
    id: string;
    name: string;
    type: 'STATE' | 'GOVERNMENT' | 'COMMERCIAL';
    foundedDate: Date; // PostgreSQL DATE
    dissolvedDate?: Date;
    location: GeoPoint;
    isFictional: boolean;
    historicalPeriod: HistoricalPeriod;
    parentUnit?: string; // ID родительской единицы
    childUnits: string[]; // ID дочерних единиц
    transformations: Transformation[];
}
```

#### Position (Должность)
```typescript
interface Position {
    id: string;
    title: string;
    organizationId: string;
    createdDate: Date;
    abolishedDate?: Date;
    hierarchy: PositionHierarchy;
    responsibilities: string[];
    isActive: boolean;
}
```

#### Person (Человек)
```typescript
interface Person {
    id: string;
    name: string;
    birthDate?: Date;
    deathDate?: Date;
    nationality: string;
    positions: PersonPosition[];
    isFictional: boolean;
    historicalPeriod: HistoricalPeriod;
}
```

#### PersonPosition (Связь человек-должность)
```typescript
interface PersonPosition {
    id: string;
    personId: string;
    positionId: string;
    startDate: Date;
    endDate?: Date;
    appointmentType: 'ELECTED' | 'APPOINTED' | 'INHERITED';
    source: string; // источник исторических данных
}
```

#### HistoricalPeriod (Исторический период)
```typescript
interface HistoricalPeriod {
    id: string;
    name: string;
    startDate: Date; // может быть -4000
    endDate?: Date;
    era: 'BCE' | 'CE';
    description: string;
}
```

#### GeoPoint (Географическая точка)
```typescript
interface GeoPoint {
    id: string;
    latitude: number;
    longitude: number;
    coordinates: [number, number]; // GeoJSON
    elevation?: number;
    accuracy: 'EXACT' | 'APPROXIMATE' | 'UNKNOWN';
}
```

### ГИС-функциональность

#### PostGIS интеграция
```sql
-- Расширение PostGIS
CREATE EXTENSION postgis;

-- Таблица с геопространственными данными
CREATE TABLE organizational_units (
    id SERIAL PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    type VARCHAR(50) NOT NULL,
    founded_date DATE NOT NULL,
    dissolved_date DATE,
    location GEOMETRY(POINT, 4326), -- WGS84
    is_fictional BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Пространственный индекс
CREATE INDEX idx_org_units_location ON organizational_units USING GIST (location);
```

## API архитектура

### GraphQL схема

#### Основные типы
```graphql
type OrganizationalUnit {
    id: ID!
    name: String!
    type: OrganizationType!
    foundedDate: Date!
    dissolvedDate: Date
    location: GeoPoint
    isFictional: Boolean!
    historicalPeriod: HistoricalPeriod!
    parentUnit: OrganizationalUnit
    childUnits: [OrganizationalUnit!]!
    positions: [Position!]!
}

type Position {
    id: ID!
    title: String!
    organization: OrganizationalUnit!
    createdDate: Date!
    abolishedDate: Date
    hierarchy: PositionHierarchy!
    responsibilities: [String!]!
    isActive: Boolean!
    holders: [PersonPosition!]!
}

type Person {
    id: ID!
    name: String!
    birthDate: Date
    deathDate: Date
    nationality: String!
    positions: [PersonPosition!]!
    isFictional: Boolean!
    historicalPeriod: HistoricalPeriod!
}

type GeoPoint {
    id: ID!
    latitude: Float!
    longitude: Float!
    coordinates: [Float!]!
    elevation: Float
    accuracy: AccuracyType!
}

enum OrganizationType {
    STATE
    GOVERNMENT
    COMMERCIAL
}

enum AccuracyType {
    EXACT
    APPROXIMATE
    UNKNOWN
}
```

#### Основные запросы
```graphql
# Получение организаций в регионе
query GetOrganizationsInRegion($bounds: BoundingBox!, $timeRange: TimeRange!) {
    organizationsInRegion(bounds: $bounds, timeRange: $timeRange) {
        id
        name
        type
        foundedDate
        location
        isFictional
    }
}

# Получение должностей в организации
query GetPositionsInOrganization($orgId: ID!, $timeRange: TimeRange!) {
    positionsInOrganization(orgId: $orgId, timeRange: $timeRange) {
        id
        title
        createdDate
        abolishedDate
        holders {
            person {
                name
                nationality
            }
            startDate
            endDate
        }
    }
}

# Поиск людей по критериям
query SearchPeople($criteria: PersonSearchCriteria!) {
    searchPeople(criteria: $criteria) {
        id
        name
        birthDate
        deathDate
        nationality
        positions {
            position {
                title
                organization {
                    name
                    type
                }
            }
            startDate
            endDate
        }
    }
}
```

## Структура проекта

### Backend структура
```
src/main/java/my/fe/vuege/
├── VuegeApplication.java
├── controller/
│   ├── GraphQLController.java
│   └── HealthController.java
├── model/
│   ├── OrganizationalUnit.java
│   ├── Position.java
│   ├── Person.java
│   ├── PersonPosition.java
│   ├── HistoricalPeriod.java
│   └── GeoPoint.java
├── repository/
│   ├── OrganizationalUnitRepository.java
│   ├── PositionRepository.java
│   ├── PersonRepository.java
│   └── PersonPositionRepository.java
├── service/
│   ├── OrganizationalUnitService.java
│   ├── PositionService.java
│   ├── PersonService.java
│   └── GISService.java
├── graphql/
│   ├── resolver/
│   │   ├── OrganizationalUnitResolver.java
│   │   ├── PositionResolver.java
│   │   └── PersonResolver.java
│   └── scalar/
│       ├── DateScalar.java
│       └── GeoPointScalar.java
└── exception/
    ├── VuegeException.java
    └── GlobalExceptionHandler.java
```

### Frontend структура
```
src/frontend-q/
├── src/
│   ├── App.vue
│   ├── main.ts
│   ├── router/
│   │   ├── index.ts
│   │   └── routes.ts
│   ├── pages/
│   │   ├── HomePage.vue
│   │   ├── OrganizationsPage.vue
│   │   ├── PositionsPage.vue
│   │   ├── PeoplePage.vue
│   │   └── GISPage.vue
│   ├── components/
│   │   ├── OrganizationCard.vue
│   │   ├── PositionList.vue
│   │   ├── PersonProfile.vue
│   │   └── GISMap.vue
│   ├── stores/
│   │   ├── organizations.ts
│   │   ├── positions.ts
│   │   └── people.ts
│   ├── types/
│   │   ├── organizational-unit.ts
│   │   ├── position.ts
│   │   ├── person.ts
│   │   └── geo-point.ts
│   ├── queries/
│   │   ├── organizations.ts
│   │   ├── positions.ts
│   │   └── people.ts
│   └── utils/
│       ├── date-utils.ts
│       ├── geo-utils.ts
│       └── validation.ts
├── public/
├── package.json
├── tsconfig.json
├── quasar.config.js
└── vite.config.ts
```

### База данных
```
db/changelog/
├── db.changelog-master.yaml
├── 001-initial-schema.yaml
├── 002-organizational-units.yaml
├── 003-positions.yaml
├── 004-people.yaml
├── 005-person-positions.yaml
├── 006-historical-periods.yaml
├── 007-gis-data.yaml
└── 008-indexes.yaml
```

## Развертывание

### Контейнерная архитектура
```yaml
# docker-compose.yml
version: '3.8'

services:
  vuege:
    build:
      context: .
      dockerfile: docker/Dockerfile.vuege
    container_name: vuege-app
    ports:
      - "8080:8080"
    environment:
      - SPRING_PROFILES_ACTIVE=prod
      - SPRING_R2DBC_URL=r2dbc:postgresql://postgres:5432/vuege_prod
      - SPRING_R2DBC_USERNAME=testuser
      - SPRING_R2DBC_PASSWORD=testpass
    depends_on:
      - postgres-java-universal
    volumes:
      - vuege_data:/app/data

  postgres-java-universal:
    build:
      context: .
      dockerfile: docker/Dockerfile.postgres-java
    container_name: postgres-java-universal
    ports:
      - "5432:5432"
    environment:
      - POSTGRES_DB=vuege_prod
      - POSTGRES_USER=testuser
      - POSTGRES_PASSWORD=testpass
    volumes:
      - postgres_data:/var/lib/postgresql/16/main
    restart: unless-stopped

volumes:
  vuege_data:
  postgres_data:
```

### Сборка и развертывание

#### Frontend разработка (SPA)
```bash
# Разработка в режиме SPA
quasar dev

# Сборка SPA для продакшена
quasar build

# Тестирование PWA возможностей
quasar dev --mode pwa

# Сборка PWA для продакшена
quasar build --mode pwa
```

#### Backend
```bash
# Сборка проекта
mvn clean package

# Сборка Docker образа
docker build -f docker/Dockerfile.vuege -t vuege:latest .

# Запуск с docker-compose
docker-compose up -d

# Проверка статуса
docker-compose ps
```

## Этапы разработки

### Этап 1: Базовая инфраструктура (Недели 1-2)
- [ ] Настройка Spring Boot проекта
- [ ] Настройка Vue.js + Quasar + TypeScript
- [ ] Интеграция TanStack Router
- [ ] Настройка GraphQL
- [ ] Настройка Liquibase

### Этап 2: Доменная модель (Недели 3-4)
- [ ] Создание сущностей БД
- [ ] Реализация репозиториев
- [ ] Создание GraphQL схемы
- [ ] Реализация резолверов

### Этап 3: Frontend (Недели 5-6)
- [ ] Настройка Quasar SPA режима разработки
- [ ] Создание основных страниц
- [ ] Интеграция с GraphQL
- [ ] Реализация CRUD операций
- [ ] Базовая валидация
- [ ] Настройка конфигурации для переключения между режимами

### Этап 4: ГИС-функциональность (Недели 7-8)
- [ ] Интеграция PostGIS
- [ ] Реализация карт
- [ ] Пространственные запросы
- [ ] Геокодирование

### Этап 5: Исторические данные (Недели 9-10)
- [ ] Работа с историческими датами
- [ ] Временные шкалы
- [ ] Исторические фильтры
- [ ] Валидация исторических данных

### Этап 6: Тестирование и оптимизация (Недели 11-12)
- [ ] Unit тесты
- [ ] Integration тесты
- [ ] E2E тесты
- [ ] Производительность
- [ ] Безопасность

## Стратегия развертывания

### Режим разработки по умолчанию: SPA
Для обеспечения максимальной скорости разработки и простоты отладки выбран **SPA (Single Page Application)** как основной режим разработки.

**Обоснование выбора:**
- ✅ **Быстрая разработка** - мгновенная перезагрузка при изменениях
- ✅ **Простая отладка** - Vue DevTools работают идеально
- ✅ **ГИС-функциональность** - карты и интерактивные элементы лучше работают в SPA
- ✅ **Исторические данные** - сложная навигация по временным шкалам удобнее в SPA
- ✅ **GraphQL интеграция** - Apollo Client лучше интегрируется с SPA

### Стратегия развертывания по этапам:
```
Разработка: SPA (быстро, просто, гибко)
    ↓
Тестирование: SPA + PWA (добавляем офлайн возможности)
    ↓
Продакшен: Выбор в зависимости от требований
    - Web: SPA или PWA
    - Mobile: Capacitor
    - Desktop: Electron
```

### Конфигурация Quasar для разработки
```javascript
// quasar.config.js
module.exports = function (ctx) {
  return {
    // Режим разработки - SPA
    build: {
      distDir: 'dist/spa',
      publicPath: '/'
    },
    
    // Легкое переключение на PWA для тестирования
    pwa: {
      workboxPluginMode: 'GenerateSW',
      workboxOptions: {
        skipWaiting: true,
        clientsClaim: true
      }
    }
  }
}
```

## Стандарты и принципы

### Принципы разработки
- **SOLID** - следование принципам SOLID
- **DRY** - не повторяем код
- **KISS** - простота решений
- **Reactive** - реактивная архитектура
- **Type Safety** - строгая типизация

### Стандарты кодирования
- **TypeScript** - строгий режим
- **ESLint** - линтинг кода
- **Prettier** - форматирование
- **Pre-commit hooks** - проверка перед коммитом

### Документирование
- **JSDoc** - документация функций
- **GraphQL Schema** - документация API
- **README** - документация проекта
- **Changelog** - история изменений

## Мониторинг и логирование

### Логирование
- **Backend**: SLF4J + Logback
- **Frontend**: Vue DevTools + Console
- **Database**: PostgreSQL logs

### Мониторинг
- **Health checks**: Spring Boot Actuator
- **Metrics**: Micrometer + Prometheus
- **Tracing**: OpenTelemetry

## Безопасность

### Аутентификация и авторизация
- **JWT** - токены аутентификации
- **OAuth2** - интеграция с внешними провайдерами
- **RBAC** - ролевая модель доступа

### Защита данных
- **HTTPS** - шифрование трафика
- **SQL Injection** - защита через R2DBC
- **XSS** - защита через Vue.js
- **CSRF** - защита от CSRF атак

## Производительность

### Оптимизации
- **Database**: индексы, партиционирование
- **GraphQL**: DataLoader, кэширование
- **Frontend**: lazy loading, code splitting
- **Caching**: Redis для кэширования

### Масштабирование
- **Horizontal scaling** - горизонтальное масштабирование
- **Load balancing** - балансировка нагрузки
- **Database sharding** - шардинг БД
- **CDN** - доставка статики

## Заключение

Vuege представляет собой современную, масштабируемую систему для учета организационных единиц с богатой исторической перспективой. Использование реактивного стека, TypeScript и современных технологий обеспечивает высокую производительность, безопасность и удобство разработки.

Проект готов к реализации и может быть адаптирован под различные требования и масштабы использования.
