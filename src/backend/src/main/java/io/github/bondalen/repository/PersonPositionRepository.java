package io.github.bondalen.repository;

import io.github.bondalen.entity.PersonPosition;
import org.springframework.data.repository.reactive.ReactiveCrudRepository;
import org.springframework.stereotype.Repository;
import reactor.core.publisher.Flux;

/**
 * Репозиторий для работы со связями человек-должность
 */
@Repository
public interface PersonPositionRepository extends ReactiveCrudRepository<PersonPosition, Long> {
    
    /**
     * Найти все должности человека
     */
    Flux<PersonPosition> findByPersonId(Long personId);
    
    /**
     * Найти всех людей на должности
     */
    Flux<PersonPosition> findByPositionId(Long positionId);
    
    /**
     * Найти активные назначения (без даты окончания)
     */
    Flux<PersonPosition> findByEndDateIsNull();
    
    /**
     * Найти назначения по типу
     */
    Flux<PersonPosition> findByAppointmentType(io.github.bondalen.entity.AppointmentType appointmentType);
    
    /**
     * Найти назначения в заданном временном диапазоне
     */
    Flux<PersonPosition> findByStartDateBetween(java.time.LocalDate startDate, java.time.LocalDate endDate);
}