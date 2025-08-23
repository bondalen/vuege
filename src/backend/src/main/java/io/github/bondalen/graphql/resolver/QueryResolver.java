package io.github.bondalen.graphql.resolver;

import io.github.bondalen.entity.*;
import io.github.bondalen.graphql.service.*;
import lombok.RequiredArgsConstructor;
import lombok.extern.slf4j.Slf4j;
import org.springframework.graphql.data.method.annotation.Argument;
import org.springframework.graphql.data.method.annotation.QueryMapping;
import org.springframework.stereotype.Controller;
import reactor.core.publisher.Flux;
import reactor.core.publisher.Mono;

import java.util.Map;

/**
 * GraphQL Query Resolver для основных запросов
 */
@Controller
@RequiredArgsConstructor
@Slf4j
public class QueryResolver {

    private final OrganizationalUnitService organizationalUnitService;
    private final PositionService positionService;
    private final PersonService personService;
    private final HistoricalPeriodService historicalPeriodService;

    // ==================== OrganizationalUnit Queries ====================

    @QueryMapping
    public Flux<OrganizationalUnit> organizationalUnits() {
        log.info("GraphQL Query: organizationalUnits");
        return organizationalUnitService.findAll();
    }

    @QueryMapping
    public Mono<OrganizationalUnit> organizationalUnit(@Argument Long id) {
        log.info("GraphQL Query: organizationalUnit with id={}", id);
        return organizationalUnitService.findById(id);
    }

    // ==================== Position Queries ====================

    @QueryMapping
    public Flux<Position> positions() {
        log.info("GraphQL Query: positions");
        return positionService.findAll();
    }

    @QueryMapping
    public Mono<Position> position(@Argument Long id) {
        log.info("GraphQL Query: position with id={}", id);
        return positionService.findById(id);
    }

    // ==================== Person Queries ====================

    @QueryMapping
    public Flux<Person> persons() {
        log.info("GraphQL Query: persons");
        return personService.findAll();
    }

    @QueryMapping
    public Mono<Person> person(@Argument Long id) {
        log.info("GraphQL Query: person with id={}", id);
        return personService.findById(id);
    }

    // ==================== HistoricalPeriod Queries ====================

    @QueryMapping
    public Flux<HistoricalPeriod> historicalPeriods() {
        log.info("GraphQL Query: historicalPeriods");
        return historicalPeriodService.findAll();
    }

    @QueryMapping
    public Mono<HistoricalPeriod> historicalPeriod(@Argument Long id) {
        log.info("GraphQL Query: historicalPeriod with id={}", id);
        return historicalPeriodService.findById(id);
    }

    // ==================== GIS Queries ====================

    @QueryMapping
    public Flux<OrganizationalUnit> organizationsInRegion(
            @Argument Map<String, Object> bounds,
            @Argument Map<String, Object> timeRange) {
        log.info("GraphQL Query: organizationsInRegion with bounds={}, timeRange={}", bounds, timeRange);
        return organizationalUnitService.findByRegion(bounds, timeRange);
    }
}