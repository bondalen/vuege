package io.github.bondalen.graphql.resolver;

import io.github.bondalen.entity.GeoPoint;
import lombok.RequiredArgsConstructor;
import lombok.extern.slf4j.Slf4j;
import org.springframework.graphql.data.method.annotation.SchemaMapping;
import org.springframework.stereotype.Controller;

import java.util.List;

/**
 * GraphQL Resolver для связей GeoPoint
 */
@Controller
@RequiredArgsConstructor
@Slf4j
public class GeoPointResolver {

    /**
     * Получить координаты как массив [latitude, longitude]
     */
    @SchemaMapping(typeName = "GeoPoint", field = "coordinates")
    public List<Double> getCoordinates(GeoPoint geoPoint) {
        log.debug("Getting coordinates for geo point: {}", geoPoint.getId());
        return List.of(geoPoint.getLatitude(), geoPoint.getLongitude());
    }
}