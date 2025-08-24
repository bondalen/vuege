package io.github.bondalen.graphql.webhook.service;

import io.github.bondalen.entity.Webhook;
import io.github.bondalen.graphql.webhook.input.WebhookInput;
import io.github.bondalen.repository.WebhookRepository;
import lombok.RequiredArgsConstructor;
import lombok.extern.slf4j.Slf4j;
import org.springframework.stereotype.Service;
import reactor.core.publisher.Flux;
import reactor.core.publisher.Mono;

import java.time.LocalDateTime;
import java.util.HashMap;
import java.util.Map;

@Service
@RequiredArgsConstructor
@Slf4j
public class WebhookService {

    private final WebhookRepository webhookRepository;

    public Flux<Webhook> getAllWebhooks() {
        log.debug("Fetching all webhooks");
        return webhookRepository.findAll();
    }

    public Mono<Webhook> getWebhookById(Long id) {
        log.debug("Fetching webhook with id: {}", id);
        return webhookRepository.findById(id);
    }

    public Mono<Webhook> createWebhook(WebhookInput input) {
        log.debug("Creating webhook: {}", input.getName());
        
        Webhook webhook = Webhook.builder()
                .name(input.getName())
                .url(input.getUrl())
                .events(input.getEvents())
                .isActive(input.getIsActive() != null ? input.getIsActive() : true)
                .secret(input.getSecret())
                .createdAt(LocalDateTime.now())
                .updatedAt(LocalDateTime.now())
                .successCount(0)
                .failureCount(0)
                .build();
        
        return webhookRepository.save(webhook)
                .doOnSuccess(savedWebhook -> log.info("Webhook created successfully: {}", savedWebhook.getName()));
    }

    public Mono<Webhook> updateWebhook(Long id, WebhookInput input) {
        log.debug("Updating webhook with id: {}", id);
        
        return webhookRepository.findById(id)
                .flatMap(existingWebhook -> {
                    existingWebhook.setName(input.getName());
                    existingWebhook.setUrl(input.getUrl());
                    existingWebhook.setEvents(input.getEvents());
                    existingWebhook.setIsActive(input.getIsActive());
                    existingWebhook.setSecret(input.getSecret());
                    existingWebhook.setUpdatedAt(LocalDateTime.now());
                    
                    return webhookRepository.save(existingWebhook);
                })
                .doOnSuccess(updatedWebhook -> log.info("Webhook updated successfully: {}", updatedWebhook.getName()));
    }

    public Mono<Boolean> deleteWebhook(Long id) {
        log.debug("Deleting webhook with id: {}", id);
        
        return webhookRepository.findById(id)
                .flatMap(webhook -> webhookRepository.delete(webhook))
                .then(Mono.just(true))
                .doOnSuccess(result -> log.info("Webhook deleted successfully with id: {}", id));
    }

    public Mono<Map<String, Object>> testWebhook(Long id) {
        log.debug("Testing webhook with id: {}", id);
        
        return webhookRepository.findById(id)
                .flatMap(webhook -> {
                    // Webhook testing logic - simulated response
                    // For now, we'll simulate a successful test
                    Map<String, Object> result = new HashMap<>();
                    result.put("success", true);
                    result.put("statusCode", 200);
                    result.put("response", "Test successful");
                    result.put("error", null);
                    
                    // Update webhook stats
                    webhookRepository.incrementSuccessCount(id).subscribe();
                    
                    return Mono.just(result);
                })
                .doOnSuccess(result -> log.info("Webhook test completed for id {}: {}", id, result.get("success")));
    }
}