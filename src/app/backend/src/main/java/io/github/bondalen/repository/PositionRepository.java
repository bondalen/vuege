package io.github.bondalen.repository;

import io.github.bondalen.entity.Position;
import org.springframework.data.r2dbc.repository.Query;
import org.springframework.data.repository.reactive.ReactiveCrudRepository;
import org.springframework.stereotype.Repository;
import reactor.core.publisher.Flux;
import reactor.core.publisher.Mono;

/**
 * Репозиторий для работы с должностями
 */
@Repository
public interface PositionRepository extends ReactiveCrudRepository<Position, Long> {
    
    /**
     * Найти должности по организации
     */
    Flux<Position> findByOrganizationId(Long organizationId);
    
    /**
     * Найти должности по иерархии
     */
    Flux<Position> findByHierarchy(io.github.bondalen.entity.PositionHierarchy hierarchy);
    
    /**
     * Найти активные должности
     */
    Flux<Position> findByIsActive(Boolean isActive);
    
    /**
     * Найти должности по названию (частичное совпадение)
     */
    Flux<Position> findByTitleContainingIgnoreCase(String title);
    
    /**
     * Найти должности в организации по иерархии
     */
    Flux<Position> findByOrganizationIdAndHierarchy(Long organizationId, 
                                                   io.github.bondalen.entity.PositionHierarchy hierarchy);
    
    /**
     * Найти должности с фильтрами и пагинацией
     */
    @Query("SELECT * FROM positions WHERE " +
           "(:hierarchy IS NULL OR hierarchy = :hierarchy) AND " +
           "(:isActive IS NULL OR is_active = :isActive) AND " +
           "(:organizationId IS NULL OR organization_id = :organizationId) AND " +
           "(:searchQuery IS NULL OR title ILIKE '%' || :searchQuery || '%') " +
           "ORDER BY title ASC " +
           "LIMIT :size OFFSET :offset")
    Flux<Position> findAllWithFilters(io.github.bondalen.graphql.input.PositionFilterInput filters, org.springframework.data.domain.Pageable pageable);
    
    /**
     * Поиск должностей
     */
    @Query("SELECT * FROM positions WHERE " +
           "title ILIKE '%' || :query || '%' " +
           "ORDER BY title ASC")
    Flux<Position> search(String query, java.util.Map<String, Object> filters);
    
    /**
     * Получить статистику должностей
     */
    @Query("SELECT " +
           "COUNT(*) as totalCount, " +
           "COUNT(CASE WHEN is_active = true THEN 1 END) as activeCount " +
           "FROM positions")
    Mono<java.util.Map<String, Object>> getStats(java.util.Map<String, Object> timeRange);
}