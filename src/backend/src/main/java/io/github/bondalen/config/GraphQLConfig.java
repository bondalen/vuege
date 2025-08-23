package io.github.bondalen.config;

import graphql.schema.GraphQLScalarType;
import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;
import org.springframework.graphql.execution.RuntimeWiringConfigurer;
import org.springframework.web.servlet.config.annotation.CorsRegistry;
import org.springframework.web.servlet.config.annotation.WebMvcConfigurer;

import java.time.LocalDate;
import java.time.format.DateTimeFormatter;
import java.util.Map;

/**
 * Конфигурация GraphQL для кастомных скаляров и CORS
 */
@Configuration
public class GraphQLConfig implements WebMvcConfigurer {

    /**
     * Кастомный скаляр для Date
     */
    @Bean
    public GraphQLScalarType dateScalar() {
        return GraphQLScalarType.newScalar()
                .name("Date")
                .description("Java LocalDate as scalar")
                .coercing(new graphql.schema.Coercing<LocalDate, String>() {
                    @Override
                    public String serialize(Object dataFetcherResult) {
                        if (dataFetcherResult instanceof LocalDate) {
                            return ((LocalDate) dataFetcherResult).format(DateTimeFormatter.ISO_LOCAL_DATE);
                        }
                        return null;
                    }

                    @Override
                    public LocalDate parseValue(Object input) {
                        if (input instanceof String) {
                            return LocalDate.parse((String) input, DateTimeFormatter.ISO_LOCAL_DATE);
                        }
                        return null;
                    }

                    @Override
                    public LocalDate parseLiteral(Object input) {
                        if (input instanceof String) {
                            return LocalDate.parse((String) input, DateTimeFormatter.ISO_LOCAL_DATE);
                        }
                        return null;
                    }
                })
                .build();
    }

    /**
     * Кастомный скаляр для GeoPoint
     */
    @Bean
    public GraphQLScalarType geoPointScalar() {
        return GraphQLScalarType.newScalar()
                .name("GeoPoint")
                .description("Geographic point as scalar")
                .coercing(new graphql.schema.Coercing<Map<String, Object>, Map<String, Object>>() {
                    @Override
                    @SuppressWarnings("unchecked")
                    public Map<String, Object> serialize(Object dataFetcherResult) {
                        if (dataFetcherResult instanceof Map) {
                            return (Map<String, Object>) dataFetcherResult;
                        }
                        return null;
                    }

                    @Override
                    @SuppressWarnings("unchecked")
                    public Map<String, Object> parseValue(Object input) {
                        if (input instanceof Map) {
                            return (Map<String, Object>) input;
                        }
                        return null;
                    }

                    @Override
                    @SuppressWarnings("unchecked")
                    public Map<String, Object> parseLiteral(Object input) {
                        if (input instanceof Map) {
                            return (Map<String, Object>) input;
                        }
                        return null;
                    }
                })
                .build();
    }

    /**
     * Конфигурация RuntimeWiring для регистрации кастомных скаляров
     */
    @Bean
    public RuntimeWiringConfigurer runtimeWiringConfigurer() {
        return wiringBuilder -> wiringBuilder
                .scalar(dateScalar())
                .scalar(geoPointScalar());
    }

    /**
     * Конфигурация CORS для разрешения кросс-доменных запросов
     */
    @Override
    public void addCorsMappings(CorsRegistry registry) {
        registry.addMapping("/api/**")
                .allowedOrigins("*")
                .allowedMethods("GET", "POST", "PUT", "DELETE", "OPTIONS")
                .allowedHeaders("*")
                .allowCredentials(false);
    }
}