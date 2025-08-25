package io.github.bondalen.graphql.security;

import io.github.bondalen.graphql.security.input.LoginInput;
import io.github.bondalen.graphql.security.input.RegisterInput;
import io.github.bondalen.graphql.security.service.AuthService;
import lombok.RequiredArgsConstructor;
import lombok.extern.slf4j.Slf4j;
import org.springframework.graphql.data.method.annotation.Argument;
import org.springframework.graphql.data.method.annotation.MutationMapping;
import org.springframework.stereotype.Controller;
import reactor.core.publisher.Mono;

import java.util.Map;

@Controller
@RequiredArgsConstructor
@Slf4j
public class AuthResolver {

    private final AuthService authService;

    @MutationMapping
    public Mono<Map<String, Object>> login(@Argument LoginInput credentials) {
        log.info("Login attempt for user: {}", credentials.getUsername());
        return authService.login(credentials);
    }

    @MutationMapping
    public Mono<Map<String, Object>> refreshToken(@Argument String token) {
        log.info("Token refresh attempt");
        return authService.refreshToken(token);
    }

    @MutationMapping
    public Mono<Boolean> logout(@Argument String token) {
        log.info("Logout attempt");
        return authService.logout(token);
    }

    @MutationMapping
    public Mono<Map<String, Object>> register(@Argument RegisterInput user) {
        log.info("Registration attempt for user: {}", user.getUsername());
        return authService.register(user);
    }
}