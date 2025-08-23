package io.github.bondalen.graphql.input;

import lombok.Data;
import lombok.Builder;
import lombok.NoArgsConstructor;
import lombok.AllArgsConstructor;

import java.time.LocalDate;

/**
 * Input тип для создания/обновления человека
 */
@Data
@Builder
@NoArgsConstructor
@AllArgsConstructor
public class PersonInput {
    
    private String name;
    private LocalDate birthDate;
    private LocalDate deathDate;
    private String nationality;
    private Boolean isFictional;
    private Long historicalPeriodId;
}