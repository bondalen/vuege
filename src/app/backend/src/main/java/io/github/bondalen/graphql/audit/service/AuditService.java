package io.github.bondalen.graphql.audit.service;

import io.github.bondalen.repository.AuditLogRepository;
import lombok.RequiredArgsConstructor;
import lombok.extern.slf4j.Slf4j;
import org.springframework.stereotype.Service;

import reactor.core.publisher.Mono;

import java.util.HashMap;
import java.util.Map;

@Service
@RequiredArgsConstructor
@Slf4j
public class AuditService {

    private final AuditLogRepository auditLogRepository;

    public Mono<Map<String, Object>> getAuditLogs(String entityId, String entityType, Integer page, Integer size) {
        log.debug("Getting audit logs for entity: {} of type: {}", entityId, entityType);
        
        int pageNum = page != null ? page : 0;
        int pageSize = size != null ? size : 20;
        
        return auditLogRepository.findByEntityIdAndEntityType(Long.valueOf(entityId), entityType)
                .skip(pageNum * pageSize)
                .take(pageSize)
                .collectList()
                .flatMap(auditLogs -> {
                    Map<String, Object> result = new HashMap<>();
                    result.put("items", auditLogs);
                    result.put("totalCount", auditLogs.size());
                    result.put("page", pageNum);
                    result.put("size", pageSize);
                    result.put("totalPages", (int) Math.ceil((double) auditLogs.size() / pageSize));
                    result.put("hasNext", auditLogs.size() == pageSize);
                    result.put("hasPrevious", pageNum > 0);
                    return Mono.just(result);
                });
    }

    public Mono<Map<String, Object>> getUserActivityLogs(String userId, Integer page, Integer size) {
        log.debug("Getting user activity logs for user: {}", userId);
        
        int pageNum = page != null ? page : 0;
        int pageSize = size != null ? size : 20;
        
        return auditLogRepository.findByUserId(userId)
                .skip(pageNum * pageSize)
                .take(pageSize)
                .collectList()
                .flatMap(auditLogs -> {
                    Map<String, Object> result = new HashMap<>();
                    result.put("items", auditLogs);
                    result.put("totalCount", auditLogs.size());
                    result.put("page", pageNum);
                    result.put("size", pageSize);
                    result.put("totalPages", (int) Math.ceil((double) auditLogs.size() / pageSize));
                    result.put("hasNext", auditLogs.size() == pageSize);
                    result.put("hasPrevious", pageNum > 0);
                    return Mono.just(result);
                });
    }
}