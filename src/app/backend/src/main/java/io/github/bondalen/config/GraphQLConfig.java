package io.github.bondalen.config;

import graphql.schema.GraphQLScalarType;
import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;
import org.springframework.graphql.execution.RuntimeWiringConfigurer;
import org.springframework.lang.NonNull;
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
                        System.out.println("parseValue called with: " + input + " (type: " + (input != null ? input.getClass().getName() : "null") + ")");
                        if (input instanceof String) {
                            try {
                                return LocalDate.parse((String) input, DateTimeFormatter.ISO_LOCAL_DATE);
                            } catch (Exception e) {
                                System.out.println("Error parsing date: " + e.getMessage());
                                // Попробуем альтернативный формат для дат до нашей эры
                                String dateStr = (String) input;
                                if (dateStr.startsWith("-")) {
                                    // Убираем минус и парсим как обычную дату
                                    dateStr = dateStr.substring(1);
                                    LocalDate date = LocalDate.parse(dateStr, DateTimeFormatter.ISO_LOCAL_DATE);
                                    // Возвращаем дату с отрицательным годом (до нашей эры)
                                    return LocalDate.of(-date.getYear(), date.getMonth(), date.getDayOfMonth());
                                }
                                return LocalDate.parse((String) input, DateTimeFormatter.ISO_LOCAL_DATE);
                            }
                        }
                        System.out.println("parseValue returning null for input: " + input);
                        return null;
                    }

                    @Override
                    public LocalDate parseLiteral(Object input) {
                        System.out.println("parseLiteral called with: " + input + " (type: " + (input != null ? input.getClass().getName() : "null") + ")");
                        if (input instanceof graphql.language.StringValue) {
                            String value = ((graphql.language.StringValue) input).getValue();
                            try {
                                return LocalDate.parse(value, DateTimeFormatter.ISO_LOCAL_DATE);
                            } catch (Exception e) {
                                System.out.println("Error parsing literal date: " + e.getMessage());
                                // Попробуем альтернативный формат для дат до нашей эры
                                if (value.startsWith("-")) {
                                    // Убираем минус и парсим как обычную дату
                                    String dateStr = value.substring(1);
                                    LocalDate date = LocalDate.parse(dateStr, DateTimeFormatter.ISO_LOCAL_DATE);
                                    // Возвращаем дату с отрицательным годом (до нашей эры)
                                    return LocalDate.of(-date.getYear(), date.getMonth(), date.getDayOfMonth());
                                }
                                return LocalDate.parse(value, DateTimeFormatter.ISO_LOCAL_DATE);
                            }
                        }
                        System.out.println("parseLiteral returning null for input: " + input);
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
     * Кастомный скаляр для Any
     */
    @Bean
    public GraphQLScalarType anyScalar() {
        return GraphQLScalarType.newScalar()
                .name("Any")
                .description("Any type as scalar")
                .coercing(new graphql.schema.Coercing<Object, Object>() {
                    @Override
                    public Object serialize(Object dataFetcherResult) {
                        return dataFetcherResult;
                    }

                    @Override
                    public Object parseValue(Object input) {
                        return input;
                    }

                    @Override
                    public Object parseLiteral(Object input) {
                        return input;
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
                .scalar(geoPointScalar())
                .scalar(anyScalar());
    }

    /**
     * Конфигурация CORS для разрешения кросс-доменных запросов
     */
    @Override
    public void addCorsMappings(@NonNull CorsRegistry registry) {
        registry.addMapping("/api/**")
                .allowedOrigins("*")
                .allowedMethods("GET", "POST", "PUT", "DELETE", "OPTIONS")
                .allowedHeaders("*")
                .allowCredentials(false);
    }
}