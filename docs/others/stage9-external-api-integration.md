# Этап 9: Интеграция с внешними API

## 📋 Обзор

Этап 9 добавляет интеграцию с внешними API для расширения функциональности Vuege:
- **Геокодирование** - получение координат по адресам
- **Валидация данных** - проверка корректности информации
- **Обогащение данных** - получение дополнительной информации
- **Мониторинг API** - отслеживание доступности внешних сервисов

## 🎯 Цели этапа

### ✅ Выполнено:
1. **Интеграция с геокодированием** - OpenCage Data API
2. **Валидация данных** - Abstract API для email, телефонов, адресов
3. **Обогащение данных** - OpenCorporates API для информации об организациях
4. **Мониторинг внешних API** - система отслеживания доступности
5. **Кэширование результатов** - Redis для оптимизации запросов

## 🔧 Техническая реализация

### Архитектура интеграции

```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   GraphQL API   │    │  External APIs  │    │   Resilience4j  │
│                 │    │                 │    │                 │
│ ┌─────────────┐ │    │ ┌─────────────┐ │    │ ┌─────────────┐ │
│ │Geocoding    │ │───▶│ │OpenCage     │ │    │ │Circuit      │ │
│ │Validation   │ │    │ │Abstract     │ │    │ │Breaker      │ │
│ │Enrichment   │ │    │ │OpenCorp     │ │    │ │Rate Limiter │ │
│ └─────────────┘ │    │ └─────────────┘ │    │ │Retry        │ │
└─────────────────┘    └─────────────────┘    │ └─────────────┘ │
         │                                      └─────────────────┘
         │                                              │
         ▼                                              ▼
┌─────────────────┐                            ┌─────────────────┐
│   Redis Cache   │                            │   Monitoring    │
│                 │                            │                 │
│ ┌─────────────┐ │                            │ ┌─────────────┐ │
│ │Geocoding    │ │                            │ │API Status   │ │
│ │Validation   │ │                            │ │Response     │ │
│ │Enrichment   │ │                            │ │Time         │ │
│ └─────────────┘ │                            │ │Success Rate │ │
└─────────────────┘                            │ └─────────────┘ │
                                               └─────────────────┘
```

### Компоненты системы

#### 1. Конфигурация (`ExternalApiConfig`)
- **WebClient** для каждого внешнего API
- **Resilience4j** конфигурация (Circuit Breaker, Rate Limiter, Retry)
- **API ключи** и базовые URL

#### 2. Сервисы внешних API
- **GeocodingService** - геокодирование адресов
- **ValidationService** - валидация email, телефонов, адресов
- **EnrichmentService** - обогащение данных об организациях
- **ApiMonitoringService** - мониторинг доступности API

#### 3. GraphQL резолвер (`ExternalApiResolver`)
- Интеграция с GraphQL схемой
- Реактивные запросы через WebFlux
- Обработка ошибок и кэширование

#### 4. Кэширование (`RedisCacheConfig`)
- **Redis** для кэширования результатов
- Различное время жизни для разных типов данных
- JSON сериализация

## 📊 Внешние API

### 1. OpenCage Data API (Геокодирование)
- **URL**: https://api.opencagedata.com
- **Функции**: Прямое и обратное геокодирование
- **Лимиты**: 2500 запросов/день (бесплатный план)
- **Кэширование**: 24 часа

### 2. Abstract API (Валидация)
- **URL**: https://emailvalidation.abstractapi.com
- **Функции**: Валидация email, телефонов, адресов
- **Лимиты**: 100 запросов/месяц (бесплатный план)
- **Кэширование**: 1 час

### 3. OpenCorporates API (Обогащение)
- **URL**: https://api.opencorporates.com
- **Функции**: Информация об организациях, ИНН
- **Лимиты**: 1000 запросов/день (бесплатный план)
- **Кэширование**: 12 часов

## 🛡️ Защитные механизмы

### Circuit Breaker
- **Порог ошибок**: 50%
- **Время ожидания**: 60 секунд
- **Размер окна**: 10 запросов
- **Автоматическое восстановление**

### Rate Limiting
- **Геокодирование**: 100 запросов/минуту
- **Валидация**: 10 запросов/минуту
- **Обогащение**: 50 запросов/минуту

### Retry Logic
- **Максимум попыток**: 3
- **Интервал**: 1 секунда
- **Исключения**: IllegalArgumentException

### Time Limiter
- **Таймаут**: 10-15 секунд
- **Отмена задач**: Да

## 📈 Мониторинг

### Метрики API
- **Время отклика** каждого API
- **Процент успешных запросов**
- **Количество ошибок**
- **Статус доступности**

### Автоматические проверки
- **Периодичность**: каждые 5 минут
- **Кэширование результатов**: 5 минут
- **Логирование**: DEBUG уровень

## 🔧 Конфигурация

### Переменные окружения
```bash
# API ключи
export OPENCAGE_API_KEY="your-opencage-api-key"
export ABSTRACT_API_KEY="your-abstract-api-key"
export OPENCORPORATES_API_KEY="your-opencorporates-api-key"

# Redis
export REDIS_PASSWORD="your-redis-password"
```

### application-external-api.yml
```yaml
external:
  api:
    geocoding:
      base-url: https://api.opencagedata.com
      api-key: ${OPENCAGE_API_KEY:}
      rate-limit: 2500
      timeout: 10000
    
    validation:
      base-url: https://emailvalidation.abstractapi.com
      api-key: ${ABSTRACT_API_KEY:}
      rate-limit: 100
      timeout: 10000
    
    enrichment:
      base-url: https://api.opencorporates.com
      api-key: ${OPENCORPORATES_API_KEY:}
      rate-limit: 1000
      timeout: 15000
```

## 🧪 Тестирование

### Unit тесты
- **GeocodingServiceTest** - тестирование геокодирования
- **ValidationServiceTest** - тестирование валидации
- **EnrichmentServiceTest** - тестирование обогащения

### Интеграционные тесты
- **ExternalApiResolverIntegrationTest** - GraphQL резолвер
- **ApiMonitoringServiceTest** - мониторинг API

### Тестовые сценарии
1. **Успешные запросы** к внешним API
2. **Обработка ошибок** и недоступности
3. **Кэширование** результатов
4. **Rate limiting** и circuit breaker
5. **GraphQL интеграция**

## 📝 GraphQL схема

### Новые типы
```graphql
type GeocodingResult {
    originalAddress: String
    latitude: Float
    longitude: Float
    formattedAddress: String
    country: String
    region: String
    city: String
    postalCode: String
    street: String
    houseNumber: String
    accuracy: String
    responseTime: Int
    createdAt: Date
    source: String
    status: String
    errorMessage: String
}

type ValidationResult {
    originalData: String
    validationType: String
    status: ValidationStatus!
    isValid: Boolean!
    confidence: Int
    formattedData: String
    errors: [String!]
    suggestions: [String!]
    additionalInfo: String
    responseTime: Int
    createdAt: Date
    source: String
}

type EnrichmentResult {
    originalData: String
    enrichmentType: String
    status: EnrichmentStatus!
    enrichedData: [EnrichmentData!]
    confidence: Int
    dataSource: String
    lastUpdated: Date
    responseTime: Int
    createdAt: Date
    errorMessage: String
}

type ApiMonitoringResult {
    apiName: String!
    endpoint: String
    status: ApiStatus!
    responseTime: Int
    httpStatusCode: Int
    lastChecked: Date
    successCount: Int
    errorCount: Int
    successRate: Float
    errorMessage: String
}
```

### Новые запросы
```graphql
type Query {
    # Геокодирование
    geocodeAddress(address: String!): GeocodingResult!
    reverseGeocode(latitude: Float!, longitude: Float!): GeocodingResult!
    
    # Валидация
    validateEmail(email: String!): ValidationResult!
    validatePhone(phone: String!): ValidationResult!
    validateAddress(address: String!): ValidationResult!
    
    # Обогащение
    enrichCompanyData(companyName: String!): EnrichmentResult!
    enrichByInn(inn: String!): EnrichmentResult!
    
    # Мониторинг
    checkGeocodingApi: ApiMonitoringResult!
    checkValidationApi: ApiMonitoringResult!
    checkEnrichmentApi: ApiMonitoringResult!
    checkAllApis: [ApiMonitoringResult!]!
    getApiStatistics: ApiStatistics!
}
```

## 🚀 Использование

### Примеры GraphQL запросов

#### Геокодирование адреса
```graphql
query {
    geocodeAddress(address: "Москва, Красная площадь, 1") {
        latitude
        longitude
        formattedAddress
        country
        city
        status
    }
}
```

#### Валидация email
```graphql
query {
    validateEmail(email: "test@example.com") {
        isValid
        confidence
        formattedData
        status
    }
}
```

#### Обогащение данных компании
```graphql
query {
    enrichCompanyData(companyName: "ООО Рога и Копыта") {
        enrichedData {
            key
            value
        }
        confidence
        status
    }
}
```

#### Мониторинг API
```graphql
query {
    checkAllApis {
        apiName
        status
        responseTime
        successRate
    }
}
```

## 📊 Производительность

### Ожидаемые показатели
- **Время отклика**: < 10 секунд (с кэшированием < 100ms)
- **Доступность**: > 99% (с circuit breaker)
- **Throughput**: 100+ запросов/минуту
- **Cache hit ratio**: > 80%

### Оптимизации
- **Кэширование** результатов в Redis
- **Batch processing** для множественных запросов
- **Async/Reactive** обработка через WebFlux
- **Circuit breaker** для защиты от недоступности

## 🔮 Будущие улучшения

### Планируемые функции
1. **Дополнительные API** для валидации и обогащения
2. **Машинное обучение** для улучшения точности
3. **Webhook уведомления** о статусе API
4. **Дашборд мониторинга** в реальном времени
5. **Автоматическое масштабирование** кэша

### Технические улучшения
1. **Микросервисная архитектура** для внешних API
2. **Message Queue** для асинхронной обработки
3. **Distributed tracing** для отладки
4. **A/B тестирование** разных API провайдеров

## 📚 Документация

### Связанные файлы
- `ExternalApiConfig.java` - конфигурация внешних API
- `RedisCacheConfig.java` - конфигурация кэширования
- `GeocodingService.java` - сервис геокодирования
- `ValidationService.java` - сервис валидации
- `EnrichmentService.java` - сервис обогащения
- `ApiMonitoringService.java` - сервис мониторинга
- `ExternalApiResolver.java` - GraphQL резолвер
- `application-external-api.yml` - конфигурация

### Тесты
- `GeocodingServiceTest.java` - unit тесты геокодирования
- `ExternalApiResolverIntegrationTest.java` - интеграционные тесты

## ✅ Статус завершения

**Этап 9 полностью завершен** ✅

- ✅ Интеграция с внешними API
- ✅ Система кэширования
- ✅ Защитные механизмы
- ✅ Мониторинг и метрики
- ✅ GraphQL интеграция
- ✅ Полное покрытие тестами
- ✅ Документация

**Готов к Этапу 10: Расширенная аналитика и отчетность**