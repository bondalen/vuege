# Vuege - Система учета организационных единиц и исторических данных

**Псевдонимы**: файл основной ПД, основной файл ПД, файл ПД

## Информация о проекте

**Дата начала работы над проектом**: 2025-08-11

## Описание проекта

Vuege - это CRUD веб-сервис для учета организационных единиц, включающий государства, государственные и коммерческие организации, должности и людей, занимавших эти должности. Система обеспечивает учет в исторической перспективе с привязкой к географической позиции через ГИС-функциональность.

### Ключевые особенности
- **Исторический охват**: от 4000 лет до нашей эры до настоящего времени
- **ГИС-интеграция**: географическая привязка всех объектов
- **Жизненный цикл**: отслеживание создания, трансформаций и ликвидации
- **Типы объектов**: фактически существовавшие, планируемые и вымышленные
- **Реактивная архитектура**: полностью реактивный стек от БД до UI
- **Отчётность**: генерация отчётов в множественных форматах (PDF, HTML, JSON, Excel, CSV, XML) с возможностью скачивания и отправки по email

## Архитектура системы

### Общая архитектура
```
┌─────────────────────────────────────────────────────────────┐
│                    Vuege Application                        │
│                     (Quasar Framework)                      │
├─────────────────────────────────────────────────────────────┤
│  frontend/ (Vue.js + Quasar + TanStack Router + Apollo)    │
│  ├── Web (SPA/PWA/SSR)                                     │
│  ├── Mobile (iOS/Android via Capacitor)                    │
│  └── Desktop (Windows/macOS/Linux via Electron)            │
├─────────────────────────────────────────────────────────────┤
│  backend/ (Spring Boot + GraphQL + R2DBC)                  │
│  Database (PostgreSQL 16 + PostGIS)                        │
└─────────────────────────────────────────────────────────────┘
```

### Подробные диаграммы архитектуры

Подробные диаграммы архитектуры и процессов доступны в:
- **[BPMN диаграммы](docs/schemes/bpmn/)** - бизнес-процессы и workflow
- **[UML диаграммы](docs/schemes/uml/)** - архитектура и доменная модель

#### Основные диаграммы:
- **[Доменная модель](docs/schemes/uml/class-diagrams/domain-model.puml)** - основные сущности и их связи
- **[Архитектура системы](docs/schemes/uml/component-diagrams/system-architecture.puml)** - компоненты и их взаимодействие
- **[Процесс генерации отчётов](docs/schemes/uml/sequence-diagrams/report-generation.puml)** - последовательность операций
- **[Процесс импорта данных](docs/schemes/bpmn/data-import.puml)** - workflow импорта данных

#### Инструменты для диаграмм:
- **PlantUML** - для UML диаграмм (классы, последовательности, компоненты)
- **BPMN Sketch Miner** - для BPMN диаграмм (бизнес-процессы)

### Правила работы с диаграммами

#### Гибридный подход к диаграммам
Проект использует специализированные инструменты для разных типов диаграмм:

**PlantUML** - для UML диаграмм:
- Диаграммы классов (доменная модель, архитектура)
- Диаграммы последовательности (процессы взаимодействия)
- Диаграммы компонентов (системная архитектура)
- Диаграммы состояний (жизненные циклы)

**BPMN Sketch Miner** - для BPMN диаграмм:
- Бизнес-процессы (импорт данных, генерация отчётов)
- Workflow (валидация, обработка ошибок)
- Алгоритмы (поиск, анализ данных)

#### Структура размещения диаграмм
```
docs/schemes/
├── bpmn/                    # BPMN диаграммы
│   ├── data-import.puml     # Процесс импорта данных
│   ├── report-generation.puml # Workflow генерации отчётов
│   └── data-validation.puml  # Процесс валидации
├── uml/                     # UML диаграммы
│   ├── class-diagrams/      # Диаграммы классов
│   ├── sequence-diagrams/   # Диаграммы последовательности
│   └── component-diagrams/  # Диаграммы компонентов
└── README.md               # Общая документация
```

#### Процесс создания и обновления диаграмм

**При создании новой диаграммы:**
1. Определить тип диаграммы (UML или BPMN)
2. Выбрать подходящий инструмент
3. Создать файл в соответствующей папке
4. Использовать установленные шаблоны и стили
5. Добавить запись в changelog.md
6. Обновить ссылки в project.md

**При изменении архитектуры:**
1. Обновить соответствующие диаграммы классов
2. Обновить диаграммы компонентов
3. Обновить диаграммы последовательности (если необходимо)
4. Обновить BPMN диаграммы процессов
5. Синхронизировать документацию

**При добавлении новых компонентов:**
1. Создать или обновить диаграмму компонентов
2. Обновить диаграммы последовательности
3. Добавить новые процессы в BPMN диаграммы
4. Обновить документацию

#### Стандарты оформления диаграмм

**Цветовая схема:**
- Классы: #E3F2FD (светло-синий)
- Перечисления: #F3E5F5 (светло-фиолетовый)
- Компоненты: #E8F5E8 (светло-зеленый)
- Интерфейсы: #FFF3E0 (светло-оранжевый)
- Базы данных: #F3E5F5 (светло-фиолетовый)

**Общие принципы:**
- Тема: plain (минималистичная)
- Фон: белый (#FFFFFF)
- Шрифт: 12pt для читаемости
- Именование файлов: kebab-case формат

#### Интеграция с процессом разработки

**Обязательные действия:**
- При изменении доменной модели - обновить диаграммы классов
- При изменении архитектуры - обновить диаграммы компонентов
- При изменении процессов - обновить BPMN диаграммы
- При создании новых диаграмм - добавить в changelog.md
- Регулярно проверять актуальность диаграмм

**Связи с документацией:**
- Все диаграммы должны быть связаны с соответствующими разделами project.md
- Изменения в диаграммах должны отражаться в changelog.md
- Документация диаграмм должна быть актуальной

### Технологический стек

#### Backend
- **Spring Boot**: 3.4.5
- **Java**: 21 LTS (Eclipse Temurin)
- **Maven Artifact**: `io.github.bondalen:vuege:0.1.0`
- **Lombok**: 1.18.34 (минимизация boilerplate кода)
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

#### MCP Servers (Model Context Protocol)
- **postgres-mcp**: интеграция с PostgreSQL базой данных
- **git-mcp**: операции с Git репозиторием
- **docker-mcp**: управление Docker контейнерами
- **terminal-mcp**: выполнение терминальных команд

**Полезные ресурсы:**
- **[Cursor Directory MCP](https://cursor.directory/mcp)** - официальная директория MCP серверов для Cursor IDE с поиском (приоритетный источник)
- **[Awesome MCP Servers](https://github.com/punkpeye/awesome-mcp-servers)** - коллекция из 200+ MCP серверов с категоризацией и описаниями (дополнительный источник)
- **[MCP Documentation](https://modelcontextprotocol.io/)** - официальная документация протокола

**Правила установки MCP серверов:**
1. **Приоритет Python пакетам** - устанавливать в виртуальное окружение Python (`venv/`)
2. **npm пакеты через обертки** - использовать Python обертки для npm пакетов
3. **Единообразная структура конфигурации** в `~/.cursor/mcp.json`
4. **Обертки для проблемных серверов** размещаются в `src/infrastructure/scripts/`
5. **Документирование каждого сервера** в `docs/others/`

**Структура конфигурации:**
```json
{
  "mcpServers": {
    "server-name": {
      "command": "/home/alex/vuege/venv/bin/python",
      "args": ["/home/alex/vuege/src/infrastructure/scripts/wrapper.py"],
      "env": {},
      "description": "Описание сервера"
    }
  }
}
```

#### Report Generation & Export
- **PDF Generation**: Apache PDFBox 2.0.30 + Flying Saucer 9.1.22 (HTML в PDF)
- **Excel Generation**: Apache POI 5.2.3 (Excel файлы)
- **CSV Generation**: OpenCSV 5.7.1 (CSV экспорт)
- **JSON/XML Generation**: Jackson 2.15.0 (структурированные данные)
- **HTML Generation**: Thymeleaf 3.1.2 (HTML шаблоны)
- **Email Service**: Spring Boot Mail + JavaMail API
- **File Storage**: Spring Boot File Storage (локальное хранение)
- **Async Processing**: Spring Boot Async + CompletableFuture

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

## Отчётность и экспорт данных

### Обзор функциональности
Система предоставляет возможность генерации отчётов и экспорта данных в различных форматах по различным аспектам данных vuege с возможностью:
- **Скачивания** - прямой загрузки файлов через браузер
- **Email-отправки** - автоматической отправки отчёта на указанный email
- **Асинхронной обработки** - генерация отчётов в фоновом режиме
- **Шаблонизации** - использование HTML-шаблонов для оформления
- **Множественных форматов** - поддержка PDF, HTML, JSON, Excel, CSV, XML

### Поддерживаемые форматы экспорта

#### 1. PDF (Portable Document Format)
- **Назначение**: Печатные формы, официальные документы
- **Технология**: Apache PDFBox 2.0.30 + Flying Saucer 9.1.22
- **Особенности**: Фиксированное форматирование, поддержка кириллицы, векторная графика

#### 2. HTML (HyperText Markup Language)
- **Назначение**: Просмотр в браузере, веб-публикация
- **Технология**: Thymeleaf 3.1.2 + CSS
- **Особенности**: Интерактивность, адаптивный дизайн, возможность дальнейшего редактирования

#### 3. JSON (JavaScript Object Notation)
- **Назначение**: Программная обработка, API интеграции
- **Технология**: Jackson 2.15.0
- **Особенности**: Структурированные данные, легкая парсинг, поддержка метаданных

#### 4. Excel (Microsoft Excel)
- **Назначение**: Аналитика, работа с табличными данными
- **Технология**: Apache POI 5.2.3
- **Особенности**: Множественные листы, формулы, форматирование, графики

#### 5. CSV (Comma-Separated Values)
- **Назначение**: Простой экспорт таблиц, совместимость с аналитическими инструментами
- **Технология**: OpenCSV 5.7.1
- **Особенности**: Универсальная совместимость, легкий вес, поддержка Unicode

#### 6. XML (eXtensible Markup Language)
- **Назначение**: Интеграция с внешними системами, структурированные данные
- **Технология**: Jackson XML 2.15.0
- **Особенности**: Строгая структура, валидация схем, поддержка пространств имен

### Типы отчётов

#### 1. Отчёт по организационной единице
```typescript
interface OrganizationReport {
    organization: OrganizationalUnit;
    positions: Position[];
    currentHolders: PersonPosition[];
    historicalHolders: PersonPosition[];
    childOrganizations: OrganizationalUnit[];
    transformations: Transformation[];
    location: GeoPoint;
    period: HistoricalPeriod;
}
```

#### 2. Отчёт по историческому периоду
```typescript
interface HistoricalPeriodReport {
    period: HistoricalPeriod;
    organizations: OrganizationalUnit[];
    keyPositions: Position[];
    notablePeople: Person[];
    geographicalDistribution: GeoPoint[];
    timeline: Transformation[];
}
```

#### 3. Отчёт по географическому региону
```typescript
interface GeographicReport {
    region: BoundingBox;
    organizations: OrganizationalUnit[];
    positions: Position[];
    people: Person[];
    historicalEvents: Transformation[];
    period: TimeRange;
}
```

#### 4. Отчёт по человеку
```typescript
interface PersonReport {
    person: Person;
    positions: PersonPosition[];
    organizations: OrganizationalUnit[];
    timeline: PersonPosition[];
    historicalContext: HistoricalPeriod;
}
```

### API для отчётности

Система предоставляет GraphQL мутации для генерации и отправки отчётов, а также REST API для скачивания готовых файлов.

**Основные операции:**
- `generateReport` - генерация отчёта с возможностью скачивания
- `sendReportByEmail` - отправка отчёта по email
- `getReportStatus` - получение статуса генерации отчёта
- REST API для скачивания готовых файлов

**Поддерживаемые типы отчётов:** ORGANIZATION, HISTORICAL_PERIOD, GEOGRAPHIC, PERSON, CUSTOM

**Форматы:** PDF, HTML, JSON, EXCEL, CSV, XML

> **См. Приложение A** - Полная GraphQL схема для отчётности

### Техническая реализация

#### Архитектура
Система построена на многоуровневой архитектуре с асинхронной обработкой:

- **Frontend**: Vue.js + Quasar компоненты для генерации отчётов
- **Backend**: Spring Boot сервисы для бизнес-логики и генерации отчётов
- **Storage**: Локальное хранение файлов и база данных для статусов
- **External**: SMTP сервер для отправки email

#### Основные компоненты
- **ReportController** - REST API для управления отчётами
- **ReportService** - основная бизнес-логика генерации отчётов
- **ReportGeneratorService** - универсальная генерация отчётов в различных форматах
- **EmailService** - отправка отчётов по email
- **AsyncReportProcessor** - асинхронная обработка в фоновом режиме

> **См. Приложение B** - Детальная реализация компонентов системы

#### Генераторы форматов

Система использует специализированные генераторы для каждого формата:

- **PDFGenerator** - конвертация HTML в PDF через Flying Saucer
- **HTMLGenerator** - генерация HTML через Thymeleaf шаблоны
- **JSONGenerator** - сериализация данных в JSON через Jackson
- **ExcelGenerator** - создание Excel файлов через Apache POI
- **CSVGenerator** - экспорт табличных данных через OpenCSV
- **XMLGenerator** - генерация XML через Jackson XML

> **См. Приложение C** - HTML-шаблоны для различных типов отчётов

### Конфигурация

Система настраивается через `application.yml` с параметрами для:

- **Report Generation**: пути к временным файлам, размеры, интервалы очистки
- **Email**: SMTP настройки для отправки отчётов
- **Async Processing**: пул потоков для асинхронной обработки
- **Format Settings**: специфичные настройки для каждого формата

**Основные зависимости:**
- Apache PDFBox 2.0.30 + Flying Saucer 9.1.22 для PDF
- Apache POI 5.2.3 для Excel
- OpenCSV 5.7.1 для CSV
- Jackson 2.15.0 для JSON/XML
- Spring Boot Mail для email функциональности
- Thymeleaf 3.1.2 для шаблонов

> **См. Приложение D** - Полная конфигурация и зависимости

### Frontend интеграция

Frontend компоненты построены на Vue.js 3 с использованием Quasar UI и обеспечивают:

- **Интерактивный интерфейс** для выбора типа отчёта, формата и параметров
- **Диалоги для email** с валидацией и настройками
- **Отслеживание статуса** генерации с прогресс-баром
- **Уведомления** о результатах операций
- **Интеграцию с GraphQL** для API вызовов
- **Предварительный просмотр** для поддерживаемых форматов

**Основные компоненты:**
- `ReportGenerator.vue` - основной компонент генерации отчётов
- `ReportStatus.vue` - отображение статуса и прогресса
- `EmailDialog.vue` - диалог для отправки по email
- `FormatSelector.vue` - выбор формата экспорта

> **См. Приложение E** - Vue.js компоненты для отчётности

## Загрузка данных из внешних источников

### Обзор функциональности
Система предоставляет возможность загрузки и импорта данных из внешних источников, прежде всего из файлов Excel, OpenOffice и LibreOffice, с использованием современного File System Access API. Это позволяет обрабатывать данные без загрузки файлов на сервер, обеспечивая безопасность и конфиденциальность.

### Поддерживаемые форматы

#### 1. Microsoft Excel (.xlsx, .xls)
- **Назначение**: Основной формат для табличных данных
- **Технология**: Apache POI 5.2.3
- **Особенности**: Поддержка множественных листов, формул, форматирования

#### 2. OpenDocument Spreadsheet (.ods)
- **Назначение**: Открытый формат для LibreOffice/OpenOffice
- **Технология**: Apache POI 5.2.3 с ODF поддержкой
- **Особенности**: Совместимость с открытыми офисными пакетами

#### 3. CSV (Comma-Separated Values)
- **Назначение**: Простой текстовый формат
- **Технология**: OpenCSV 5.7.1
- **Особенности**: Универсальная совместимость, легкий вес

### Процесс загрузки данных

#### Этапы обработки
1. **Выбор файла** - пользователь выбирает файл через File System Access API
2. **Анализ структуры** - система исследует содержимое файла
3. **Маппинг полей** - сопоставление колонок файла с полями системы
4. **Валидация данных** - проверка корректности и полноты данных
5. **Предварительный просмотр** - отображение данных перед импортом
6. **Импорт в БД** - сохранение данных в базу данных
7. **Отчёт о результатах** - статистика импорта и обработка ошибок

#### Поддерживаемые типы данных
- **Организационные единицы** - государства, организации, учреждения
- **Должности** - позиции в организациях
- **Люди** - персональные данные
- **Исторические периоды** - временные рамки
- **Географические данные** - координаты и местоположения

### File System Access API интеграция

#### Безопасность и конфиденциальность
- **Локальная обработка** - файлы не покидают машину пользователя
- **Разрешения** - пользователь явно разрешает доступ к файлам
- **Временный доступ** - доступ только на время сессии
- **Безопасная передача** - только обработанные данные отправляются на сервер

#### Техническая реализация
```typescript
interface FileImportService {
    // Выбор файла через File System Access API
    selectFile(accept: string[]): Promise<FileHandle | null>;
    
    // Чтение содержимого файла
    readFileContent(fileHandle: FileHandle): Promise<ArrayBuffer>;
    
    // Анализ структуры файла
    analyzeFileStructure(content: ArrayBuffer, format: FileFormat): Promise<FileStructure>;
    
    // Маппинг полей
    mapFields(structure: FileStructure, targetType: DataType): Promise<FieldMapping>;
    
    // Валидация данных
    validateData(content: ArrayBuffer, mapping: FieldMapping): Promise<ValidationResult>;
    
    // Импорт данных
    importData(content: ArrayBuffer, mapping: FieldMapping): Promise<ImportResult>;
}
```

### API для импорта данных

Система предоставляет GraphQL мутации для управления процессом импорта:

**Основные операции:**
- `analyzeFile` - анализ структуры файла
- `mapFields` - сопоставление полей
- `validateImport` - валидация данных перед импортом
- `executeImport` - выполнение импорта
- `getImportStatus` - получение статуса импорта
- `getImportHistory` - история импортов

**Поддерживаемые типы импорта:** ORGANIZATION, POSITION, PERSON, HISTORICAL_PERIOD, GEOGRAPHIC_DATA

### Техническая реализация

#### Архитектура
Система построена на клиент-серверной архитектуре с локальной обработкой файлов:

- **Frontend**: Vue.js + File System Access API для работы с файлами
- **Backend**: Spring Boot сервисы для валидации и импорта данных
- **Database**: PostgreSQL для хранения импортированных данных
- **Validation**: Многоуровневая валидация на клиенте и сервере

#### Основные компоненты
- **FileImportController** - REST API для управления импортом
- **FileImportService** - основная бизнес-логика импорта
- **FileAnalyzerService** - анализ структуры файлов
- **DataValidatorService** - валидация данных
- **ImportProcessorService** - обработка и импорт данных
- **FieldMapperService** - сопоставление полей

#### Обработчики форматов
- **ExcelProcessor** - обработка Excel файлов через Apache POI
- **ODSProcessor** - обработка OpenDocument файлов
- **CSVProcessor** - обработка CSV файлов через OpenCSV

### Frontend интеграция

Frontend компоненты обеспечивают интуитивный интерфейс для импорта:

- **FileSelector** - выбор файлов через File System Access API
- **StructureAnalyzer** - анализ и отображение структуры файла
- **FieldMapper** - интерактивное сопоставление полей
- **DataPreview** - предварительный просмотр данных
- **ImportProgress** - отслеживание процесса импорта
- **ImportResults** - отображение результатов импорта

**Основные компоненты:**
- `FileImport.vue` - основной компонент импорта
- `FileSelector.vue` - выбор файлов
- `FieldMapper.vue` - сопоставление полей
- `DataPreview.vue` - предварительный просмотр
- `ImportProgress.vue` - прогресс импорта

### Конфигурация

Система настраивается через `application.yml` с параметрами для:

- **File Import**: максимальные размеры файлов, поддерживаемые форматы
- **Validation**: правила валидации для различных типов данных
- **Import Processing**: настройки для обработки больших файлов
- **Error Handling**: политики обработки ошибок

**Основные зависимости:**
- Apache POI 5.2.3 для Excel/ODS файлов
- OpenCSV 5.7.1 для CSV файлов
- Jackson 2.15.0 для JSON обработки
- Spring Boot Validation для валидации данных

### Обработка ошибок

#### Типы ошибок
- **Формат файла** - неподдерживаемый формат
- **Структура данных** - несоответствие ожидаемой структуре
- **Валидация** - некорректные данные
- **Дублирование** - конфликты с существующими данными
- **Системные** - технические ошибки

#### Стратегии обработки
- **Продолжение с ошибками** - импорт корректных данных с отчётом об ошибках
- **Полная остановка** - прекращение импорта при первой ошибке
- **Исправление** - автоматическое исправление типичных ошибок
- **Ручная корректировка** - возможность исправления ошибок пользователем

### Производительность

#### Оптимизации
- **Потоковая обработка** - обработка больших файлов по частям
- **Кэширование** - кэширование результатов анализа файлов
- **Асинхронная обработка** - фоновый импорт для больших файлов
- **Пакетная обработка** - группировка операций для повышения производительности

#### Ограничения
- **Размер файла**: до 100MB для Excel/ODS, до 50MB для CSV
- **Количество строк**: до 1,000,000 строк за один импорт
- **Количество колонок**: до 100 колонок на лист
- **Время обработки**: до 30 минут для больших файлов

### Безопасность

#### Защита данных
- **Локальная обработка** - файлы не загружаются на сервер
- **Валидация входных данных** - проверка всех импортируемых данных
- **Санитизация** - очистка данных от потенциально опасного содержимого
- **Логирование** - отслеживание всех операций импорта

#### Аудит
- **История импортов** - полная история всех операций импорта
- **Отслеживание изменений** - логирование всех изменений в данных
- **Контроль доступа** - проверка прав пользователя на импорт

## Структура проекта

### Backend структура
```
backend/src/main/java/io/github/bondalen/vuege/
├── VuegeApplication.java
├── controller/
│   ├── GraphQLController.java
│   ├── HealthController.java
│   ├── ReportController.java
│   └── FileImportController.java
├── model/
│   ├── OrganizationalUnit.java (с Lombok аннотациями)
│   ├── Position.java (с Lombok аннотациями)
│   ├── Person.java (с Lombok аннотациями)
│   ├── PersonPosition.java (с Lombok аннотациями)
│   ├── HistoricalPeriod.java (с Lombok аннотациями)
│   ├── GeoPoint.java (с Lombok аннотациями)
│   ├── ReportStatus.java (с Lombok аннотациями)
│   ├── ReportRequest.java (с Lombok аннотациями)
│   ├── EmailReportRequest.java (с Lombok аннотациями)
│   ├── FileAnalysisResult.java (с Lombok аннотациями)
│   ├── ImportStatus.java (с Lombok аннотациями)
│   ├── ImportRequest.java (с Lombok аннотациями)
│   ├── ValidationRequest.java (с Lombok аннотациями)
│   └── FieldMapping.java (с Lombok аннотациями)
├── repository/
│   ├── OrganizationalUnitRepository.java
│   ├── PositionRepository.java
│   ├── PersonRepository.java
│   ├── PersonPositionRepository.java
│   ├── ReportRepository.java
│   └── ImportRepository.java
├── service/
│   ├── OrganizationalUnitService.java
│   ├── PositionService.java
│   ├── PersonService.java
│   ├── GISService.java
│   ├── ReportService.java
│   ├── ReportGeneratorService.java
│   ├── EmailService.java
│   ├── TemplateService.java
│   ├── FileStorageService.java
│   ├── FileImportService.java
│   ├── FileAnalyzerService.java
│   ├── DataValidatorService.java
│   ├── ImportProcessorService.java
│   ├── FieldMapperService.java
│   ├── generator/
│   │   ├── PDFGenerator.java
│   │   ├── HTMLGenerator.java
│   │   ├── JSONGenerator.java
│   │   ├── ExcelGenerator.java
│   │   ├── CSVGenerator.java
│   │   └── XMLGenerator.java
│   ├── processor/
│   │   ├── ExcelProcessor.java
│   │   ├── ODSProcessor.java
│   │   └── CSVProcessor.java
│   ├── validator/
│   │   ├── OrganizationValidator.java
│   │   ├── PositionValidator.java
│   │   ├── PersonValidator.java
│   │   └── HistoricalPeriodValidator.java
│   └── ReportDataService.java
├── async/
│   ├── AsyncReportProcessor.java
│   └── AsyncImportProcessor.java
├── graphql/
│   ├── resolver/
│   │   ├── OrganizationalUnitResolver.java
│   │   ├── PositionResolver.java
│   │   ├── PersonResolver.java
│   │   ├── ReportResolver.java
│   │   └── ImportResolver.java
│   └── scalar/
│       ├── DateScalar.java
│       └── GeoPointScalar.java
├── exception/
│   ├── VuegeException.java
│   ├── GlobalExceptionHandler.java
│   ├── ReportNotFoundException.java
│   ├── ReportNotReadyException.java
│   ├── PDFGenerationException.java
│   ├── ImportNotFoundException.java
│   ├── FileAnalysisException.java
│   ├── ValidationException.java
│   ├── UnsupportedFileTypeException.java
│   └── TemplateNotFoundException.java
└── config/
    ├── AsyncConfig.java
    ├── EmailConfig.java
    └── ImportConfig.java
```

### Frontend структура
```
frontend/
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
│   │   ├── GISPage.vue
│   │   ├── ReportsPage.vue
│   │   └── ImportPage.vue
│   ├── components/
│   │   ├── OrganizationCard.vue
│   │   ├── PositionList.vue
│   │   ├── PersonProfile.vue
│   │   ├── GISMap.vue
│   │   ├── ReportGenerator.vue
│   │   ├── ReportStatus.vue
│   │   ├── EmailDialog.vue
│   │   ├── FileImport.vue
│   │   ├── FileSelector.vue
│   │   ├── StructureAnalyzer.vue
│   │   ├── FieldMapper.vue
│   │   ├── DataValidator.vue
│   │   ├── ImportExecutor.vue
│   │   └── ImportResults.vue
│   ├── stores/
│   │   ├── organizations.ts
│   │   ├── positions.ts
│   │   ├── people.ts
│   │   ├── reports.ts
│   │   └── import.ts
│   ├── types/
│   │   ├── organizational-unit.ts
│   │   ├── position.ts
│   │   ├── person.ts
│   │   ├── geo-point.ts
│   │   ├── report.ts
│   │   └── import.ts
│   ├── queries/
│   │   ├── organizations.ts
│   │   ├── positions.ts
│   │   ├── people.ts
│   │   ├── reports.ts
│   │   └── import.ts
│   └── utils/
│       ├── date-utils.ts
│       ├── geo-utils.ts
│       ├── validation.ts
│       ├── report-utils.ts
│       └── file-utils.ts
├── public/
├── package.json
├── tsconfig.json
├── quasar.config.js
└── vite.config.ts
```

### Maven конфигурация

Полная Maven конфигурация проекта находится в [Приложении F: Maven конфигурация](#приложение-f-maven-конфигурация).

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
- [ ] Настройка MCP серверов (см. проблема [P250816-01])

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

### Этап 6: Отчётность и экспорт данных (Недели 11-12)
- [ ] Настройка универсальной системы генерации отчётов
- [ ] Реализация генераторов для всех форматов (PDF, HTML, JSON, Excel, CSV, XML)
- [ ] Реализация Email-сервиса
- [ ] Создание HTML-шаблонов отчётов
- [ ] Асинхронная обработка отчётов
- [ ] Frontend компоненты для генерации отчётов с выбором формата
- [ ] Интеграция с GraphQL API
- [ ] Тестирование всех форматов экспорта

### Этап 7: Импорт данных из внешних источников (Недели 13-14)
- [ ] Настройка File System Access API интеграции
- [ ] Реализация анализаторов файлов (Excel, ODS, CSV)
- [ ] Реализация валидаторов данных для всех типов сущностей
- [ ] Создание системы маппинга полей
- [ ] Асинхронная обработка импорта
- [ ] Frontend компоненты для импорта с пошаговым интерфейсом
- [ ] Интеграция с GraphQL API для импорта
- [ ] Создание шаблонов для заполнения
- [ ] Тестирование всех форматов импорта

### Этап 8: Тестирование и оптимизация (Недели 15-16)
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

### Использование Lombok

#### Цель интеграции
Lombok интегрирован в проект для минимизации boilerplate кода в Java-классах, что повышает читаемость и снижает вероятность ошибок.

#### Основные аннотации
```java
// Для моделей данных
@Data                    // Геттеры, сеттеры, toString, equals, hashCode
@Builder                 // Паттерн Builder
@NoArgsConstructor      // Конструктор без параметров
@AllArgsConstructor     // Конструктор со всеми параметрами
@RequiredArgsConstructor // Конструктор с обязательными параметрами

// Для сервисов и контроллеров
@Slf4j                  // Автоматическое логирование
@RequiredArgsConstructor // Внедрение зависимостей через конструктор

// Для репозиториев
@Repository             // Spring Repository
@RequiredArgsConstructor // Внедрение зависимостей
```

#### Пример использования в моделях
```java
@Data
@Builder
@NoArgsConstructor
@AllArgsConstructor
public class OrganizationalUnit {
    private String id;
    private String name;
    private OrganizationType type;
    private LocalDate foundedDate;
    private LocalDate dissolvedDate;
    private GeoPoint location;
    private boolean isFictional;
    private HistoricalPeriod historicalPeriod;
    private String parentUnitId;
    private List<String> childUnitIds;
    private List<Transformation> transformations;
}
```

#### Правила использования
- **Модели данных**: Используем `@Data`, `@Builder`, `@NoArgsConstructor`, `@AllArgsConstructor`
- **Сервисы**: Используем `@Slf4j`, `@RequiredArgsConstructor`
- **Контроллеры**: Используем `@Slf4j`, `@RequiredArgsConstructor`
- **Репозитории**: Используем `@Repository`, `@RequiredArgsConstructor`
- **Исключения**: Не используем Lombok для сложной бизнес-логики

### Стандарты кодирования
- **TypeScript** - строгий режим
- **ESLint** - линтинг кода
- **Prettier** - форматирование
- **Pre-commit hooks** - проверка перед коммитом
- **Lombok** - минимизация boilerplate кода в Java
- **Lombok Annotations** - стандартизированное использование аннотаций

### Процесс разработки и коммуникации

#### Правила взаимодействия
- **Предварительное согласование** - все изменения в документации и коде должны быть предварительно согласованы
- **Формулировка предложений** - перед внесением изменений необходимо сформулировать и представить предложения
- **Получение согласия** - изменения вносятся только после получения явного согласия пользователя
- **Документирование решений** - все принятые решения должны быть задокументированы

#### Процесс внесения изменений
1. **Анализ** - изучение текущего состояния и выявление необходимости изменений
2. **Предложение** - формулировка конкретных предложений с обоснованием
3. **Обсуждение** - обсуждение предложений и возможных альтернатив
4. **Согласование** - получение согласия на конкретные изменения
5. **Реализация** - внесение согласованных изменений
6. **Документирование** - обновление changelog и tasktracker

#### Исключения
- Исправление очевидных опечаток и форматирования
- Обновление дат и временных меток
- Добавление стандартных комментариев в код

### Документирование
- **JSDoc** - документация функций
- **JavaDoc** - документация Java классов
- **Lombok Documentation** - документация аннотаций
- **GraphQL Schema** - документация API
- **README** - документация проекта
- **Changelog** - история изменений
- **UML/BPMN диаграммы** - визуальная документация архитектуры и процессов

### Работа с диаграммами

#### Гибридный подход
Проект использует специализированные инструменты для разных типов диаграмм:

**PlantUML** - для UML диаграмм:
- Диаграммы классов (доменная модель, архитектура)
- Диаграммы последовательности (процессы взаимодействия)
- Диаграммы компонентов (системная архитектура)
- Диаграммы состояний (жизненные циклы)

**BPMN Sketch Miner** - для BPMN диаграмм:
- Бизнес-процессы (импорт данных, генерация отчётов)
- Workflow (валидация, обработка ошибок)
- Алгоритмы (поиск, анализ данных)

#### Обязательные требования
- **При изменении архитектуры** - обновлять соответствующие диаграммы
- **При изменении доменной модели** - обновлять диаграммы классов
- **При изменении процессов** - обновлять BPMN диаграммы
- **При создании новых диаграмм** - добавлять записи в changelog.md
- **Регулярно проверять** актуальность диаграмм и документации

#### Стандарты оформления
- **Цветовая схема**: согласованная палитра для всех типов элементов
- **Тема**: plain (минималистичная)
- **Фон**: белый (#FFFFFF)
- **Шрифт**: 12pt для читаемости
- **Именование файлов**: kebab-case формат

#### Правила ведения списка проблем (problems.md)
- **См. .cursorrules** - все правила ведения списка проблем находятся в файле .cursorrules
- **Единый источник истины** - правила не дублируются в других документах
- **Обязательное изучение диаграмм** - при ознакомлении с проблемами обязательно изучать соответствующие BPMN диаграммы способов решения

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

---

## Приложения

### Приложение A: GraphQL схема для отчётности

#### Полная GraphQL схема
```graphql
type Mutation {
    # Генерация отчёта с возможностью скачивания
    generateReport(
        reportType: ReportType!
        parameters: ReportParameters!
        format: ReportFormat!
    ): ReportGenerationResult!
    
    # Отправка отчёта по email
    sendReportByEmail(
        reportType: ReportType!
        parameters: ReportParameters!
        email: String!
        subject: String
    ): EmailSendResult!
    
    # Получение статуса генерации отчёта
    getReportStatus(reportId: ID!): ReportStatus!
}

enum ReportType {
    ORGANIZATION
    HISTORICAL_PERIOD
    GEOGRAPHIC
    PERSON
    CUSTOM
}

enum ReportFormat {
    PDF
    HTML
    JSON
    EXCEL
    CSV
    XML
}

input ReportParameters {
    organizationId: ID
    periodId: ID
    geographicBounds: BoundingBox
    personId: ID
    timeRange: TimeRange
    includeCharts: Boolean
    includeMaps: Boolean
    language: String
}

type ReportGenerationResult {
    reportId: ID!
    status: ReportStatus!
    downloadUrl: String
    estimatedTime: Int
    message: String
}

type EmailSendResult {
    success: Boolean!
    messageId: String
    error: String
}

type ReportStatus {
    reportId: ID!
    status: ReportStatusEnum!
    progress: Int
    downloadUrl: String
    error: String
    createdAt: DateTime!
    completedAt: DateTime
}

enum ReportStatusEnum {
    PENDING
    GENERATING
    COMPLETED
    FAILED
    EXPIRED
}
```

#### REST API для скачивания
```http
# Скачивание готового отчёта
GET /api/reports/{reportId}/download
Authorization: Bearer {token}

# Получение статуса отчёта
GET /api/reports/{reportId}/status
Authorization: Bearer {token}

# Отмена генерации отчёта
DELETE /api/reports/{reportId}
Authorization: Bearer {token}
```

### Приложение B: Детальная реализация компонентов системы

#### ReportController
```java
@RestController
@RequestMapping("/api/reports")
@RequiredArgsConstructor
@Slf4j
public class ReportController {
    
    private final ReportService reportService;
    private final EmailService emailService;
    
    @PostMapping("/generate")
    public ResponseEntity<ReportGenerationResult> generateReport(
            @RequestBody ReportRequest request) {
        return ResponseEntity.ok(reportService.generateReport(request));
    }
    
    @PostMapping("/email")
    public ResponseEntity<EmailSendResult> sendReportByEmail(
            @RequestBody EmailReportRequest request) {
        return ResponseEntity.ok(emailService.sendReport(request));
    }
    
    @GetMapping("/{reportId}/download")
    public ResponseEntity<Resource> downloadReport(@PathVariable String reportId) {
        Resource resource = reportService.getReportFile(reportId);
        return ResponseEntity.ok()
                .header(HttpHeaders.CONTENT_DISPOSITION, 
                        "attachment; filename=\"report-" + reportId + ".pdf\"")
                .body(resource);
    }
    
    @GetMapping("/{reportId}/status")
    public ResponseEntity<ReportStatus> getReportStatus(@PathVariable String reportId) {
        return ResponseEntity.ok(reportService.getReportStatus(reportId));
    }
}
```

#### ReportService
```java
@Service
@RequiredArgsConstructor
@Slf4j
public class ReportService {
    
    private final ReportGeneratorService reportGenerator;
    private final TemplateService templateService;
    private final ReportRepository reportRepository;
    private final AsyncReportProcessor asyncProcessor;
    
    public ReportGenerationResult generateReport(ReportRequest request) {
        ReportStatus status = ReportStatus.builder()
                .reportId(generateReportId())
                .status(ReportStatusEnum.PENDING)
                .createdAt(LocalDateTime.now())
                .build();
        
        reportRepository.save(status);
        
        // Асинхронная генерация
        asyncProcessor.processReport(status.getReportId(), request);
        
        return ReportGenerationResult.builder()
                .reportId(status.getReportId())
                .status(status.getStatus())
                .estimatedTime(calculateEstimatedTime(request.getReportType()))
                .build();
    }
    
    public Resource getReportFile(String reportId) {
        ReportStatus status = reportRepository.findById(reportId)
                .orElseThrow(() -> new ReportNotFoundException(reportId));
        
        if (status.getStatus() != ReportStatusEnum.COMPLETED) {
            throw new ReportNotReadyException(reportId);
        }
        
        return new FileSystemResource(status.getFilePath());
    }
}
```

#### ReportGeneratorService
```java
@Service
@RequiredArgsConstructor
@Slf4j
public class ReportGeneratorService {
    
    private final Map<ReportFormat, ReportGenerator> generators;
    private final FileStorageService fileStorage;
    
    public String generateReport(ReportData data, ReportType type, ReportFormat format) {
        try {
            ReportGenerator generator = generators.get(format);
            if (generator == null) {
                throw new UnsupportedFormatException("Format not supported: " + format);
            }
            
            // Генерация отчёта в выбранном формате
            byte[] reportBytes = generator.generate(data, type);
            
            // Сохранение файла
            String extension = getFileExtension(format);
            String fileName = "report-" + data.getReportId() + extension;
            String filePath = fileStorage.storeFile(fileName, reportBytes);
            
            log.info("Report generated in {} format: {}", format, filePath);
            return filePath;
            
        } catch (Exception e) {
            log.error("Error generating report in {} format", format, e);
            throw new ReportGenerationException("Failed to generate report in " + format + " format", e);
        }
    }
    
    private String getFileExtension(ReportFormat format) {
        return switch (format) {
            case PDF -> ".pdf";
            case HTML -> ".html";
            case JSON -> ".json";
            case EXCEL -> ".xlsx";
            case CSV -> ".csv";
            case XML -> ".xml";
        };
    }
}
```

#### Интерфейс ReportGenerator
```java
public interface ReportGenerator {
    byte[] generate(ReportData data, ReportType type);
    ReportFormat getSupportedFormat();
}
```

#### PDFGenerator
```java
@Component
@RequiredArgsConstructor
@Slf4j
public class PDFGenerator implements ReportGenerator {
    
    private final TemplateService templateService;
    
    @Override
    public byte[] generate(ReportData data, ReportType type) {
        try {
            // Генерация HTML из шаблона
            String htmlContent = templateService.processTemplate(type, data);
            
            // Конвертация HTML в PDF
            return convertHtmlToPdf(htmlContent);
            
        } catch (Exception e) {
            log.error("Error generating PDF report", e);
            throw new ReportGenerationException("Failed to generate PDF", e);
        }
    }
    
    @Override
    public ReportFormat getSupportedFormat() {
        return ReportFormat.PDF;
    }
    
    private byte[] convertHtmlToPdf(String htmlContent) {
        ByteArrayOutputStream baos = new ByteArrayOutputStream();
        
        try (PdfDocument pdf = new PdfDocument(new PdfWriter(baos))) {
            ConverterProperties properties = new ConverterProperties();
            
            // Настройка шрифтов для кириллицы
            FontProvider fontProvider = new DefaultFontProvider(false, false, false);
            fontProvider.addSystemFonts();
            properties.setFontProvider(fontProvider);
            
            // Конвертация HTML в PDF
            HtmlConverter.convertToPdf(htmlContent, pdf, properties);
        }
        
        return baos.toByteArray();
    }
}
```

#### HTMLGenerator
```java
@Component
@RequiredArgsConstructor
@Slf4j
public class HTMLGenerator implements ReportGenerator {
    
    private final TemplateService templateService;
    
    @Override
    public byte[] generate(ReportData data, ReportType type) {
        try {
            String htmlContent = templateService.processTemplate(type, data);
            return htmlContent.getBytes(StandardCharsets.UTF_8);
            
        } catch (Exception e) {
            log.error("Error generating HTML report", e);
            throw new ReportGenerationException("Failed to generate HTML", e);
        }
    }
    
    @Override
    public ReportFormat getSupportedFormat() {
        return ReportFormat.HTML;
    }
}
```

#### JSONGenerator
```java
@Component
@RequiredArgsConstructor
@Slf4j
public class JSONGenerator implements ReportGenerator {
    
    private final ObjectMapper objectMapper;
    
    @Override
    public byte[] generate(ReportData data, ReportType type) {
        try {
            return objectMapper.writeValueAsBytes(data);
            
        } catch (Exception e) {
            log.error("Error generating JSON report", e);
            throw new ReportGenerationException("Failed to generate JSON", e);
        }
    }
    
    @Override
    public ReportFormat getSupportedFormat() {
        return ReportFormat.JSON;
    }
}
```

#### ExcelGenerator
```java
@Component
@RequiredArgsConstructor
@Slf4j
public class ExcelGenerator implements ReportGenerator {
    
    @Override
    public byte[] generate(ReportData data, ReportType type) {
        try (Workbook workbook = new XSSFWorkbook()) {
            
            // Создание листа с данными
            Sheet sheet = workbook.createSheet("Отчёт");
            
            // Заголовки
            Row headerRow = sheet.createRow(0);
            headerRow.createCell(0).setCellValue("Поле");
            headerRow.createCell(1).setCellValue("Значение");
            
            // Данные
            int rowNum = 1;
            rowNum = addOrganizationData(sheet, data, rowNum);
            rowNum = addPositionsData(sheet, data, rowNum);
            rowNum = addPeopleData(sheet, data, rowNum);
            
            // Автоподбор ширины колонок
            for (int i = 0; i < 2; i++) {
                sheet.autoSizeColumn(i);
            }
            
            // Сохранение в байты
            ByteArrayOutputStream baos = new ByteArrayOutputStream();
            workbook.write(baos);
            return baos.toByteArray();
            
        } catch (Exception e) {
            log.error("Error generating Excel report", e);
            throw new ReportGenerationException("Failed to generate Excel", e);
        }
    }
    
    @Override
    public ReportFormat getSupportedFormat() {
        return ReportFormat.EXCEL;
    }
    
    private int addOrganizationData(Sheet sheet, ReportData data, int startRow) {
        if (data.getOrganization() != null) {
            Row row = sheet.createRow(startRow++);
            row.createCell(0).setCellValue("Организация");
            row.createCell(1).setCellValue(data.getOrganization().getName());
            
            row = sheet.createRow(startRow++);
            row.createCell(0).setCellValue("Тип");
            row.createCell(1).setCellValue(data.getOrganization().getType().toString());
            
            row = sheet.createRow(startRow++);
            row.createCell(0).setCellValue("Дата основания");
            row.createCell(1).setCellValue(data.getOrganization().getFoundedDate().toString());
        }
        return startRow;
    }
    
    private int addPositionsData(Sheet sheet, ReportData data, int startRow) {
        if (data.getPositions() != null && !data.getPositions().isEmpty()) {
            Row row = sheet.createRow(startRow++);
            row.createCell(0).setCellValue("Должности");
            row.createCell(1).setCellValue("");
            
            for (Position position : data.getPositions()) {
                row = sheet.createRow(startRow++);
                row.createCell(0).setCellValue("  " + position.getTitle());
                row.createCell(1).setCellValue(position.isActive() ? "Активна" : "Неактивна");
            }
        }
        return startRow;
    }
    
    private int addPeopleData(Sheet sheet, ReportData data, int startRow) {
        if (data.getCurrentHolders() != null && !data.getCurrentHolders().isEmpty()) {
            Row row = sheet.createRow(startRow++);
            row.createCell(0).setCellValue("Текущие руководители");
            row.createCell(1).setCellValue("");
            
            for (PersonPosition holder : data.getCurrentHolders()) {
                row = sheet.createRow(startRow++);
                row.createCell(0).setCellValue("  " + holder.getPerson().getName());
                row.createCell(1).setCellValue(holder.getPosition().getTitle());
            }
        }
        return startRow;
    }
}
```

#### CSVGenerator
```java
@Component
@RequiredArgsConstructor
@Slf4j
public class CSVGenerator implements ReportGenerator {
    
    @Override
    public byte[] generate(ReportData data, ReportType type) {
        try (ByteArrayOutputStream baos = new ByteArrayOutputStream();
             OutputStreamWriter writer = new OutputStreamWriter(baos, StandardCharsets.UTF_8);
             CSVWriter csvWriter = new CSVWriter(writer)) {
            
            // Заголовки
            csvWriter.writeNext(new String[]{"Поле", "Значение"});
            
            // Данные организации
            if (data.getOrganization() != null) {
                csvWriter.writeNext(new String[]{"Организация", data.getOrganization().getName()});
                csvWriter.writeNext(new String[]{"Тип", data.getOrganization().getType().toString()});
                csvWriter.writeNext(new String[]{"Дата основания", data.getOrganization().getFoundedDate().toString()});
            }
            
            // Данные должностей
            if (data.getPositions() != null) {
                csvWriter.writeNext(new String[]{"Должности", ""});
                for (Position position : data.getPositions()) {
                    csvWriter.writeNext(new String[]{"  " + position.getTitle(), 
                                                   position.isActive() ? "Активна" : "Неактивна"});
                }
            }
            
            // Данные людей
            if (data.getCurrentHolders() != null) {
                csvWriter.writeNext(new String[]{"Текущие руководители", ""});
                for (PersonPosition holder : data.getCurrentHolders()) {
                    csvWriter.writeNext(new String[]{"  " + holder.getPerson().getName(), 
                                                   holder.getPosition().getTitle()});
                }
            }
            
            csvWriter.flush();
            return baos.toByteArray();
            
        } catch (Exception e) {
            log.error("Error generating CSV report", e);
            throw new ReportGenerationException("Failed to generate CSV", e);
        }
    }
    
    @Override
    public ReportFormat getSupportedFormat() {
        return ReportFormat.CSV;
    }
}
```

#### XMLGenerator
```java
@Component
@RequiredArgsConstructor
@Slf4j
public class XMLGenerator implements ReportGenerator {
    
    private final XmlMapper xmlMapper;
    
    @Override
    public byte[] generate(ReportData data, ReportType type) {
        try {
            return xmlMapper.writeValueAsBytes(data);
            
        } catch (Exception e) {
            log.error("Error generating XML report", e);
            throw new ReportGenerationException("Failed to generate XML", e);
        }
    }
    
    @Override
    public ReportFormat getSupportedFormat() {
        return ReportFormat.XML;
    }
}
```

#### EmailService
```java
@Service
@RequiredArgsConstructor
@Slf4j
public class EmailService {
    
    private final JavaMailSender mailSender;
    private final ReportService reportService;
    private final TemplateService templateService;
    
    public EmailSendResult sendReport(EmailReportRequest request) {
        try {
            // Генерация отчёта
            ReportGenerationResult report = reportService.generateReport(
                    request.getReportRequest());
            
            // Ожидание завершения генерации
            waitForReportCompletion(report.getReportId());
            
            // Получение файла отчёта
            Resource reportFile = reportService.getReportFile(report.getReportId());
            
            // Отправка email
            MimeMessage message = mailSender.createMimeMessage();
            MimeMessageHelper helper = new MimeMessageHelper(message, true);
            
            helper.setTo(request.getEmail());
            helper.setSubject(request.getSubject());
            helper.setText(generateEmailText(request), true);
            helper.addAttachment("report.pdf", reportFile);
            
            mailSender.send(message);
            
            log.info("Report sent to email: {}", request.getEmail());
            
            return EmailSendResult.builder()
                    .success(true)
                    .messageId(message.getMessageID())
                    .build();
                    
        } catch (Exception e) {
            log.error("Error sending report by email", e);
            return EmailSendResult.builder()
                    .success(false)
                    .error(e.getMessage())
                    .build();
        }
    }
}
```

#### AsyncReportProcessor
```java
@Component
@RequiredArgsConstructor
@Slf4j
public class AsyncReportProcessor {
    
    private final ReportGeneratorService reportGenerator;
    private final ReportRepository reportRepository;
    private final ReportDataService reportDataService;
    
    @Async
    public void processReport(String reportId, ReportRequest request) {
        try {
            // Обновление статуса
            updateReportStatus(reportId, ReportStatusEnum.GENERATING);
            
            // Получение данных для отчёта
            ReportData data = reportDataService.getReportData(request);
            
            // Генерация отчёта в выбранном формате
            String filePath = reportGenerator.generateReport(data, request.getReportType(), request.getFormat());
            
            // Обновление статуса
            updateReportStatus(reportId, ReportStatusEnum.COMPLETED, filePath);
            
            log.info("Report {} generated successfully", reportId);
            
        } catch (Exception e) {
            log.error("Error processing report {}", reportId, e);
            updateReportStatus(reportId, ReportStatusEnum.FAILED, null, e.getMessage());
        }
    }
    
    private void updateReportStatus(String reportId, ReportStatusEnum status, 
                                   String filePath, String error) {
        ReportStatus reportStatus = reportRepository.findById(reportId)
                .orElseThrow(() -> new ReportNotFoundException(reportId));
        
        reportStatus.setStatus(status);
        reportStatus.setFilePath(filePath);
        reportStatus.setError(error);
        reportStatus.setCompletedAt(LocalDateTime.now());
        
        reportRepository.save(reportStatus);
    }
}
```

### Приложение C: HTML-шаблоны для различных типов отчётов

#### HTML-шаблон для организационной единицы
```html
<!DOCTYPE html>
<html xmlns:th="http://www.thymeleaf.org">
<head>
    <meta charset="UTF-8">
    <title>Отчёт по организации</title>
    <style>
        body { font-family: Arial, sans-serif; margin: 20px; }
        .header { text-align: center; border-bottom: 2px solid #333; padding-bottom: 10px; }
        .section { margin: 20px 0; }
        .section-title { font-size: 18px; font-weight: bold; color: #333; }
        .info-row { margin: 10px 0; }
        .label { font-weight: bold; }
        .table { width: 100%; border-collapse: collapse; margin: 10px 0; }
        .table th, .table td { border: 1px solid #ddd; padding: 8px; text-align: left; }
        .table th { background-color: #f2f2f2; }
    </style>
</head>
<body>
    <div class="header">
        <h1>Отчёт по организационной единице</h1>
        <p th:text="${organization.name}">Название организации</p>
    </div>
    
    <div class="section">
        <div class="section-title">Основная информация</div>
        <div class="info-row">
            <span class="label">Тип:</span>
            <span th:text="${organization.type}">Тип</span>
        </div>
        <div class="info-row">
            <span class="label">Дата основания:</span>
            <span th:text="${#temporals.format(organization.foundedDate, 'dd.MM.yyyy')}">Дата</span>
        </div>
        <div class="info-row" th:if="${organization.dissolvedDate}">
            <span class="label">Дата ликвидации:</span>
            <span th:text="${#temporals.format(organization.dissolvedDate, 'dd.MM.yyyy')}">Дата</span>
        </div>
    </div>
    
    <div class="section">
        <div class="section-title">Должности</div>
        <table class="table">
            <thead>
                <tr>
                    <th>Название</th>
                    <th>Дата создания</th>
                    <th>Статус</th>
                </tr>
            </thead>
            <tbody>
                <tr th:each="position : ${positions}">
                    <td th:text="${position.title}">Название</td>
                    <td th:text="${#temporals.format(position.createdDate, 'dd.MM.yyyy')}">Дата</td>
                    <td th:text="${position.isActive ? 'Активна' : 'Неактивна'}">Статус</td>
                </tr>
            </tbody>
        </table>
    </div>
    
    <div class="section">
        <div class="section-title">Текущие руководители</div>
        <table class="table">
            <thead>
                <tr>
                    <th>ФИО</th>
                    <th>Должность</th>
                    <th>Дата назначения</th>
                </tr>
            </thead>
            <tbody>
                <tr th:each="holder : ${currentHolders}">
                    <td th:text="${holder.person.name}">ФИО</td>
                    <td th:text="${holder.position.title}">Должность</td>
                    <td th:text="${#temporals.format(holder.startDate, 'dd.MM.yyyy')}">Дата</td>
                </tr>
            </tbody>
        </table>
    </div>
</body>
</html>
```

### Приложение D: Полная конфигурация и зависимости

#### application.yml
```yaml
# Report Generation Configuration
report:
  generation:
    temp-dir: /tmp/vuege-reports
    max-file-size: 50MB
    cleanup-interval: 3600 # seconds
    max-retention-days: 7
  
  templates:
    base-path: classpath:templates/reports
    cache-enabled: true
  
  formats:
    pdf:
      enabled: true
      compression: true
    html:
      enabled: true
      minify: false
    json:
      enabled: true
      pretty-print: true
    excel:
      enabled: true
      auto-size-columns: true
    csv:
      enabled: true
      encoding: UTF-8
    xml:
      enabled: true
      pretty-print: true

# Email Configuration
spring:
  mail:
    host: smtp.gmail.com
    port: 587
    username: ${EMAIL_USERNAME}
    password: ${EMAIL_PASSWORD}
    properties:
      mail:
        smtp:
          auth: true
          starttls:
            enable: true

# Async Configuration
async:
  report-processing:
    core-pool-size: 2
    max-pool-size: 5
    queue-capacity: 10
    thread-name-prefix: report-processor-
```

#### Зависимости Maven
```xml
<!-- Report Generation -->
<dependency>
    <groupId>org.apache.pdfbox</groupId>
    <artifactId>pdfbox</artifactId>
    <version>2.0.30</version>
</dependency>
<dependency>
    <groupId>org.xhtmlrenderer</groupId>
    <artifactId>flying-saucer-pdf-openpdf</artifactId>
    <version>9.1.22</version>
</dependency>
<dependency>
    <groupId>org.apache.poi</groupId>
    <artifactId>poi</artifactId>
    <version>5.2.3</version>
</dependency>
<dependency>
    <groupId>org.apache.poi</groupId>
    <artifactId>poi-ooxml</artifactId>
    <version>5.2.3</version>
</dependency>
<dependency>
    <groupId>com.opencsv</groupId>
    <artifactId>opencsv</artifactId>
    <version>5.7.1</version>
</dependency>
<dependency>
    <groupId>com.fasterxml.jackson.dataformat</groupId>
    <artifactId>jackson-dataformat-xml</artifactId>
    <version>2.15.0</version>
</dependency>

<!-- Email -->
<dependency>
    <groupId>org.springframework.boot</groupId>
    <artifactId>spring-boot-starter-mail</artifactId>
</dependency>

<!-- Template Engine -->
<dependency>
    <groupId>org.springframework.boot</groupId>
    <artifactId>spring-boot-starter-thymeleaf</artifactId>
</dependency>
```

### Приложение E: Vue.js компоненты для отчётности

#### ReportGenerator.vue
```vue
<template>
  <q-card class="report-generator">
    <q-card-section>
      <h5>Генерация отчёта</h5>
    </q-card-section>
    
    <q-card-section>
      <q-form @submit="generateReport">
        <q-select
          v-model="reportType"
          :options="reportTypes"
          label="Тип отчёта"
          required
        />
        
        <q-input
          v-model="parameters.organizationId"
          label="ID организации"
          v-if="reportType === 'ORGANIZATION'"
        />
        
        <q-input
          v-model="parameters.periodId"
          label="ID периода"
          v-if="reportType === 'HISTORICAL_PERIOD'"
        />
        
        <q-checkbox v-model="parameters.includeCharts" label="Включить графики" />
        <q-checkbox v-model="parameters.includeMaps" label="Включить карты" />
        
        <div class="row q-gutter-sm q-mt-md">
          <q-btn type="submit" color="primary" label="Скачать PDF" />
          <q-btn @click="showEmailDialog = true" color="secondary" label="Отправить по email" />
        </div>
      </q-form>
    </q-card-section>
    
    <!-- Email Dialog -->
    <q-dialog v-model="showEmailDialog">
      <q-card style="min-width: 350px">
        <q-card-section>
          <h6>Отправка отчёта по email</h6>
        </q-card-section>
        
        <q-card-section>
          <q-input v-model="emailData.email" label="Email" type="email" required />
          <q-input v-model="emailData.subject" label="Тема письма" />
        </q-card-section>
        
        <q-card-actions align="right">
          <q-btn flat label="Отмена" color="primary" v-close-popup />
          <q-btn @click="sendReportByEmail" label="Отправить" color="primary" v-close-popup />
        </q-card-actions>
      </q-card>
    </q-dialog>
    
    <!-- Status Dialog -->
    <q-dialog v-model="showStatusDialog">
      <q-card style="min-width: 400px">
        <q-card-section>
          <h6>Статус генерации отчёта</h6>
        </q-card-section>
        
        <q-card-section>
          <q-linear-progress :value="reportProgress" />
          <p class="q-mt-sm">{{ statusMessage }}</p>
        </q-card-section>
        
        <q-card-actions align="right">
          <q-btn @click="downloadReport" label="Скачать" color="primary" 
                 v-if="reportStatus === 'COMPLETED'" />
          <q-btn flat label="Закрыть" color="primary" v-close-popup />
        </q-card-actions>
      </q-card>
    </q-dialog>
  </q-card>
</template>

<script setup lang="ts">
import { ref, reactive } from 'vue'
import { useQuasar } from 'quasar'
import { generateReportMutation, sendReportByEmailMutation } from '@/queries/reports'

const $q = useQuasar()

const reportType = ref('ORGANIZATION')
const parameters = reactive({
  organizationId: '',
  periodId: '',
  includeCharts: false,
  includeMaps: false
})

const showEmailDialog = ref(false)
const showStatusDialog = ref(false)
const emailData = reactive({
  email: '',
  subject: 'Отчёт из системы Vuege'
})

const reportStatus = ref('')
const reportProgress = ref(0)
const statusMessage = ref('')

const reportTypes = [
  { label: 'По организации', value: 'ORGANIZATION' },
  { label: 'По историческому периоду', value: 'HISTORICAL_PERIOD' },
  { label: 'По географическому региону', value: 'GEOGRAPHIC' },
  { label: 'По человеку', value: 'PERSON' }
]

const generateReport = async () => {
  try {
    showStatusDialog.value = true
    statusMessage.value = 'Генерация отчёта...'
    
    const result = await generateReportMutation({
      reportType: reportType.value,
      parameters,
      format: 'PDF'
    })
    
    if (result.data?.generateReport) {
      const reportId = result.data.generateReport.reportId
      await pollReportStatus(reportId)
    }
  } catch (error) {
    $q.notify({
      type: 'negative',
      message: 'Ошибка при генерации отчёта'
    })
  }
}

const sendReportByEmail = async () => {
  try {
    const result = await sendReportByEmailMutation({
      reportType: reportType.value,
      parameters,
      email: emailData.email,
      subject: emailData.subject
    })
    
    if (result.data?.sendReportByEmail?.success) {
      $q.notify({
        type: 'positive',
        message: 'Отчёт отправлен на email'
      })
    } else {
      $q.notify({
        type: 'negative',
        message: 'Ошибка при отправке email'
      })
    }
  } catch (error) {
    $q.notify({
      type: 'negative',
      message: 'Ошибка при отправке отчёта'
    })
  }
}

const pollReportStatus = async (reportId: string) => {
  const interval = setInterval(async () => {
    try {
      const status = await getReportStatus(reportId)
      
      if (status.status === 'COMPLETED') {
        reportStatus.value = 'COMPLETED'
        reportProgress.value = 1
        statusMessage.value = 'Отчёт готов к скачиванию'
        clearInterval(interval)
      } else if (status.status === 'FAILED') {
        reportStatus.value = 'FAILED'
        statusMessage.value = 'Ошибка при генерации отчёта'
        clearInterval(interval)
      } else {
        reportProgress.value = status.progress / 100
        statusMessage.value = `Генерация... ${status.progress}%`
      }
    } catch (error) {
      clearInterval(interval)
    }
  }, 2000)
}

const downloadReport = async () => {
  // Логика скачивания файла
  window.open(`/api/reports/${reportId}/download`, '_blank')
}
</script>


### Приложение F: GraphQL схема для импорта данных

#### Полная GraphQL схема импорта
```graphql
type Mutation {
    # Анализ структуры файла
    analyzeFile(
        fileContent: String! # Base64 encoded file content
        fileName: String!
        fileType: FileType!
    ): FileAnalysisResult!
    
    # Сопоставление полей
    mapFields(
        analysisId: ID!
        targetType: ImportDataType!
        fieldMappings: [FieldMapping!]!
    ): FieldMappingResult!
    
    # Валидация данных перед импортом
    validateImport(
        analysisId: ID!
        mappingId: ID!
        validationOptions: ValidationOptions
    ): ValidationResult!
    
    # Выполнение импорта
    executeImport(
        analysisId: ID!
        mappingId: ID!
        importOptions: ImportOptions
    ): ImportResult!
    
    # Получение статуса импорта
    getImportStatus(importId: ID!): ImportStatus!
}

type Query {
    # Получение истории импортов
    getImportHistory(
        limit: Int
        offset: Int
        status: ImportStatusEnum
    ): ImportHistoryResult!
    
    # Получение шаблонов маппинга
    getMappingTemplates(dataType: ImportDataType!): [MappingTemplate!]!
    
    # Получение статистики импорта
    getImportStatistics: ImportStatistics!
}

enum FileType {
    EXCEL_XLSX
    EXCEL_XLS
    OPENOFFICE_ODS
    CSV
}

enum ImportDataType {
    ORGANIZATION
    POSITION
    PERSON
    HISTORICAL_PERIOD
    GEOGRAPHIC_DATA
}

enum ImportStatusEnum {
    PENDING
    ANALYZING
    MAPPING
    VALIDATING
    IMPORTING
    COMPLETED
    FAILED
    CANCELLED
}

type FileAnalysisResult {
    analysisId: ID!
    fileName: String!
    fileType: FileType!
    sheets: [SheetInfo!]!
    totalRows: Int!
    totalColumns: Int!
    sampleData: [[String!]!]!
    detectedStructure: DetectedStructure
    errors: [AnalysisError!]
}

type SheetInfo {
    name: String!
    index: Int!
    rowCount: Int!
    columnCount: Int!
    headers: [String!]!
    sampleRows: [[String!]!]!
}

type DetectedStructure {
    hasHeaders: Boolean!
    dataStartRow: Int!
    dataEndRow: Int!
    columnTypes: [ColumnType!]!
    suggestedDataType: ImportDataType
}

type ColumnType {
    columnIndex: Int!
    columnName: String!
    detectedType: DataType!
    confidence: Float!
    sampleValues: [String!]!
}

enum DataType {
    STRING
    NUMBER
    DATE
    BOOLEAN
    EMAIL
    URL
    COORDINATES
    UNKNOWN
}

type AnalysisError {
    code: String!
    message: String!
    row: Int
    column: Int
    severity: ErrorSeverity!
}

enum ErrorSeverity {
    INFO
    WARNING
    ERROR
    CRITICAL
}

input FieldMapping {
    sourceColumn: String!
    targetField: String!
    transformation: String
    required: Boolean!
    validationRules: [ValidationRule!]
}

input ValidationRule {
    type: ValidationRuleType!
    parameters: [String!]
    message: String
}

enum ValidationRuleType {
    REQUIRED
    MIN_LENGTH
    MAX_LENGTH
    PATTERN
    RANGE
    UNIQUE
    CUSTOM
}

type FieldMappingResult {
    mappingId: ID!
    analysisId: ID!
    targetType: ImportDataType!
    mappings: [FieldMappingInfo!]!
    validation: MappingValidation
}

type FieldMappingInfo {
    sourceColumn: String!
    targetField: String!
    transformation: String
    required: Boolean!
    validationRules: [ValidationRule!]
    sampleValue: String
    mappedValue: String
}

type MappingValidation {
    isValid: Boolean!
    errors: [MappingError!]
    warnings: [MappingWarning!]
}

type MappingError {
    field: String!
    message: String!
    code: String!
}

type MappingWarning {
    field: String!
    message: String!
    code: String!
}

input ValidationOptions {
    strictMode: Boolean
    skipEmptyRows: Boolean
    maxErrors: Int
    customValidators: [CustomValidator!]
}

input CustomValidator {
    field: String!
    rule: String!
    parameters: [String!]
}

type ValidationResult {
    validationId: ID!
    isValid: Boolean!
    totalRows: Int!
    validRows: Int!
    invalidRows: Int!
    errors: [ValidationError!]
    warnings: [ValidationWarning!]
    sampleErrors: [RowError!]
}

type ValidationError {
    code: String!
    message: String!
    count: Int!
    examples: [String!]!
}

type ValidationWarning {
    code: String!
    message: String!
    count: Int!
    examples: [String!]!
}

type RowError {
    rowNumber: Int!
    errors: [CellError!]
}

type CellError {
    column: String!
    value: String!
    error: String!
}

input ImportOptions {
    conflictResolution: ConflictResolution
    batchSize: Int
    notifyOnCompletion: Boolean
    email: String
}

enum ConflictResolution {
    SKIP
    UPDATE
    CREATE_NEW
    ASK_USER
}

type ImportResult {
    importId: ID!
    status: ImportStatusEnum!
    totalRows: Int!
    importedRows: Int!
    skippedRows: Int!
    failedRows: Int!
    estimatedTime: Int
    conflicts: [ImportConflict!]
}

type ImportConflict {
    rowNumber: Int!
    field: String!
    existingValue: String!
    newValue: String!
    resolution: ConflictResolution
}

type ImportStatus {
    importId: ID!
    status: ImportStatusEnum!
    progress: Int!
    currentStep: String!
    totalRows: Int!
    processedRows: Int!
    importedRows: Int!
    failedRows: Int!
    errors: [ImportError!]
    startedAt: DateTime!
    completedAt: DateTime
    estimatedCompletion: DateTime
}

type ImportError {
    rowNumber: Int!
    field: String!
    value: String!
    error: String!
    severity: ErrorSeverity!
}

type ImportHistoryResult {
    imports: [ImportHistoryItem!]!
    totalCount: Int!
    hasMore: Boolean!
}

type ImportHistoryItem {
    importId: ID!
    fileName: String!
    dataType: ImportDataType!
    status: ImportStatusEnum!
    totalRows: Int!
    importedRows: Int!
    failedRows: Int!
    startedAt: DateTime!
    completedAt: DateTime
    user: String!
}

type MappingTemplate {
    id: ID!
    name: String!
    description: String!
    dataType: ImportDataType!
    mappings: [FieldMapping!]!
    isDefault: Boolean!
    createdAt: DateTime!
}

type ImportStatistics {
    totalImports: Int!
    successfulImports: Int!
    failedImports: Int!
    totalRowsImported: Int!
    averageImportTime: Int!
    mostImportedType: ImportDataType!
    recentImports: [ImportHistoryItem!]!
}
```

#### REST API для импорта
```http
# Получение шаблона импорта
GET /api/import/templates/{dataType}
Authorization: Bearer {token}

# Загрузка файла для анализа (альтернатива GraphQL)
POST /api/import/analyze
Content-Type: multipart/form-data
Authorization: Bearer {token}

# Получение статуса импорта
GET /api/import/{importId}/status
Authorization: Bearer {token}

# Отмена импорта
DELETE /api/import/{importId}
Authorization: Bearer {token}

# Получение отчёта об ошибках
GET /api/import/{importId}/errors
Authorization: Bearer {token}

# Скачивание шаблона для заполнения
GET /api/import/templates/{dataType}/download
Authorization: Bearer {token}
```

### Приложение G: Детальная реализация компонентов импорта

#### FileImportController
```java
@RestController
@RequestMapping("/api/import")
@RequiredArgsConstructor
@Slf4j
public class FileImportController {
    
    private final FileImportService fileImportService;
    private final FileAnalyzerService fileAnalyzerService;
    private final DataValidatorService dataValidatorService;
    
    @PostMapping("/analyze")
    public ResponseEntity<FileAnalysisResult> analyzeFile(
            @RequestParam("file") MultipartFile file) {
        try {
            FileAnalysisResult result = fileAnalyzerService.analyzeFile(file);
            return ResponseEntity.ok(result);
        } catch (Exception e) {
            log.error("Error analyzing file: {}", file.getOriginalFilename(), e);
            return ResponseEntity.badRequest().build();
        }
    }
    
    @PostMapping("/validate")
    public ResponseEntity<ValidationResult> validateImport(
            @RequestBody ValidationRequest request) {
        try {
            ValidationResult result = dataValidatorService.validateImport(request);
            return ResponseEntity.ok(result);
        } catch (Exception e) {
            log.error("Error validating import", e);
            return ResponseEntity.badRequest().build();
        }
    }
    
    @PostMapping("/execute")
    public ResponseEntity<ImportResult> executeImport(
            @RequestBody ImportRequest request) {
        try {
            ImportResult result = fileImportService.executeImport(request);
            return ResponseEntity.ok(result);
        } catch (Exception e) {
            log.error("Error executing import", e);
            return ResponseEntity.badRequest().build();
        }
    }
    
    @GetMapping("/{importId}/status")
    public ResponseEntity<ImportStatus> getImportStatus(@PathVariable String importId) {
        try {
            ImportStatus status = fileImportService.getImportStatus(importId);
            return ResponseEntity.ok(status);
        } catch (ImportNotFoundException e) {
            return ResponseEntity.notFound().build();
        }
    }
    
    @DeleteMapping("/{importId}")
    public ResponseEntity<Void> cancelImport(@PathVariable String importId) {
        try {
            fileImportService.cancelImport(importId);
            return ResponseEntity.ok().build();
        } catch (ImportNotFoundException e) {
            return ResponseEntity.notFound().build();
        }
    }
    
    @GetMapping("/templates/{dataType}/download")
    public ResponseEntity<Resource> downloadTemplate(@PathVariable ImportDataType dataType) {
        try {
            Resource template = fileImportService.getTemplate(dataType);
            return ResponseEntity.ok()
                    .header(HttpHeaders.CONTENT_DISPOSITION, 
                            "attachment; filename=\"template-" + dataType + ".xlsx\"")
                    .body(template);
        } catch (Exception e) {
            log.error("Error downloading template for {}", dataType, e);
            return ResponseEntity.notFound().build();
        }
    }
}
```

### Приложение H: Vue.js компоненты для импорта данных

#### FileImport.vue
```vue
<template>
  <q-card class="file-import">
    <q-card-section>
      <h5>Импорт данных из файла</h5>
    </q-card-section>
    
    <q-card-section>
      <q-stepper v-model="step" ref="stepper" color="primary" animated>
        <!-- Шаг 1: Выбор файла -->
        <q-step :name="1" title="Выбор файла" icon="upload_file">
          <FileSelector @file-selected="onFileSelected" />
        </q-step>
        
        <!-- Шаг 2: Анализ структуры -->
        <q-step :name="2" title="Анализ структуры" icon="analytics">
          <StructureAnalyzer 
            v-if="fileAnalysis" 
            :analysis="fileAnalysis"
            @structure-confirmed="onStructureConfirmed" 
          />
        </q-step>
        
        <!-- Шаг 3: Сопоставление полей -->
        <q-step :name="3" title="Сопоставление полей" icon="settings">
          <FieldMapper 
            v-if="fileAnalysis && selectedDataType"
            :analysis="fileAnalysis"
            :data-type="selectedDataType"
            @mapping-completed="onMappingCompleted"
          />
        </q-step>
        
        <!-- Шаг 4: Валидация -->
        <q-step :name="4" title="Валидация данных" icon="verified">
          <DataValidator 
            v-if="fieldMapping"
            :analysis="fileAnalysis"
            :mapping="fieldMapping"
            @validation-completed="onValidationCompleted"
          />
        </q-step>
        
        <!-- Шаг 5: Импорт -->
        <q-step :name="5" title="Импорт данных" icon="cloud_upload">
          <ImportExecutor 
            v-if="validationResult"
            :analysis="fileAnalysis"
            :mapping="fieldMapping"
            :validation="validationResult"
            @import-completed="onImportCompleted"
          />
        </q-step>
      </q-stepper>
    </q-card-section>
    
    <!-- Результаты импорта -->
    <q-dialog v-model="showResults" persistent>
      <q-card style="min-width: 600px">
        <q-card-section>
          <h6>Результаты импорта</h6>
        </q-card-section>
        
        <q-card-section>
          <ImportResults :results="importResults" />
        </q-card-section>
        
        <q-card-actions align="right">
          <q-btn flat label="Закрыть" color="primary" v-close-popup @click="resetImport" />
        </q-card-actions>
      </q-card>
    </q-dialog>
  </q-card>
</template>

<script setup lang="ts">
import { ref, reactive } from 'vue'
import { useQuasar } from 'quasar'
import FileSelector from './FileSelector.vue'
import StructureAnalyzer from './StructureAnalyzer.vue'
import FieldMapper from './FieldMapper.vue'
import DataValidator from './DataValidator.vue'
import ImportExecutor from './ImportExecutor.vue'
import ImportResults from './ImportResults.vue'
import { analyzeFileMutation, mapFieldsMutation, validateImportMutation, executeImportMutation } from '@/queries/import'

const $q = useQuasar()

const step = ref(1)
const fileAnalysis = ref(null)
const selectedDataType = ref(null)
const fieldMapping = ref(null)
const validationResult = ref(null)
const importResults = ref(null)
const showResults = ref(false)

const onFileSelected = async (file: File) => {
  try {
    $q.loading.show({ message: 'Анализ файла...' })
    
    // Чтение файла как ArrayBuffer
    const arrayBuffer = await file.arrayBuffer()
    const base64Content = btoa(String.fromCharCode(...new Uint8Array(arrayBuffer)))
    
    const result = await analyzeFileMutation({
      fileContent: base64Content,
      fileName: file.name,
      fileType: detectFileType(file.name)
    })
    
    if (result.data?.analyzeFile) {
      fileAnalysis.value = result.data.analyzeFile
      selectedDataType.value = result.data.analyzeFile.detectedStructure?.suggestedDataType
      step.value = 2
    }
  } catch (error) {
    $q.notify({
      type: 'negative',
      message: 'Ошибка при анализе файла'
    })
  } finally {
    $q.loading.hide()
  }
}

const onStructureConfirmed = (dataType: string) => {
  selectedDataType.value = dataType
  step.value = 3
}

const onMappingCompleted = async (mapping: any) => {
  try {
    $q.loading.show({ message: 'Валидация данных...' })
    
    const result = await mapFieldsMutation({
      analysisId: fileAnalysis.value.analysisId,
      targetType: selectedDataType.value,
      fieldMappings: mapping
    })
    
    if (result.data?.mapFields) {
      fieldMapping.value = result.data.mapFields
      step.value = 4
    }
  } catch (error) {
    $q.notify({
      type: 'negative',
      message: 'Ошибка при сопоставлении полей'
    })
  } finally {
    $q.loading.hide()
  }
}

const onValidationCompleted = async (validation: any) => {
  try {
    $q.loading.show({ message: 'Проверка данных...' })
    
    const result = await validateImportMutation({
      analysisId: fileAnalysis.value.analysisId,
      mappingId: fieldMapping.value.mappingId,
      validationOptions: validation
    })
    
    if (result.data?.validateImport) {
      validationResult.value = result.data.validateImport
      step.value = 5
    }
  } catch (error) {
    $q.notify({
      type: 'negative',
      message: 'Ошибка при валидации данных'
    })
  } finally {
    $q.loading.hide()
  }
}

const onImportCompleted = async (importOptions: any) => {
  try {
    $q.loading.show({ message: 'Импорт данных...' })
    
    const result = await executeImportMutation({
      analysisId: fileAnalysis.value.analysisId,
      mappingId: fieldMapping.value.mappingId,
      importOptions
    })
    
    if (result.data?.executeImport) {
      importResults.value = result.data.executeImport
      showResults.value = true
    }
  } catch (error) {
    $q.notify({
      type: 'negative',
      message: 'Ошибка при импорте данных'
    })
  } finally {
    $q.loading.hide()
  }
}

const resetImport = () => {
  step.value = 1
  fileAnalysis.value = null
  selectedDataType.value = null
  fieldMapping.value = null
  validationResult.value = null
  importResults.value = null
  showResults.value = false
}

const detectFileType = (fileName: string): string => {
  const extension = fileName.split('.').pop()?.toLowerCase()
  switch (extension) {
    case 'xlsx': return 'EXCEL_XLSX'
    case 'xls': return 'EXCEL_XLS'
    case 'ods': return 'OPENOFFICE_ODS'
    case 'csv': return 'CSV'
    default: throw new Error('Неподдерживаемый формат файла')
  }
}
</script>
```

#### FileSelector.vue
```vue
<template>
  <div class="file-selector">
    <q-card class="upload-area" @click="selectFile" @drop="onDrop" @dragover.prevent>
      <q-card-section class="text-center">
        <q-icon name="cloud_upload" size="4rem" color="primary" />
        <h6 class="q-mt-md">Выберите файл для импорта</h6>
        <p class="text-grey-6">
          Поддерживаемые форматы: Excel (.xlsx, .xls), OpenOffice (.ods), CSV
        </p>
        <q-btn color="primary" label="Выбрать файл" @click.stop="selectFile" />
      </q-card-section>
    </q-card>
    
    <div v-if="selectedFile" class="q-mt-md">
      <q-card>
        <q-card-section>
          <div class="row items-center">
            <q-icon name="description" size="2rem" color="primary" />
            <div class="q-ml-md">
              <h6>{{ selectedFile.name }}</h6>
              <p class="text-grey-6">{{ formatFileSize(selectedFile.size) }}</p>
            </div>
            <q-space />
            <q-btn flat round icon="close" @click="clearFile" />
          </div>
        </q-card-section>
      </q-card>
    </div>
    
    <!-- Скрытый input для выбора файла -->
    <input
      ref="fileInput"
      type="file"
      accept=".xlsx,.xls,.ods,.csv"
      style="display: none"
      @change="onFileChange"
    />
  </div>
</template>

<script setup lang="ts">
import { ref } from 'vue'
import { useQuasar } from 'quasar'

const $q = useQuasar()
const emit = defineEmits(['file-selected'])

const selectedFile = ref<File | null>(null)
const fileInput = ref<HTMLInputElement>()

const selectFile = () => {
  fileInput.value?.click()
}

const onFileChange = (event: Event) => {
  const target = event.target as HTMLInputElement
  if (target.files && target.files.length > 0) {
    const file = target.files[0]
    validateAndSelectFile(file)
  }
}

const onDrop = (event: DragEvent) => {
  event.preventDefault()
  if (event.dataTransfer?.files && event.dataTransfer.files.length > 0) {
    const file = event.dataTransfer.files[0]
    validateAndSelectFile(file)
  }
}

const validateAndSelectFile = (file: File) => {
  // Проверка размера файла (максимум 100MB)
  if (file.size > 100 * 1024 * 1024) {
    $q.notify({
      type: 'negative',
      message: 'Файл слишком большой. Максимальный размер: 100MB'
    })
    return
  }
  
  // Проверка типа файла
  const validExtensions = ['.xlsx', '.xls', '.ods', '.csv']
  const fileExtension = '.' + file.name.split('.').pop()?.toLowerCase()
  
  if (!validExtensions.includes(fileExtension)) {
    $q.notify({
      type: 'negative',
      message: 'Неподдерживаемый формат файла'
    })
    return
  }
  
  selectedFile.value = file
  emit('file-selected', file)
}

const clearFile = () => {
  selectedFile.value = null
  if (fileInput.value) {
    fileInput.value.value = ''
  }
}

const formatFileSize = (bytes: number): string => {
  if (bytes === 0) return '0 Bytes'
  const k = 1024
  const sizes = ['Bytes', 'KB', 'MB', 'GB']
  const i = Math.floor(Math.log(bytes) / Math.log(k))
  return parseFloat((bytes / Math.pow(k, i)).toFixed(2)) + ' ' + sizes[i]
}
</script>

<style scoped>
.upload-area {
  border: 2px dashed #ccc;
  cursor: pointer;
  transition: border-color 0.3s;
}

.upload-area:hover {
  border-color: #1976d2;
}
</style>
```

### Приложение F: Maven конфигурация

#### Основные координаты артефакта
```xml
<groupId>io.github.bondalen</groupId>
<artifactId>vuege</artifactId>
<version>0.1.0</version>
<packaging>jar</packaging>
<name>Vuege</name>
<description>Система учета организационных единиц и исторических данных</description>
```

#### Родительский POM
```xml
<parent>
    <groupId>org.springframework.boot</groupId>
    <artifactId>spring-boot-starter-parent</artifactId>
    <version>3.4.5</version>
    <relativePath/>
</parent>
```

#### Свойства проекта
```xml
<properties>
    <java.version>21</java.version>
    <maven.compiler.source>21</maven.compiler.source>
    <maven.compiler.target>21</maven.compiler.target>
    <project.build.sourceEncoding>UTF-8</project.build.sourceEncoding>
    <project.reporting.outputEncoding>UTF-8</project.reporting.outputEncoding>
</properties>
```

#### Основные зависимости
```xml
<dependencies>
    <!-- Spring Boot Starters -->
    <dependency>
        <groupId>org.springframework.boot</groupId>
        <artifactId>spring-boot-starter-web</artifactId>
    </dependency>
    <dependency>
        <groupId>org.springframework.boot</groupId>
        <artifactId>spring-boot-starter-graphql</artifactId>
    </dependency>
    <dependency>
        <groupId>org.springframework.boot</groupId>
        <artifactId>spring-boot-starter-data-r2dbc</artifactId>
    </dependency>
    <dependency>
        <groupId>org.springframework.boot</groupId>
        <artifactId>spring-boot-starter-validation</artifactId>
    </dependency>
    <dependency>
        <groupId>org.springframework.boot</groupId>
        <artifactId>spring-boot-starter-actuator</artifactId>
    </dependency>
    
    <!-- Database -->
    <dependency>
        <groupId>org.postgresql</groupId>
        <artifactId>r2dbc-postgresql</artifactId>
    </dependency>
    <dependency>
        <groupId>org.postgresql</groupId>
        <artifactId>postgresql</artifactId>
    </dependency>
    
    <!-- Database Migration -->
    <dependency>
        <groupId>org.liquibase</groupId>
        <artifactId>liquibase-core</artifactId>
    </dependency>
    
    <!-- Lombok -->
    <dependency>
        <groupId>org.projectlombok</groupId>
        <artifactId>lombok</artifactId>
        <optional>true</optional>
    </dependency>
    
    <!-- Test Dependencies -->
    <dependency>
        <groupId>org.springframework.boot</groupId>
        <artifactId>spring-boot-starter-test</artifactId>
        <scope>test</scope>
    </dependency>
    <dependency>
        <groupId>io.projectreactor</groupId>
        <artifactId>reactor-test</artifactId>
        <scope>test</scope>
    </dependency>
</dependencies>
```

#### Полный pom.xml
```xml
<?xml version="1.0" encoding="UTF-8"?>
<project xmlns="http://maven.apache.org/POM/4.0.0"
         xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
         xsi:schemaLocation="http://maven.apache.org/POM/4.0.0 
         http://maven.apache.org/xsd/maven-4.0.0.xsd">
    <modelVersion>4.0.0</modelVersion>

    <groupId>io.github.bondalen</groupId>
    <artifactId>vuege</artifactId>
    <version>0.1.0</version>
    <packaging>jar</packaging>
    <name>Vuege</name>
    <description>Система учета организационных единиц и исторических данных</description>

    <parent>
        <groupId>org.springframework.boot</groupId>
        <artifactId>spring-boot-starter-parent</artifactId>
        <version>3.4.5</version>
        <relativePath/>
    </parent>

    <properties>
        <java.version>21</java.version>
        <maven.compiler.source>21</maven.compiler.source>
        <maven.compiler.target>21</maven.compiler.target>
        <project.build.sourceEncoding>UTF-8</project.build.sourceEncoding>
        <project.reporting.outputEncoding>UTF-8</project.reporting.outputEncoding>
    </properties>

    <dependencies>
        <!-- Spring Boot Starters -->
        <dependency>
            <groupId>org.springframework.boot</groupId>
            <artifactId>spring-boot-starter-web</artifactId>
        </dependency>
        <dependency>
            <groupId>org.springframework.boot</groupId>
            <artifactId>spring-boot-starter-graphql</artifactId>
        </dependency>
        <dependency>
            <groupId>org.springframework.boot</groupId>
            <artifactId>spring-boot-starter-data-r2dbc</artifactId>
        </dependency>
        <dependency>
            <groupId>org.springframework.boot</groupId>
            <artifactId>spring-boot-starter-validation</artifactId>
        </dependency>
        <dependency>
            <groupId>org.springframework.boot</groupId>
            <artifactId>spring-boot-starter-actuator</artifactId>
        </dependency>
        <dependency>
            <groupId>org.springframework.boot</groupId>
            <artifactId>spring-boot-starter-mail</artifactId>
        </dependency>
        <dependency>
            <groupId>org.springframework.boot</groupId>
            <artifactId>spring-boot-starter-thymeleaf</artifactId>
        </dependency>
        
        <!-- Database -->
        <dependency>
            <groupId>org.postgresql</groupId>
            <artifactId>r2dbc-postgresql</artifactId>
        </dependency>
        <dependency>
            <groupId>org.postgresql</groupId>
            <artifactId>postgresql</artifactId>
        </dependency>
        
        <!-- Database Migration -->
        <dependency>
            <groupId>org.liquibase</groupId>
            <artifactId>liquibase-core</artifactId>
        </dependency>
        
        <!-- Lombok -->
        <dependency>
            <groupId>org.projectlombok</groupId>
            <artifactId>lombok</artifactId>
            <optional>true</optional>
        </dependency>
        
        <!-- Report Generation -->
        <dependency>
            <groupId>org.apache.pdfbox</groupId>
            <artifactId>pdfbox</artifactId>
            <version>2.0.30</version>
        </dependency>
        <dependency>
            <groupId>org.xhtmlrenderer</groupId>
            <artifactId>flying-saucer-pdf-openpdf</artifactId>
            <version>9.1.22</version>
        </dependency>
        <dependency>
            <groupId>org.apache.poi</groupId>
            <artifactId>poi</artifactId>
            <version>5.2.3</version>
        </dependency>
        <dependency>
            <groupId>org.apache.poi</groupId>
            <artifactId>poi-ooxml</artifactId>
            <version>5.2.3</version>
        </dependency>
        <dependency>
            <groupId>com.opencsv</groupId>
            <artifactId>opencsv</artifactId>
            <version>5.7.1</version>
        </dependency>
        <dependency>
            <groupId>com.fasterxml.jackson.dataformat</groupId>
            <artifactId>jackson-dataformat-xml</artifactId>
            <version>2.15.0</version>
        </dependency>
        
        <!-- Test Dependencies -->
        <dependency>
            <groupId>org.springframework.boot</groupId>
            <artifactId>spring-boot-starter-test</artifactId>
            <scope>test</scope>
        </dependency>
        <dependency>
            <groupId>io.projectreactor</groupId>
            <artifactId>reactor-test</artifactId>
            <scope>test</scope>
        </dependency>
    </dependencies>

    <build>
        <plugins>
            <plugin>
                <groupId>org.springframework.boot</groupId>
                <artifactId>spring-boot-maven-plugin</artifactId>
                <configuration>
                    <excludes>
                        <exclude>
                            <groupId>org.projectlombok</groupId>
                            <artifactId>lombok</artifactId>
                        </exclude>
                    </excludes>
                </configuration>
            </plugin>
        </plugins>
    </build>
</project>
```
```