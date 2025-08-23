package io.github.bondalen.graphql.input;

import io.github.bondalen.entity.AccuracyType;
import lombok.Data;
import lombok.Builder;
import lombok.NoArgsConstructor;
import lombok.AllArgsConstructor;

/**
 * Input тип для географической точки
 */
@Data
@Builder
@NoArgsConstructor
@AllArgsConstructor
public class GeoPointInput {
    
    private Double latitude;
    private Double longitude;
    private Double elevation;
    private AccuracyType accuracy;
}