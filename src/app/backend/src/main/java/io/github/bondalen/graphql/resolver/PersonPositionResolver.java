package io.github.bondalen.graphql.resolver;

import io.github.bondalen.entity.Person;
import io.github.bondalen.entity.PersonPosition;
import io.github.bondalen.entity.Position;
import io.github.bondalen.graphql.service.PersonService;
import io.github.bondalen.graphql.service.PositionService;
import lombok.RequiredArgsConstructor;
import lombok.extern.slf4j.Slf4j;
import org.springframework.graphql.data.method.annotation.SchemaMapping;
import org.springframework.stereotype.Controller;
import reactor.core.publisher.Mono;

/**
 * GraphQL Resolver для связей PersonPosition
 */
@Controller
@RequiredArgsConstructor
@Slf4j
public class PersonPositionResolver {

    private final PersonService personService;
    private final PositionService positionService;

    /**
     * Получить человека для связи
     */
    @SchemaMapping(typeName = "PersonPosition", field = "person")
    public Mono<Person> getPerson(PersonPosition personPosition) {
        log.debug("Fetching person for person position: {}", personPosition.getId());
        return personService.findById(personPosition.getPersonId());
    }

    /**
     * Получить должность для связи
     */
    @SchemaMapping(typeName = "PersonPosition", field = "position")
    public Mono<Position> getPosition(PersonPosition personPosition) {
        log.debug("Fetching position for person position: {}", personPosition.getId());
        return positionService.findById(personPosition.getPositionId());
    }
}