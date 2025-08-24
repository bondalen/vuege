package io.github.bondalen.config;

import io.r2dbc.pool.ConnectionPool;
import io.r2dbc.pool.ConnectionPoolConfiguration;
import io.r2dbc.postgresql.PostgresqlConnectionConfiguration;
import io.r2dbc.postgresql.PostgresqlConnectionFactory;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;
import org.springframework.context.annotation.Primary;

import java.time.Duration;

/**
 * Конфигурация для оптимизации производительности
 */
@Configuration
public class PerformanceConfig {

    @Value("${spring.r2dbc.url}")
    private String r2dbcUrl;

    @Value("${spring.r2dbc.username}")
    private String username;

    @Value("${spring.r2dbc.password}")
    private String password;

    /**
     * Оптимизированная конфигурация connection pool
     */
    @Bean
    @Primary
    public ConnectionPool connectionPool() {
        // Парсим URL для получения параметров подключения
        String url = r2dbcUrl.replace("r2dbc:postgresql://", "");
        String[] parts = url.split("/");
        String hostPort = parts[0];
        String database = parts[1];
        
        String[] hostPortParts = hostPort.split(":");
        String host = hostPortParts[0];
        int port = hostPortParts.length > 1 ? Integer.parseInt(hostPortParts[1]) : 5432;

        PostgresqlConnectionConfiguration configuration = PostgresqlConnectionConfiguration.builder()
                .host(host)
                .port(port)
                .database(database)
                .username(username)
                .password(password)
                .build();

        PostgresqlConnectionFactory connectionFactory = new PostgresqlConnectionFactory(configuration);

        ConnectionPoolConfiguration poolConfig = ConnectionPoolConfiguration.builder(connectionFactory)
                .maxIdleTime(Duration.ofMinutes(30))
                .maxLifeTime(Duration.ofHours(1))
                .maxSize(20) // Увеличиваем размер пула для лучшей производительности
                .initialSize(5) // Начальный размер пула
                .acquireRetry(5)
                .validationQuery("SELECT 1")
                .validationDepth(io.r2dbc.spi.ValidationDepth.REMOTE)
                .build();

        return new ConnectionPool(poolConfig);
    }


}