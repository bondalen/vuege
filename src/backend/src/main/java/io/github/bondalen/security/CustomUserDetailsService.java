package io.github.bondalen.security;

import org.springframework.security.core.userdetails.UserDetails;
import org.springframework.security.core.userdetails.UserDetailsService;
import org.springframework.security.core.userdetails.UsernameNotFoundException;
import org.springframework.stereotype.Service;

import java.util.List;

/**
 * Сервис для загрузки пользователей
 * Временная реализация с хардкодом пользователей
 * В будущем будет заменена на работу с базой данных
 */
@Service
public class CustomUserDetailsService implements UserDetailsService {

    @Override
    public UserDetails loadUserByUsername(String username) throws UsernameNotFoundException {
        // Временные пользователи для тестирования (незашифрованные пароли)
        if ("admin".equals(username)) {
            return UserPrincipal.create(1L, "admin", "admin@vuege.com", 
                "admin123", 
                List.of("ADMIN", "USER", "MONITOR"));
        } else if ("user".equals(username)) {
            return UserPrincipal.create(2L, "user", "user@vuege.com", 
                "user123", 
                List.of("USER"));
        } else if ("monitor".equals(username)) {
            return UserPrincipal.create(3L, "monitor", "monitor@vuege.com", 
                "monitor123", 
                List.of("MONITOR"));
        }

        throw new UsernameNotFoundException("User not found with username: " + username);
    }

    public List<String> getAvailableUsers() {
        return List.of("admin", "user", "monitor");
    }

    public String getDefaultPassword(String username) {
        return switch (username) {
            case "admin" -> "admin123";
            case "user" -> "user123";
            case "monitor" -> "monitor123";
            default -> null;
        };
    }
}