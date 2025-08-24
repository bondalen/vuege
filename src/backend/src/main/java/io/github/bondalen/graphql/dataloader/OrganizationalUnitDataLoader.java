package io.github.bondalen.graphql.dataloader;

import io.github.bondalen.entity.OrganizationalUnit;
import io.github.bondalen.graphql.service.OrganizationalUnitService;
import lombok.RequiredArgsConstructor;
import lombok.extern.slf4j.Slf4j;
import org.springframework.stereotype.Component;

import java.util.List;
import java.util.Map;
import java.util.ArrayList;
import java.util.concurrent.CompletableFuture;
import java.util.stream.Collectors;

/**
 * DataLoader для организационных единиц для предотвращения N+1 проблем
 */
@Component
@RequiredArgsConstructor
@Slf4j
public class OrganizationalUnitDataLoader {

    private final OrganizationalUnitService organizationalUnitService;

    /**
     * Batch loader для загрузки организационных единиц по ID
     */
    public CompletableFuture<List<OrganizationalUnit>> organizationalUnitBatchLoader(List<Long> ids) {
        log.debug("Batch loading organizational units for IDs: {}", ids);
        
        return CompletableFuture.supplyAsync(() -> {
            List<Long> idList = new ArrayList<>(ids);
            
            return organizationalUnitService.findByIds(idList)
                .collectMap(OrganizationalUnit::getId)
                .map(unitMap -> idList.stream()
                    .map(id -> unitMap.getOrDefault(id, null))
                    .collect(Collectors.toList()))
                .block();
        });
    }

    /**
     * Batch loader для загрузки дочерних организационных единиц
     */
    public CompletableFuture<List<List<OrganizationalUnit>>> childUnitsBatchLoader(List<Long> parentIds) {
        log.debug("Batch loading child units for parent IDs: {}", parentIds);
        
        return CompletableFuture.supplyAsync(() -> {
            List<Long> parentIdList = new ArrayList<>(parentIds);
            
            Map<Long, List<OrganizationalUnit>> childUnitsMap = organizationalUnitService
                .findChildUnitsBatch(parentIdList)
                .collectList()
                .map(units -> units.stream()
                    .collect(Collectors.groupingBy(OrganizationalUnit::getParentUnitId)))
                .block();
            
            return parentIdList.stream()
                .map(parentId -> childUnitsMap.getOrDefault(parentId, List.of()))
                .collect(Collectors.toList());
        });
    }

    /**
     * Batch loader для загрузки родительских организационных единиц
     */
    public CompletableFuture<List<OrganizationalUnit>> parentUnitBatchLoader(List<Long> childIds) {
        log.debug("Batch loading parent units for child IDs: {}", childIds);
        
        return CompletableFuture.supplyAsync(() -> {
            List<Long> childIdList = new ArrayList<>(childIds);
            
            // Получаем все организационные единицы
            Map<Long, OrganizationalUnit> unitsMap = organizationalUnitService
                .findByIds(childIdList)
                .collectMap(OrganizationalUnit::getId)
                .block();
            
            // Получаем ID родительских единиц
            List<Long> parentIds = childIdList.stream()
                .map(childId -> unitsMap.get(childId))
                .filter(unit -> unit != null && unit.getParentUnitId() != null)
                .map(OrganizationalUnit::getParentUnitId)
                .distinct()
                .collect(Collectors.toList());
            
            // Загружаем родительские единицы
            Map<Long, OrganizationalUnit> parentUnitsMap = organizationalUnitService
                .findByIds(parentIds)
                .collectMap(OrganizationalUnit::getId)
                .block();
            
            return childIdList.stream()
                .map(childId -> {
                    OrganizationalUnit child = unitsMap.get(childId);
                    if (child != null && child.getParentUnitId() != null) {
                        return parentUnitsMap.get(child.getParentUnitId());
                    }
                    return null;
                })
                .collect(Collectors.toList());
        });
    }
}