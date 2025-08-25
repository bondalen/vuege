package io.github.bondalen.repository;

import io.github.bondalen.entity.AuditLog;
import org.springframework.data.r2dbc.repository.Query;
import org.springframework.data.repository.reactive.ReactiveCrudRepository;
import org.springframework.stereotype.Repository;
import reactor.core.publisher.Flux;

@Repository
public interface AuditLogRepository extends ReactiveCrudRepository<AuditLog, Long> {
    
    @Query("SELECT * FROM audit_logs WHERE entity_id = :entityId AND entity_type = :entityType ORDER BY timestamp DESC")
    Flux<AuditLog> findByEntityIdAndEntityType(Long entityId, String entityType);
    
    @Query("SELECT * FROM audit_logs WHERE user_id = :userId ORDER BY timestamp DESC")
    Flux<AuditLog> findByUserId(String userId);
    
    @Query("SELECT * FROM audit_logs WHERE action = :action ORDER BY timestamp DESC")
    Flux<AuditLog> findByAction(String action);
}