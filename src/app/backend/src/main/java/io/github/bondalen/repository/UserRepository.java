package io.github.bondalen.repository;

import io.github.bondalen.entity.User;
import org.springframework.data.r2dbc.repository.Query;
import org.springframework.data.repository.reactive.ReactiveCrudRepository;
import org.springframework.stereotype.Repository;
import reactor.core.publisher.Mono;

@Repository
public interface UserRepository extends ReactiveCrudRepository<User, Long> {
    
    @Query("SELECT * FROM users WHERE username = :username")
    Mono<User> findByUsername(String username);
    
    @Query("SELECT * FROM users WHERE email = :email")
    Mono<User> findByEmail(String email);
    
    @Query("SELECT * FROM users WHERE username = :username AND is_active = true")
    Mono<User> findActiveByUsername(String username);
    
    @Query("UPDATE users SET last_login = NOW() WHERE id = :id")
    Mono<Void> updateLastLogin(Long id);
}