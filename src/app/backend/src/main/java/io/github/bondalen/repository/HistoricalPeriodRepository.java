package io.github.bondalen.repository;

import io.github.bondalen.entity.HistoricalPeriod;
import org.springframework.data.repository.reactive.ReactiveCrudRepository;
import org.springframework.stereotype.Repository;
import reactor.core.publisher.Flux;

/**
 * Репозиторий для работы с историческими периодами
 */
@Repository
public interface HistoricalPeriodRepository extends ReactiveCrudRepository<HistoricalPeriod, Long> {
    
    /**
     * Найти периоды по эпохе
     */
    Flux<HistoricalPeriod> findByEra(io.github.bondalen.entity.Era era);
    
    /**
     * Найти периоды в заданном временном диапазоне
     */
    Flux<HistoricalPeriod> findByStartDateBetween(java.time.LocalDate startDate, java.time.LocalDate endDate);
}