package io.github.bondalen.graphql.resolver;

import io.github.bondalen.entity.Person;
import io.github.bondalen.entity.PersonPosition;
import io.github.bondalen.entity.HistoricalPeriod;
import io.github.bondalen.graphql.service.PersonPositionService;
import io.github.bondalen.graphql.service.HistoricalPeriodService;
import reactor.core.publisher.Mono;
import lombok.RequiredArgsConstructor;
import lombok.extern.slf4j.Slf4j;
import org.springframework.graphql.data.method.annotation.SchemaMapping;
import org.springframework.stereotype.Controller;
import reactor.core.publisher.Flux;

/**
 * GraphQL Resolver для связей Person
 */
@Controller
@RequiredArgsConstructor
@Slf4j
public class PersonResolver {

    private final PersonPositionService personPositionService;
    private final HistoricalPeriodService historicalPeriodService;

    /**
     * Получить должности человека
     */
    @SchemaMapping(typeName = "Person", field = "positions")
    public Flux<PersonPosition> getPositions(Person person) {
        log.debug("Fetching positions for person: {}", person.getId());
        return personPositionService.findByPersonId(person.getId());
    }

    /**
     * Получить исторический период
     */
    @SchemaMapping(typeName = "Person", field = "historicalPeriod")
    public Mono<HistoricalPeriod> getHistoricalPeriod(Person person) {
        log.debug("Fetching historical period for person: {}", person.getId());
        return historicalPeriodService.findById(person.getHistoricalPeriodId());
    }
}