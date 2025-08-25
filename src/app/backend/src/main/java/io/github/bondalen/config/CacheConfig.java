package io.github.bondalen.config;

import com.github.benmanes.caffeine.cache.Caffeine;
import org.springframework.cache.CacheManager;
import org.springframework.cache.annotation.EnableCaching;
import org.springframework.cache.caffeine.CaffeineCacheManager;
import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;

import java.util.concurrent.TimeUnit;

/**
 * Конфигурация кэширования для оптимизации производительности
 */
@Configuration
@EnableCaching
public class CacheConfig {

    /**
     * Кэш для организационных единиц
     */
    @Bean
    public Caffeine<Object, Object> organizationalUnitsCacheBuilder() {
        return Caffeine.newBuilder()
                .maximumSize(1000)
                .expireAfterWrite(30, TimeUnit.MINUTES)
                .expireAfterAccess(15, TimeUnit.MINUTES)
                .recordStats();
    }

    /**
     * Кэш для персон
     */
    @Bean
    public Caffeine<Object, Object> personsCacheBuilder() {
        return Caffeine.newBuilder()
                .maximumSize(2000)
                .expireAfterWrite(30, TimeUnit.MINUTES)
                .expireAfterAccess(15, TimeUnit.MINUTES)
                .recordStats();
    }

    /**
     * Кэш для должностей
     */
    @Bean
    public Caffeine<Object, Object> positionsCacheBuilder() {
        return Caffeine.newBuilder()
                .maximumSize(500)
                .expireAfterWrite(30, TimeUnit.MINUTES)
                .expireAfterAccess(15, TimeUnit.MINUTES)
                .recordStats();
    }

    /**
     * Кэш для географических точек
     */
    @Bean
    public Caffeine<Object, Object> geoPointsCacheBuilder() {
        return Caffeine.newBuilder()
                .maximumSize(500)
                .expireAfterWrite(60, TimeUnit.MINUTES)
                .expireAfterAccess(30, TimeUnit.MINUTES)
                .recordStats();
    }

    /**
     * Кэш для исторических периодов
     */
    @Bean
    public Caffeine<Object, Object> historicalPeriodsCacheBuilder() {
        return Caffeine.newBuilder()
                .maximumSize(100)
                .expireAfterWrite(120, TimeUnit.MINUTES)
                .expireAfterAccess(60, TimeUnit.MINUTES)
                .recordStats();
    }

    /**
     * Кэш для связей персон и должностей
     */
    @Bean
    public Caffeine<Object, Object> personPositionsCacheBuilder() {
        return Caffeine.newBuilder()
                .maximumSize(3000)
                .expireAfterWrite(30, TimeUnit.MINUTES)
                .expireAfterAccess(15, TimeUnit.MINUTES)
                .recordStats();
    }

    /**
     * Настройка CacheManager с Caffeine
     */
    @Bean
    public CacheManager cacheManager() {
        CaffeineCacheManager cacheManager = new CaffeineCacheManager();
        
        // Настройка имен кэшей
        cacheManager.setCacheNames(java.util.Arrays.asList(
            "organizationalUnits",
            "persons", 
            "positions",
            "geoPoints",
            "historicalPeriods",
            "personPositions"
        ));
        
        // Настройка конфигурации для каждого кэша
        cacheManager.setCaffeine(organizationalUnitsCacheBuilder());
        
        return cacheManager;
    }
}