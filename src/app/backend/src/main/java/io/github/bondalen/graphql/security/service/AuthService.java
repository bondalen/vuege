package io.github.bondalen.graphql.security.service;

import io.github.bondalen.entity.User;
import io.github.bondalen.entity.UserRole;
import io.github.bondalen.graphql.security.input.LoginInput;
import io.github.bondalen.graphql.security.input.RegisterInput;
import io.github.bondalen.repository.UserRepository;
import lombok.RequiredArgsConstructor;
import lombok.extern.slf4j.Slf4j;
import org.springframework.security.crypto.password.PasswordEncoder;
import org.springframework.stereotype.Service;
import reactor.core.publisher.Mono;

import java.time.LocalDateTime;
import java.util.Arrays;
import java.util.HashMap;
import java.util.Map;

@Service
@RequiredArgsConstructor
@Slf4j
public class AuthService {

    private final UserRepository userRepository;
    private final PasswordEncoder passwordEncoder;
    private final JwtService jwtService;

    public Mono<Map<String, Object>> login(LoginInput credentials) {
        log.debug("Processing login for user: {}", credentials.getUsername());
        
        return userRepository.findActiveByUsername(credentials.getUsername())
                .filter(user -> passwordEncoder.matches(credentials.getPassword(), user.getPasswordHash()))
                .flatMap(user -> {
                    // Update last login
                    userRepository.updateLastLogin(user.getId()).subscribe();
                    
                    // Generate tokens
                    String token = jwtService.generateToken(user);
                    String refreshToken = jwtService.generateRefreshToken(user);
                    
                    Map<String, Object> result = new HashMap<>();
                    result.put("token", token);
                    result.put("refreshToken", refreshToken);
                    result.put("expiresIn", 3600); // 1 hour
                    result.put("user", createUserMap(user));
                    
                    log.info("Successful login for user: {}", credentials.getUsername());
                    return Mono.just(result);
                })
                .switchIfEmpty(Mono.error(new RuntimeException("Invalid credentials")));
    }

    public Mono<Map<String, Object>> refreshToken(String token) {
        log.debug("Processing token refresh");
        
        if (!jwtService.isValidToken(token)) {
            return Mono.error(new RuntimeException("Invalid refresh token"));
        }
        
        String username = jwtService.extractUsername(token);
        return userRepository.findActiveByUsername(username)
                .flatMap(user -> {
                    String newToken = jwtService.generateToken(user);
                    String newRefreshToken = jwtService.generateRefreshToken(user);
                    
                    Map<String, Object> result = new HashMap<>();
                    result.put("token", newToken);
                    result.put("refreshToken", newRefreshToken);
                    result.put("expiresIn", 3600);
                    result.put("user", createUserMap(user));
                    
                    log.info("Token refreshed for user: {}", username);
                    return Mono.just(result);
                })
                .switchIfEmpty(Mono.error(new RuntimeException("User not found")));
    }

    public Mono<Boolean> logout(String token) {
        log.debug("Processing logout");
        
        // In a real application, you would add the token to a blacklist
        // For now, we'll just return true
        return Mono.just(true);
    }

    public Mono<Map<String, Object>> register(RegisterInput userInput) {
        log.debug("Processing registration for user: {}", userInput.getUsername());
        
        return userRepository.findByUsername(userInput.getUsername())
                .hasElement()
                .flatMap(usernameExists -> {
                    if (usernameExists) {
                        return Mono.error(new RuntimeException("Username already exists"));
                    }
                    return userRepository.findByEmail(userInput.getEmail()).hasElement();
                })
                .flatMap(emailExists -> {
                    if (emailExists) {
                        return Mono.error(new RuntimeException("Email already exists"));
                    }
                    return createNewUser(userInput);
                });
    }

    private Mono<Map<String, Object>> createNewUser(RegisterInput userInput) {
        User newUser = User.builder()
                .username(userInput.getUsername())
                .email(userInput.getEmail())
                .passwordHash(passwordEncoder.encode(userInput.getPassword()))
                .firstName(userInput.getFirstName())
                .lastName(userInput.getLastName())
                .roles(Arrays.asList(UserRole.USER))
                .isActive(true)
                .createdAt(LocalDateTime.now())
                .build();
        
        return userRepository.save(newUser)
                .map(savedUser -> {
                    String token = jwtService.generateToken(savedUser);
                    String refreshToken = jwtService.generateRefreshToken(savedUser);
                    
                    Map<String, Object> result = new HashMap<>();
                    result.put("token", token);
                    result.put("refreshToken", refreshToken);
                    result.put("expiresIn", 3600);
                    result.put("user", createUserMap(savedUser));
                    
                    log.info("User registered successfully: {}", userInput.getUsername());
                    return result;
                });
    }

    private Map<String, Object> createUserMap(User user) {
        Map<String, Object> userMap = new HashMap<>();
        userMap.put("id", user.getId());
        userMap.put("username", user.getUsername());
        userMap.put("email", user.getEmail());
        userMap.put("roles", user.getRoles());
        userMap.put("isActive", user.getIsActive());
        userMap.put("createdAt", user.getCreatedAt());
        userMap.put("lastLogin", user.getLastLogin());
        return userMap;
    }
}