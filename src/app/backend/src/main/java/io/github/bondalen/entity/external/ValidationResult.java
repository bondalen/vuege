package io.github.bondalen.entity.external;

import lombok.AllArgsConstructor;
import lombok.Builder;
import lombok.Data;
import lombok.NoArgsConstructor;

import java.time.LocalDateTime;
import java.util.List;

/**
 * Результат валидации данных
 */
@Data
@Builder
@NoArgsConstructor
@AllArgsConstructor
public class ValidationResult {
    
    /**
     * Исходные данные для валидации
     */
    private String originalData;
    
    /**
     * Тип валидации (email, phone, address, etc.)
     */
    private String validationType;
    
    /**
     * Статус валидации
     */
    private ValidationStatus status;
    
    /**
     * Валидность данных
     */
    private boolean isValid;
    
    /**
     * Уровень достоверности (0-100)
     */
    private Integer confidence;
    
    /**
     * Форматированные данные
     */
    private String formattedData;
    
    /**
     * Список ошибок валидации
     */
    private List<String> errors;
    
    /**
     * Предложения по исправлению
     */
    private List<String> suggestions;
    
    /**
     * Дополнительная информация
     */
    private String additionalInfo;
    
    /**
     * Время выполнения валидации (мс)
     */
    private Long responseTime;
    
    /**
     * Время создания результата
     */
    private LocalDateTime createdAt;
    
    /**
     * Источник валидации
     */
    private String source;
    
    /**
     * Статусы валидации
     */
    public enum ValidationStatus {
        VALID,
        INVALID,
        UNKNOWN,
        ERROR
    }
}