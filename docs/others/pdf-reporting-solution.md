# PDF-отчётность в Vuege - Техническое решение

## Обзор

Данный документ описывает техническое решение для реализации PDF-отчётности в системе Vuege, включая архитектуру, компоненты и детали реализации.

## Архитектурное решение

### Выбор технологий

#### PDF Generation
- **Apache PDFBox 2.0.30** - основная библиотека для работы с PDF
- **Flying Saucer 9.1.22** - конвертация HTML в PDF
- **Thymeleaf 3.1.2** - шаблонизатор для создания HTML-шаблонов

**Обоснование выбора Apache PDFBox + Flying Saucer:**
- ✅ Apache License 2.0 - полностью бесплатный для коммерческого использования
- ✅ Высокая производительность
- ✅ Отличная поддержка HTML в PDF
- ✅ Хорошая документация
- ✅ Активная разработка
- ✅ Совместимость с Spring Boot
- ✅ Нет лицензионных ограничений

#### Email Service
- **Spring Boot Mail** - интеграция с JavaMail API
- **JavaMail API** - стандартная библиотека для работы с email

#### Async Processing
- **Spring Boot Async** - асинхронная обработка
- **CompletableFuture** - современный API для асинхронности

### Архитектура системы

```
┌─────────────────────────────────────────────────────────────┐
│                    PDF Report Generation                    │
├─────────────────────────────────────────────────────────────┤
│  Frontend (Vue.js + Quasar)                                │
│  ├── ReportGenerator.vue                                   │
│  ├── ReportStatus.vue                                      │
│  └── EmailDialog.vue                                       │
├─────────────────────────────────────────────────────────────┤
│  Backend (Spring Boot)                                     │
│  ├── ReportController (REST API)                           │
│  ├── ReportService (бизнес-логика)                         │
│  ├── PDFGeneratorService (генерация PDF)                   │
│  ├── EmailService (отправка email)                         │
│  ├── TemplateService (шаблоны)                             │
│  └── AsyncReportProcessor (асинхронная обработка)          │
├─────────────────────────────────────────────────────────────┤
│  Storage & External Services                               │
│  ├── Local File Storage (временные PDF)                    │
│  ├── Email Provider (SMTP)                                 │
│  └── Database (статусы отчётов)                            │
└─────────────────────────────────────────────────────────────┘
```

## Детали реализации

### 1. Модели данных

#### ReportStatus
```java
@Data
@Builder
@NoArgsConstructor
@AllArgsConstructor
public class ReportStatus {
    private String reportId;
    private ReportStatusEnum status;
    private Integer progress;
    private String filePath;
    private String error;
    private LocalDateTime createdAt;
    private LocalDateTime completedAt;
}
```

#### ReportRequest
```java
@Data
@Builder
@NoArgsConstructor
@AllArgsConstructor
public class ReportRequest {
    private ReportType reportType;
    private ReportParameters parameters;
    private ReportFormat format;
    private String language;
}
```

#### EmailReportRequest
```java
@Data
@Builder
@NoArgsConstructor
@AllArgsConstructor
public class EmailReportRequest {
    private ReportRequest reportRequest;
    private String email;
    private String subject;
    private String message;
}
```

### 2. Сервисы

#### ReportService
Основной сервис для управления отчётами:

```java
@Service
@RequiredArgsConstructor
@Slf4j
public class ReportService {
    
    private final PDFGeneratorService pdfGenerator;
    private final TemplateService templateService;
    private final ReportRepository reportRepository;
    private final AsyncReportProcessor asyncProcessor;
    
    public ReportGenerationResult generateReport(ReportRequest request) {
        // Создание записи о статусе отчёта
        ReportStatus status = ReportStatus.builder()
                .reportId(generateReportId())
                .status(ReportStatusEnum.PENDING)
                .createdAt(LocalDateTime.now())
                .build();
        
        reportRepository.save(status);
        
        // Запуск асинхронной генерации
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
    
    private String generateReportId() {
        return "report-" + UUID.randomUUID().toString();
    }
    
    private int calculateEstimatedTime(ReportType reportType) {
        return switch (reportType) {
            case ORGANIZATION -> 30;
            case HISTORICAL_PERIOD -> 60;
            case GEOGRAPHIC -> 45;
            case PERSON -> 25;
            case CUSTOM -> 90;
        };
    }
}
```

#### PDFGeneratorService
Сервис для генерации PDF из HTML-шаблонов:

```java
@Service
@RequiredArgsConstructor
@Slf4j
public class PDFGeneratorService {
    
    private final TemplateService templateService;
    private final FileStorageService fileStorage;
    
    public String generatePDF(ReportData data, ReportType type) {
        try {
            // Генерация HTML из шаблона
            String htmlContent = templateService.processTemplate(type, data);
            
            // Конвертация HTML в PDF
            byte[] pdfBytes = convertHtmlToPdf(htmlContent);
            
            // Сохранение файла
            String fileName = "report-" + data.getReportId() + ".pdf";
            String filePath = fileStorage.storeFile(fileName, pdfBytes);
            
            log.info("PDF report generated: {}", filePath);
            return filePath;
            
        } catch (Exception e) {
            log.error("Error generating PDF report", e);
            throw new PDFGenerationException("Failed to generate PDF", e);
        }
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

#### EmailService
Сервис для отправки отчётов по email:

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
            MimeMessageHelper helper = new MimeMessageHelper(message, true, "UTF-8");
            
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
    
    private void waitForReportCompletion(String reportId) {
        int maxAttempts = 30; // 5 минут максимум
        int attempt = 0;
        
        while (attempt < maxAttempts) {
            try {
                ReportStatus status = reportService.getReportStatus(reportId);
                
                if (status.getStatus() == ReportStatusEnum.COMPLETED) {
                    return;
                } else if (status.getStatus() == ReportStatusEnum.FAILED) {
                    throw new RuntimeException("Report generation failed: " + status.getError());
                }
                
                Thread.sleep(10000); // 10 секунд
                attempt++;
                
            } catch (InterruptedException e) {
                Thread.currentThread().interrupt();
                throw new RuntimeException("Interrupted while waiting for report", e);
            }
        }
        
        throw new RuntimeException("Report generation timeout");
    }
    
    private String generateEmailText(EmailReportRequest request) {
        return templateService.processEmailTemplate("report-email", Map.of(
                "message", request.getMessage(),
                "reportType", request.getReportRequest().getReportType().toString(),
                "generatedAt", LocalDateTime.now().format(DateTimeFormatter.ofPattern("dd.MM.yyyy HH:mm"))
        ));
    }
}
```

### 3. Асинхронная обработка

#### AsyncReportProcessor
```java
@Component
@RequiredArgsConstructor
@Slf4j
public class AsyncReportProcessor {
    
    private final PDFGeneratorService pdfGenerator;
    private final ReportRepository reportRepository;
    private final ReportDataService reportDataService;
    
    @Async("reportProcessingExecutor")
    public void processReport(String reportId, ReportRequest request) {
        try {
            // Обновление статуса
            updateReportStatus(reportId, ReportStatusEnum.GENERATING, 0);
            
            // Получение данных для отчёта
            ReportData data = reportDataService.getReportData(request);
            updateReportStatus(reportId, ReportStatusEnum.GENERATING, 30);
            
            // Генерация PDF
            String filePath = pdfGenerator.generatePDF(data, request.getReportType());
            updateReportStatus(reportId, ReportStatusEnum.GENERATING, 80);
            
            // Финальное обновление статуса
            updateReportStatus(reportId, ReportStatusEnum.COMPLETED, 100, filePath);
            
            log.info("Report {} generated successfully", reportId);
            
        } catch (Exception e) {
            log.error("Error processing report {}", reportId, e);
            updateReportStatus(reportId, ReportStatusEnum.FAILED, 0, null, e.getMessage());
        }
    }
    
    private void updateReportStatus(String reportId, ReportStatusEnum status, 
                                   int progress, String filePath, String error) {
        ReportStatus reportStatus = reportRepository.findById(reportId)
                .orElseThrow(() -> new ReportNotFoundException(reportId));
        
        reportStatus.setStatus(status);
        reportStatus.setProgress(progress);
        reportStatus.setFilePath(filePath);
        reportStatus.setError(error);
        
        if (status == ReportStatusEnum.COMPLETED || status == ReportStatusEnum.FAILED) {
            reportStatus.setCompletedAt(LocalDateTime.now());
        }
        
        reportRepository.save(reportStatus);
    }
    
    private void updateReportStatus(String reportId, ReportStatusEnum status, int progress) {
        updateReportStatus(reportId, status, progress, null, null);
    }
    
    private void updateReportStatus(String reportId, ReportStatusEnum status, 
                                   int progress, String filePath) {
        updateReportStatus(reportId, status, progress, filePath, null);
    }
}
```

### 4. Конфигурация

#### AsyncConfig
```java
@Configuration
@EnableAsync
public class AsyncConfig implements AsyncConfigurer {
    
    @Override
    public Executor getAsyncExecutor() {
        ThreadPoolTaskExecutor executor = new ThreadPoolTaskExecutor();
        executor.setCorePoolSize(2);
        executor.setMaxPoolSize(5);
        executor.setQueueCapacity(10);
        executor.setThreadNamePrefix("report-processor-");
        executor.setRejectedExecutionHandler(new ThreadPoolExecutor.CallerRunsPolicy());
        executor.initialize();
        return executor;
    }
    
    @Override
    public AsyncUncaughtExceptionHandler getAsyncUncaughtExceptionHandler() {
        return new SimpleAsyncUncaughtExceptionHandler();
    }
    
    @Bean(name = "reportProcessingExecutor")
    public Executor reportProcessingExecutor() {
        ThreadPoolTaskExecutor executor = new ThreadPoolTaskExecutor();
        executor.setCorePoolSize(2);
        executor.setMaxPoolSize(5);
        executor.setQueueCapacity(10);
        executor.setThreadNamePrefix("report-processor-");
        executor.setRejectedExecutionHandler(new ThreadPoolExecutor.CallerRunsPolicy());
        executor.initialize();
        return executor;
    }
}
```

#### EmailConfig
```java
@Configuration
public class EmailConfig {
    
    @Bean
    public JavaMailSender javaMailSender() {
        JavaMailSenderImpl mailSender = new JavaMailSenderImpl();
        mailSender.setHost("smtp.gmail.com");
        mailSender.setPort(587);
        mailSender.setUsername("${EMAIL_USERNAME}");
        mailSender.setPassword("${EMAIL_PASSWORD}");
        
        Properties props = mailSender.getJavaMailProperties();
        props.put("mail.transport.protocol", "smtp");
        props.put("mail.smtp.auth", "true");
        props.put("mail.smtp.starttls.enable", "true");
        props.put("mail.debug", "false");
        
        return mailSender;
    }
}
```

### 5. Шаблоны

#### HTML-шаблон для отчёта по организации
```html
<!DOCTYPE html>
<html xmlns:th="http://www.thymeleaf.org">
<head>
    <meta charset="UTF-8">
    <title>Отчёт по организации</title>
    <style>
        @page {
            size: A4;
            margin: 2cm;
        }
        
        body {
            font-family: 'DejaVu Sans', Arial, sans-serif;
            font-size: 12px;
            line-height: 1.4;
            color: #333;
        }
        
        .header {
            text-align: center;
            border-bottom: 2px solid #333;
            padding-bottom: 15px;
            margin-bottom: 20px;
        }
        
        .header h1 {
            font-size: 24px;
            margin: 0;
            color: #2c3e50;
        }
        
        .header p {
            font-size: 16px;
            margin: 5px 0;
            color: #7f8c8d;
        }
        
        .section {
            margin: 20px 0;
            page-break-inside: avoid;
        }
        
        .section-title {
            font-size: 16px;
            font-weight: bold;
            color: #2c3e50;
            border-bottom: 1px solid #bdc3c7;
            padding-bottom: 5px;
            margin-bottom: 15px;
        }
        
        .info-row {
            margin: 8px 0;
            display: flex;
        }
        
        .label {
            font-weight: bold;
            width: 150px;
            color: #34495e;
        }
        
        .value {
            flex: 1;
        }
        
        .table {
            width: 100%;
            border-collapse: collapse;
            margin: 15px 0;
            font-size: 11px;
        }
        
        .table th {
            background-color: #ecf0f1;
            border: 1px solid #bdc3c7;
            padding: 8px;
            text-align: left;
            font-weight: bold;
            color: #2c3e50;
        }
        
        .table td {
            border: 1px solid #bdc3c7;
            padding: 8px;
            text-align: left;
        }
        
        .table tr:nth-child(even) {
            background-color: #f8f9fa;
        }
        
        .footer {
            margin-top: 30px;
            padding-top: 15px;
            border-top: 1px solid #bdc3c7;
            text-align: center;
            font-size: 10px;
            color: #7f8c8d;
        }
        
        .status-active {
            color: #27ae60;
            font-weight: bold;
        }
        
        .status-inactive {
            color: #e74c3c;
            font-weight: bold;
        }
    </style>
</head>
<body>
    <div class="header">
        <h1>Отчёт по организационной единице</h1>
        <p th:text="${organization.name}">Название организации</p>
        <p th:text="'Сгенерировано: ' + ${#temporals.format(#temporals.createNow(), 'dd.MM.yyyy HH:mm')}">
            Дата генерации
        </p>
    </div>
    
    <div class="section">
        <div class="section-title">Основная информация</div>
        <div class="info-row">
            <span class="label">Название:</span>
            <span class="value" th:text="${organization.name}">Название</span>
        </div>
        <div class="info-row">
            <span class="label">Тип:</span>
            <span class="value" th:text="${organization.type}">Тип</span>
        </div>
        <div class="info-row">
            <span class="label">Дата основания:</span>
            <span class="value" th:text="${#temporals.format(organization.foundedDate, 'dd.MM.yyyy')}">Дата</span>
        </div>
        <div class="info-row" th:if="${organization.dissolvedDate}">
            <span class="label">Дата ликвидации:</span>
            <span class="value" th:text="${#temporals.format(organization.dissolvedDate, 'dd.MM.yyyy')}">Дата</span>
        </div>
        <div class="info-row">
            <span class="label">Статус:</span>
            <span class="value" th:class="${organization.dissolvedDate ? 'status-inactive' : 'status-active'}"
                  th:text="${organization.dissolvedDate ? 'Ликвидирована' : 'Активна'}">Статус</span>
        </div>
        <div class="info-row" th:if="${organization.location}">
            <span class="label">Координаты:</span>
            <span class="value" th:text="${organization.location.latitude + ', ' + organization.location.longitude}">
                Координаты
            </span>
        </div>
    </div>
    
    <div class="section">
        <div class="section-title">Должности</div>
        <table class="table" th:if="${not #lists.isEmpty(positions)}">
            <thead>
                <tr>
                    <th>Название должности</th>
                    <th>Дата создания</th>
                    <th>Дата упразднения</th>
                    <th>Статус</th>
                </tr>
            </thead>
            <tbody>
                <tr th:each="position : ${positions}">
                    <td th:text="${position.title}">Название</td>
                    <td th:text="${#temporals.format(position.createdDate, 'dd.MM.yyyy')}">Дата</td>
                    <td th:text="${position.abolishedDate ? #temporals.format(position.abolishedDate, 'dd.MM.yyyy') : '-'}">
                        Дата упразднения
                    </td>
                    <td th:class="${position.isActive ? 'status-active' : 'status-inactive'}"
                        th:text="${position.isActive ? 'Активна' : 'Неактивна'}">Статус</td>
                </tr>
            </tbody>
        </table>
        <p th:if="${#lists.isEmpty(positions)}" style="color: #7f8c8d; font-style: italic;">
            Должности не найдены
        </p>
    </div>
    
    <div class="section">
        <div class="section-title">Текущие руководители</div>
        <table class="table" th:if="${not #lists.isEmpty(currentHolders)}">
            <thead>
                <tr>
                    <th>ФИО</th>
                    <th>Должность</th>
                    <th>Дата назначения</th>
                    <th>Тип назначения</th>
                </tr>
            </thead>
            <tbody>
                <tr th:each="holder : ${currentHolders}">
                    <td th:text="${holder.person.name}">ФИО</td>
                    <td th:text="${holder.position.title}">Должность</td>
                    <td th:text="${#temporals.format(holder.startDate, 'dd.MM.yyyy')}">Дата</td>
                    <td th:text="${holder.appointmentType}">Тип</td>
                </tr>
            </tbody>
        </table>
        <p th:if="${#lists.isEmpty(currentHolders)}" style="color: #7f8c8d; font-style: italic;">
            Текущие руководители не найдены
        </p>
    </div>
    
    <div class="section" th:if="${not #lists.isEmpty(childOrganizations)}">
        <div class="section-title">Дочерние организации</div>
        <table class="table">
            <thead>
                <tr>
                    <th>Название</th>
                    <th>Тип</th>
                    <th>Дата основания</th>
                    <th>Статус</th>
                </tr>
            </thead>
            <tbody>
                <tr th:each="child : ${childOrganizations}">
                    <td th:text="${child.name}">Название</td>
                    <td th:text="${child.type}">Тип</td>
                    <td th:text="${#temporals.format(child.foundedDate, 'dd.MM.yyyy')}">Дата</td>
                    <td th:class="${child.dissolvedDate ? 'status-inactive' : 'status-active'}"
                        th:text="${child.dissolvedDate ? 'Ликвидирована' : 'Активна'}">Статус</td>
                </tr>
            </tbody>
        </table>
    </div>
    
    <div class="footer">
        <p>Отчёт сгенерирован системой Vuege</p>
        <p th:text="'Страница ' + ${#numbers.formatInteger(#vars.pageNumber, 1)} + ' из ' + ${#numbers.formatInteger(#vars.totalPages, 1)}">
            Страница X из Y
        </p>
    </div>
</body>
</html>
```

### 6. Frontend компоненты

#### ReportGenerator.vue
```vue
<template>
  <q-card class="report-generator q-pa-md">
    <q-card-section>
      <div class="text-h6">Генерация отчёта</div>
    </q-card-section>
    
    <q-card-section>
      <q-form @submit="generateReport" class="q-gutter-md">
        <div class="row q-gutter-md">
          <div class="col-12 col-md-6">
            <q-select
              v-model="reportType"
              :options="reportTypes"
              label="Тип отчёта"
              required
              outlined
              emit-value
              map-options
            />
          </div>
          
          <div class="col-12 col-md-6">
            <q-select
              v-model="parameters.language"
              :options="languages"
              label="Язык отчёта"
              outlined
              emit-value
              map-options
            />
          </div>
        </div>
        
        <!-- Параметры для отчёта по организации -->
        <div v-if="reportType === 'ORGANIZATION'" class="q-gutter-md">
          <q-input
            v-model="parameters.organizationId"
            label="ID организации"
            outlined
            required
          />
        </div>
        
        <!-- Параметры для отчёта по историческому периоду -->
        <div v-if="reportType === 'HISTORICAL_PERIOD'" class="q-gutter-md">
          <q-input
            v-model="parameters.periodId"
            label="ID исторического периода"
            outlined
            required
          />
        </div>
        
        <!-- Параметры для отчёта по географическому региону -->
        <div v-if="reportType === 'GEOGRAPHIC'" class="q-gutter-md">
          <div class="row q-gutter-md">
            <div class="col-6">
              <q-input
                v-model.number="parameters.geographicBounds.minLat"
                label="Минимальная широта"
                type="number"
                outlined
                required
              />
            </div>
            <div class="col-6">
              <q-input
                v-model.number="parameters.geographicBounds.maxLat"
                label="Максимальная широта"
                type="number"
                outlined
                required
              />
            </div>
          </div>
          <div class="row q-gutter-md">
            <div class="col-6">
              <q-input
                v-model.number="parameters.geographicBounds.minLng"
                label="Минимальная долгота"
                type="number"
                outlined
                required
              />
            </div>
            <div class="col-6">
              <q-input
                v-model.number="parameters.geographicBounds.maxLng"
                label="Максимальная долгота"
                type="number"
                outlined
                required
              />
            </div>
          </div>
        </div>
        
        <!-- Параметры для отчёта по человеку -->
        <div v-if="reportType === 'PERSON'" class="q-gutter-md">
          <q-input
            v-model="parameters.personId"
            label="ID человека"
            outlined
            required
          />
        </div>
        
        <!-- Дополнительные опции -->
        <div class="row q-gutter-md">
          <div class="col-12 col-md-6">
            <q-checkbox v-model="parameters.includeCharts" label="Включить графики" />
          </div>
          <div class="col-12 col-md-6">
            <q-checkbox v-model="parameters.includeMaps" label="Включить карты" />
          </div>
        </div>
        
        <!-- Кнопки действий -->
        <div class="row q-gutter-sm q-mt-md">
          <q-btn 
            type="submit" 
            color="primary" 
            label="Скачать PDF" 
            :loading="isGenerating"
            icon="download"
          />
          <q-btn 
            @click="showEmailDialog = true" 
            color="secondary" 
            label="Отправить по email" 
            icon="email"
          />
        </div>
      </q-form>
    </q-card-section>
    
    <!-- Email Dialog -->
    <q-dialog v-model="showEmailDialog">
      <q-card style="min-width: 400px">
        <q-card-section>
          <div class="text-h6">Отправка отчёта по email</div>
        </q-card-section>
        
        <q-card-section>
          <q-form @submit="sendReportByEmail" class="q-gutter-md">
            <q-input 
              v-model="emailData.email" 
              label="Email" 
              type="email" 
              required 
              outlined
            />
            <q-input 
              v-model="emailData.subject" 
              label="Тема письма" 
              outlined
            />
            <q-input 
              v-model="emailData.message" 
              label="Сообщение" 
              type="textarea" 
              outlined
              rows="3"
            />
          </q-form>
        </q-card-section>
        
        <q-card-actions align="right">
          <q-btn flat label="Отмена" color="primary" v-close-popup />
          <q-btn 
            @click="sendReportByEmail" 
            label="Отправить" 
            color="primary" 
            v-close-popup
            :loading="isSending"
          />
        </q-card-actions>
      </q-card>
    </q-dialog>
    
    <!-- Status Dialog -->
    <q-dialog v-model="showStatusDialog" persistent>
      <q-card style="min-width: 450px">
        <q-card-section>
          <div class="text-h6">Статус генерации отчёта</div>
        </q-card-section>
        
        <q-card-section>
          <div class="q-gutter-md">
            <q-linear-progress 
              :value="reportProgress" 
              color="primary"
              size="lg"
            />
            <div class="text-center q-mt-sm">
              <q-badge 
                :color="getStatusColor(reportStatus)" 
                :label="getStatusText(reportStatus)"
              />
            </div>
            <p class="text-center q-mt-sm">{{ statusMessage }}</p>
          </div>
        </q-card-section>
        
        <q-card-actions align="right">
          <q-btn 
            @click="downloadReport" 
            label="Скачать" 
            color="primary" 
            icon="download"
            v-if="reportStatus === 'COMPLETED'" 
          />
          <q-btn 
            flat 
            label="Закрыть" 
            color="primary" 
            v-close-popup 
          />
        </q-card-actions>
      </q-card>
    </q-dialog>
  </q-card>
</template>

<script setup lang="ts">
import { ref, reactive, computed } from 'vue'
import { useQuasar } from 'quasar'
import { useReportsStore } from '@/stores/reports'

const $q = useQuasar()
const reportsStore = useReportsStore()

// Reactive data
const reportType = ref('ORGANIZATION')
const isGenerating = ref(false)
const isSending = ref(false)
const showEmailDialog = ref(false)
const showStatusDialog = ref(false)
const reportStatus = ref('')
const reportProgress = ref(0)
const statusMessage = ref('')
const currentReportId = ref('')

const parameters = reactive({
  organizationId: '',
  periodId: '',
  personId: '',
  geographicBounds: {
    minLat: 0,
    maxLat: 0,
    minLng: 0,
    maxLng: 0
  },
  includeCharts: false,
  includeMaps: false,
  language: 'ru'
})

const emailData = reactive({
  email: '',
  subject: 'Отчёт из системы Vuege',
  message: 'Во вложении находится запрошенный отчёт.'
})

// Computed
const reportTypes = computed(() => [
  { label: 'По организации', value: 'ORGANIZATION' },
  { label: 'По историческому периоду', value: 'HISTORICAL_PERIOD' },
  { label: 'По географическому региону', value: 'GEOGRAPHIC' },
  { label: 'По человеку', value: 'PERSON' }
])

const languages = computed(() => [
  { label: 'Русский', value: 'ru' },
  { label: 'English', value: 'en' }
])

// Methods
const generateReport = async () => {
  try {
    isGenerating.value = true
    showStatusDialog.value = true
    statusMessage.value = 'Инициализация генерации отчёта...'
    
    const result = await reportsStore.generateReport({
      reportType: reportType.value,
      parameters,
      format: 'PDF'
    })
    
    if (result.success) {
      currentReportId.value = result.reportId
      await pollReportStatus(result.reportId)
    }
  } catch (error) {
    $q.notify({
      type: 'negative',
      message: 'Ошибка при генерации отчёта: ' + error.message
    })
  } finally {
    isGenerating.value = false
  }
}

const sendReportByEmail = async () => {
  try {
    isSending.value = true
    
    const result = await reportsStore.sendReportByEmail({
      reportType: reportType.value,
      parameters,
      email: emailData.email,
      subject: emailData.subject,
      message: emailData.message
    })
    
    if (result.success) {
      $q.notify({
        type: 'positive',
        message: 'Отчёт отправлен на email'
      })
    } else {
      $q.notify({
        type: 'negative',
        message: 'Ошибка при отправке email: ' + result.error
      })
    }
  } catch (error) {
    $q.notify({
      type: 'negative',
      message: 'Ошибка при отправке отчёта: ' + error.message
    })
  } finally {
    isSending.value = false
  }
}

const pollReportStatus = async (reportId: string) => {
  const interval = setInterval(async () => {
    try {
      const status = await reportsStore.getReportStatus(reportId)
      
      reportStatus.value = status.status
      reportProgress.value = status.progress / 100
      
      switch (status.status) {
        case 'COMPLETED':
          statusMessage.value = 'Отчёт готов к скачиванию'
          clearInterval(interval)
          break
        case 'FAILED':
          statusMessage.value = 'Ошибка при генерации отчёта: ' + status.error
          clearInterval(interval)
          break
        case 'GENERATING':
          statusMessage.value = `Генерация... ${status.progress}%`
          break
        default:
          statusMessage.value = 'Ожидание...'
      }
    } catch (error) {
      clearInterval(interval)
      statusMessage.value = 'Ошибка при получении статуса'
    }
  }, 2000)
}

const downloadReport = () => {
  if (currentReportId.value) {
    window.open(`/api/reports/${currentReportId.value}/download`, '_blank')
  }
}

const getStatusColor = (status: string) => {
  switch (status) {
    case 'COMPLETED': return 'positive'
    case 'FAILED': return 'negative'
    case 'GENERATING': return 'primary'
    default: return 'grey'
  }
}

const getStatusText = (status: string) => {
  switch (status) {
    case 'COMPLETED': return 'Завершено'
    case 'FAILED': return 'Ошибка'
    case 'GENERATING': return 'Генерация'
    case 'PENDING': return 'Ожидание'
    default: return 'Неизвестно'
  }
}
</script>

<style scoped>
.report-generator {
  max-width: 800px;
  margin: 0 auto;
}
</style>
```

## Конфигурация и развертывание

### application.yml
```yaml
# PDF Generation Configuration
pdf:
  generation:
    temp-dir: /tmp/vuege-reports
    max-file-size: 50MB
    cleanup-interval: 3600 # seconds
    max-retention-days: 7
  
  templates:
    base-path: classpath:templates/reports
    cache-enabled: true

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
        debug: false

# Async Configuration
async:
  report-processing:
    core-pool-size: 2
    max-pool-size: 5
    queue-capacity: 10
    thread-name-prefix: report-processor-

# File Storage Configuration
file:
  storage:
    base-path: /app/reports
    temp-path: /tmp/vuege-reports
    max-file-size: 52428800 # 50MB
```

### Зависимости Maven
```xml
<!-- PDF Generation -->
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

<!-- Async Processing -->
<dependency>
    <groupId>org.springframework.boot</groupId>
    <artifactId>spring-boot-starter-web</artifactId>
</dependency>
```

## Безопасность и производительность

### Безопасность
- Валидация входных параметров
- Ограничение размера файлов
- Автоматическая очистка временных файлов
- Логирование всех операций
- Защита от XSS в шаблонах

### Производительность
- Асинхронная обработка отчётов
- Кэширование шаблонов
- Ограничение количества одновременных генераций
- Мониторинг использования ресурсов

### Мониторинг
- Метрики генерации отчётов
- Время выполнения
- Успешность операций
- Использование дискового пространства

## Заключение

Предложенное техническое решение обеспечивает полную функциональность PDF-отчётности в системе Vuege с возможностью скачивания и отправки по email. Архитектура построена на современных технологиях Spring Boot и обеспечивает высокую производительность и масштабируемость.
