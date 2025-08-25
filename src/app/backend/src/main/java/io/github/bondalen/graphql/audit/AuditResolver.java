package io.github.bondalen.graphql.audit;

import io.github.bondalen.graphql.audit.service.AuditService;
import lombok.RequiredArgsConstructor;
import lombok.extern.slf4j.Slf4j;
import org.springframework.graphql.data.method.annotation.Argument;
import org.springframework.graphql.data.method.annotation.QueryMapping;
import org.springframework.stereotype.Controller;

import reactor.core.publisher.Mono;

import java.util.Map;

@Controller
@RequiredArgsConstructor
@Slf4j
public class AuditResolver {

    private final AuditService auditService;

    @QueryMapping
    public Mono<Map<String, Object>> auditLogs(
            @Argument String entityId,
            @Argument String entityType,
            @Argument Integer page,
            @Argument Integer size) {
        
        log.debug("Fetching audit logs for entity: {} of type: {}", entityId, entityType);
        return auditService.getAuditLogs(entityId, entityType, page, size);
    }

    @QueryMapping
    public Mono<Map<String, Object>> userActivityLogs(
            @Argument String userId,
            @Argument Integer page,
            @Argument Integer size) {
        
        log.debug("Fetching user activity logs for user: {}", userId);
        return auditService.getUserActivityLogs(userId, page, size);
    }
}