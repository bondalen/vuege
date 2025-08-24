package io.github.bondalen.service.external;

import io.github.bondalen.entity.external.ApiMonitoringResult;
import lombok.RequiredArgsConstructor;
import lombok.extern.slf4j.Slf4j;
import org.springframework.cache.annotation.CacheEvict;
import org.springframework.cache.annotation.Cacheable;
import org.springframework.scheduling.annotation.Scheduled;
import org.springframework.stereotype.Service;
import org.springframework.web.reactive.function.client.WebClient;
import reactor.core.publisher.Mono;

import java.time.LocalDateTime;
import java.util.List;
import java.util.Map;
import java.util.concurrent.ConcurrentHashMap;
import java.util.concurrent.atomic.AtomicLong;

/**
 * Сервис для мониторинга внешних API
 * 
 * Отслеживает:
 * - Доступность API
 * - Время отклика
 * - Статистику успешных/неуспешных запросов
 * - Автоматические проверки каждые 5 минут
 */
@Slf4j
@Service
@RequiredArgsConstructor
public class ApiMonitoringService {

    private final WebClient geocodingWebClient;
    private final WebClient validationWebClient;
    private final WebClient enrichmentWebClient;

    // Статистика запросов для каждого API
    private final Map<String, AtomicLong> successCounters = new ConcurrentHashMap<>();
    private final Map<String, AtomicLong> errorCounters = new ConcurrentHashMap<>();

    /**
     * Проверка доступности API геокодирования
     */
    @Cacheable(value = "api-monitoring", key = "'geocoding'")
    public Mono<ApiMonitoringResult> checkGeocodingApi() {
        return checkApiHealth("geocoding", geocodingWebClient, "/geocode/v1/json?q=test&key=test");
    }

    /**
     * Проверка доступности API валидации
     */
    @Cacheable(value = "api-monitoring", key = "'validation'")
    public Mono<ApiMonitoringResult> checkValidationApi() {
        return checkApiHealth("validation", validationWebClient, "/v1/validation/email?api_key=test&email=test@test.com");
    }

    /**
     * Проверка доступности API обогащения
     */
    @Cacheable(value = "api-monitoring", key = "'enrichment'")
    public Mono<ApiMonitoringResult> checkEnrichmentApi() {
        return checkApiHealth("enrichment", enrichmentWebClient, "/v0.4/companies/search?q=test&api_token=test");
    }

    /**
     * Общая проверка всех API
     */
    public Mono<List<ApiMonitoringResult>> checkAllApis() {
        return Mono.zip(
                checkGeocodingApi(),
                checkValidationApi(),
                checkEnrichmentApi()
        ).map(tuple -> List.of(tuple.getT1(), tuple.getT2(), tuple.getT3()));
    }

    /**
     * Проверка здоровья конкретного API
     */
    private Mono<ApiMonitoringResult> checkApiHealth(String apiName, WebClient webClient, String healthEndpoint) {
        long startTime = System.currentTimeMillis();
        
        return webClient.get()
                .uri(healthEndpoint)
                .retrieve()
                .toBodilessEntity()
                .map(response -> {
                    long responseTime = System.currentTimeMillis() - startTime;
                    successCounters.computeIfAbsent(apiName, k -> new AtomicLong(0)).incrementAndGet();
                    
                    return ApiMonitoringResult.builder()
                            .apiName(apiName)
                            .endpoint(healthEndpoint)
                            .status(ApiMonitoringResult.ApiStatus.UP)
                            .responseTime(responseTime)
                            .httpStatusCode(response.getStatusCode().value())
                            .lastChecked(LocalDateTime.now())
                            .successCount(successCounters.get(apiName).get())
                            .errorCount(errorCounters.getOrDefault(apiName, new AtomicLong(0)).get())
                            .successRate(calculateSuccessRate(apiName))
                            .build();
                })
                .onErrorResume(error -> {
                    long responseTime = System.currentTimeMillis() - startTime;
                    errorCounters.computeIfAbsent(apiName, k -> new AtomicLong(0)).incrementAndGet();
                    
                    return Mono.just(ApiMonitoringResult.builder()
                            .apiName(apiName)
                            .endpoint(healthEndpoint)
                            .status(ApiMonitoringResult.ApiStatus.DOWN)
                            .responseTime(responseTime)
                            .lastChecked(LocalDateTime.now())
                            .successCount(successCounters.getOrDefault(apiName, new AtomicLong(0)).get())
                            .errorCount(errorCounters.get(apiName).get())
                            .successRate(calculateSuccessRate(apiName))
                            .errorMessage(error.getMessage())
                            .build());
                });
    }

    /**
     * Расчет процента успешных запросов
     */
    private double calculateSuccessRate(String apiName) {
        long successCount = successCounters.getOrDefault(apiName, new AtomicLong(0)).get();
        long errorCount = errorCounters.getOrDefault(apiName, new AtomicLong(0)).get();
        long totalCount = successCount + errorCount;
        
        if (totalCount == 0) {
            return 0.0;
        }
        
        return (double) successCount / totalCount * 100;
    }

    /**
     * Получение статистики API
     */
    public Map<String, Object> getApiStatistics() {
        Map<String, Object> statistics = new ConcurrentHashMap<>();
        
        successCounters.forEach((apiName, counter) -> {
            Map<String, Object> apiStats = new ConcurrentHashMap<>();
            apiStats.put("successCount", counter.get());
            apiStats.put("errorCount", errorCounters.getOrDefault(apiName, new AtomicLong(0)).get());
            apiStats.put("successRate", calculateSuccessRate(apiName));
            statistics.put(apiName, apiStats);
        });
        
        return statistics;
    }

    /**
     * Сброс статистики
     */
    public void resetStatistics() {
        successCounters.clear();
        errorCounters.clear();
        log.info("Статистика API сброшена");
    }

    /**
     * Автоматическая проверка всех API каждые 5 минут
     */
    @Scheduled(fixedRate = 300000) // 5 минут
    @CacheEvict(value = "api-monitoring", allEntries = true)
    public void scheduledApiCheck() {
        log.info("Запуск автоматической проверки API");
        checkAllApis()
                .subscribe(
                        results -> {
                            results.forEach(result -> {
                                if (result.getStatus() == ApiMonitoringResult.ApiStatus.DOWN) {
                                    log.warn("API {} недоступен: {}", result.getApiName(), result.getErrorMessage());
                                } else {
                                    log.info("API {} доступен, время отклика: {}ms", 
                                            result.getApiName(), result.getResponseTime());
                                }
                            });
                        },
                        error -> log.error("Ошибка при автоматической проверке API: {}", error.getMessage())
                );
    }
}