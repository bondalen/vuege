package io.github.bondalen.service.external;

import io.github.bondalen.entity.external.EnrichmentResult;
import io.github.resilience4j.circuitbreaker.annotation.CircuitBreaker;
import io.github.resilience4j.ratelimiter.annotation.RateLimiter;
import io.github.resilience4j.retry.annotation.Retry;
import io.github.resilience4j.timelimiter.annotation.TimeLimiter;
import lombok.RequiredArgsConstructor;
import lombok.extern.slf4j.Slf4j;
import org.springframework.cache.annotation.Cacheable;
import org.springframework.stereotype.Service;
import org.springframework.web.reactive.function.client.WebClient;
import reactor.core.publisher.Mono;

import java.time.LocalDateTime;
import java.util.HashMap;
import java.util.Map;

/**
 * Сервис для обогащения данных через внешние API
 * 
 * Поддерживает обогащение:
 * - Информации об организациях
 * - Данных о юридических лицах
 * - Дополнительной информации по адресам
 */
@Slf4j
@Service
@RequiredArgsConstructor
public class EnrichmentService {

    private final WebClient enrichmentWebClient;
    private final String enrichmentApiKey;

    /**
     * Обогащение данных об организации
     */
    @Cacheable(value = "enrichment", key = "'company_' + #companyName")
    @CircuitBreaker(name = "enrichmentCircuitBreaker")
    @RateLimiter(name = "enrichmentRateLimiter")
    @Retry(name = "enrichmentRetry")
    @TimeLimiter(name = "enrichmentTimeLimiter")
    public Mono<EnrichmentResult> enrichCompanyData(String companyName) {
        log.info("Обогащение данных компании: {}", companyName);
        
        long startTime = System.currentTimeMillis();
        
        return enrichmentWebClient.get()
                .uri(uriBuilder -> uriBuilder
                        .path("/v0.4/companies/search")
                        .queryParam("q", companyName)
                        .queryParam("api_token", enrichmentApiKey)
                        .build())
                .retrieve()
                .bodyToMono(Map.class)
                .map(this::parseCompanyEnrichmentResponse)
                .map(result -> {
                    result.setResponseTime(System.currentTimeMillis() - startTime);
                    result.setCreatedAt(LocalDateTime.now());
                    result.setSource("OpenCorporates API");
                    return result;
                })
                .onErrorResume(error -> {
                    log.error("Ошибка обогащения данных компании {}: {}", companyName, error.getMessage());
                    return Mono.just(createErrorResult(companyName, "company", error.getMessage(), startTime));
                });
    }

    /**
     * Обогащение данных по ИНН
     */
    @Cacheable(value = "enrichment", key = "'inn_' + #inn")
    @CircuitBreaker(name = "enrichmentCircuitBreaker")
    @RateLimiter(name = "enrichmentRateLimiter")
    @Retry(name = "enrichmentRetry")
    @TimeLimiter(name = "enrichmentTimeLimiter")
    public Mono<EnrichmentResult> enrichByInn(String inn) {
        log.info("Обогащение данных по ИНН: {}", inn);
        
        long startTime = System.currentTimeMillis();
        
        return enrichmentWebClient.get()
                .uri(uriBuilder -> uriBuilder
                        .path("/v0.4/companies/search")
                        .queryParam("q", inn)
                        .queryParam("api_token", enrichmentApiKey)
                        .build())
                .retrieve()
                .bodyToMono(Map.class)
                .map(this::parseInnEnrichmentResponse)
                .map(result -> {
                    result.setResponseTime(System.currentTimeMillis() - startTime);
                    result.setCreatedAt(LocalDateTime.now());
                    result.setSource("OpenCorporates API");
                    return result;
                })
                .onErrorResume(error -> {
                    log.error("Ошибка обогащения данных по ИНН {}: {}", inn, error.getMessage());
                    return Mono.just(createErrorResult(inn, "inn", error.getMessage(), startTime));
                });
    }

    /**
     * Парсинг ответа обогащения данных компании
     */
    @SuppressWarnings("unchecked")
    private EnrichmentResult parseCompanyEnrichmentResponse(Map<String, Object> response) {
        try {
            Map<String, Object> results = ((java.util.List<Map<String, Object>>) response.get("results")).get(0);
            Map<String, Object> company = (Map<String, Object>) results.get("company");
            
            Map<String, Object> enrichedData = new HashMap<>();
            enrichedData.put("name", company.get("name"));
            enrichedData.put("company_number", company.get("company_number"));
            enrichedData.put("jurisdiction_code", company.get("jurisdiction_code"));
            enrichedData.put("incorporation_date", company.get("incorporation_date"));
            enrichedData.put("dissolution_date", company.get("dissolution_date"));
            enrichedData.put("company_type", company.get("company_type"));
            enrichedData.put("status", company.get("status"));
            
            return EnrichmentResult.builder()
                    .enrichmentType("company")
                    .status(EnrichmentResult.EnrichmentStatus.SUCCESS)
                    .enrichedData(enrichedData)
                    .confidence(85)
                    .dataSource("OpenCorporates")
                    .lastUpdated(LocalDateTime.now())
                    .build();
        } catch (Exception e) {
            log.error("Ошибка парсинга ответа обогащения компании: {}", e.getMessage());
            return EnrichmentResult.builder()
                    .enrichmentType("company")
                    .status(EnrichmentResult.EnrichmentStatus.ERROR)
                    .errorMessage("Не удалось обработать ответ API")
                    .build();
        }
    }

    /**
     * Парсинг ответа обогащения данных по ИНН
     */
    @SuppressWarnings("unchecked")
    private EnrichmentResult parseInnEnrichmentResponse(Map<String, Object> response) {
        try {
            Map<String, Object> results = ((java.util.List<Map<String, Object>>) response.get("results")).get(0);
            Map<String, Object> company = (Map<String, Object>) results.get("company");
            
            Map<String, Object> enrichedData = new HashMap<>();
            enrichedData.put("inn", company.get("name"));
            enrichedData.put("company_number", company.get("company_number"));
            enrichedData.put("jurisdiction_code", company.get("jurisdiction_code"));
            enrichedData.put("incorporation_date", company.get("incorporation_date"));
            enrichedData.put("company_type", company.get("company_type"));
            enrichedData.put("status", company.get("status"));
            
            return EnrichmentResult.builder()
                    .enrichmentType("inn")
                    .status(EnrichmentResult.EnrichmentStatus.SUCCESS)
                    .enrichedData(enrichedData)
                    .confidence(90)
                    .dataSource("OpenCorporates")
                    .lastUpdated(LocalDateTime.now())
                    .build();
        } catch (Exception e) {
            log.error("Ошибка парсинга ответа обогащения ИНН: {}", e.getMessage());
            return EnrichmentResult.builder()
                    .enrichmentType("inn")
                    .status(EnrichmentResult.EnrichmentStatus.ERROR)
                    .errorMessage("Не удалось обработать ответ API")
                    .build();
        }
    }

    /**
     * Создание результата с ошибкой
     */
    private EnrichmentResult createErrorResult(String data, String type, String errorMessage, long startTime) {
        return EnrichmentResult.builder()
                .originalData(data)
                .enrichmentType(type)
                .status(EnrichmentResult.EnrichmentStatus.ERROR)
                .confidence(0)
                .responseTime(System.currentTimeMillis() - startTime)
                .createdAt(LocalDateTime.now())
                .source("OpenCorporates API")
                .errorMessage(errorMessage)
                .build();
    }
}