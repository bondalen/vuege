# Руководство по настройке Spring Boot проекта Vuege

## Обзор

Данный документ содержит полную информацию, необходимую для создания и настройки Spring Boot проекта Vuege с использованием определенных Maven координат и технологического стека.

## Maven координаты артефакта

```xml
<groupId>io.github.bondalen</groupId>
<artifactId>vuege</artifactId>
<version>0.1.0</version>
<packaging>jar</packaging>
<name>Vuege</name>
<description>Система учета организационных единиц и исторических данных</description>
```

## Полный pom.xml

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

## Структура папок

```
backend/
├── src/
│   ├── main/
│   │   ├── java/
│   │   │   └── io/github/bondalen/vuege/
│   │   │       ├── VuegeApplication.java
│   │   │       ├── config/
│   │   │       │   ├── AsyncConfig.java
│   │   │       │   ├── EmailConfig.java
│   │   │       │   ├── GraphQLConfig.java
│   │   │       │   ├── R2dbcConfig.java
│   │   │       │   └── ImportConfig.java
│   │   │       ├── model/
│   │   │       │   ├── OrganizationalUnit.java
│   │   │       │   ├── Position.java
│   │   │       │   ├── Person.java
│   │   │       │   ├── PersonPosition.java
│   │   │       │   ├── HistoricalPeriod.java
│   │   │       │   ├── GeoPoint.java
│   │   │       │   ├── ReportStatus.java
│   │   │       │   ├── ReportRequest.java
│   │   │       │   ├── EmailReportRequest.java
│   │   │       │   ├── FileAnalysisResult.java
│   │   │       │   ├── ImportStatus.java
│   │   │       │   ├── ImportRequest.java
│   │   │       │   ├── ValidationRequest.java
│   │   │       │   └── FieldMapping.java
│   │   │       ├── repository/
│   │   │       │   ├── OrganizationalUnitRepository.java
│   │   │       │   ├── PositionRepository.java
│   │   │       │   ├── PersonRepository.java
│   │   │       │   ├── PersonPositionRepository.java
│   │   │       │   ├── ReportRepository.java
│   │   │       │   └── ImportRepository.java
│   │   │       ├── service/
│   │   │       │   ├── OrganizationalUnitService.java
│   │   │       │   ├── PositionService.java
│   │   │       │   ├── PersonService.java
│   │   │       │   ├── GISService.java
│   │   │       │   ├── ReportService.java
│   │   │       │   ├── ReportGeneratorService.java
│   │   │       │   ├── EmailService.java
│   │   │       │   ├── TemplateService.java
│   │   │       │   ├── FileStorageService.java
│   │   │       │   ├── FileImportService.java
│   │   │       │   ├── FileAnalyzerService.java
│   │   │       │   ├── DataValidatorService.java
│   │   │       │   ├── ImportProcessorService.java
│   │   │       │   ├── FieldMapperService.java
│   │   │       │   └── ReportDataService.java
│   │   │       ├── async/
│   │   │       │   ├── AsyncReportProcessor.java
│   │   │       │   └── AsyncImportProcessor.java
│   │   │       ├── graphql/
│   │   │       │   ├── resolver/
│   │   │       │   │   ├── OrganizationalUnitResolver.java
│   │   │       │   │   ├── PositionResolver.java
│   │   │       │   │   ├── PersonResolver.java
│   │   │       │   │   ├── ReportResolver.java
│   │   │       │   │   └── ImportResolver.java
│   │   │       │   └── scalar/
│   │   │       │       ├── DateScalar.java
│   │   │       │       └── GeoPointScalar.java
│   │   │       ├── exception/
│   │   │       │   ├── VuegeException.java
│   │   │       │   ├── GlobalExceptionHandler.java
│   │   │       │   ├── ReportNotFoundException.java
│   │   │       │   ├── ReportNotReadyException.java
│   │   │       │   ├── PDFGenerationException.java
│   │   │       │   ├── ImportNotFoundException.java
│   │   │       │   ├── FileAnalysisException.java
│   │   │       │   ├── ValidationException.java
│   │   │       │   ├── UnsupportedFileTypeException.java
│   │   │       │   └── TemplateNotFoundException.java
│   │   │       └── util/
│   │   │           ├── DateUtils.java
│   │   │           ├── GeoUtils.java
│   │   │           ├── ValidationUtils.java
│   │   │           ├── ReportUtils.java
│   │   │           └── FileUtils.java
│   │   └── resources/
│   │       ├── application.yml
│   │       ├── application-dev.yml
│   │       ├── application-prod.yml
│   │       ├── graphql/
│   │       │   ├── schema.graphqls
│   │       │   └── queries/
│   │       ├── db/migration/
│   │       │   ├── db.changelog-master.yaml
│   │       │   ├── 001-initial-schema.yaml
│   │       │   ├── 002-organizational-units.yaml
│   │       │   ├── 003-positions.yaml
│   │       │   ├── 004-people.yaml
│   │       │   ├── 005-person-positions.yaml
│   │       │   ├── 006-historical-periods.yaml
│   │       │   ├── 007-gis-data.yaml
│   │       │   └── 008-indexes.yaml
│   │       └── templates/
│   │           ├── reports/
│   │           │   ├── organization-report.html
│   │           │   ├── historical-period-report.html
│   │           │   ├── geographic-region-report.html
│   │           │   └── person-report.html
│   │           └── emails/
│   │               ├── report-ready.html
│   │               └── import-complete.html
│   └── test/
│       └── java/
│           └── io/github/bondalen/vuege/
│               ├── VuegeApplicationTests.java
│               ├── integration/
│               │   ├── OrganizationalUnitIntegrationTest.java
│               │   ├── PositionIntegrationTest.java
│               │   ├── PersonIntegrationTest.java
│               │   ├── ReportIntegrationTest.java
│               │   └── ImportIntegrationTest.java
│               └── unit/
│                   ├── OrganizationalUnitServiceTest.java
│                   ├── PositionServiceTest.java
│                   ├── PersonServiceTest.java
│                   ├── ReportServiceTest.java
│                   └── ImportServiceTest.java
├── pom.xml
└── .mvn/
    └── wrapper/
        ├── maven-wrapper.jar
        └── maven-wrapper.properties
```

## Основной класс приложения

```java
/**
 * @file: VuegeApplication.java
 * @description: Главный класс Spring Boot приложения Vuege
 * @dependencies: Spring Boot AutoConfiguration
 * @created: 2024-12-19
 */
package io.github.bondalen.vuege;

import org.springframework.boot.SpringApplication;
import org.springframework.boot.autoconfigure.SpringBootApplication;
import org.springframework.scheduling.annotation.EnableAsync;

@SpringBootApplication
@EnableAsync
public class VuegeApplication {

    public static void main(String[] args) {
        SpringApplication.run(VuegeApplication.class, args);
    }
}
```

## Конфигурация приложения

### application.yml
```yaml
spring:
  application:
    name: vuege
  
  profiles:
    active: dev
  
  # Database Configuration
  r2dbc:
    url: r2dbc:postgresql://localhost:5432/vuege_dev
    username: testuser
    password: testpass
  
  # GraphQL Configuration
  graphql:
    graphiql:
      enabled: true
      path: /graphiql
    schema:
      locations: classpath:graphql/
  
  # Liquibase Configuration
  liquibase:
    enabled: true
    change-log: classpath:db/migration/db.changelog-master.yaml
  
  # Mail Configuration
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
  
  # Thymeleaf Configuration
  thymeleaf:
    cache: false
    prefix: classpath:/templates/
    suffix: .html

# Server Configuration
server:
  port: 8080
  servlet:
    context-path: /api

# Actuator Configuration
management:
  endpoints:
    web:
      exposure:
        include: health,info,metrics,prometheus
  endpoint:
    health:
      show-details: when-authorized

# Async Configuration
async:
  report-processing:
    core-pool-size: 2
    max-pool-size: 5
    queue-capacity: 10
    thread-name-prefix: report-processor-

# Report Generation Configuration
report:
  generation:
    pdf:
      enabled: true
      temp-dir: /tmp/vuege/reports
    excel:
      enabled: true
      auto-size-columns: true
    csv:
      enabled: true
      encoding: UTF-8
    xml:
      enabled: true
      pretty-print: true

# File Import Configuration
import:
  max-file-size: 100MB
  supported-formats:
    - xlsx
    - xls
    - ods
    - csv
  validation:
    strict-mode: false
    auto-fix: true
```

### application-dev.yml
```yaml
spring:
  r2dbc:
    url: r2dbc:postgresql://localhost:5432/vuege_dev
    username: testuser
    password: testpass

logging:
  level:
    io.github.bondalen.vuege: DEBUG
    org.springframework.graphql: DEBUG
    org.springframework.r2dbc: DEBUG
```

### application-prod.yml
```yaml
spring:
  r2dbc:
    url: r2dbc:postgresql://postgres:5432/vuege_prod
    username: ${DB_USERNAME}
    password: ${DB_PASSWORD}

logging:
  level:
    io.github.bondalen.vuege: INFO
    org.springframework.graphql: WARN
    org.springframework.r2dbc: WARN
```

## Необходимые переменные окружения

```bash
# Database
DB_USERNAME=testuser
DB_PASSWORD=testpass

# Email
EMAIL_USERNAME=your-email@gmail.com
EMAIL_PASSWORD=your-app-password

# Application
SPRING_PROFILES_ACTIVE=dev
```

## Команды для создания проекта

### 1. Создание структуры папок
```bash
mkdir -p backend/src/main/java/io/github/bondalen/vuege/{config,model,repository,service,async,graphql/{resolver,scalar},exception,util}
mkdir -p backend/src/main/resources/{graphql,db/migration,templates/{reports,emails}}
mkdir -p backend/src/test/java/io/github/bondalen/vuege/{integration,unit}
mkdir -p backend/.mvn/wrapper
```

### 2. Создание pom.xml
```bash
# Скопировать содержимое pom.xml из раздела выше
```

### 3. Инициализация Maven Wrapper
```bash
cd backend
mvn wrapper:wrapper
```

### 4. Сборка проекта
```bash
mvn clean compile
```

### 5. Запуск приложения
```bash
mvn spring-boot:run
```

## Следующие шаги

1. **Создание моделей данных** с использованием Lombok аннотаций
2. **Настройка GraphQL схемы** в `src/main/resources/graphql/schema.graphqls`
3. **Создание Liquibase миграций** для инициализации базы данных
4. **Реализация репозиториев** с использованием R2DBC
5. **Создание сервисов** с бизнес-логикой
6. **Настройка GraphQL резолверов**
7. **Добавление тестов** для всех компонентов

## Полезные ссылки

- [Spring Boot 3.4.5 Documentation](https://docs.spring.io/spring-boot/docs/3.4.5/reference/html/)
- [Spring GraphQL Documentation](https://docs.spring.io/spring-graphql/docs/current/reference/html/)
- [Spring Data R2DBC Documentation](https://docs.spring.io/spring-data/r2dbc/docs/current/reference/html/)
- [Lombok Documentation](https://projectlombok.org/features/all)
- [PostgreSQL R2DBC Driver](https://github.com/pgjdbc/r2dbc-postgresql)
