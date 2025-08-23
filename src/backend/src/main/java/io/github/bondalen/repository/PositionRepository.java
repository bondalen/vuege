package io.github.bondalen.repository;

import io.github.bondalen.entity.Position;
import org.springframework.data.repository.reactive.ReactiveCrudRepository;
import org.springframework.stereotype.Repository;
import reactor.core.publisher.Flux;

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
}