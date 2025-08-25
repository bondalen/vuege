package io.github.bondalen.graphql.input;

import io.github.bondalen.entity.AppointmentType;
import lombok.Data;
import lombok.Builder;
import lombok.NoArgsConstructor;
import lombok.AllArgsConstructor;

import java.time.LocalDate;

/**
 * Input тип для назначения человека на должность
 */
@Data
@Builder
@NoArgsConstructor
@AllArgsConstructor
public class PersonPositionInput {
    
    private Long personId;
    private Long positionId;
    private LocalDate startDate;
    private LocalDate endDate;
    private AppointmentType appointmentType;
    private String source;
}