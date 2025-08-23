package io.github.bondalen.controller;

import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;

import java.time.LocalDateTime;
import java.util.HashMap;
import java.util.Map;

/**
 * Тестовый контроллер для проверки работы приложения
 */
@RestController
@RequestMapping("/test")
public class TestController {

    @GetMapping("/status")
    public Map<String, Object> getStatus() {
        Map<String, Object> status = new HashMap<>();
        status.put("application", "Vuege");
        status.put("version", "0.1.0");
        status.put("timestamp", LocalDateTime.now());
        status.put("status", "running");
        return status;
    }

    @GetMapping("/entities")
    public Map<String, Object> getEntities() {
        Map<String, Object> entities = new HashMap<>();
        entities.put("message", "Тестовый endpoint для проверки доменной модели");
        entities.put("timestamp", LocalDateTime.now());
        entities.put("available", true);
        return entities;
    }

    @GetMapping("/health")
    public Map<String, Object> getHealth() {
        Map<String, Object> health = new HashMap<>();
        health.put("status", "UP");
        health.put("timestamp", LocalDateTime.now());
        health.put("service", "Vuege Backend");
        return health;
    }
}