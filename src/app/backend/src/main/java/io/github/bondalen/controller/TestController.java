package io.github.bondalen.controller;

import io.github.bondalen.entity.OrganizationalUnit;
import io.github.bondalen.entity.OrganizationType;
import io.github.bondalen.entity.StatusType;
import io.github.bondalen.graphql.input.OrganizationalUnitInput;
import io.github.bondalen.graphql.service.OrganizationalUnitService;
import io.github.bondalen.repository.OrganizationalUnitRepository;
import lombok.RequiredArgsConstructor;
import lombok.extern.slf4j.Slf4j;
import org.springframework.web.bind.annotation.*;
import reactor.core.publisher.Mono;

import java.time.LocalDate;
import java.time.LocalDateTime;

@RestController
@RequestMapping("/api/test")
@RequiredArgsConstructor
@Slf4j
public class TestController {

    private final OrganizationalUnitService organizationalUnitService;
    private final OrganizationalUnitRepository organizationalUnitRepository;

    @PostMapping("/create-unit")
    public Mono<OrganizationalUnit> createUnit(@RequestBody OrganizationalUnitInput input) {
        log.info("Test controller: Creating unit with input: {}", input);
        return organizationalUnitService.create(input)
                .doOnSuccess(unit -> log.info("Test controller: Successfully created unit: {}", unit))
                .doOnError(error -> log.error("Test controller: Error creating unit: {}", error.getMessage(), error));
    }

    @PostMapping("/create-unit-direct")
    public Mono<OrganizationalUnit> createUnitDirect() {
        log.info("Test controller: Creating unit directly through repository");
        
        OrganizationalUnit unit = OrganizationalUnit.builder()
                .name("Test Direct Unit 2")
                .type(OrganizationType.STATE)
                .foundedDate(LocalDate.of(2024, 1, 1))
                .isFictional(false)
                .historicalPeriodId(5L)
                .status(StatusType.ACTIVE)
                .createdAt(LocalDateTime.now())
                .updatedAt(LocalDateTime.now())
                .build();
        
        log.info("Built unit: {}", unit);
        
        return organizationalUnitRepository.save(unit)
                .doOnSuccess(savedUnit -> log.info("Test controller: Successfully saved unit directly: {}", savedUnit))
                .doOnError(error -> log.error("Test controller: Error saving unit directly: {}", error.getMessage(), error));
    }

    @PostMapping("/create-unit-via-service")
    public Mono<OrganizationalUnit> createUnitViaService() {
        log.info("Test controller: Creating unit via service with hardcoded input");
        
        OrganizationalUnitInput input = OrganizationalUnitInput.builder()
                .name("Test Service Unit")
                .type(OrganizationType.STATE)
                .foundedDate(LocalDate.of(2024, 1, 1))
                .isFictional(false)
                .historicalPeriodId(5L)
                .build();
        
        log.info("Built input: {}", input);
        
        return organizationalUnitService.create(input)
                .doOnSuccess(unit -> log.info("Test controller: Successfully created unit via service: {}", unit))
                .doOnError(error -> log.error("Test controller: Error creating unit via service: {}", error.getMessage(), error));
    }

    @GetMapping("/health")
    public Mono<String> health() {
        return Mono.just("OK");
    }
}