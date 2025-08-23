package io.github.bondalen.repository;

import io.github.bondalen.entity.Person;
import org.springframework.data.repository.reactive.ReactiveCrudRepository;
import org.springframework.stereotype.Repository;
import reactor.core.publisher.Flux;

/**
 * Репозиторий для работы с людьми
 */
@Repository
public interface PersonRepository extends ReactiveCrudRepository<Person, Long> {
    
    /**
     * Найти людей по национальности
     */
    Flux<Person> findByNationality(String nationality);
    
    /**
     * Найти людей по историческому периоду
     */
    Flux<Person> findByHistoricalPeriodId(Long historicalPeriodId);
    
    /**
     * Найти вымышленных/реальных людей
     */
    Flux<Person> findByIsFictional(Boolean isFictional);
    
    /**
     * Найти людей по имени (частичное совпадение)
     */
    Flux<Person> findByNameContainingIgnoreCase(String name);
}