package io.github.bondalen.graphql.webhook.input;

import lombok.Data;
import lombok.Builder;
import lombok.NoArgsConstructor;
import lombok.AllArgsConstructor;

import java.util.List;

@Data
@Builder
@NoArgsConstructor
@AllArgsConstructor
public class WebhookInput {
    private String name;
    private String url;
    private List<String> events;
    private Boolean isActive;
    private String secret;
}