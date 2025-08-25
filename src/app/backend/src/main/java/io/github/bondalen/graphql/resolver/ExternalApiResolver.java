package io.github.bondalen.graphql.resolver;

import io.github.bondalen.entity.external.ApiMonitoringResult;
import io.github.bondalen.entity.external.EnrichmentResult;
import io.github.bondalen.entity.external.GeocodingResult;
import io.github.bondalen.entity.external.ValidationResult;
import io.github.bondalen.service.external.ApiMonitoringService;
import io.github.bondalen.service.external.EnrichmentService;
import io.github.bondalen.service.external.GeocodingService;
import io.github.bondalen.service.external.ValidationService;
import lombok.RequiredArgsConstructor;
import lombok.extern.slf4j.Slf4j;
import org.springframework.graphql.data.method.annotation.Argument;
import org.springframework.graphql.data.method.annotation.QueryMapping;
import org.springframework.stereotype.Controller;
import reactor.core.publisher.Flux;
import reactor.core.publisher.Mono;

import java.math.BigDecimal;
import java.util.Map;

/**
 * GraphQL резолвер для интеграции с внешними API
 * 
 * Предоставляет:
 * - Геокодирование адресов
 * - Валидацию данных
 * - Обогащение информации
 * - Мониторинг API
 */
@Slf4j
@Controller
@RequiredArgsConstructor
public class ExternalApiResolver {

    private final GeocodingService geocodingService;
    private final ValidationService validationService;
    private final EnrichmentService enrichmentService;
    private final ApiMonitoringService apiMonitoringService;

    /**
     * Геокодирование адреса
     */
    @QueryMapping
    public Mono<GeocodingResult> geocodeAddress(@Argument String address) {
        log.info("GraphQL запрос: геокодирование адреса '{}'", address);
        return geocodingService.geocodeAddress(address);
    }

    /**
     * Обратное геокодирование (координаты -> адрес)
     */
    @QueryMapping
    public Mono<GeocodingResult> reverseGeocode(
            @Argument BigDecimal latitude,
            @Argument BigDecimal longitude) {
        log.info("GraphQL запрос: обратное геокодирование координат {}, {}", latitude, longitude);
        return geocodingService.reverseGeocode(latitude, longitude);
    }

    /**
     * Валидация email
     */
    @QueryMapping
    public Mono<ValidationResult> validateEmail(@Argument String email) {
        log.info("GraphQL запрос: валидация email '{}'", email);
        return validationService.validateEmail(email);
    }

    /**
     * Валидация телефона
     */
    @QueryMapping
    public Mono<ValidationResult> validatePhone(@Argument String phone) {
        log.info("GraphQL запрос: валидация телефона '{}'", phone);
        return validationService.validatePhone(phone);
    }

    /**
     * Валидация адреса
     */
    @QueryMapping
    public Mono<ValidationResult> validateAddress(@Argument String address) {
        log.info("GraphQL запрос: валидация адреса '{}'", address);
        return validationService.validateAddress(address);
    }

    /**
     * Обогащение данных компании
     */
    @QueryMapping
    public Mono<EnrichmentResult> enrichCompanyData(@Argument String companyName) {
        log.info("GraphQL запрос: обогащение данных компании '{}'", companyName);
        return enrichmentService.enrichCompanyData(companyName);
    }

    /**
     * Обогащение данных по ИНН
     */
    @QueryMapping
    public Mono<EnrichmentResult> enrichByInn(@Argument String inn) {
        log.info("GraphQL запрос: обогащение данных по ИНН '{}'", inn);
        return enrichmentService.enrichByInn(inn);
    }

    /**
     * Проверка доступности API геокодирования
     */
    @QueryMapping
    public Mono<ApiMonitoringResult> checkGeocodingApi() {
        log.info("GraphQL запрос: проверка API геокодирования");
        return apiMonitoringService.checkGeocodingApi();
    }

    /**
     * Проверка доступности API валидации
     */
    @QueryMapping
    public Mono<ApiMonitoringResult> checkValidationApi() {
        log.info("GraphQL запрос: проверка API валидации");
        return apiMonitoringService.checkValidationApi();
    }

    /**
     * Проверка доступности API обогащения
     */
    @QueryMapping
    public Mono<ApiMonitoringResult> checkEnrichmentApi() {
        log.info("GraphQL запрос: проверка API обогащения");
        return apiMonitoringService.checkEnrichmentApi();
    }

    /**
     * Проверка всех API
     */
    @QueryMapping
    public Flux<ApiMonitoringResult> checkAllApis() {
        log.info("GraphQL запрос: проверка всех API");
        return apiMonitoringService.checkAllApis().flatMapMany(Flux::fromIterable);
    }

    /**
     * Получение статистики API
     */
    @QueryMapping
    public Mono<Map<String, Object>> getApiStatistics() {
        log.info("GraphQL запрос: получение статистики API");
        return Mono.just(apiMonitoringService.getApiStatistics());
    }
}