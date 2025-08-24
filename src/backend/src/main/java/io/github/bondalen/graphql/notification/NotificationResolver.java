package io.github.bondalen.graphql.notification;

import io.github.bondalen.graphql.notification.service.NotificationService;
import lombok.RequiredArgsConstructor;
import lombok.extern.slf4j.Slf4j;
import org.springframework.graphql.data.method.annotation.Argument;
import org.springframework.graphql.data.method.annotation.MutationMapping;
import org.springframework.graphql.data.method.annotation.QueryMapping;
import org.springframework.stereotype.Controller;
import reactor.core.publisher.Mono;

import java.util.Map;

@Controller
@RequiredArgsConstructor
@Slf4j
public class NotificationResolver {

    private final NotificationService notificationService;

    @QueryMapping
    public Mono<Map<String, Object>> notifications(
            @Argument String userId,
            @Argument Integer page,
            @Argument Integer size) {
        
        log.debug("Fetching notifications for user: {}", userId);
        return notificationService.getNotifications(userId, page, size);
    }

    @QueryMapping
    public Mono<Integer> unreadNotificationsCount(@Argument String userId) {
        log.debug("Getting unread notifications count for user: {}", userId);
        return notificationService.getUnreadCount(userId);
    }

    @MutationMapping
    public Mono<Boolean> markNotificationAsRead(@Argument String id) {
        log.info("Marking notification as read: {}", id);
        return notificationService.markAsRead(Long.valueOf(id));
    }

    @MutationMapping
    public Mono<Boolean> markAllNotificationsAsRead(@Argument String userId) {
        log.info("Marking all notifications as read for user: {}", userId);
        return notificationService.markAllAsRead(userId);
    }

    @MutationMapping
    public Mono<Boolean> deleteNotification(@Argument String id) {
        log.info("Deleting notification: {}", id);
        return notificationService.deleteNotification(Long.valueOf(id));
    }
}