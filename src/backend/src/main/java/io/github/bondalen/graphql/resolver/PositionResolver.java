package io.github.bondalen.graphql.resolver;

import io.github.bondalen.entity.OrganizationalUnit;
import io.github.bondalen.entity.PersonPosition;
import io.github.bondalen.entity.Position;
import io.github.bondalen.graphql.service.OrganizationalUnitService;
import io.github.bondalen.graphql.service.PersonPositionService;
import io.github.bondalen.graphql.service.PositionService;
import lombok.RequiredArgsConstructor;
import lombok.extern.slf4j.Slf4j;
import org.springframework.graphql.data.method.annotation.SchemaMapping;
import org.springframework.stereotype.Controller;
import reactor.core.publisher.Flux;
import reactor.core.publisher.Mono;

import java.util.List;

/**
 * GraphQL Resolver для связей Position
 */
@Controller
@RequiredArgsConstructor
@Slf4j
public class PositionResolver {

    private final OrganizationalUnitService organizationalUnitService;
    private final PersonPositionService personPositionService;
    private final PositionService positionService;

    /**
     * Получить организацию для должности
     */
    @SchemaMapping(typeName = "Position", field = "organization")
    public Mono<OrganizationalUnit> getOrganization(Position position) {
        log.debug("Fetching organization for position: {}", position.getId());
        return organizationalUnitService.findById(position.getOrganizationId());
    }

    /**
     * Получить список обязанностей как массив строк
     */
    @SchemaMapping(typeName = "Position", field = "responsibilities")
    public List<String> getResponsibilities(Position position) {
        log.debug("Getting responsibilities for position: {}", position.getId());
        return positionService.deserializeResponsibilities(position.getResponsibilities());
    }

    /**
     * Получить держателей должности
     */
    @SchemaMapping(typeName = "Position", field = "holders")
    public Flux<PersonPosition> getHolders(Position position) {
        log.debug("Fetching holders for position: {}", position.getId());
        return personPositionService.findByPositionId(position.getId());
    }
}