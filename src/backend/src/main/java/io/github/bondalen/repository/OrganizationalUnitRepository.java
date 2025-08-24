package io.github.bondalen.repository;

import io.github.bondalen.entity.OrganizationalUnit;
import io.github.bondalen.entity.StatusType;
import io.github.bondalen.graphql.input.OrganizationFilterInput;
import org.springframework.data.domain.Pageable;
import org.springframework.data.r2dbc.repository.Query;
import org.springframework.data.repository.reactive.ReactiveCrudRepository;
import org.springframework.stereotype.Repository;
import reactor.core.publisher.Flux;
import reactor.core.publisher.Mono;

import java.util.Map;

/**
 * Репозиторий для работы с организационными единицами
 */
@Repository
public interface OrganizationalUnitRepository extends ReactiveCrudRepository<OrganizationalUnit, Long> {
    
    /**
     * Найти организации по типу
     */
    Flux<OrganizationalUnit> findByType(io.github.bondalen.entity.OrganizationType type);
    
    /**
     * Найти организации по историческому периоду
     */
    Flux<OrganizationalUnit> findByHistoricalPeriodId(Long historicalPeriodId);
    
    /**
     * Найти дочерние организации
     */
    Flux<OrganizationalUnit> findByParentUnitId(Long parentUnitId);
    
    /**
     * Найти корневые организации (без родителя)
     */
    Flux<OrganizationalUnit> findByParentUnitIdIsNull();
    
    /**
     * Найти организации по названию (частичное совпадение)
     */
    Flux<OrganizationalUnit> findByNameContainingIgnoreCase(String name);
    
    /**
     * Найти вымышленные/реальные организации
     */
    Flux<OrganizationalUnit> findByIsFictional(Boolean isFictional);
    
    /**
     * Найти дочерние организации по списку родительских ID (для batch loading)
     */
    Flux<OrganizationalUnit> findByParentUnitIdIn(java.util.List<Long> parentUnitIds);
    
    /**
     * Найти организации по списку ID (для batch loading)
     */
    Flux<OrganizationalUnit> findByIdIn(java.util.List<Long> ids);
    
    /**
     * Найти организации по статусу
     */
    Flux<OrganizationalUnit> findByStatus(StatusType status);
    
    /**
     * Найти организации с фильтрами и пагинацией
     */
    @Query("SELECT * FROM organizational_units WHERE " +
           "(:type IS NULL OR type = :type) AND " +
           "(:status IS NULL OR status = :status) AND " +
           "(:isFictional IS NULL OR is_fictional = :isFictional) AND " +
           "(:historicalPeriodId IS NULL OR historical_period_id = :historicalPeriodId) AND " +
           "(:parentUnitId IS NULL OR parent_unit_id = :parentUnitId) AND " +
           "(:searchQuery IS NULL OR name ILIKE '%' || :searchQuery || '%') " +
           "ORDER BY name ASC " +
           "LIMIT :size OFFSET :offset")
    Flux<OrganizationalUnit> findAllWithFilters(OrganizationFilterInput filters, Pageable pageable);
    
    /**
     * Поиск организаций
     */
    @Query("SELECT * FROM organizational_units WHERE " +
           "name ILIKE '%' || :query || '%' OR " +
           "description ILIKE '%' || :query || '%' " +
           "ORDER BY name ASC")
    Flux<OrganizationalUnit> search(String query, Map<String, Object> filters);
    
    /**
     * Получить статистику организаций
     */
    @Query("SELECT " +
           "COUNT(*) as totalCount, " +
           "COUNT(CASE WHEN status = 'ACTIVE' THEN 1 END) as activeCount, " +
           "COUNT(CASE WHEN status = 'DISSOLVED' THEN 1 END) as dissolvedCount " +
           "FROM organizational_units")
    Mono<Map<String, Object>> getStats(Map<String, Object> timeRange);
}