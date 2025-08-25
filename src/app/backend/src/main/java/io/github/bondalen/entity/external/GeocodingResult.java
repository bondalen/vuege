package io.github.bondalen.entity.external;

import lombok.AllArgsConstructor;
import lombok.Builder;
import lombok.Data;
import lombok.NoArgsConstructor;

import java.math.BigDecimal;
import java.time.LocalDateTime;

/**
 * Результат геокодирования адреса
 */
@Data
@Builder
@NoArgsConstructor
@AllArgsConstructor
public class GeocodingResult {
    
    /**
     * Исходный адрес
     */
    private String originalAddress;
    
    /**
     * Широта
     */
    private BigDecimal latitude;
    
    /**
     * Долгота
     */
    private BigDecimal longitude;
    
    /**
     * Форматированный адрес
     */
    private String formattedAddress;
    
    /**
     * Страна
     */
    private String country;
    
    /**
     * Регион/область
     */
    private String region;
    
    /**
     * Город
     */
    private String city;
    
    /**
     * Почтовый индекс
     */
    private String postalCode;
    
    /**
     * Улица
     */
    private String street;
    
    /**
     * Номер дома
     */
    private String houseNumber;
    
    /**
     * Уровень точности геокодирования
     */
    private String accuracy;
    
    /**
     * Время выполнения запроса (мс)
     */
    private Long responseTime;
    
    /**
     * Время создания результата
     */
    private LocalDateTime createdAt;
    
    /**
     * Источник геокодирования
     */
    private String source;
    
    /**
     * Статус запроса
     */
    private String status;
    
    /**
     * Сообщение об ошибке (если есть)
     */
    private String errorMessage;
}