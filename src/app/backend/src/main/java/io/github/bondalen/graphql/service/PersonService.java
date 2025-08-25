package io.github.bondalen.graphql.service;

import io.github.bondalen.entity.Person;
import io.github.bondalen.graphql.input.PersonInput;
import io.github.bondalen.repository.PersonRepository;
import lombok.RequiredArgsConstructor;
import lombok.extern.slf4j.Slf4j;
import org.springframework.stereotype.Service;
import reactor.core.publisher.Flux;
import reactor.core.publisher.Mono;

/**
 * Сервис для работы с людьми
 */
@Service
@RequiredArgsConstructor
@Slf4j
public class PersonService {

    private final PersonRepository personRepository;

    /**
     * Получить всех людей
     */
    public Flux<Person> findAll() {
        log.debug("Finding all persons");
        return personRepository.findAll();
    }

    /**
     * Найти человека по ID
     */
    public Mono<Person> findById(Long id) {
        log.debug("Finding person by id: {}", id);
        return personRepository.findById(id)
                .switchIfEmpty(Mono.error(new RuntimeException("Person not found with id: " + id)));
    }

    /**
     * Создать нового человека
     */
    public Mono<Person> create(PersonInput input) {
        log.debug("Creating person with input: {}", input);
        
        Person person = Person.builder()
                .name(input.getName())
                .birthDate(input.getBirthDate())
                .deathDate(input.getDeathDate())
                .nationality(input.getNationality())
                .isFictional(input.getIsFictional())
                .historicalPeriodId(input.getHistoricalPeriodId())
                .build();
        
        return personRepository.save(person);
    }

    /**
     * Обновить человека
     */
    public Mono<Person> update(Long id, PersonInput input) {
        log.debug("Updating person with id: {} and input: {}", id, input);
        
        return personRepository.findById(id)
                .switchIfEmpty(Mono.error(new RuntimeException("Person not found with id: " + id)))
                .flatMap(existingPerson -> {
                    existingPerson.setName(input.getName());
                    existingPerson.setBirthDate(input.getBirthDate());
                    existingPerson.setDeathDate(input.getDeathDate());
                    existingPerson.setNationality(input.getNationality());
                    existingPerson.setIsFictional(input.getIsFictional());
                    existingPerson.setHistoricalPeriodId(input.getHistoricalPeriodId());
                    
                    return personRepository.save(existingPerson);
                });
    }

    /**
     * Удалить человека
     */
    public Mono<Boolean> delete(Long id) {
        log.debug("Deleting person with id: {}", id);
        
        return personRepository.findById(id)
                .switchIfEmpty(Mono.error(new RuntimeException("Person not found with id: " + id)))
                .flatMap(person -> personRepository.deleteById(id))
                .then(Mono.just(true));
    }
}