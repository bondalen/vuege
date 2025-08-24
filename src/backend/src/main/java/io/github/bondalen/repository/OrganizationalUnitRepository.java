package io.github.bondalen.repository;

import io.github.bondalen.entity.OrganizationalUnit;
import org.springframework.data.repository.reactive.ReactiveCrudRepository;
import org.springframework.stereotype.Repository;
import reactor.core.publisher.Flux;

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
}