package io.github.bondalen.graphql.input;

import lombok.Data;
import lombok.Builder;
import lombok.NoArgsConstructor;
import lombok.AllArgsConstructor;
import io.github.bondalen.entity.PositionHierarchy;

import java.time.LocalDate;

@Data
@Builder
@NoArgsConstructor
@AllArgsConstructor
public class PositionFilterInput {
    private PositionHierarchy hierarchy;
    private Boolean isActive;
    private Long organizationId;
    private LocalDate createdDateFrom;
    private LocalDate createdDateTo;
    private LocalDate abolishedDateFrom;
    private LocalDate abolishedDateTo;
    private Boolean hasSalary;
    private String searchQuery;
}