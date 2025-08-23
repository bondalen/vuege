package io.github.bondalen.entity;

import lombok.Data;
import lombok.NoArgsConstructor;
import lombok.AllArgsConstructor;
import lombok.Builder;
import org.springframework.data.annotation.Id;
import org.springframework.data.relational.core.mapping.Table;
import org.springframework.data.relational.core.mapping.Column;

import java.time.LocalDate;
import java.util.List;

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
}