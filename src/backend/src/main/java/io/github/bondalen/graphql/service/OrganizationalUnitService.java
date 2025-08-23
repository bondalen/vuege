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
     * Создать новую организационную единицу
     */
    public Mono<OrganizationalUnit> create(OrganizationalUnitInput input) {
        log.debug("Creating organizational unit with input: {}", input);
        validateGeoPointService();
        
        // Создаем GeoPoint если указан
        Mono<Long> locationIdMono;
        if (input.getLocation() != null) {
            locationIdMono = geoPointService.createGeoPoint(input.getLocation()).map(GeoPoint::getId);
        } else {
            locationIdMono = Mono.just(null);
        }
        
        return locationIdMono.flatMap(locationId -> {
            OrganizationalUnit unit = OrganizationalUnit.builder()
                    .name(input.getName())
                    .type(input.getType())
                    .foundedDate(input.getFoundedDate())
                    .dissolvedDate(input.getDissolvedDate())
                    .locationId(locationId)
                    .isFictional(input.getIsFictional())
                    .historicalPeriodId(input.getHistoricalPeriodId())
                    .parentUnitId(input.getParentUnitId())
                    .build();
            
            return organizationalUnitRepository.save(unit);
        });
    }

    /**
     * Обновить организационную единицу
     */
    public Mono<OrganizationalUnit> update(Long id, OrganizationalUnitInput input) {
        log.debug("Updating organizational unit with id: {} and input: {}", id, input);
        validateGeoPointService();
        
        return organizationalUnitRepository.findById(id)
                .switchIfEmpty(Mono.error(new RuntimeException("Organizational unit not found with id: " + id)))
                .flatMap(existingUnit -> {
                    // Обновляем GeoPoint если указан
                    Mono<Long> locationIdMono;
                    if (input.getLocation() != null) {
                        locationIdMono = geoPointService.createGeoPoint(input.getLocation()).map(GeoPoint::getId);
                    } else {
                        locationIdMono = Mono.just(existingUnit.getLocationId());
                    }
                    
                    return locationIdMono.flatMap(locationId -> {
                        existingUnit.setLocationId(locationId);
                        existingUnit.setName(input.getName());
                        existingUnit.setType(input.getType());
                        existingUnit.setFoundedDate(input.getFoundedDate());
                        existingUnit.setDissolvedDate(input.getDissolvedDate());
                        existingUnit.setIsFictional(input.getIsFictional());
                        existingUnit.setHistoricalPeriodId(input.getHistoricalPeriodId());
                        existingUnit.setParentUnitId(input.getParentUnitId());
                        
                        return organizationalUnitRepository.save(existingUnit);
                    });
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