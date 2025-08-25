package io.github.bondalen.config;

import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;
import org.springframework.data.r2dbc.dialect.PostgresDialect;
import org.springframework.data.r2dbc.dialect.R2dbcDialect;

/**
 * Конфигурация для поддержки PostGIS типов
 */
@Configuration
public class PostgisConfig {

    /**
     * Настройка диалекта PostgreSQL с поддержкой PostGIS
     */
    @Bean
    public R2dbcDialect postgresDialect() {
        return PostgresDialect.INSTANCE;
    }
}