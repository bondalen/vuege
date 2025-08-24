package io.github.bondalen.graphql.resolver;

import io.github.bondalen.entity.OrganizationalUnit;
import io.github.bondalen.entity.StatusType;
import io.github.bondalen.graphql.input.OrganizationFilterInput;
import io.github.bondalen.graphql.input.PaginationInput;
import io.github.bondalen.graphql.input.PersonFilterInput;
import io.github.bondalen.graphql.input.PositionFilterInput;
import io.github.bondalen.graphql.service.ExtendedQueryService;
import lombok.RequiredArgsConstructor;
import lombok.extern.slf4j.Slf4j;
import org.springframework.graphql.data.method.annotation.Argument;
import org.springframework.graphql.data.method.annotation.QueryMapping;
import org.springframework.stereotype.Controller;
import reactor.core.publisher.Flux;
import reactor.core.publisher.Mono;

import java.util.Map;

@Controller
@RequiredArgsConstructor
@Slf4j
public class ExtendedQueryResolver {

    private final ExtendedQueryService extendedQueryService;

    @QueryMapping
    public Flux<OrganizationalUnit> organizationsByStatus(@Argument StatusType status) {
        log.info("Querying organizations by status: {}", status);
        return extendedQueryService.findOrganizationsByStatus(status);
    }

    @QueryMapping
    public Mono<Map<String, Object>> organizationsWithPagination(
            @Argument Integer page,
            @Argument Integer size,
            @Argument OrganizationFilterInput filters,
            @Argument Map<String, Object> sort) {
        
        PaginationInput pagination = PaginationInput.builder()
                .page(page != null ? page : 0)
                .size(size != null ? size : 20)
                .build();
        
        log.info("Querying organizations with pagination: page={}, size={}, filters={}", page, size, filters);
        return extendedQueryService.findOrganizationsWithPagination(pagination, filters, sort);
    }

    @QueryMapping
    public Mono<Map<String, Object>> personsWithPagination(
            @Argument Integer page,
            @Argument Integer size,
            @Argument PersonFilterInput filters,
            @Argument Map<String, Object> sort) {
        
        PaginationInput pagination = PaginationInput.builder()
                .page(page != null ? page : 0)
                .size(size != null ? size : 20)
                .build();
        
        log.info("Querying persons with pagination: page={}, size={}, filters={}", page, size, filters);
        return extendedQueryService.findPersonsWithPagination(pagination, filters, sort);
    }

    @QueryMapping
    public Mono<Map<String, Object>> positionsWithPagination(
            @Argument Integer page,
            @Argument Integer size,
            @Argument PositionFilterInput filters,
            @Argument Map<String, Object> sort) {
        
        PaginationInput pagination = PaginationInput.builder()
                .page(page != null ? page : 0)
                .size(size != null ? size : 20)
                .build();
        
        log.info("Querying positions with pagination: page={}, size={}, filters={}", page, size, filters);
        return extendedQueryService.findPositionsWithPagination(pagination, filters, sort);
    }

    @QueryMapping
    public Mono<Map<String, Object>> searchOrganizations(
            @Argument String query,
            @Argument Map<String, Object> filters) {
        
        log.info("Searching organizations with query: {}", query);
        return extendedQueryService.searchOrganizations(query, filters);
    }

    @QueryMapping
    public Mono<Map<String, Object>> searchPersons(
            @Argument String query,
            @Argument Map<String, Object> filters) {
        
        log.info("Searching persons with query: {}", query);
        return extendedQueryService.searchPersons(query, filters);
    }

    @QueryMapping
    public Mono<Map<String, Object>> searchPositions(
            @Argument String query,
            @Argument Map<String, Object> filters) {
        
        log.info("Searching positions with query: {}", query);
        return extendedQueryService.searchPositions(query, filters);
    }

    @QueryMapping
    public Mono<Map<String, Object>> organizationStats(@Argument Map<String, Object> timeRange) {
        log.info("Getting organization statistics for time range: {}", timeRange);
        return extendedQueryService.getOrganizationStats(timeRange);
    }

    @QueryMapping
    public Mono<Map<String, Object>> personStats(@Argument Map<String, Object> timeRange) {
        log.info("Getting person statistics for time range: {}", timeRange);
        return extendedQueryService.getPersonStats(timeRange);
    }

    @QueryMapping
    public Mono<Map<String, Object>> positionStats(@Argument Map<String, Object> timeRange) {
        log.info("Getting position statistics for time range: {}", timeRange);
        return extendedQueryService.getPositionStats(timeRange);
    }
}