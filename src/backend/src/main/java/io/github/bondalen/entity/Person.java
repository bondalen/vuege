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
 * Человек
 */
@Data
@NoArgsConstructor
@AllArgsConstructor
@Builder
@Table("persons")
public class Person {
    
    @Id
    private Long id;
    
    @Column("name")
    private String name;
    
    @Column("birth_date")
    private LocalDate birthDate;
    
    @Column("death_date")
    private LocalDate deathDate;
    
    @Column("nationality")
    private String nationality;
    
    @Column("is_fictional")
    private Boolean isFictional;
    
    @Column("historical_period_id")
    private Long historicalPeriodId;
}