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
 * Должность
 */
@Data
@NoArgsConstructor
@AllArgsConstructor
@Builder
@Table("positions")
public class Position {
    
    @Id
    private Long id;
    
    @Column("title")
    private String title;
    
    @Column("organization_id")
    private Long organizationId;
    
    @Column("created_date")
    private LocalDate createdDate;
    
    @Column("abolished_date")
    private LocalDate abolishedDate;
    
    @Column("hierarchy")
    private PositionHierarchy hierarchy;
    
    @Column("responsibilities")
    private String responsibilities; // JSON array as string
    
    @Column("is_active")
    private Boolean isActive;
    
    @Column("salary_min")
    private java.math.BigDecimal salaryMin;
    
    @Column("salary_max")
    private java.math.BigDecimal salaryMax;
    
    @Column("salary_currency")
    private String salaryCurrency;
    
    @Column("salary_period")
    private String salaryPeriod;
    
    @Column("requirements")
    private String[] requirements;
    
    @Column("benefits")
    private String[] benefits;
    
    @Column("reports_to_id")
    private Long reportsToId;
    
    @Column("created_at")
    private java.time.LocalDateTime createdAt;
    
    @Column("updated_at")
    private java.time.LocalDateTime updatedAt;
    
    @Column("created_by")
    private String createdBy;
    
    @Column("updated_by")
    private String updatedBy;
}