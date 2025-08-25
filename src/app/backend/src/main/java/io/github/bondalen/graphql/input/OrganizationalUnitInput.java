package io.github.bondalen.graphql.input;

import io.github.bondalen.entity.OrganizationType;
import lombok.Data;
import lombok.Builder;
import lombok.NoArgsConstructor;
import lombok.AllArgsConstructor;

import java.time.LocalDate;

/**
 * Input тип для создания/обновления организационной единицы
 */
@Data
@Builder
@NoArgsConstructor
@AllArgsConstructor
public class OrganizationalUnitInput {
    
    private String name;
    private OrganizationType type;
    private LocalDate foundedDate;
    private LocalDate dissolvedDate;
    private GeoPointInput location;
    private Boolean isFictional;
    private Long historicalPeriodId;
    private Long parentUnitId;
}