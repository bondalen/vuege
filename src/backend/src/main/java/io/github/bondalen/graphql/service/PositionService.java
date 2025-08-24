package io.github.bondalen.graphql.service;

import com.fasterxml.jackson.core.JsonProcessingException;
import com.fasterxml.jackson.core.type.TypeReference;
import com.fasterxml.jackson.databind.ObjectMapper;
import io.github.bondalen.entity.Position;
import io.github.bondalen.graphql.input.PositionInput;
import io.github.bondalen.repository.PositionRepository;
import lombok.RequiredArgsConstructor;
import lombok.extern.slf4j.Slf4j;
import org.springframework.stereotype.Service;
import reactor.core.publisher.Flux;
import reactor.core.publisher.Mono;

import java.time.LocalDate;
import java.util.List;

/**
 * Сервис для работы с должностями
 */
@Service
@RequiredArgsConstructor
@Slf4j
public class PositionService {

    private final PositionRepository positionRepository;
    private final ObjectMapper objectMapper;

    /**
     * Получить все должности
     */
    public Flux<Position> findAll() {
        log.debug("Finding all positions");
        return positionRepository.findAll();
    }

    /**
     * Найти должность по ID
     */
    public Mono<Position> findById(Long id) {
        log.debug("Finding position by id: {}", id);
        return positionRepository.findById(id)
                .switchIfEmpty(Mono.error(new RuntimeException("Position not found with id: " + id)));
    }

    /**
     * Создать новую должность
     */
    public Mono<Position> create(PositionInput input) {
        log.debug("Creating position with input: {}", input);
        
        String responsibilitiesJson = serializeResponsibilities(input.getResponsibilities());
        
        // Используем текущую дату если createdDate не указана
        LocalDate createdDate = input.getCreatedDate();
        if (createdDate == null) {
            createdDate = LocalDate.now();
            log.debug("Using current date for createdDate: {}", createdDate);
        }
        
        Position position = Position.builder()
                .title(input.getTitle())
                .organizationId(input.getOrganizationId())
                .createdDate(createdDate)
                .abolishedDate(input.getAbolishedDate())
                .hierarchy(input.getHierarchy())
                .responsibilities(responsibilitiesJson)
                .isActive(input.getIsActive())
                .build();
        
        return positionRepository.save(position);
    }

    /**
     * Обновить должность
     */
    public Mono<Position> update(Long id, PositionInput input) {
        log.debug("Updating position with id: {} and input: {}", id, input);
        
        return positionRepository.findById(id)
                .switchIfEmpty(Mono.error(new RuntimeException("Position not found with id: " + id)))
                .flatMap(existingPosition -> {
                    String responsibilitiesJson = serializeResponsibilities(input.getResponsibilities());
                    
                    existingPosition.setTitle(input.getTitle());
                    existingPosition.setOrganizationId(input.getOrganizationId());
                    existingPosition.setCreatedDate(input.getCreatedDate());
                    existingPosition.setAbolishedDate(input.getAbolishedDate());
                    existingPosition.setHierarchy(input.getHierarchy());
                    existingPosition.setResponsibilities(responsibilitiesJson);
                    existingPosition.setIsActive(input.getIsActive());
                    
                    return positionRepository.save(existingPosition);
                });
    }

    /**
     * Удалить должность
     */
    public Mono<Boolean> delete(Long id) {
        log.debug("Deleting position with id: {}", id);
        
        return positionRepository.findById(id)
                .switchIfEmpty(Mono.error(new RuntimeException("Position not found with id: " + id)))
                .flatMap(position -> positionRepository.deleteById(id))
                .then(Mono.just(true));
    }

    /**
     * Сериализовать список обязанностей в JSON
     */
    private String serializeResponsibilities(List<String> responsibilities) {
        try {
            return objectMapper.writeValueAsString(responsibilities);
        } catch (JsonProcessingException e) {
            log.error("Error serializing responsibilities: {}", e.getMessage());
            throw new RuntimeException("Error serializing responsibilities", e);
        }
    }

    /**
     * Десериализовать JSON в список обязанностей
     */
    public List<String> deserializeResponsibilities(String responsibilitiesJson) {
        try {
            return objectMapper.readValue(responsibilitiesJson, new TypeReference<List<String>>() {});
        } catch (JsonProcessingException e) {
            log.error("Error deserializing responsibilities: {}", e.getMessage());
            throw new RuntimeException("Error deserializing responsibilities", e);
        }
    }

    /**
     * Найти должности по организации
     */
    public Flux<Position> findByOrganizationId(Long organizationId) {
        log.debug("Finding positions by organization: {}", organizationId);
        return positionRepository.findByOrganizationId(organizationId);
    }
}