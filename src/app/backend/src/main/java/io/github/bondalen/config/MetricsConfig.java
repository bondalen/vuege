package io.github.bondalen.config;

import io.micrometer.core.aop.TimedAspect;
import io.micrometer.core.instrument.MeterRegistry;
import io.micrometer.core.instrument.Timer;
import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;
import org.springframework.context.annotation.EnableAspectJAutoProxy;

/**
 * Конфигурация метрик для мониторинга производительности
 */
@Configuration
@EnableAspectJAutoProxy
public class MetricsConfig {

    /**
     * Включение автоматического тайминга для методов с аннотацией @Timed
     */
    @Bean
    public TimedAspect timedAspect(MeterRegistry registry) {
        return new TimedAspect(registry);
    }

    /**
     * Таймер для GraphQL запросов
     */
    @Bean
    public Timer graphqlQueryTimer(MeterRegistry registry) {
        return Timer.builder("graphql.query.duration")
                .description("Duration of GraphQL queries")
                .register(registry);
    }

    /**
     * Таймер для GraphQL мутаций
     */
    @Bean
    public Timer graphqlMutationTimer(MeterRegistry registry) {
        return Timer.builder("graphql.mutation.duration")
                .description("Duration of GraphQL mutations")
                .register(registry);
    }

    /**
     * Таймер для операций с базой данных
     */
    @Bean
    public Timer databaseOperationTimer(MeterRegistry registry) {
        return Timer.builder("database.operation.duration")
                .description("Duration of database operations")
                .register(registry);
    }

    /**
     * Таймер для кэш операций
     */
    @Bean
    public Timer cacheOperationTimer(MeterRegistry registry) {
        return Timer.builder("cache.operation.duration")
                .description("Duration of cache operations")
                .register(registry);
    }
}