package io.github.bondalen.service.external;

import io.github.bondalen.entity.external.ValidationResult;
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
import java.util.List;
import java.util.Map;

/**
 * Сервис для валидации данных через внешние API
 * 
 * Поддерживает валидацию:
 * - Email адресов
 * - Телефонных номеров
 * - Почтовых адресов
 * - ИНН/ОГРН организаций
 */
@Slf4j
@Service
@RequiredArgsConstructor
public class ValidationService {

    private final WebClient validationWebClient;
    private final String validationApiKey;

    /**
     * Валидация email адреса
     */
    @Cacheable(value = "validation", key = "'email_' + #email")
    @CircuitBreaker(name = "validationCircuitBreaker")
    @RateLimiter(name = "validationRateLimiter")
    @Retry(name = "validationRetry")
    @TimeLimiter(name = "validationTimeLimiter")
    public Mono<ValidationResult> validateEmail(String email) {
        log.info("Валидация email: {}", email);
        
        long startTime = System.currentTimeMillis();
        
        return validationWebClient.get()
                .uri(uriBuilder -> uriBuilder
                        .path("/v1/validation/email")
                        .queryParam("api_key", validationApiKey)
                        .queryParam("email", email)
                        .build())
                .retrieve()
                .bodyToMono(Map.class)
                .map(this::parseEmailValidationResponse)
                .map(result -> {
                    result.setResponseTime(System.currentTimeMillis() - startTime);
                    result.setCreatedAt(LocalDateTime.now());
                    result.setSource("Abstract API");
                    return result;
                })
                .onErrorResume(error -> {
                    log.error("Ошибка валидации email {}: {}", email, error.getMessage());
                    return Mono.just(createErrorResult(email, "email", error.getMessage(), startTime));
                });
    }

    /**
     * Валидация телефонного номера
     */
    @Cacheable(value = "validation", key = "'phone_' + #phone")
    @CircuitBreaker(name = "validationCircuitBreaker")
    @RateLimiter(name = "validationRateLimiter")
    @Retry(name = "validationRetry")
    @TimeLimiter(name = "validationTimeLimiter")
    public Mono<ValidationResult> validatePhone(String phone) {
        log.info("Валидация телефона: {}", phone);
        
        long startTime = System.currentTimeMillis();
        
        return validationWebClient.get()
                .uri(uriBuilder -> uriBuilder
                        .path("/v1/validation/phone")
                        .queryParam("api_key", validationApiKey)
                        .queryParam("phone", phone)
                        .build())
                .retrieve()
                .bodyToMono(Map.class)
                .map(this::parsePhoneValidationResponse)
                .map(result -> {
                    result.setResponseTime(System.currentTimeMillis() - startTime);
                    result.setCreatedAt(LocalDateTime.now());
                    result.setSource("Abstract API");
                    return result;
                })
                .onErrorResume(error -> {
                    log.error("Ошибка валидации телефона {}: {}", phone, error.getMessage());
                    return Mono.just(createErrorResult(phone, "phone", error.getMessage(), startTime));
                });
    }

    /**
     * Валидация почтового адреса
     */
    @Cacheable(value = "validation", key = "'address_' + #address")
    @CircuitBreaker(name = "validationCircuitBreaker")
    @RateLimiter(name = "validationRateLimiter")
    @Retry(name = "validationRetry")
    @TimeLimiter(name = "validationTimeLimiter")
    public Mono<ValidationResult> validateAddress(String address) {
        log.info("Валидация адреса: {}", address);
        
        long startTime = System.currentTimeMillis();
        
        return validationWebClient.get()
                .uri(uriBuilder -> uriBuilder
                        .path("/v1/validation/address")
                        .queryParam("api_key", validationApiKey)
                        .queryParam("address", address)
                        .build())
                .retrieve()
                .bodyToMono(Map.class)
                .map(this::parseAddressValidationResponse)
                .map(result -> {
                    result.setResponseTime(System.currentTimeMillis() - startTime);
                    result.setCreatedAt(LocalDateTime.now());
                    result.setSource("Abstract API");
                    return result;
                })
                .onErrorResume(error -> {
                    log.error("Ошибка валидации адреса {}: {}", address, error.getMessage());
                    return Mono.just(createErrorResult(address, "address", error.getMessage(), startTime));
                });
    }

    /**
     * Парсинг ответа валидации email
     */
    private ValidationResult parseEmailValidationResponse(Map<String, Object> response) {
        boolean isValid = Boolean.TRUE.equals(response.get("is_valid"));
        String formattedEmail = (String) response.get("email");
        Integer confidence = (Integer) response.get("confidence");
        
        return ValidationResult.builder()
                .validationType("email")
                .status(isValid ? ValidationResult.ValidationStatus.VALID : ValidationResult.ValidationStatus.INVALID)
                .isValid(isValid)
                .confidence(confidence)
                .formattedData(formattedEmail)
                .build();
    }

    /**
     * Парсинг ответа валидации телефона
     */
    private ValidationResult parsePhoneValidationResponse(Map<String, Object> response) {
        boolean isValid = Boolean.TRUE.equals(response.get("is_valid"));
        String formattedPhone = (String) response.get("phone");
        Integer confidence = (Integer) response.get("confidence");
        
        return ValidationResult.builder()
                .validationType("phone")
                .status(isValid ? ValidationResult.ValidationStatus.VALID : ValidationResult.ValidationStatus.INVALID)
                .isValid(isValid)
                .confidence(confidence)
                .formattedData(formattedPhone)
                .build();
    }

    /**
     * Парсинг ответа валидации адреса
     */
    private ValidationResult parseAddressValidationResponse(Map<String, Object> response) {
        boolean isValid = Boolean.TRUE.equals(response.get("is_valid"));
        String formattedAddress = (String) response.get("formatted_address");
        Integer confidence = (Integer) response.get("confidence");
        
        return ValidationResult.builder()
                .validationType("address")
                .status(isValid ? ValidationResult.ValidationStatus.VALID : ValidationResult.ValidationStatus.INVALID)
                .isValid(isValid)
                .confidence(confidence)
                .formattedData(formattedAddress)
                .build();
    }

    /**
     * Создание результата с ошибкой
     */
    private ValidationResult createErrorResult(String data, String type, String errorMessage, long startTime) {
        return ValidationResult.builder()
                .originalData(data)
                .validationType(type)
                .status(ValidationResult.ValidationStatus.ERROR)
                .isValid(false)
                .confidence(0)
                .responseTime(System.currentTimeMillis() - startTime)
                .createdAt(LocalDateTime.now())
                .source("Abstract API")
                .errors(List.of(errorMessage))
                .build();
    }
}