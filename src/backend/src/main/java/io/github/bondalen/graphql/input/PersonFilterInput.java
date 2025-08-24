package io.github.bondalen.graphql.input;

import lombok.Data;
import lombok.Builder;
import lombok.NoArgsConstructor;
import lombok.AllArgsConstructor;

import java.time.LocalDate;

@Data
@Builder
@NoArgsConstructor
@AllArgsConstructor
public class PersonFilterInput {
    private String nationality;
    private Boolean isFictional;
    private Long historicalPeriodId;
    private LocalDate birthDateFrom;
    private LocalDate birthDateTo;
    private LocalDate deathDateFrom;
    private LocalDate deathDateTo;
    private Boolean hasEmail;
    private Boolean hasPhone;
    private String searchQuery;
}