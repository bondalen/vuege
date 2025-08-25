package io.github.bondalen.graphql.input;

import io.github.bondalen.entity.PositionHierarchy;
import lombok.Data;
import lombok.Builder;
import lombok.NoArgsConstructor;
import lombok.AllArgsConstructor;

import java.time.LocalDate;
import java.util.List;

/**
 * Input тип для создания/обновления должности
 */
@Data
@Builder
@NoArgsConstructor
@AllArgsConstructor
public class PositionInput {
    
    private String title;
    private Long organizationId;
    private LocalDate createdDate;
    private LocalDate abolishedDate;
    private PositionHierarchy hierarchy;
    private List<String> responsibilities;
    private Boolean isActive;
}