package io.github.bondalen.service.external;

import io.github.bondalen.entity.external.GeocodingResult;
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

import java.math.BigDecimal;
import java.time.LocalDateTime;
import java.util.Map;

/**
 * Сервис для геокодирования адресов через внешние API
 * 
 * Использует OpenCage Data API для получения координат по адресам
 * Включает кэширование, circuit breaker, rate limiting и retry логику
 */
@Slf4j
@Service
@RequiredArgsConstructor
public class GeocodingService {

    private final WebClient geocodingWebClient;
    private final String geocodingApiKey;

    /**
     * Геокодирование адреса с кэшированием и защитой от ошибок
     */
    @Cacheable(value = "geocoding", key = "#address")
    @CircuitBreaker(name = "geocodingCircuitBreaker")
    @RateLimiter(name = "geocodingRateLimiter")
    @Retry(name = "geocodingRetry")
    @TimeLimiter(name = "geocodingTimeLimiter")
    public Mono<GeocodingResult> geocodeAddress(String address) {
        log.info("Геокодирование адреса: {}", address);
        
        long startTime = System.currentTimeMillis();
        
        return geocodingWebClient.get()
                .uri(uriBuilder -> uriBuilder
                        .path("/geocode/v1/json")
                        .queryParam("q", address)
                        .queryParam("key", geocodingApiKey)
                        .queryParam("limit", 1)
                        .queryParam("no_annotations", 1)
                        .build())
                .retrieve()
                .bodyToMono(Map.class)
                .map(this::parseGeocodingResponse)
                .map(result -> {
                    result.setOriginalAddress(address);
                    result.setResponseTime(System.currentTimeMillis() - startTime);
                    result.setCreatedAt(LocalDateTime.now());
                    result.setSource("OpenCage Data API");
                    result.setStatus("SUCCESS");
                    return result;
                })
                .onErrorResume(error -> {
                    log.error("Ошибка геокодирования для адреса {}: {}", address, error.getMessage());
                    return Mono.just(GeocodingResult.builder()
                            .originalAddress(address)
                            .status("ERROR")
                            .errorMessage(error.getMessage())
                            .responseTime(System.currentTimeMillis() - startTime)
                            .createdAt(LocalDateTime.now())
                            .source("OpenCage Data API")
                            .build());
                });
    }

    /**
     * Обратное геокодирование (координаты -> адрес)
     */
    @Cacheable(value = "geocoding", key = "'reverse_' + #latitude + '_' + #longitude")
    @CircuitBreaker(name = "geocodingCircuitBreaker")
    @RateLimiter(name = "geocodingRateLimiter")
    @Retry(name = "geocodingRetry")
    @TimeLimiter(name = "geocodingTimeLimiter")
    public Mono<GeocodingResult> reverseGeocode(BigDecimal latitude, BigDecimal longitude) {
        log.info("Обратное геокодирование координат: {}, {}", latitude, longitude);
        
        long startTime = System.currentTimeMillis();
        
        return geocodingWebClient.get()
                .uri(uriBuilder -> uriBuilder
                        .path("/geocode/v1/json")
                        .queryParam("q", latitude + "," + longitude)
                        .queryParam("key", geocodingApiKey)
                        .queryParam("limit", 1)
                        .queryParam("no_annotations", 1)
                        .build())
                .retrieve()
                .bodyToMono(Map.class)
                .map(this::parseGeocodingResponse)
                .map(result -> {
                    result.setResponseTime(System.currentTimeMillis() - startTime);
                    result.setCreatedAt(LocalDateTime.now());
                    result.setSource("OpenCage Data API");
                    result.setStatus("SUCCESS");
                    return result;
                })
                .onErrorResume(error -> {
                    log.error("Ошибка обратного геокодирования для координат {}, {}: {}", 
                            latitude, longitude, error.getMessage());
                    return Mono.just(GeocodingResult.builder()
                            .latitude(latitude)
                            .longitude(longitude)
                            .status("ERROR")
                            .errorMessage(error.getMessage())
                            .responseTime(System.currentTimeMillis() - startTime)
                            .createdAt(LocalDateTime.now())
                            .source("OpenCage Data API")
                            .build());
                });
    }

    /**
     * Парсинг ответа от API геокодирования
     */
    @SuppressWarnings("unchecked")
    private GeocodingResult parseGeocodingResponse(Map<String, Object> response) {
        try {
            Map<String, Object> results = ((java.util.List<Map<String, Object>>) response.get("results")).get(0);
            Map<String, Object> geometry = (Map<String, Object>) results.get("geometry");
            Map<String, Object> components = (Map<String, Object>) results.get("components");
            
            return GeocodingResult.builder()
                    .originalAddress("") // Будет установлено позже
                    .latitude(new BigDecimal(geometry.get("lat").toString()))
                    .longitude(new BigDecimal(geometry.get("lng").toString()))
                    .formattedAddress((String) results.get("formatted"))
                    .country((String) components.get("country"))
                    .region((String) components.get("state"))
                    .city((String) components.get("city"))
                    .postalCode((String) components.get("postcode"))
                    .street((String) components.get("road"))
                    .houseNumber((String) components.get("house_number"))
                    .accuracy((String) results.get("confidence"))
                    .build();
        } catch (Exception e) {
            log.error("Ошибка парсинга ответа геокодирования: {}", e.getMessage());
            throw new RuntimeException("Не удалось обработать ответ API геокодирования", e);
        }
    }
}