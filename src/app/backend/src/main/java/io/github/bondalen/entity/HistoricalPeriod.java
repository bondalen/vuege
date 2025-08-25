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
 * Исторический период
 */
@Data
@NoArgsConstructor
@AllArgsConstructor
@Builder
@Table("historical_periods")
public class HistoricalPeriod {
    
    @Id
    private Long id;
    
    @Column("name")
    private String name;
    
    @Column("start_date")
    private LocalDate startDate;
    
    @Column("end_date")
    private LocalDate endDate;
    
    @Column("era")
    private Era era;
    
    @Column("description")
    private String description;
}