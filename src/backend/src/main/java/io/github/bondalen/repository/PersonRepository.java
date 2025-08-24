package io.github.bondalen.repository;

import io.github.bondalen.entity.Person;
import org.springframework.data.r2dbc.repository.Query;
import org.springframework.data.repository.reactive.ReactiveCrudRepository;
import org.springframework.stereotype.Repository;
import reactor.core.publisher.Flux;
import reactor.core.publisher.Mono;

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
    
    /**
     * Найти людей с фильтрами и пагинацией
     */
    @Query("SELECT * FROM persons WHERE " +
           "(:nationality IS NULL OR nationality = :nationality) AND " +
           "(:isFictional IS NULL OR is_fictional = :isFictional) AND " +
           "(:historicalPeriodId IS NULL OR historical_period_id = :historicalPeriodId) AND " +
           "(:searchQuery IS NULL OR name ILIKE '%' || :searchQuery || '%') " +
           "ORDER BY name ASC " +
           "LIMIT :size OFFSET :offset")
    Flux<Person> findAllWithFilters(io.github.bondalen.graphql.input.PersonFilterInput filters, org.springframework.data.domain.Pageable pageable);
    
    /**
     * Поиск людей
     */
    @Query("SELECT * FROM persons WHERE " +
           "name ILIKE '%' || :query || '%' OR " +
           "biography ILIKE '%' || :query || '%' " +
           "ORDER BY name ASC")
    Flux<Person> search(String query, java.util.Map<String, Object> filters);
    
    /**
     * Получить статистику людей
     */
    @Query("SELECT " +
           "COUNT(*) as totalCount, " +
           "COUNT(CASE WHEN is_fictional = false THEN 1 END) as activeCount " +
           "FROM persons")
    Mono<java.util.Map<String, Object>> getStats(java.util.Map<String, Object> timeRange);
}