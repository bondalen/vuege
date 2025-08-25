package io.github.bondalen.entity.external;

import lombok.AllArgsConstructor;
import lombok.Builder;
import lombok.Data;
import lombok.NoArgsConstructor;

import java.time.LocalDateTime;
import java.util.Map;

/**
 * Результат обогащения данных
 */
@Data
@Builder
@NoArgsConstructor
@AllArgsConstructor
public class EnrichmentResult {
    
    /**
     * Исходные данные
     */
    private String originalData;
    
    /**
     * Тип обогащения
     */
    private String enrichmentType;
    
    /**
     * Статус обогащения
     */
    private EnrichmentStatus status;
    
    /**
     * Дополнительные данные в формате ключ-значение
     */
    private Map<String, Object> enrichedData;
    
    /**
     * Уровень достоверности (0-100)
     */
    private Integer confidence;
    
    /**
     * Источник данных
     */
    private String dataSource;
    
    /**
     * Время последнего обновления данных
     */
    private LocalDateTime lastUpdated;
    
    /**
     * Время выполнения запроса (мс)
     */
    private Long responseTime;
    
    /**
     * Время создания результата
     */
    private LocalDateTime createdAt;
    
    /**
     * Источник обогащения
     */
    private String source;
    
    /**
     * Сообщение об ошибке (если есть)
     */
    private String errorMessage;
    
    /**
     * Статусы обогащения
     */
    public enum EnrichmentStatus {
        SUCCESS,
        PARTIAL,
        NOT_FOUND,
        ERROR
    }
}