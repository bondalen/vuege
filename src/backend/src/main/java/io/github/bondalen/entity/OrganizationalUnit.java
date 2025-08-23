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
 * Организационная единица
 */
@Data
@NoArgsConstructor
@AllArgsConstructor
@Builder
@Table("organizational_units")
public class OrganizationalUnit {
    
    @Id
    private Long id;
    
    @Column("name")
    private String name;
    
    @Column("type")
    private OrganizationType type;
    
    @Column("founded_date")
    private LocalDate foundedDate;
    
    @Column("dissolved_date")
    private LocalDate dissolvedDate;
    
    @Column("location_id")
    private Long locationId;
    
    @Column("is_fictional")
    private Boolean isFictional;
    
    @Column("historical_period_id")
    private Long historicalPeriodId;
    
    @Column("parent_unit_id")
    private Long parentUnitId;
}