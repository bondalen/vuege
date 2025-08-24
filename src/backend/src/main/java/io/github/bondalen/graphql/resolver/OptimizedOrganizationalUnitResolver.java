package io.github.bondalen.graphql.resolver;

import io.github.bondalen.entity.OrganizationalUnit;
import io.github.bondalen.entity.Position;
import io.github.bondalen.entity.GeoPoint;
import io.github.bondalen.entity.HistoricalPeriod;
import io.github.bondalen.graphql.service.OrganizationalUnitService;
import io.github.bondalen.graphql.service.PositionService;
import io.github.bondalen.graphql.service.GeoPointService;
import io.github.bondalen.graphql.service.HistoricalPeriodService;
import lombok.RequiredArgsConstructor;
import lombok.extern.slf4j.Slf4j;
import org.springframework.cache.annotation.Cacheable;
import org.springframework.graphql.data.method.annotation.SchemaMapping;
import org.springframework.stereotype.Controller;
import reactor.core.publisher.Flux;
import reactor.core.publisher.Mono;
import io.micrometer.core.annotation.Timed;

/**
 * Оптимизированный GraphQL Resolver для организационных единиц
 */
@Controller
@RequiredArgsConstructor
@Slf4j
public class OptimizedOrganizationalUnitResolver {

    private final OrganizationalUnitService organizationalUnitService;
    private final PositionService positionService;
    private final GeoPointService geoPointService;
    private final HistoricalPeriodService historicalPeriodService;

    /**
     * Получить родительскую организационную единицу с кэшированием
     */
    @SchemaMapping(typeName = "OrganizationalUnit", field = "parentUnit")
    @Timed(value = "graphql.resolver.parent_unit", description = "Time to resolve parent unit")
    @Cacheable(value = "organizationalUnits", key = "#unit.parentUnitId")
    public Mono<OrganizationalUnit> getParentUnit(OrganizationalUnit unit) {
        if (unit.getParentUnitId() == null) {
            return Mono.empty();
        }
        log.debug("Fetching parent unit for organizational unit: {}", unit.getId());
        return organizationalUnitService.findById(unit.getParentUnitId());
    }

    /**
     * Получить дочерние организационные единицы с кэшированием
     */
    @SchemaMapping(typeName = "OrganizationalUnit", field = "childUnits")
    @Timed(value = "graphql.resolver.child_units", description = "Time to resolve child units")
    @Cacheable(value = "organizationalUnits", key = "'child_' + #unit.id")
    public Flux<OrganizationalUnit> getChildUnits(OrganizationalUnit unit) {
        log.debug("Fetching child units for organizational unit: {}", unit.getId());
        return organizationalUnitService.findChildUnits(unit.getId());
    }

    /**
     * Получить должности в организационной единице с кэшированием
     */
    @SchemaMapping(typeName = "OrganizationalUnit", field = "positions")
    @Timed(value = "graphql.resolver.positions", description = "Time to resolve positions")
    @Cacheable(value = "positions", key = "'org_' + #unit.id")
    public Flux<Position> getPositions(OrganizationalUnit unit) {
        log.debug("Fetching positions for organizational unit: {}", unit.getId());
        return positionService.findByOrganizationId(unit.getId());
    }

    /**
     * Получить географическую точку с кэшированием
     */
    @SchemaMapping(typeName = "OrganizationalUnit", field = "location")
    @Timed(value = "graphql.resolver.location", description = "Time to resolve location")
    @Cacheable(value = "geoPoints", key = "#unit.locationId")
    public Mono<GeoPoint> getLocation(OrganizationalUnit unit) {
        if (unit.getLocationId() == null) {
            return Mono.empty();
        }
        log.debug("Fetching location for organizational unit: {}", unit.getId());
        return geoPointService.findById(unit.getLocationId());
    }

    /**
     * Получить исторический период с кэшированием
     */
    @SchemaMapping(typeName = "OrganizationalUnit", field = "historicalPeriod")
    @Timed(value = "graphql.resolver.historical_period", description = "Time to resolve historical period")
    @Cacheable(value = "historicalPeriods", key = "#unit.historicalPeriodId")
    public Mono<HistoricalPeriod> getHistoricalPeriod(OrganizationalUnit unit) {
        log.debug("Fetching historical period for organizational unit: {}", unit.getId());
        return historicalPeriodService.findById(unit.getHistoricalPeriodId());
    }
}