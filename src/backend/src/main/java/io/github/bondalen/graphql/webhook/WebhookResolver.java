package io.github.bondalen.graphql.webhook;

import io.github.bondalen.entity.Webhook;
import io.github.bondalen.graphql.webhook.input.WebhookInput;
import io.github.bondalen.graphql.webhook.service.WebhookService;
import lombok.RequiredArgsConstructor;
import lombok.extern.slf4j.Slf4j;
import org.springframework.graphql.data.method.annotation.Argument;
import org.springframework.graphql.data.method.annotation.MutationMapping;
import org.springframework.graphql.data.method.annotation.QueryMapping;
import org.springframework.stereotype.Controller;
import reactor.core.publisher.Flux;
import reactor.core.publisher.Mono;

import java.util.Map;

@Controller
@RequiredArgsConstructor
@Slf4j
public class WebhookResolver {

    private final WebhookService webhookService;

    @QueryMapping
    public Flux<Webhook> webhooks() {
        log.debug("Fetching all webhooks");
        return webhookService.getAllWebhooks();
    }

    @QueryMapping
    public Mono<Webhook> webhook(@Argument String id) {
        log.debug("Fetching webhook with id: {}", id);
        return webhookService.getWebhookById(Long.valueOf(id));
    }

    @MutationMapping
    public Mono<Webhook> createWebhook(@Argument WebhookInput input) {
        log.info("Creating new webhook: {}", input.getName());
        return webhookService.createWebhook(input);
    }

    @MutationMapping
    public Mono<Webhook> updateWebhook(@Argument String id, @Argument WebhookInput input) {
        log.info("Updating webhook with id: {}", id);
        return webhookService.updateWebhook(Long.valueOf(id), input);
    }

    @MutationMapping
    public Mono<Boolean> deleteWebhook(@Argument String id) {
        log.info("Deleting webhook with id: {}", id);
        return webhookService.deleteWebhook(Long.valueOf(id));
    }

    @MutationMapping
    public Mono<Map<String, Object>> testWebhook(@Argument String id) {
        log.info("Testing webhook with id: {}", id);
        return webhookService.testWebhook(Long.valueOf(id));
    }
}