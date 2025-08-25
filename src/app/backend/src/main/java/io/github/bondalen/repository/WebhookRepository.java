package io.github.bondalen.repository;

import io.github.bondalen.entity.Webhook;
import org.springframework.data.r2dbc.repository.Query;
import org.springframework.data.repository.reactive.ReactiveCrudRepository;
import org.springframework.stereotype.Repository;
import reactor.core.publisher.Flux;
import reactor.core.publisher.Mono;

@Repository
public interface WebhookRepository extends ReactiveCrudRepository<Webhook, Long> {
    
    @Query("SELECT * FROM webhooks WHERE is_active = true")
    Flux<Webhook> findActiveWebhooks();
    
    @Query("SELECT * FROM webhooks WHERE :event = ANY(events) AND is_active = true")
    Flux<Webhook> findByEvent(String event);
    
    @Query("UPDATE webhooks SET last_triggered = NOW(), success_count = success_count + 1 WHERE id = :id")
    Mono<Void> incrementSuccessCount(Long id);
    
    @Query("UPDATE webhooks SET last_triggered = NOW(), failure_count = failure_count + 1 WHERE id = :id")
    Mono<Void> incrementFailureCount(Long id);
}