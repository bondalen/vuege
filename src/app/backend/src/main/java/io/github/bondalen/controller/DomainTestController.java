package io.github.bondalen.controller;

import io.github.bondalen.entity.OrganizationalUnit;
import io.github.bondalen.graphql.service.OrganizationalUnitService;
import lombok.RequiredArgsConstructor;
import lombok.extern.slf4j.Slf4j;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;
import reactor.core.publisher.Flux;
import reactor.core.publisher.Mono;

/**
 * Тестовый контроллер для проверки доменной модели
 */
@Slf4j
@RestController
@RequestMapping("/api/domain-test")
@RequiredArgsConstructor
public class DomainTestController {

    private final OrganizationalUnitService organizationalUnitService;

    /**
     * Получить все организационные единицы
     */
    @GetMapping("/organizational-units")
    public Flux<OrganizationalUnit> getAllOrganizationalUnits() {
        log.info("Запрос всех организационных единиц");
        return organizationalUnitService.findAll();
    }

    /**
     * Получить организационную единицу по ID
     */
    @GetMapping("/organizational-units/{id}")
    public Mono<ResponseEntity<OrganizationalUnit>> getOrganizationalUnitById(@PathVariable Long id) {
        log.info("Запрос организационной единицы с ID: {}", id);
        return organizationalUnitService.findById(id)
                .map(ResponseEntity::ok)
                .defaultIfEmpty(ResponseEntity.notFound().build());
    }

    /**
     * Создать новую организационную единицу
     */
    @PostMapping("/organizational-units")
    public Mono<OrganizationalUnit> createOrganizationalUnit(@RequestBody OrganizationalUnit unit) {
        log.info("Создание новой организационной единицы: {}", unit.getName());
        return organizationalUnitService.create(unit);
    }

    /**
     * Обновить организационную единицу
     */
    @PutMapping("/organizational-units/{id}")
    public Mono<ResponseEntity<OrganizationalUnit>> updateOrganizationalUnit(
            @PathVariable Long id, 
            @RequestBody OrganizationalUnit unit) {
        log.info("Обновление организационной единицы с ID: {}", id);
        return organizationalUnitService.update(id, unit)
                .map(ResponseEntity::ok)
                .defaultIfEmpty(ResponseEntity.notFound().build());
    }

    /**
     * Удалить организационную единицу
     */
    @DeleteMapping("/organizational-units/{id}")
    public Mono<ResponseEntity<Void>> deleteOrganizationalUnit(@PathVariable Long id) {
        log.info("Удаление организационной единицы с ID: {}", id);
        return organizationalUnitService.delete(id)
                .then(Mono.just(ResponseEntity.ok().<Void>build()));
    }

    /**
     * Получить дочерние организации
     */
    @GetMapping("/organizational-units/{id}/children")
    public Flux<OrganizationalUnit> getChildren(@PathVariable Long id) {
        log.info("Получение дочерних организаций для ID: {}", id);
        return organizationalUnitService.findChildUnits(id);
    }
}