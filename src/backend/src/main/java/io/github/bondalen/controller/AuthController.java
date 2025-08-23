package io.github.bondalen.controller;

import io.github.bondalen.security.CustomUserDetailsService;
import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;

import java.util.HashMap;
import java.util.List;
import java.util.Map;

/**
 * Контроллер для аутентификации и получения JWT токенов
 */
@RestController
@RequestMapping("/auth")
@CrossOrigin(origins = "*")
public class AuthController {

    private final CustomUserDetailsService userDetailsService;

    public AuthController(CustomUserDetailsService userDetailsService) {
        this.userDetailsService = userDetailsService;
    }

    @PostMapping("/login")
    public ResponseEntity<?> authenticateUser(@RequestBody LoginRequest loginRequest) {
        try {
            // Простая проверка без JWT для тестирования
            if ("admin".equals(loginRequest.getUsername()) && "admin123".equals(loginRequest.getPassword())) {
                Map<String, Object> response = new HashMap<>();
                response.put("accessToken", "test-token-admin");
                response.put("tokenType", "Bearer");
                response.put("username", loginRequest.getUsername());
                response.put("roles", List.of("ADMIN", "USER", "MONITOR"));
                response.put("message", "Authentication successful (test mode)");
                
                return ResponseEntity.ok(response);
            } else {
                return ResponseEntity.status(HttpStatus.UNAUTHORIZED)
                    .body(Map.of("error", "Invalid credentials"));
            }
        } catch (Exception e) {
            return ResponseEntity.status(HttpStatus.UNAUTHORIZED)
                .body(Map.of("error", "Authentication failed", "message", e.getMessage()));
        }
    }

    @GetMapping("/users")
    public ResponseEntity<?> getAvailableUsers() {
        Map<String, Object> response = new HashMap<>();
        response.put("users", userDetailsService.getAvailableUsers());
        response.put("message", "Доступные пользователи для тестирования");
        
        return ResponseEntity.ok(response);
    }

    @GetMapping("/test")
    public ResponseEntity<?> testAuth() {
        return ResponseEntity.ok(Map.of("message", "Auth endpoint доступен"));
    }

    // Внутренний класс для запроса логина
    public static class LoginRequest {
        private String username;
        private String password;

        public String getUsername() {
            return username;
        }

        public void setUsername(String username) {
            this.username = username;
        }

        public String getPassword() {
            return password;
        }

        public void setPassword(String password) {
            this.password = password;
        }
    }
}