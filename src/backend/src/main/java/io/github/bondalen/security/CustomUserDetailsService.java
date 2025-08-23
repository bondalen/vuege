package io.github.bondalen.security;

import org.springframework.security.core.userdetails.User;
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
        // Временные пользователи для тестирования
        if ("admin".equals(username)) {
            return User.builder()
                    .username("admin")
                    .password("admin123")
                    .roles("ADMIN", "USER", "MONITOR")
                    .build();
        } else if ("user".equals(username)) {
            return User.builder()
                    .username("user")
                    .password("user123")
                    .roles("USER")
                    .build();
        } else if ("monitor".equals(username)) {
            return User.builder()
                    .username("monitor")
                    .password("monitor123")
                    .roles("MONITOR")
                    .build();
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