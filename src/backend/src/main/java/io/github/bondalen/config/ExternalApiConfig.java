package io.github.bondalen.config;

import io.github.resilience4j.circuitbreaker.CircuitBreakerConfig;
import io.github.resilience4j.ratelimiter.RateLimiterConfig;
import io.github.resilience4j.retry.RetryConfig;
import io.github.resilience4j.timelimiter.TimeLimiterConfig;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;
import org.springframework.web.reactive.function.client.WebClient;

import java.time.Duration;

/**
 * Конфигурация для интеграции с внешними API
 * 
 * Включает:
 * - WebClient для HTTP запросов
 * - Circuit Breaker для защиты от недоступности сервисов
 * - Rate Limiting для соблюдения лимитов API
 * - Retry логика для обработки временных ошибок
 * - Time Limiter для контроля времени ответа
 */
@Configuration
public class ExternalApiConfig {

    @Value("${external.api.geocoding.base-url:https://api.opencagedata.com}")
    private String geocodingBaseUrl;
    
    @Value("${external.api.geocoding.api-key:}")
    private String geocodingApiKey;
    
    @Value("${external.api.validation.base-url:https://api.abstractapi.com}")
    private String validationBaseUrl;
    
    @Value("${external.api.validation.api-key:}")
    private String validationApiKey;
    
    @Value("${external.api.enrichment.base-url:https://api.opencorporates.com}")
    private String enrichmentBaseUrl;
    
    @Value("${external.api.enrichment.api-key:}")
    private String enrichmentApiKey;

    /**
     * WebClient для геокодирования
     */
    @Bean("geocodingWebClient")
    public WebClient geocodingWebClient() {
        return WebClient.builder()
                .baseUrl(geocodingBaseUrl)
                .defaultHeader("User-Agent", "Vuege/1.0")
                .defaultHeader("Accept", "application/json")
                .build();
    }

    /**
     * Bean для API ключа геокодирования
     */
    @Bean("geocodingApiKey")
    public String geocodingApiKey() {
        return geocodingApiKey;
    }

    /**
     * Bean для API ключа валидации
     */
    @Bean("validationApiKey")
    public String validationApiKey() {
        return validationApiKey;
    }

    /**
     * Bean для API ключа обогащения
     */
    @Bean("enrichmentApiKey")
    public String enrichmentApiKey() {
        return enrichmentApiKey;
    }

    /**
     * WebClient для валидации данных
     */
    @Bean("validationWebClient")
    public WebClient validationWebClient() {
        return WebClient.builder()
                .baseUrl(validationBaseUrl)
                .defaultHeader("User-Agent", "Vuege/1.0")
                .defaultHeader("Accept", "application/json")
                .build();
    }

    /**
     * WebClient для обогащения данных
     */
    @Bean("enrichmentWebClient")
    public WebClient enrichmentWebClient() {
        return WebClient.builder()
                .baseUrl(enrichmentBaseUrl)
                .defaultHeader("User-Agent", "Vuege/1.0")
                .defaultHeader("Accept", "application/json")
                .build();
    }

    /**
     * Circuit Breaker для защиты от недоступности внешних сервисов
     */
    @Bean
    public CircuitBreakerConfig circuitBreakerConfig() {
        return CircuitBreakerConfig.custom()
                .failureRateThreshold(50) // 50% ошибок для открытия circuit breaker
                .waitDurationInOpenState(Duration.ofSeconds(60)) // 60 секунд в открытом состоянии
                .slidingWindowSize(10) // Размер окна для подсчета ошибок
                .minimumNumberOfCalls(5) // Минимум вызовов перед активацией
                .permittedNumberOfCallsInHalfOpenState(3) // Разрешенные вызовы в полуоткрытом состоянии
                .automaticTransitionFromOpenToHalfOpenEnabled(true)
                .recordExceptions(Exception.class)
                .build();
    }

    /**
     * Rate Limiter для соблюдения лимитов внешних API
     */
    @Bean
    public RateLimiterConfig rateLimiterConfig() {
        return RateLimiterConfig.custom()
                .limitForPeriod(100) // 100 запросов
                .limitRefreshPeriod(Duration.ofMinutes(1)) // за минуту
                .timeoutDuration(Duration.ofSeconds(5)) // таймаут 5 секунд
                .build();
    }

    /**
     * Retry конфигурация для обработки временных ошибок
     */
    @Bean
    public RetryConfig retryConfig() {
        return RetryConfig.custom()
                .maxAttempts(3) // Максимум 3 попытки
                .waitDuration(Duration.ofSeconds(1)) // Ждать 1 секунду между попытками
                .retryExceptions(Exception.class)
                .ignoreExceptions(IllegalArgumentException.class) // Не повторять для некорректных аргументов
                .build();
    }

    /**
     * Time Limiter для контроля времени ответа
     */
    @Bean
    public TimeLimiterConfig timeLimiterConfig() {
        return TimeLimiterConfig.custom()
                .timeoutDuration(Duration.ofSeconds(10)) // Таймаут 10 секунд
                .cancelRunningFuture(true) // Отменять выполняющиеся задачи
                .build();
    }

    // Геттеры для API ключей
    public String getGeocodingApiKey() {
        return geocodingApiKey;
    }

    public String getValidationApiKey() {
        return validationApiKey;
    }

    public String getEnrichmentApiKey() {
        return enrichmentApiKey;
    }
}