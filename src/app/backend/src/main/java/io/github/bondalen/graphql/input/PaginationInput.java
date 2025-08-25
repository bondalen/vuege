package io.github.bondalen.graphql.input;

import lombok.Data;
import lombok.Builder;
import lombok.NoArgsConstructor;
import lombok.AllArgsConstructor;

@Data
@Builder
@NoArgsConstructor
@AllArgsConstructor
public class PaginationInput {
    @Builder.Default
    private Integer page = 0;
    @Builder.Default
    private Integer size = 20;
    private String sortField;
    @Builder.Default
    private String sortOrder = "ASC";
}