/**
 * @file: OrganizationalUnit.java
 * @description: Модель организационной единицы с поддержкой исторических данных и ГИС
 * @lombok: @Data, @Builder, @NoArgsConstructor, @AllArgsConstructor, @ToString(exclude = "transformations")
 * @created: 2024-12-19
 */
package my.fe.vuege.model;

import lombok.AllArgsConstructor;
import lombok.Builder;
import lombok.Data;
import lombok.NoArgsConstructor;
import lombok.ToString;

import jakarta.validation.constraints.NotBlank;
import jakarta.validation.constraints.NotNull;
import jakarta.validation.constraints.PastOrPresent;
import java.time.LocalDate;
import java.util.List;

@Data
@Builder
@NoArgsConstructor
@AllArgsConstructor
@ToString(exclude = "transformations") // Исключаем большие коллекции из toString
public class OrganizationalUnit {
    
    @NotBlank(message = "ID не может быть пустым")
    private String id;
    
    @NotBlank(message = "Название не может быть пустым")
    private String name;
    
    @NotNull(message = "Тип организации обязателен")
    private OrganizationType type;
    
    @NotNull(message = "Дата основания обязательна")
    @PastOrPresent(message = "Дата основания не может быть в будущем")
    private LocalDate foundedDate;
    
    private LocalDate dissolvedDate;
    
    @NotNull(message = "Географическое местоположение обязательно")
    private GeoPoint location;
    
    @Builder.Default
    private boolean isFictional = false;
    
    @NotNull(message = "Исторический период обязателен")
    private HistoricalPeriod historicalPeriod;
    
    private String parentUnitId;
    
    @Builder.Default
    private List<String> childUnitIds = List.of();
    
    @Builder.Default
    private List<Transformation> transformations = List.of();
    
    // Кастомные методы для бизнес-логики
    public boolean isActive() {
        return dissolvedDate == null;
    }
    
    public boolean hasParent() {
        return parentUnitId != null && !parentUnitId.isEmpty();
    }
    
    public boolean hasChildren() {
        return childUnitIds != null && !childUnitIds.isEmpty();
    }
    
    public long getAgeInYears() {
        LocalDate endDate = dissolvedDate != null ? dissolvedDate : LocalDate.now();
        return java.time.Period.between(foundedDate, endDate).getYears();
    }
}

/**
 * @file: OrganizationType.java
 * @description: Enum типов организационных единиц
 * @created: 2024-12-19
 */
enum OrganizationType {
    STATE,        // Государство
    GOVERNMENT,   // Правительственная организация
    COMMERCIAL    // Коммерческая организация
}

/**
 * @file: GeoPoint.java
 * @description: Модель географической точки с поддержкой PostGIS
 * @lombok: @Data, @Builder, @NoArgsConstructor, @AllArgsConstructor
 * @created: 2024-12-19
 */
@Data
@Builder
@NoArgsConstructor
@AllArgsConstructor
class GeoPoint {
    
    @NotBlank(message = "ID не может быть пустым")
    private String id;
    
    @NotNull(message = "Широта обязательна")
    private Double latitude;
    
    @NotNull(message = "Долгота обязательна")
    private Double longitude;
    
    private Double elevation;
    
    @NotNull(message = "Точность координат обязательна")
    private AccuracyType accuracy;
    
    // Метод для получения координат в формате GeoJSON
    public double[] getCoordinates() {
        return new double[]{longitude, latitude};
    }
    
    // Метод для проверки валидности координат
    public boolean isValid() {
        return latitude != null && longitude != null &&
               latitude >= -90 && latitude <= 90 &&
               longitude >= -180 && longitude <= 180;
    }
}

/**
 * @file: AccuracyType.java
 * @description: Enum типов точности географических координат
 * @created: 2024-12-19
 */
enum AccuracyType {
    EXACT,        // Точные координаты
    APPROXIMATE,  // Приблизительные координаты
    UNKNOWN       // Неизвестная точность
}

/**
 * @file: HistoricalPeriod.java
 * @description: Модель исторического периода
 * @lombok: @Data, @Builder, @NoArgsConstructor, @AllArgsConstructor
 * @created: 2024-12-19
 */
@Data
@Builder
@NoArgsConstructor
@AllArgsConstructor
class HistoricalPeriod {
    
    @NotBlank(message = "ID не может быть пустым")
    private String id;
    
    @NotBlank(message = "Название периода не может быть пустым")
    private String name;
    
    @NotNull(message = "Дата начала обязательна")
    private LocalDate startDate;
    
    private LocalDate endDate;
    
    @NotNull(message = "Эра обязательна")
    private Era era;
    
    private String description;
    
    // Метод для проверки, активен ли период
    public boolean isActive() {
        return endDate == null;
    }
    
    // Метод для получения длительности периода в годах
    public long getDurationInYears() {
        LocalDate end = endDate != null ? endDate : LocalDate.now();
        return java.time.Period.between(startDate, end).getYears();
    }
}

/**
 * @file: Era.java
 * @description: Enum исторических эр
 * @created: 2024-12-19
 */
enum Era {
    BCE,  // До нашей эры (Before Common Era)
    CE    // Нашей эры (Common Era)
}

/**
 * @file: Transformation.java
 * @description: Модель трансформации организационной единицы
 * @lombok: @Data, @Builder, @NoArgsConstructor, @AllArgsConstructor
 * @created: 2024-12-19
 */
@Data
@Builder
@NoArgsConstructor
@AllArgsConstructor
class Transformation {
    
    @NotBlank(message = "ID не может быть пустым")
    private String id;
    
    @NotBlank(message = "Тип трансформации не может быть пустым")
    private String type;
    
    @NotNull(message = "Дата трансформации обязательна")
    private LocalDate date;
    
    private String description;
    
    @Builder.Default
    private boolean isCompleted = false;
}
