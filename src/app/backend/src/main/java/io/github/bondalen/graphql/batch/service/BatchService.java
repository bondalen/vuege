package io.github.bondalen.graphql.batch.service;

import io.github.bondalen.entity.OrganizationalUnit;
import io.github.bondalen.graphql.input.OrganizationalUnitInput;
import io.github.bondalen.repository.OrganizationalUnitRepository;
import lombok.RequiredArgsConstructor;
import lombok.extern.slf4j.Slf4j;
import org.springframework.stereotype.Service;
import reactor.core.publisher.Flux;
import reactor.core.publisher.Mono;

import java.util.HashMap;
import java.util.List;
import java.util.Map;

@Service
@RequiredArgsConstructor
@Slf4j
public class BatchService {

    private final OrganizationalUnitRepository organizationalUnitRepository;

    public Flux<OrganizationalUnit> batchCreateOrganizations(List<OrganizationalUnitInput> inputs) {
        log.debug("Processing batch creation of {} organizations", inputs.size());
        
        return Flux.fromIterable(inputs)
                .flatMap(input -> {
                    // Convert input to entity
                    OrganizationalUnit organization = convertInputToEntity(input);
                    return organizationalUnitRepository.save(organization);
                })
                .doOnComplete(() -> log.info("Batch creation completed for {} organizations", inputs.size()));
    }

    public Flux<OrganizationalUnit> batchUpdateOrganizations(List<Map<String, Object>> inputs) {
        log.debug("Processing batch update of {} organizations", inputs.size());
        
        return Flux.fromIterable(inputs)
                .flatMap(input -> {
                    Long id = Long.valueOf((String) input.get("id"));
                    return organizationalUnitRepository.findById(id)
                            .flatMap(existingOrg -> {
                                // Update existing organization with new data
                                OrganizationalUnit updatedOrg = updateEntityFromMap(existingOrg, input);
                                return organizationalUnitRepository.save(updatedOrg);
                            });
                })
                .doOnComplete(() -> log.info("Batch update completed for {} organizations", inputs.size()));
    }

    public Mono<Map<String, Object>> batchDeleteOrganizations(List<String> ids) {
        log.debug("Processing batch deletion of {} organizations", ids.size());
        
        return Flux.fromIterable(ids)
                .flatMap(id -> organizationalUnitRepository.deleteById(Long.valueOf(id)))
                .collectList()
                .flatMap(deletedCount -> {
                    Map<String, Object> result = new HashMap<>();
                    result.put("successCount", deletedCount.size());
                    result.put("failureCount", 0);
                    result.put("errors", List.of());
                    return Mono.just(result);
                })
                .doOnSuccess(result -> log.info("Batch deletion completed: {}", result));
    }

    private OrganizationalUnit convertInputToEntity(OrganizationalUnitInput input) {
        // Conversion logic for OrganizationalUnit
        return OrganizationalUnit.builder()
                .name(input.getName())
                .type(input.getType())
                .foundedDate(input.getFoundedDate())
                .dissolvedDate(input.getDissolvedDate())
                .isFictional(input.getIsFictional())
                .historicalPeriodId(input.getHistoricalPeriodId())
                .parentUnitId(input.getParentUnitId())
                .status(io.github.bondalen.entity.StatusType.ACTIVE)
                .build();
    }

    private OrganizationalUnit updateEntityFromMap(OrganizationalUnit existing, Map<String, Object> updates) {
        // Update logic for OrganizationalUnit
        if (updates.containsKey("name")) {
            existing.setName((String) updates.get("name"));
        }
        if (updates.containsKey("type")) {
            existing.setType((io.github.bondalen.entity.OrganizationType) updates.get("type"));
        }
        // Add more fields as needed
        return existing;
    }
}