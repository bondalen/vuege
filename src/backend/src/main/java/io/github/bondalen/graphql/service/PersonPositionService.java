package io.github.bondalen.graphql.service;

import io.github.bondalen.entity.PersonPosition;
import io.github.bondalen.graphql.input.PersonPositionInput;
import io.github.bondalen.repository.PersonPositionRepository;
import lombok.RequiredArgsConstructor;
import lombok.extern.slf4j.Slf4j;
import org.springframework.stereotype.Service;
import reactor.core.publisher.Flux;
import reactor.core.publisher.Mono;

/**
 * Сервис для работы со связями человек-должность
 */
@Service
@RequiredArgsConstructor
@Slf4j
public class PersonPositionService {

    private final PersonPositionRepository personPositionRepository;

    /**
     * Назначить человека на должность
     */
    public Mono<PersonPosition> assign(PersonPositionInput input) {
        log.debug("Assigning person to position with input: {}", input);
        
        PersonPosition personPosition = PersonPosition.builder()
                .personId(input.getPersonId())
                .positionId(input.getPositionId())
                .startDate(input.getStartDate())
                .endDate(input.getEndDate())
                .appointmentType(input.getAppointmentType())
                .source(input.getSource())
                .build();
        
        return personPositionRepository.save(personPosition);
    }

    /**
     * Снять человека с должности
     */
    public Mono<Boolean> remove(Long personId, Long positionId) {
        log.debug("Removing person from position with personId: {}, positionId: {}", personId, positionId);
        
        return personPositionRepository.findByPersonIdAndPositionId(personId, positionId)
                .switchIfEmpty(Mono.error(new RuntimeException("Person position not found")))
                .flatMap(personPosition -> personPositionRepository.deleteById(personPosition.getId()))
                .then(Mono.just(true));
    }

    /**
     * Найти связи по человеку
     */
    public Flux<PersonPosition> findByPersonId(Long personId) {
        log.debug("Finding person positions by person: {}", personId);
        return personPositionRepository.findByPersonId(personId);
    }

    /**
     * Найти связи по должности
     */
    public Flux<PersonPosition> findByPositionId(Long positionId) {
        log.debug("Finding person positions by position: {}", positionId);
        return personPositionRepository.findByPositionId(positionId);
    }
}