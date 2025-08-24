package io.github.bondalen.graphql.input;

import lombok.Data;
import lombok.Builder;
import lombok.NoArgsConstructor;
import lombok.AllArgsConstructor;
import io.github.bondalen.entity.OrganizationType;
import io.github.bondalen.entity.StatusType;

import java.time.LocalDate;
import java.util.List;

@Data
@Builder
@NoArgsConstructor
@AllArgsConstructor
public class OrganizationFilterInput {
    private OrganizationType type;
    private StatusType status;
    private LocalDate foundedDateFrom;
    private LocalDate foundedDateTo;
    private LocalDate dissolvedDateFrom;
    private LocalDate dissolvedDateTo;
    private Boolean hasLocation;
    private Boolean isFictional;
    private Long historicalPeriodId;
    private Long parentUnitId;
    private List<String> tags;
    private String searchQuery;
}