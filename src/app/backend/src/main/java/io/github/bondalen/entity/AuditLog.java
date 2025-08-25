package io.github.bondalen.entity;

import lombok.Data;
import lombok.Builder;
import lombok.NoArgsConstructor;
import lombok.AllArgsConstructor;
import org.springframework.data.annotation.Id;
import org.springframework.data.relational.core.mapping.Table;

import java.time.LocalDateTime;
import java.util.Map;

@Data
@Builder
@NoArgsConstructor
@AllArgsConstructor
@Table("audit_logs")
public class AuditLog {
    @Id
    private Long id;
    private Long entityId;
    private String entityType;
    private AuditActionType action;
    private Map<String, Object> oldValues;
    private Map<String, Object> newValues;
    private String userId;
    private LocalDateTime timestamp;
    private String ipAddress;
    private String userAgent;
}