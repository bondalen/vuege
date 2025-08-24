package io.github.bondalen.service.external;

// Удаляем неиспользуемый импорт
import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.Test;
import org.junit.jupiter.api.extension.ExtendWith;
import org.mockito.Mock;
import org.mockito.junit.jupiter.MockitoExtension;
import org.springframework.web.reactive.function.client.WebClient;
import reactor.core.publisher.Mono;
import reactor.test.StepVerifier;

import java.math.BigDecimal;
import java.util.Map;
import org.springframework.core.ParameterizedTypeReference;

import static org.mockito.ArgumentMatchers.any;
import static org.mockito.Mockito.when;

/**
 * Тесты для сервиса геокодирования
 */
@ExtendWith(MockitoExtension.class)
@SuppressWarnings("unchecked")
class GeocodingServiceTest {

    @Mock
    private WebClient geocodingWebClient;
    
    @SuppressWarnings("rawtypes")
    @Mock
    private WebClient.RequestHeadersUriSpec requestHeadersUriSpec;
    
    @Mock
    private WebClient.ResponseSpec responseSpec;

    private GeocodingService geocodingService;
    private String testApiKey = "test-api-key";

    @BeforeEach
    void setUp() {
        geocodingService = new GeocodingService(geocodingWebClient, testApiKey);
    }

    @Test
    void geocodeAddress_Success() {
        // Given
        String address = "Москва, Красная площадь, 1";

        when(geocodingWebClient.get()).thenReturn(requestHeadersUriSpec);
        when(requestHeadersUriSpec.uri(any(java.util.function.Function.class))).thenReturn(requestHeadersUriSpec);
        when(requestHeadersUriSpec.retrieve()).thenReturn(responseSpec);
        when(responseSpec.bodyToMono(Map.class)).thenReturn(Mono.just(createMockResponse()));

        // When & Then
        StepVerifier.create(geocodingService.geocodeAddress(address))
                .expectNextMatches(result -> 
                    result.getOriginalAddress().equals(address) &&
                    result.getStatus().equals("SUCCESS") &&
                    result.getLatitude() != null &&
                    result.getLongitude() != null
                )
                .verifyComplete();
    }

    @Test
    void geocodeAddress_Error() {
        // Given
        String address = "Invalid Address";
        
        when(geocodingWebClient.get()).thenReturn(requestHeadersUriSpec);
        when(requestHeadersUriSpec.uri(any(java.util.function.Function.class))).thenReturn(requestHeadersUriSpec);
        when(requestHeadersUriSpec.retrieve()).thenReturn(responseSpec);
        when(responseSpec.bodyToMono(Map.class)).thenReturn(Mono.error(new RuntimeException("API Error")));

        // When & Then
        StepVerifier.create(geocodingService.geocodeAddress(address))
                .expectNextMatches(result -> 
                    result.getOriginalAddress().equals(address) &&
                    result.getStatus().equals("ERROR") &&
                    result.getErrorMessage() != null
                )
                .verifyComplete();
    }

    @Test
    void reverseGeocode_Success() {
        // Given
        BigDecimal latitude = new BigDecimal("55.7558");
        BigDecimal longitude = new BigDecimal("37.6176");
        
        when(geocodingWebClient.get()).thenReturn(requestHeadersUriSpec);
        when(requestHeadersUriSpec.uri(any(java.util.function.Function.class))).thenReturn(requestHeadersUriSpec);
        when(requestHeadersUriSpec.retrieve()).thenReturn(responseSpec);
        when(responseSpec.bodyToMono(Map.class)).thenReturn(Mono.just(createMockResponse()));

        // When & Then
        StepVerifier.create(geocodingService.reverseGeocode(latitude, longitude))
                .expectNextMatches(result -> 
                    result.getLatitude().equals(latitude) &&
                    result.getLongitude().equals(longitude) &&
                    result.getStatus().equals("SUCCESS")
                )
                .verifyComplete();
    }

    @Test
    void reverseGeocode_Error() {
        // Given
        BigDecimal latitude = new BigDecimal("999.0");
        BigDecimal longitude = new BigDecimal("999.0");
        
        when(geocodingWebClient.get()).thenReturn(requestHeadersUriSpec);
        when(requestHeadersUriSpec.uri(any(java.util.function.Function.class))).thenReturn(requestHeadersUriSpec);
        when(requestHeadersUriSpec.retrieve()).thenReturn(responseSpec);
        when(responseSpec.bodyToMono(Map.class)).thenReturn(Mono.error(new RuntimeException("API Error")));

        // When & Then
        StepVerifier.create(geocodingService.reverseGeocode(latitude, longitude))
                .expectNextMatches(result -> 
                    result.getLatitude().equals(latitude) &&
                    result.getLongitude().equals(longitude) &&
                    result.getStatus().equals("ERROR")
                )
                .verifyComplete();
    }

    /**
     * Создание мок-ответа от API геокодирования
     */
    private java.util.Map<String, Object> createMockResponse() {
        java.util.Map<String, Object> response = new java.util.HashMap<>();
        java.util.List<java.util.Map<String, Object>> results = new java.util.ArrayList<>();
        
        java.util.Map<String, Object> result = new java.util.HashMap<>();
        result.put("formatted", "Красная площадь, 1, Москва, Россия");
        
        java.util.Map<String, Object> geometry = new java.util.HashMap<>();
        geometry.put("lat", 55.7558);
        geometry.put("lng", 37.6176);
        result.put("geometry", geometry);
        
        java.util.Map<String, Object> components = new java.util.HashMap<>();
        components.put("country", "Россия");
        components.put("city", "Москва");
        components.put("road", "Красная площадь");
        components.put("house_number", "1");
        result.put("components", components);
        
        result.put("confidence", "high");
        results.add(result);
        response.put("results", results);
        
        return response;
    }
}