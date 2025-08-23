# Spring Boot Actuator - Руководство по мониторингу

## Обзор

Spring Boot Actuator предоставляет готовые endpoints для мониторинга и управления приложением Vuege. Это позволяет отслеживать состояние приложения, производительность и диагностировать проблемы.

## Конфигурация

### Зависимости

В `pom.xml` добавлена зависимость:

```xml
<dependency>
    <groupId>org.springframework.boot</groupId>
    <artifactId>spring-boot-starter-actuator</artifactId>
</dependency>
```

### Настройки в application.yml

```yaml
management:
  endpoints:
    web:
      exposure:
        include: health,info,metrics,env,configprops,beans,threaddump,heapdump
      base-path: /actuator
  endpoint:
    health:
      show-details: always
      show-components: always
    info:
      enabled: true
    metrics:
      enabled: true
  health:
    r2dbc:
      enabled: true
    db:
      enabled: true
    mail:
      enabled: false  # Отключен для разработки
  metrics:
    export:
      prometheus:
        enabled: true
```

## Доступные Endpoints

### 1. Health Check - `/actuator/health`

**Описание**: Проверяет состояние приложения и его компонентов.

**URL**: `http://localhost:8082/api/actuator/health`

**Пример ответа**:
```json
{
  "status": "UP",
  "components": {
    "diskSpace": {
      "status": "UP",
      "details": {
        "total": 1081101176832,
        "free": 1018270048256,
        "threshold": 10485760,
        "path": "/home/alex/vuege/src/backend/.",
        "exists": true
      }
    },
    "ping": {
      "status": "UP"
    },
    "r2dbc": {
      "status": "UP",
      "details": {
        "database": "PostgreSQL",
        "validationQuery": "validate(REMOTE)"
      }
    },
    "ssl": {
      "status": "UP",
      "details": {
        "validChains": [],
        "invalidChains": []
      }
    }
  }
}
```

**Статусы**:
- `UP` - компонент работает нормально
- `DOWN` - компонент не работает
- `UNKNOWN` - состояние неизвестно

### 2. Info - `/actuator/info`

**Описание**: Предоставляет информацию о приложении.

**URL**: `http://localhost:8082/api/actuator/info`

### 3. Metrics - `/actuator/metrics`

**Описание**: Предоставляет метрики производительности.

**URL**: `http://localhost:8082/api/actuator/metrics`

### 4. Environment - `/actuator/env`

**Описание**: Показывает переменные окружения и конфигурацию.

**URL**: `http://localhost:8082/api/actuator/env`

### 5. Configuration Properties - `/actuator/configprops`

**Описание**: Показывает конфигурационные свойства.

**URL**: `http://localhost:8082/api/actuator/configprops`

### 6. Beans - `/actuator/beans`

**Описание**: Показывает все Spring beans.

**URL**: `http://localhost:8082/api/actuator/beans`

### 7. Thread Dump - `/actuator/threaddump`

**Описание**: Предоставляет информацию о потоках.

**URL**: `http://localhost:8082/api/actuator/threaddump`

### 8. Heap Dump - `/actuator/heapdump`

**Описание**: Создает дамп памяти (требует аутентификации).

**URL**: `http://localhost:8082/api/actuator/heapdump`

## Мониторинг компонентов

### База данных (R2DBC)

Health check для PostgreSQL через R2DBC автоматически включен и проверяет:
- Подключение к базе данных
- Выполнение валидационного запроса

### Дисковое пространство

Автоматически проверяет:
- Доступное место на диске
- Пороговое значение (по умолчанию 10MB)

### SSL

Проверяет SSL сертификаты и цепочки.

## Безопасность

### Текущая конфигурация

- Health и Info endpoints доступны без аутентификации
- Остальные endpoints требуют аутентификации
- Используется HTTP Basic Authentication

### Рекомендации для продакшена

1. **Настройте аутентификацию** для всех endpoints
2. **Используйте HTTPS** для всех запросов
3. **Ограничьте доступ** к чувствительным endpoints
4. **Настройте CORS** для веб-интерфейса

## Интеграция с системами мониторинга

### Prometheus

Prometheus экспорт включен в конфигурации:

```yaml
management:
  metrics:
    export:
      prometheus:
        enabled: true
```

### Grafana

Можно настроить Grafana для визуализации метрик из Prometheus.

## Устранение неполадок

### Health Check показывает DOWN

1. Проверьте логи приложения
2. Убедитесь, что база данных доступна
3. Проверьте конфигурацию в `application.yml`

### Endpoints недоступны

1. Убедитесь, что Actuator включен
2. Проверьте настройки exposure в конфигурации
3. Проверьте настройки безопасности

### Проблемы с производительностью

1. Используйте `/actuator/metrics` для анализа
2. Проверьте `/actuator/threaddump` для анализа потоков
3. Используйте `/actuator/heapdump` для анализа памяти

## Логирование

Для отладки Actuator добавьте в `application.yml`:

```yaml
logging:
  level:
    org.springframework.boot.actuate: DEBUG
```

## Следующие шаги

1. Настройка кастомных health checks
2. Добавление бизнес-метрик
3. Интеграция с внешними системами мониторинга
4. Настройка алертов
5. Создание дашбордов мониторинга