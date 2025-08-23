package io.github.bondalen.service;

import io.github.bondalen.entity.OrganizationalUnit;
import io.github.bondalen.repository.OrganizationalUnitRepository;
import lombok.RequiredArgsConstructor;
import lombok.extern.slf4j.Slf4j;
import org.springframework.stereotype.Service;
import reactor.core.publisher.Flux;
import reactor.core.publisher.Mono;

/**
 * Сервис для работы с организационными единицами
 */
@Slf4j
@Service
@RequiredArgsConstructor
public class OrganizationalUnitService {

    private final OrganizationalUnitRepository repository;

    /**
     * Получить все организационные единицы
     */
    public Flux<OrganizationalUnit> findAll() {
        return repository.findAll();
    }

    /**
     * Найти организационную единицу по ID
     */
    public Mono<OrganizationalUnit> findById(Long id) {
        return repository.findById(id);
    }

    /**
     * Создать новую организационную единицу
     */
    public Mono<OrganizationalUnit> create(OrganizationalUnit unit) {
        return repository.save(unit);
    }

    /**
     * Обновить организационную единицу
     */
    public Mono<OrganizationalUnit> update(Long id, OrganizationalUnit unit) {
        return repository.findById(id)
                .flatMap(existing -> {
                    unit.setId(id);
                    return repository.save(unit);
                });
    }

    /**
     * Удалить организационную единицу
     */
    public Mono<Void> delete(Long id) {
        return repository.deleteById(id);
    }

    /**
     * Найти организации по типу
     */
    public Flux<OrganizationalUnit> findByType(io.github.bondalen.entity.OrganizationType type) {
        return repository.findByType(type);
    }

    /**
     * Найти дочерние организации
     */
    public Flux<OrganizationalUnit> findChildren(Long parentId) {
        return repository.findByParentUnitId(parentId);
    }
}