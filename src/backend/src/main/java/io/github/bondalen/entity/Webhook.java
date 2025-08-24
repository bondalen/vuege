package io.github.bondalen.entity;

import lombok.Data;
import lombok.Builder;
import lombok.NoArgsConstructor;
import lombok.AllArgsConstructor;
import org.springframework.data.annotation.Id;
import org.springframework.data.relational.core.mapping.Table;

import java.time.LocalDateTime;
import java.util.List;

@Data
@Builder
@NoArgsConstructor
@AllArgsConstructor
@Table("webhooks")
public class Webhook {
    @Id
    private Long id;
    private String name;
    private String url;
    private List<String> events;
    private Boolean isActive;
    private String secret;
    private LocalDateTime createdAt;
    private LocalDateTime updatedAt;
    private LocalDateTime lastTriggered;
    private Integer successCount;
    private Integer failureCount;
}