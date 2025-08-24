package io.github.bondalen.repository;

import io.github.bondalen.entity.Notification;
import org.springframework.data.r2dbc.repository.Query;
import org.springframework.data.repository.reactive.ReactiveCrudRepository;
import org.springframework.stereotype.Repository;
import reactor.core.publisher.Flux;
import reactor.core.publisher.Mono;

@Repository
public interface NotificationRepository extends ReactiveCrudRepository<Notification, Long> {
    
    @Query("SELECT * FROM notifications WHERE user_id = :userId ORDER BY created_at DESC")
    Flux<Notification> findByUserId(String userId);
    
    @Query("SELECT * FROM notifications WHERE user_id = :userId AND is_read = false ORDER BY created_at DESC")
    Flux<Notification> findUnreadByUserId(String userId);
    
    @Query("SELECT COUNT(*) FROM notifications WHERE user_id = :userId AND is_read = false")
    Mono<Long> countUnreadByUserId(String userId);
    
    @Query("UPDATE notifications SET is_read = true, read_at = NOW() WHERE id = :id")
    Mono<Void> markAsRead(Long id);
    
    @Query("UPDATE notifications SET is_read = true, read_at = NOW() WHERE user_id = :userId")
    Mono<Void> markAllAsRead(String userId);
}