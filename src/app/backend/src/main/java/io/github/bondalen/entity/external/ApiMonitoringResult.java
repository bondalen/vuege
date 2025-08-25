package io.github.bondalen.entity.external;

import lombok.AllArgsConstructor;
import lombok.Builder;
import lombok.Data;
import lombok.NoArgsConstructor;

import java.time.LocalDateTime;

/**
 * Результат мониторинга внешнего API
 */
@Data
@Builder
@NoArgsConstructor
@AllArgsConstructor
public class ApiMonitoringResult {
    
    /**
     * Название API
     */
    private String apiName;
    
    /**
     * URL эндпоинта
     */
    private String endpoint;
    
    /**
     * Статус доступности
     */
    private ApiStatus status;
    
    /**
     * Время отклика (мс)
     */
    private Long responseTime;
    
    /**
     * HTTP статус код
     */
    private Integer httpStatusCode;
    
    /**
     * Время последней проверки
     */
    private LocalDateTime lastChecked;
    
    /**
     * Количество успешных запросов за последний час
     */
    private Long successCount;
    
    /**
     * Количество неуспешных запросов за последний час
     */
    private Long errorCount;
    
    /**
     * Процент успешных запросов
     */
    private Double successRate;
    
    /**
     * Сообщение об ошибке (если есть)
     */
    private String errorMessage;
    
    /**
     * Статусы API
     */
    public enum ApiStatus {
        UP,
        DOWN,
        DEGRADED,
        UNKNOWN
    }
}