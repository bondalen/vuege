package io.github.bondalen.graphql.service;

import io.github.bondalen.entity.HistoricalPeriod;
import io.github.bondalen.repository.HistoricalPeriodRepository;
import lombok.RequiredArgsConstructor;
import lombok.extern.slf4j.Slf4j;
import org.springframework.stereotype.Service;
import reactor.core.publisher.Flux;
import reactor.core.publisher.Mono;

/**
 * Сервис для работы с историческими периодами
 */
@Service
@RequiredArgsConstructor
@Slf4j
public class HistoricalPeriodService {

    private final HistoricalPeriodRepository historicalPeriodRepository;

    /**
     * Получить все исторические периоды
     */
    public Flux<HistoricalPeriod> findAll() {
        log.debug("Finding all historical periods");
        return historicalPeriodRepository.findAll();
    }

    /**
     * Найти исторический период по ID
     */
    public Mono<HistoricalPeriod> findById(Long id) {
        log.debug("Finding historical period by id: {}", id);
        return historicalPeriodRepository.findById(id)
                .switchIfEmpty(Mono.error(new RuntimeException("Historical period not found with id: " + id)));
    }
}