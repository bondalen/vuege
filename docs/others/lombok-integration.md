# Интеграция Lombok в проект Vuege

## Обзор

Lombok интегрирован в проект Vuege для минимизации boilerplate кода в Java-классах, что повышает читаемость и снижает вероятность ошибок.

## Зависимости

### Maven (pom.xml)
```xml
<dependency>
    <groupId>org.projectlombok</groupId>
    <artifactId>lombok</artifactId>
    <version>1.18.34</version>
    <scope>provided</scope>
</dependency>
```

### Gradle (build.gradle)
```gradle
dependencies {
    compileOnly 'org.projectlombok:lombok:1.18.34'
    annotationProcessor 'org.projectlombok:lombok:1.18.34'
}
```

## Основные аннотации

### Для моделей данных
```java
@Data                    // Геттеры, сеттеры, toString, equals, hashCode
@Builder                 // Паттерн Builder
@NoArgsConstructor      // Конструктор без параметров
@AllArgsConstructor     // Конструктор со всеми параметрами
@RequiredArgsConstructor // Конструктор с обязательными параметрами
```

### Для сервисов и контроллеров
```java
@Slf4j                  // Автоматическое логирование
@RequiredArgsConstructor // Внедрение зависимостей через конструктор
```

### Для репозиториев
```java
@Repository             // Spring Repository
@RequiredArgsConstructor // Внедрение зависимостей
```

## Примеры использования

### Модель данных
```java
/**
 * @file: OrganizationalUnit.java
 * @description: Модель организационной единицы
 * @lombok: @Data, @Builder, @NoArgsConstructor, @AllArgsConstructor
 * @created: 2024-12-19
 */
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

### Сервис
```java
/**
 * @file: OrganizationalUnitService.java
 * @description: Сервис для работы с организационными единицами
 * @lombok: @Slf4j, @RequiredArgsConstructor
 * @created: 2024-12-19
 */
@Slf4j
@RequiredArgsConstructor
@Service
public class OrganizationalUnitService {
    private final OrganizationalUnitRepository repository;
    private final GISService gisService;
    
    public Mono<OrganizationalUnit> createUnit(OrganizationalUnit unit) {
        log.info("Creating organizational unit: {}", unit.getName());
        return repository.save(unit);
    }
}
```

### Контроллер
```java
/**
 * @file: GraphQLController.java
 * @description: GraphQL контроллер
 * @lombok: @Slf4j, @RequiredArgsConstructor
 * @created: 2024-12-19
 */
@Slf4j
@RequiredArgsConstructor
@Controller
public class GraphQLController {
    private final OrganizationalUnitService unitService;
    private final PositionService positionService;
    
    @QueryMapping
    public Flux<OrganizationalUnit> organizations() {
        log.debug("Fetching all organizations");
        return unitService.findAll();
    }
}
```

## Правила использования

### Модели данных
- ✅ Используем `@Data`, `@Builder`, `@NoArgsConstructor`, `@AllArgsConstructor`
- ✅ Для сложных моделей добавляем `@ToString(exclude = "sensitiveField")`
- ✅ Для коллекций используем `@EqualsAndHashCode(exclude = "id")`

### Сервисы
- ✅ Используем `@Slf4j`, `@RequiredArgsConstructor`
- ✅ Для сложной логики избегаем избыточного использования Lombok

### Контроллеры
- ✅ Используем `@Slf4j`, `@RequiredArgsConstructor`
- ✅ Для GraphQL резолверов добавляем `@Component`

### Репозитории
- ✅ Используем `@Repository`, `@RequiredArgsConstructor`
- ✅ Для кастомных запросов избегаем Lombok

## Настройка IDE

### IntelliJ IDEA
1. Установить плагин "Lombok"
2. Включить обработку аннотаций: Settings → Build, Execution, Deployment → Compiler → Annotation Processors → Enable annotation processing
3. Добавить lombok.jar в classpath

### Eclipse
1. Установить lombok.jar в Eclipse
2. Перезапустить Eclipse
3. Проверить, что аннотации обрабатываются

### VS Code
1. Установить расширение "Lombok Annotations Support"
2. Настроить Java Extension Pack
3. Убедиться, что проект использует правильную версию Java

## Преимущества использования

1. **Меньше кода**: Автоматическая генерация геттеров, сеттеров, конструкторов
2. **Меньше ошибок**: Снижение вероятности ошибок в boilerplate коде
3. **Лучшая читаемость**: Фокус на бизнес-логике, а не на технических деталях
4. **Стандартизация**: Единый подход к созданию моделей
5. **Производительность**: Меньше кода для компиляции

## Ограничения

1. **Зависимость от библиотеки**: Проект зависит от Lombok
2. **Сложность отладки**: Генерированный код может быть сложнее для отладки
3. **IDE поддержка**: Требует настройки IDE
4. **Обучение команды**: Команда должна знать правила использования

## Миграция существующего кода

### Пошаговый план
1. Добавить зависимость Lombok
2. Настроить IDE
3. Постепенно мигрировать модели данных
4. Мигрировать сервисы и контроллеры
5. Обновить тесты
6. Провести code review

### Пример миграции
```java
// До
public class OrganizationalUnit {
    private String id;
    private String name;
    
    public OrganizationalUnit() {}
    
    public OrganizationalUnit(String id, String name) {
        this.id = id;
        this.name = name;
    }
    
    public String getId() { return id; }
    public void setId(String id) { this.id = id; }
    public String getName() { return name; }
    public void setName(String name) { this.name = name; }
    
    @Override
    public String toString() {
        return "OrganizationalUnit{id='" + id + "', name='" + name + "'}";
    }
}

// После
@Data
@Builder
@NoArgsConstructor
@AllArgsConstructor
public class OrganizationalUnit {
    private String id;
    private String name;
}
```

## Заключение

Lombok значительно упрощает разработку Java-кода в проекте Vuege, позволяя сосредоточиться на бизнес-логике и архитектуре, а не на технических деталях. Правильное использование аннотаций обеспечивает читаемость и поддерживаемость кода.
