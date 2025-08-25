package io.github.bondalen.entity;

import lombok.Data;
import lombok.NoArgsConstructor;
import lombok.AllArgsConstructor;
import lombok.Builder;
import org.springframework.data.annotation.Id;
import org.springframework.data.relational.core.mapping.Table;
import org.springframework.data.relational.core.mapping.Column;

/**
 * Географическая точка
 */
@Data
@NoArgsConstructor
@AllArgsConstructor
@Builder
@Table("geo_points")
public class GeoPoint {
    
    @Id
    private Long id;
    
    @Column("latitude")
    private Double latitude;
    
    @Column("longitude")
    private Double longitude;
    
    @Column("elevation")
    private Double elevation;
    
    @Column("accuracy")
    private AccuracyType accuracy;
}