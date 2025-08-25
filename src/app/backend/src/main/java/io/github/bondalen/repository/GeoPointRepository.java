package io.github.bondalen.repository;

import io.github.bondalen.entity.GeoPoint;
import org.springframework.data.repository.reactive.ReactiveCrudRepository;
import org.springframework.stereotype.Repository;
import reactor.core.publisher.Flux;

/**
 * Репозиторий для работы с географическими точками
 */
@Repository
public interface GeoPointRepository extends ReactiveCrudRepository<GeoPoint, Long> {
    
    /**
     * Найти точки в заданном прямоугольнике
     */
    Flux<GeoPoint> findByLatitudeBetweenAndLongitudeBetween(
        Double minLat, Double maxLat, Double minLng, Double maxLng);
    
    /**
     * Найти точки по точности
     */
    Flux<GeoPoint> findByAccuracy(io.github.bondalen.entity.AccuracyType accuracy);
}