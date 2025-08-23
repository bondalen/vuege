package io.github.bondalen.graphql.service;

import io.github.bondalen.entity.GeoPoint;
import io.github.bondalen.graphql.input.GeoPointInput;
import io.github.bondalen.repository.GeoPointRepository;
import lombok.RequiredArgsConstructor;
import lombok.extern.slf4j.Slf4j;
import org.springframework.stereotype.Service;
import reactor.core.publisher.Flux;
import reactor.core.publisher.Mono;

/**
 * Сервис для работы с географическими точками
 */
@Service
@RequiredArgsConstructor
@Slf4j
public class GeoPointService {

    private final GeoPointRepository geoPointRepository;

    /**
     * Получить все географические точки
     */
    public Flux<GeoPoint> findAll() {
        log.debug("Finding all geo points");
        return geoPointRepository.findAll();
    }

    /**
     * Найти географическую точку по ID
     */
    public Mono<GeoPoint> findById(Long id) {
        log.debug("Finding geo point by id: {}", id);
        return geoPointRepository.findById(id)
                .switchIfEmpty(Mono.error(new RuntimeException("Geo point not found with id: " + id)));
    }

    /**
     * Создать новую географическую точку
     */
    public Mono<GeoPoint> createGeoPoint(GeoPointInput input) {
        log.debug("Creating geo point with input: {}", input);
        
        GeoPoint geoPoint = GeoPoint.builder()
                .latitude(input.getLatitude())
                .longitude(input.getLongitude())
                .elevation(input.getElevation())
                .accuracy(input.getAccuracy())
                .build();
        
        return geoPointRepository.save(geoPoint);
    }
}