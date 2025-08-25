package io.github.bondalen.config;

import io.r2dbc.h2.H2ConnectionConfiguration;
import io.r2dbc.h2.H2ConnectionFactory;
import io.r2dbc.postgresql.PostgresqlConnectionConfiguration;
import io.r2dbc.postgresql.PostgresqlConnectionFactory;
import io.r2dbc.spi.ConnectionFactory;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;
import org.springframework.data.r2dbc.config.AbstractR2dbcConfiguration;
import org.springframework.data.r2dbc.repository.config.EnableR2dbcRepositories;
import org.springframework.lang.NonNull;

/**
 * Конфигурация R2DBC для работы с PostgreSQL и PostGIS
 */
@Configuration
@EnableR2dbcRepositories(basePackages = "io.github.bondalen.repository")
public class R2dbcConfig extends AbstractR2dbcConfiguration {

    @Value("${spring.r2dbc.url}")
    private String r2dbcUrl;

    @Value("${spring.r2dbc.username}")
    private String username;

    @Value("${spring.r2dbc.password}")
    private String password;

    @Override
    @Bean
    @NonNull
    public ConnectionFactory connectionFactory() {
        if (r2dbcUrl.startsWith("r2dbc:h2:")) {
            // Конфигурация для H2 (тесты)
            return new H2ConnectionFactory(
                H2ConnectionConfiguration.builder()
                    .inMemory("testdb")
                    .build()
            );
        } else if (r2dbcUrl.startsWith("r2dbc:postgresql://")) {
            // Конфигурация для PostgreSQL (продакшн)
            String cleanUrl = r2dbcUrl.replace("r2dbc:postgresql://", "");
            String[] parts = cleanUrl.split("/");
            String hostPort = parts[0];
            String database = parts[1].split("\\?")[0];
            
            String[] hostPortParts = hostPort.split(":");
            String host = hostPortParts[0];
            int port = hostPortParts.length > 1 ? Integer.parseInt(hostPortParts[1]) : 5432;

            return new PostgresqlConnectionFactory(
                PostgresqlConnectionConfiguration.builder()
                    .host(host)
                    .port(port)
                    .database(database)
                    .username(username)
                    .password(password)
                    .build()
            );
        } else {
            throw new IllegalArgumentException("Unsupported R2DBC URL: " + r2dbcUrl);
        }
    }
}