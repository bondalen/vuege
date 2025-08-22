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
        status.put("status", "RUNNING");
        status.put("timestamp", LocalDateTime.now());
        status.put("message", "Backend приложение Vuege успешно запущено!");
        return status;
    }

    @GetMapping("/info")
    public Map<String, Object> getInfo() {
        Map<String, Object> info = new HashMap<>();
        info.put("name", "Vuege");
        info.put("description", "CRUD веб-сервис для учета организационных единиц с исторической перспективой и ГИС-функциональностью");
        info.put("technologies", new String[]{
            "Spring Boot 3.4.5",
            "Java 21 LTS",
            "GraphQL",
            "R2DBC",
            "PostgreSQL + PostGIS",
            "Liquibase"
        });
        info.put("features", new String[]{
            "Исторический охват от 4000 лет до н.э.",
            "ГИС-интеграция через PostGIS",
            "Реактивная архитектура",
            "GraphQL API"
        });
        return info;
    }
}