package io.github.bondalen.graphql.resolver;

import io.github.bondalen.entity.*;
import io.github.bondalen.graphql.service.*;
import io.github.bondalen.graphql.input.*;
import lombok.RequiredArgsConstructor;
import lombok.extern.slf4j.Slf4j;
import org.springframework.graphql.data.method.annotation.Argument;
import org.springframework.graphql.data.method.annotation.MutationMapping;
import org.springframework.stereotype.Controller;
import reactor.core.publisher.Mono;

/**
 * GraphQL Mutation Resolver для операций изменения данных
 */
@Controller
@RequiredArgsConstructor
@Slf4j
public class MutationResolver {

    private final OrganizationalUnitService organizationalUnitService;
    private final PositionService positionService;
    private final PersonService personService;
    private final PersonPositionService personPositionService;

    // ==================== OrganizationalUnit Mutations ====================

    @MutationMapping
    public Mono<OrganizationalUnit> createOrganizationalUnit(
            @Argument OrganizationalUnitInput input) {
        log.info("GraphQL Mutation: createOrganizationalUnit with input={}", input);
        
        // Детальное логирование входных данных
        if (input != null) {
            log.info("Input details - name: '{}', type: {}, foundedDate: {}, dissolvedDate: {}, isFictional: {}, historicalPeriodId: {}, parentUnitId: {}", 
                    input.getName(), input.getType(), input.getFoundedDate(), input.getDissolvedDate(), 
                    input.getIsFictional(), input.getHistoricalPeriodId(), input.getParentUnitId());
        } else {
            log.error("Input is null!");
            return Mono.error(new IllegalArgumentException("Input cannot be null"));
        }
        
        return organizationalUnitService.create(input)
                .doOnSuccess(result -> log.info("Successfully created organizational unit: {}", result))
                .doOnError(error -> log.error("Error creating organizational unit: {}", error.getMessage(), error));
    }

    @MutationMapping
    public Mono<OrganizationalUnit> updateOrganizationalUnit(
            @Argument Long id,
            @Argument OrganizationalUnitInput input) {
        log.info("GraphQL Mutation: updateOrganizationalUnit with id={}, input={}", id, input);
        return organizationalUnitService.update(id, input);
    }

    @MutationMapping
    public Mono<Boolean> deleteOrganizationalUnit(@Argument Long id) {
        log.info("GraphQL Mutation: deleteOrganizationalUnit with id={}", id);
        return organizationalUnitService.delete(id);
    }

    // ==================== Position Mutations ====================

    @MutationMapping
    public Mono<Position> createPosition(@Argument PositionInput input) {
        log.info("GraphQL Mutation: createPosition with input={}", input);
        return positionService.create(input);
    }

    @MutationMapping
    public Mono<Position> updatePosition(
            @Argument Long id,
            @Argument PositionInput input) {
        log.info("GraphQL Mutation: updatePosition with id={}, input={}", id, input);
        return positionService.update(id, input);
    }

    @MutationMapping
    public Mono<Boolean> deletePosition(@Argument Long id) {
        log.info("GraphQL Mutation: deletePosition with id={}", id);
        return positionService.delete(id);
    }

    // ==================== Person Mutations ====================

    @MutationMapping
    public Mono<Person> createPerson(@Argument PersonInput input) {
        log.info("GraphQL Mutation: createPerson with input={}", input);
        return personService.create(input);
    }

    @MutationMapping
    public Mono<Person> updatePerson(
            @Argument Long id,
            @Argument PersonInput input) {
        log.info("GraphQL Mutation: updatePerson with id={}, input={}", id, input);
        return personService.update(id, input);
    }

    @MutationMapping
    public Mono<Boolean> deletePerson(@Argument Long id) {
        log.info("GraphQL Mutation: deletePerson with id={}", id);
        return personService.delete(id);
    }

    // ==================== PersonPosition Mutations ====================

    @MutationMapping
    public Mono<PersonPosition> assignPersonToPosition(
            @Argument PersonPositionInput input) {
        log.info("GraphQL Mutation: assignPersonToPosition with input={}", input);
        return personPositionService.assign(input);
    }

    @MutationMapping
    public Mono<Boolean> removePersonFromPosition(
            @Argument Long personId,
            @Argument Long positionId) {
        log.info("GraphQL Mutation: removePersonFromPosition with personId={}, positionId={}", 
                personId, positionId);
        return personPositionService.remove(personId, positionId);
    }
}