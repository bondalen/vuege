package io.github.bondalen.graphql.notification.service;

import io.github.bondalen.repository.NotificationRepository;
import lombok.RequiredArgsConstructor;
import lombok.extern.slf4j.Slf4j;
import org.springframework.stereotype.Service;
import reactor.core.publisher.Mono;

import java.util.HashMap;
import java.util.Map;

@Service
@RequiredArgsConstructor
@Slf4j
public class NotificationService {

    private final NotificationRepository notificationRepository;

    public Mono<Map<String, Object>> getNotifications(String userId, Integer page, Integer size) {
        log.debug("Getting notifications for user: {}", userId);
        
        int pageNum = page != null ? page : 0;
        int pageSize = size != null ? size : 20;
        
        return notificationRepository.findByUserId(userId)
                .skip(pageNum * pageSize)
                .take(pageSize)
                .collectList()
                .flatMap(notifications -> {
                    Map<String, Object> result = new HashMap<>();
                    result.put("items", notifications);
                    result.put("totalCount", notifications.size());
                    result.put("page", pageNum);
                    result.put("size", pageSize);
                    result.put("totalPages", (int) Math.ceil((double) notifications.size() / pageSize));
                    result.put("hasNext", notifications.size() == pageSize);
                    result.put("hasPrevious", pageNum > 0);
                    return Mono.just(result);
                });
    }

    public Mono<Integer> getUnreadCount(String userId) {
        log.debug("Getting unread notifications count for user: {}", userId);
        return notificationRepository.countUnreadByUserId(userId)
                .map(Long::intValue);
    }

    public Mono<Boolean> markAsRead(Long id) {
        log.debug("Marking notification as read: {}", id);
        return notificationRepository.markAsRead(id)
                .then(Mono.just(true))
                .doOnSuccess(result -> log.info("Notification marked as read: {}", id));
    }

    public Mono<Boolean> markAllAsRead(String userId) {
        log.debug("Marking all notifications as read for user: {}", userId);
        return notificationRepository.markAllAsRead(userId)
                .then(Mono.just(true))
                .doOnSuccess(result -> log.info("All notifications marked as read for user: {}", userId));
    }

    public Mono<Boolean> deleteNotification(Long id) {
        log.debug("Deleting notification: {}", id);
        return notificationRepository.deleteById(id)
                .then(Mono.just(true))
                .doOnSuccess(result -> log.info("Notification deleted: {}", id));
    }
}