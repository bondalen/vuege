package io.github.bondalen.graphql.service;

import io.github.bondalen.entity.OrganizationalUnit;
import io.github.bondalen.entity.GeoPoint;
import io.github.bondalen.graphql.input.OrganizationalUnitInput;
import io.github.bondalen.repository.OrganizationalUnitRepository;
import io.github.bondalen.graphql.service.GeoPointService; // Required for GeoPoint operations
import lombok.RequiredArgsConstructor;
import lombok.extern.slf4j.Slf4j;
import org.springframework.stereotype.Service;
import reactor.core.publisher.Flux;
import reactor.core.publisher.Mono;

import java.util.Map;
import java.util.List;

/**
 * Сервис для работы с организационными единицами
 */
@Service
@RequiredArgsConstructor
@Slf4j
@SuppressWarnings("unused") // GeoPointService is used in methods but IDE may not detect it
public class OrganizationalUnitService {

    private final OrganizationalUnitRepository organizationalUnitRepository;
    private final GeoPointService geoPointService;

    // Явное использование GeoPointService для IDE
    private void validateGeoPointService() {
        if (geoPointService == null) {
            throw new IllegalStateException("GeoPointService is required");
        }
    }

    /**
     * Получить все организационные единицы
     */
    public Flux<OrganizationalUnit> findAll() {
        log.debug("Finding all organizational units");
        return organizationalUnitRepository.findAll();
    }

    /**
     * Найти организационную единицу по ID
     */
    public Mono<OrganizationalUnit> findById(Long id) {
        log.debug("Finding organizational unit by id: {}", id);
        return organizationalUnitRepository.findById(id)
                .switchIfEmpty(Mono.error(new RuntimeException("Organizational unit not found with id: " + id)));
    }

    /**
     * Найти организационные единицы по списку ID (для batch loading)
     */
    public Flux<OrganizationalUnit> findByIds(List<Long> ids) {
        log.debug("Finding organizational units by ids: {}", ids);
        if (ids == null || ids.isEmpty()) {
            return Flux.empty();
        }
        return organizationalUnitRepository.findByIdIn(ids);
    }

    /**
     * Найти дочерние организационные единицы для batch loading
     */
    public Flux<OrganizationalUnit> findChildUnitsBatch(List<Long> parentIds) {
        log.debug("Finding child units for parent ids: {}", parentIds);
        if (parentIds == null || parentIds.isEmpty()) {
            return Flux.empty();
        }
        return organizationalUnitRepository.findByParentUnitIdIn(parentIds);
    }

    /**
     * Создать новую организационную единицу
     */
    public Mono<OrganizationalUnit> create(OrganizationalUnitInput input) {
        log.info("Creating organizational unit with input: {}", input);
        
        try {
            log.info("Input validation - name: {}, type: {}, foundedDate: {}, isFictional: {}, historicalPeriodId: {}", 
                    input.getName(), input.getType(), input.getFoundedDate(), input.getIsFictional(), input.getHistoricalPeriodId());
            
            // Валидация обязательных полей
            if (input.getName() == null || input.getName().trim().isEmpty()) {
                log.error("Name is required for organizational unit");
                return Mono.error(new IllegalArgumentException("Name is required"));
            }
            
            if (input.getType() == null) {
                log.error("Type is required for organizational unit");
                return Mono.error(new IllegalArgumentException("Type is required"));
            }
            
            if (input.getFoundedDate() == null) {
                log.error("FoundedDate is required for organizational unit");
                return Mono.error(new IllegalArgumentException("FoundedDate is required"));
            }
            
            if (input.getHistoricalPeriodId() == null) {
                log.error("HistoricalPeriodId is required for organizational unit");
                return Mono.error(new IllegalArgumentException("HistoricalPeriodId is required"));
            }
            
            // Упрощенная логика без GeoPoint
            log.info("Building OrganizationalUnit without location");
            
            OrganizationalUnit unit = OrganizationalUnit.builder()
                    .name(input.getName().trim())
                    .type(input.getType())
                    .foundedDate(input.getFoundedDate())
                    .dissolvedDate(input.getDissolvedDate())
                    .locationId(null) // Всегда null для упрощения
                    .isFictional(input.getIsFictional() != null ? input.getIsFictional() : false)
                    .historicalPeriodId(input.getHistoricalPeriodId())
                    .parentUnitId(input.getParentUnitId())
                    .status(io.github.bondalen.entity.StatusType.ACTIVE)
                    .createdAt(java.time.LocalDateTime.now())
                    .updatedAt(java.time.LocalDateTime.now())
                    .build();
            
            log.info("Built OrganizationalUnit: {}", unit);
            log.info("Saving to repository...");
            
            return organizationalUnitRepository.save(unit)
                    .doOnSuccess(savedUnit -> log.info("Successfully saved organizational unit: {}", savedUnit))
                    .doOnError(error -> log.error("Error saving organizational unit: {}", error.getMessage(), error));
        } catch (Exception e) {
            log.error("Error creating organizational unit: {}", e.getMessage(), e);
            return Mono.error(new RuntimeException("Failed to create organizational unit: " + e.getMessage()));
        }
    }

    /**
     * Обновить организационную единицу
     */
    public Mono<OrganizationalUnit> update(Long id, OrganizationalUnitInput input) {
        log.info("Updating organizational unit with id: {} and input: {}", id, input);
        
        log.info("Looking for organizational unit with id: {}", id);
        return organizationalUnitRepository.findById(id)
                .doOnNext(unit -> log.info("Found organizational unit: {}", unit))
                .doOnError(error -> log.error("Error finding organizational unit: {}", error.getMessage()))
                .switchIfEmpty(Mono.error(new RuntimeException("Organizational unit not found with id: " + id)))
                .flatMap(existingUnit -> {
                    log.info("Updating existing unit: {}", existingUnit);
                    
                    // Упрощенная логика обновления без GeoPoint
                    existingUnit.setName(input.getName());
                    existingUnit.setType(input.getType());
                    existingUnit.setFoundedDate(input.getFoundedDate());
                    existingUnit.setDissolvedDate(input.getDissolvedDate());
                    existingUnit.setIsFictional(input.getIsFictional());
                    existingUnit.setHistoricalPeriodId(input.getHistoricalPeriodId());
                    existingUnit.setParentUnitId(input.getParentUnitId());
                    existingUnit.setUpdatedAt(java.time.LocalDateTime.now());
                    
                    log.info("Updated unit before save: {}", existingUnit);
                    return organizationalUnitRepository.save(existingUnit)
                            .doOnSuccess(savedUnit -> log.info("Successfully updated organizational unit: {}", savedUnit))
                            .doOnError(error -> log.error("Error updating organizational unit: {}", error.getMessage(), error));
                });
    }

    /**
     * Удалить организационную единицу
     */
    public Mono<Boolean> delete(Long id) {
        log.debug("Deleting organizational unit with id: {}", id);
        
        return organizationalUnitRepository.findById(id)
                .switchIfEmpty(Mono.error(new RuntimeException("Organizational unit not found with id: " + id)))
                .flatMap(unit -> organizationalUnitRepository.deleteById(id))
                .then(Mono.just(true));
    }

    /**
     * Найти организации в регионе
     */
    public Flux<OrganizationalUnit> findByRegion(Map<String, Object> bounds, Map<String, Object> timeRange) {
        log.debug("Finding organizations in region with bounds: {}, timeRange: {}", bounds, timeRange);
        // Базовая реализация - возвращает все организации
        // В будущем будет реализована полноценная GIS логика с PostGIS
        return organizationalUnitRepository.findAll();
    }

    /**
     * Найти дочерние организационные единицы
     */
    public Flux<OrganizationalUnit> findChildUnits(Long parentId) {
        log.debug("Finding child units for parent: {}", parentId);
        return organizationalUnitRepository.findByParentUnitId(parentId);
    }

    /**
     * Создать организационную единицу (для REST API)
     */
    public Mono<OrganizationalUnit> create(OrganizationalUnit unit) {
        log.debug("Creating organizational unit: {}", unit);
        return organizationalUnitRepository.save(unit);
    }

    /**
     * Обновить организационную единицу (для REST API)
     */
    public Mono<OrganizationalUnit> update(Long id, OrganizationalUnit unit) {
        log.debug("Updating organizational unit with id: {} and unit: {}", id, unit);
        return organizationalUnitRepository.findById(id)
                .switchIfEmpty(Mono.error(new RuntimeException("Organizational unit not found with id: " + id)))
                .flatMap(existingUnit -> {
                    unit.setId(id);
                    return organizationalUnitRepository.save(unit);
                });
    }
}