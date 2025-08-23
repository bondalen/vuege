package io.github.bondalen.entity;

import lombok.Data;
import lombok.NoArgsConstructor;
import lombok.AllArgsConstructor;
import lombok.Builder;
import org.springframework.data.annotation.Id;
import org.springframework.data.relational.core.mapping.Table;
import org.springframework.data.relational.core.mapping.Column;

import java.time.LocalDate;

/**
 * Связь человек-должность
 */
@Data
@NoArgsConstructor
@AllArgsConstructor
@Builder
@Table("person_positions")
public class PersonPosition {
    
    @Id
    private Long id;
    
    @Column("person_id")
    private Long personId;
    
    @Column("position_id")
    private Long positionId;
    
    @Column("start_date")
    private LocalDate startDate;
    
    @Column("end_date")
    private LocalDate endDate;
    
    @Column("appointment_type")
    private AppointmentType appointmentType;
    
    @Column("source")
    private String source;
}