package io.github.bondalen.controller;

import io.github.bondalen.security.CustomUserDetailsService;
import io.github.bondalen.security.JwtTokenProvider;
import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.security.authentication.AuthenticationManager;
import org.springframework.security.authentication.UsernamePasswordAuthenticationToken;
import org.springframework.security.core.Authentication;
import org.springframework.security.core.AuthenticationException;
import org.springframework.web.bind.annotation.*;

import java.util.HashMap;
import java.util.Map;

/**
 * Контроллер для аутентификации и получения JWT токенов
 */
@RestController
@RequestMapping("/auth")
@CrossOrigin(origins = "*")
public class AuthController {

    private final CustomUserDetailsService userDetailsService;
    private final AuthenticationManager authenticationManager;
    private final JwtTokenProvider jwtTokenProvider;

    public AuthController(CustomUserDetailsService userDetailsService, 
                         AuthenticationManager authenticationManager,
                         JwtTokenProvider jwtTokenProvider) {
        this.userDetailsService = userDetailsService;
        this.authenticationManager = authenticationManager;
        this.jwtTokenProvider = jwtTokenProvider;
    }

    @PostMapping("/login")
    public ResponseEntity<?> authenticateUser(@RequestBody LoginRequest loginRequest) {
        try {
            // Реальная аутентификация через Spring Security
            Authentication authentication = authenticationManager.authenticate(
                new UsernamePasswordAuthenticationToken(
                    loginRequest.getUsername(), 
                    loginRequest.getPassword()
                )
            );

            // Генерация JWT токена
            String jwt = jwtTokenProvider.generateToken(authentication);
            
            Map<String, Object> response = new HashMap<>();
            response.put("accessToken", jwt);
            response.put("tokenType", "Bearer");
            response.put("username", loginRequest.getUsername());
            response.put("roles", jwtTokenProvider.getRolesFromJWT(jwt));
            response.put("message", "Authentication successful");
            
            return ResponseEntity.ok(response);
            
        } catch (AuthenticationException e) {
            return ResponseEntity.status(HttpStatus.UNAUTHORIZED)
                .body(Map.of("error", "Invalid credentials"));
        } catch (Exception e) {
            return ResponseEntity.status(HttpStatus.INTERNAL_SERVER_ERROR)
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

    @GetMapping("/protected")
    public ResponseEntity<?> protectedEndpoint() {
        Map<String, Object> response = new HashMap<>();
        response.put("message", "Доступ к защищенному endpoint разрешен");
        response.put("timestamp", java.time.LocalDateTime.now());
        response.put("status", "success");
        return ResponseEntity.ok(response);
    }

    @GetMapping("/admin-only")
    public ResponseEntity<?> adminOnlyEndpoint() {
        Map<String, Object> response = new HashMap<>();
        response.put("message", "Доступ к admin endpoint разрешен");
        response.put("timestamp", java.time.LocalDateTime.now());
        response.put("role", "ADMIN");
        response.put("status", "success");
        return ResponseEntity.ok(response);
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