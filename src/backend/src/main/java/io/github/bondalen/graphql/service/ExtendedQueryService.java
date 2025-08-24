package io.github.bondalen.graphql.service;

import io.github.bondalen.entity.OrganizationalUnit;

import io.github.bondalen.entity.StatusType;
import io.github.bondalen.graphql.input.OrganizationFilterInput;
import io.github.bondalen.graphql.input.PaginationInput;
import io.github.bondalen.graphql.input.PersonFilterInput;
import io.github.bondalen.graphql.input.PositionFilterInput;
import io.github.bondalen.repository.OrganizationalUnitRepository;
import io.github.bondalen.repository.PersonRepository;
import io.github.bondalen.repository.PositionRepository;
import lombok.RequiredArgsConstructor;
import lombok.extern.slf4j.Slf4j;
import org.springframework.data.domain.PageRequest;
import org.springframework.data.domain.Pageable;
import org.springframework.data.domain.Sort;
import org.springframework.stereotype.Service;
import reactor.core.publisher.Flux;
import reactor.core.publisher.Mono;


import java.util.HashMap;
import java.util.Map;

@Service
@RequiredArgsConstructor
@Slf4j
public class ExtendedQueryService {

    private final OrganizationalUnitRepository organizationalUnitRepository;
    private final PersonRepository personRepository;
    private final PositionRepository positionRepository;

    public Flux<OrganizationalUnit> findOrganizationsByStatus(StatusType status) {
        log.debug("Finding organizations by status: {}", status);
        return organizationalUnitRepository.findByStatus(status);
    }

    public Mono<Map<String, Object>> findOrganizationsWithPagination(
            PaginationInput pagination,
            OrganizationFilterInput filters,
            Map<String, Object> sort) {
        
        log.debug("Finding organizations with pagination: pagination={}, filters={}, sort={}", 
                pagination, filters, sort);
        
        Pageable pageable = createPageable(pagination, sort);
        
        return organizationalUnitRepository.findAllWithFilters(filters, pageable)
                .collectList()
                .flatMap(organizations -> {
                    Map<String, Object> result = new HashMap<>();
                    result.put("items", organizations);
                    result.put("totalCount", organizations.size());
                    result.put("page", pagination.getPage());
                    result.put("size", pagination.getSize());
                    result.put("totalPages", (int) Math.ceil((double) organizations.size() / pagination.getSize()));
                    result.put("hasNext", organizations.size() == pagination.getSize());
                    result.put("hasPrevious", pagination.getPage() > 0);
                    return Mono.just(result);
                });
    }

    public Mono<Map<String, Object>> findPersonsWithPagination(
            PaginationInput pagination,
            PersonFilterInput filters,
            Map<String, Object> sort) {
        
        log.debug("Finding persons with pagination: pagination={}, filters={}, sort={}", 
                pagination, filters, sort);
        
        Pageable pageable = createPageable(pagination, sort);
        
        return personRepository.findAllWithFilters(filters, pageable)
                .collectList()
                .flatMap(persons -> {
                    Map<String, Object> result = new HashMap<>();
                    result.put("items", persons);
                    result.put("totalCount", persons.size());
                    result.put("page", pagination.getPage());
                    result.put("size", pagination.getSize());
                    result.put("totalPages", (int) Math.ceil((double) persons.size() / pagination.getSize()));
                    result.put("hasNext", persons.size() == pagination.getSize());
                    result.put("hasPrevious", pagination.getPage() > 0);
                    return Mono.just(result);
                });
    }

    public Mono<Map<String, Object>> findPositionsWithPagination(
            PaginationInput pagination,
            PositionFilterInput filters,
            Map<String, Object> sort) {
        
        log.debug("Finding positions with pagination: pagination={}, filters={}, sort={}", 
                pagination, filters, sort);
        
        Pageable pageable = createPageable(pagination, sort);
        
        return positionRepository.findAllWithFilters(filters, pageable)
                .collectList()
                .flatMap(positions -> {
                    Map<String, Object> result = new HashMap<>();
                    result.put("items", positions);
                    result.put("totalCount", positions.size());
                    result.put("page", pagination.getPage());
                    result.put("size", pagination.getSize());
                    result.put("totalPages", (int) Math.ceil((double) positions.size() / pagination.getSize()));
                    result.put("hasNext", positions.size() == pagination.getSize());
                    result.put("hasPrevious", pagination.getPage() > 0);
                    return Mono.just(result);
                });
    }

    public Mono<Map<String, Object>> searchOrganizations(String query, Map<String, Object> filters) {
        log.debug("Searching organizations with query: {}", query);
        
        return organizationalUnitRepository.search(query, filters)
                .collectList()
                .flatMap(organizations -> {
                    Map<String, Object> result = new HashMap<>();
                    result.put("items", organizations);
                    result.put("totalCount", organizations.size());
                    result.put("query", query);
                    result.put("filters", filters);
                    result.put("executionTime", System.currentTimeMillis());
                    return Mono.just(result);
                });
    }

    public Mono<Map<String, Object>> searchPersons(String query, Map<String, Object> filters) {
        log.debug("Searching persons with query: {}", query);
        
        return personRepository.search(query, filters)
                .collectList()
                .flatMap(persons -> {
                    Map<String, Object> result = new HashMap<>();
                    result.put("items", persons);
                    result.put("totalCount", persons.size());
                    result.put("query", query);
                    result.put("filters", filters);
                    result.put("executionTime", System.currentTimeMillis());
                    return Mono.just(result);
                });
    }

    public Mono<Map<String, Object>> searchPositions(String query, Map<String, Object> filters) {
        log.debug("Searching positions with query: {}", query);
        
        return positionRepository.search(query, filters)
                .collectList()
                .flatMap(positions -> {
                    Map<String, Object> result = new HashMap<>();
                    result.put("items", positions);
                    result.put("totalCount", positions.size());
                    result.put("query", query);
                    result.put("filters", filters);
                    result.put("executionTime", System.currentTimeMillis());
                    return Mono.just(result);
                });
    }

    public Mono<Map<String, Object>> getOrganizationStats(Map<String, Object> timeRange) {
        log.debug("Getting organization statistics for time range: {}", timeRange);
        
        return organizationalUnitRepository.getStats(timeRange)
                .map(stats -> {
                    Map<String, Object> result = new HashMap<>();
                    result.put("totalCount", stats.get("totalCount"));
                    result.put("activeCount", stats.get("activeCount"));
                    result.put("dissolvedCount", stats.get("dissolvedCount"));
                    result.put("byType", stats.get("byType"));
                    result.put("byStatus", stats.get("byStatus"));
                    result.put("createdInPeriod", stats.get("createdInPeriod"));
                    result.put("dissolvedInPeriod", stats.get("dissolvedInPeriod"));
                    return result;
                });
    }

    public Mono<Map<String, Object>> getPersonStats(Map<String, Object> timeRange) {
        log.debug("Getting person statistics for time range: {}", timeRange);
        
        return personRepository.getStats(timeRange)
                .map(stats -> {
                    Map<String, Object> result = new HashMap<>();
                    result.put("totalCount", stats.get("totalCount"));
                    result.put("activeCount", stats.get("activeCount"));
                    result.put("byNationality", stats.get("byNationality"));
                    result.put("byPosition", stats.get("byPosition"));
                    result.put("averageAge", stats.get("averageAge"));
                    return result;
                });
    }

    public Mono<Map<String, Object>> getPositionStats(Map<String, Object> timeRange) {
        log.debug("Getting position statistics for time range: {}", timeRange);
        
        return positionRepository.getStats(timeRange)
                .map(stats -> {
                    Map<String, Object> result = new HashMap<>();
                    result.put("totalCount", stats.get("totalCount"));
                    result.put("activeCount", stats.get("activeCount"));
                    result.put("byHierarchy", stats.get("byHierarchy"));
                    result.put("byOrganization", stats.get("byOrganization"));
                    result.put("averageSalary", stats.get("averageSalary"));
                    return result;
                });
    }

    private Pageable createPageable(PaginationInput pagination, Map<String, Object> sort) {
        Sort sortObj = Sort.unsorted();
        if (sort != null && sort.containsKey("field") && sort.containsKey("order")) {
            String field = (String) sort.get("field");
            String order = (String) sort.get("order");
            sortObj = "DESC".equalsIgnoreCase(order) ? 
                    Sort.by(Sort.Direction.DESC, field) : 
                    Sort.by(Sort.Direction.ASC, field);
        }
        
        return PageRequest.of(pagination.getPage(), pagination.getSize(), sortObj);
    }
}