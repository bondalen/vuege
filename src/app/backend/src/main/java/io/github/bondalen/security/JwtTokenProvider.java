package io.github.bondalen.security;

import io.jsonwebtoken.*;
import io.jsonwebtoken.security.Keys;
import io.jsonwebtoken.security.SecurityException;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.security.core.Authentication;
import org.springframework.security.core.GrantedAuthority;
import org.springframework.stereotype.Component;

import javax.crypto.SecretKey;
import java.util.Arrays;
import java.util.Date;
import java.util.List;
import java.util.stream.Collectors;

/**
 * Провайдер для работы с JWT токенами
 * Генерация, валидация и извлечение информации из токенов
 */
@Component
public class JwtTokenProvider {

    @Value("${app.jwt.secret:vuege-secret-key-for-jwt-token-generation}")
    private String jwtSecret;

    @Value("${app.jwt.expiration:86400000}") // 24 часа по умолчанию
    private long jwtExpirationMs;

    private SecretKey getSigningKey() {
        return Keys.hmacShaKeyFor(jwtSecret.getBytes());
    }

    public String generateToken(Authentication authentication) {
        UserPrincipal userPrincipal = (UserPrincipal) authentication.getPrincipal();
        
        Date now = new Date();
        Date expiryDate = new Date(now.getTime() + jwtExpirationMs);

        String authorities = authentication.getAuthorities().stream()
                .map(GrantedAuthority::getAuthority)
                .collect(Collectors.joining(","));

        return Jwts.builder()
                .subject(Long.toString(userPrincipal.getId()))
                .claim("username", userPrincipal.getUsername())
                .claim("authorities", authorities)
                .issuedAt(new Date())
                .expiration(expiryDate)
                .signWith(getSigningKey(), Jwts.SIG.HS512)
                .compact();
    }

    public Long getUserIdFromJWT(String token) {
        Claims claims = Jwts.parser()
                .verifyWith(getSigningKey())
                .build()
                .parseSignedClaims(token)
                .getPayload();

        return Long.parseLong(claims.getSubject());
    }

    public String getUsernameFromJWT(String token) {
        Claims claims = Jwts.parser()
                .verifyWith(getSigningKey())
                .build()
                .parseSignedClaims(token)
                .getPayload();

        return claims.get("username", String.class);
    }

    public List<String> getRolesFromJWT(String token) {
        Claims claims = Jwts.parser()
                .verifyWith(getSigningKey())
                .build()
                .parseSignedClaims(token)
                .getPayload();

        String authorities = claims.get("authorities", String.class);
        if (authorities != null && !authorities.isEmpty()) {
            return Arrays.asList(authorities.split(","));
        }
        return Arrays.asList();
    }

    public boolean validateToken(String authToken) {
        try {
            Jwts.parser()
                    .verifyWith(getSigningKey())
                    .build()
                    .parseSignedClaims(authToken);
            return true;
        } catch (SecurityException ex) {
            // Неверная подпись JWT
            return false;
        } catch (MalformedJwtException ex) {
            // Неверный JWT токен
            return false;
        } catch (ExpiredJwtException ex) {
            // Истекший JWT токен
            return false;
        } catch (UnsupportedJwtException ex) {
            // Неподдерживаемый JWT токен
            return false;
        } catch (IllegalArgumentException ex) {
            // Пустая строка JWT
            return false;
        }
    }
}