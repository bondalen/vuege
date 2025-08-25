package io.github.bondalen.vuege.performance;

import io.github.bondalen.VuegeApplication;
import java.util.concurrent.TimeoutException;
import org.junit.jupiter.api.Test;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.test.context.SpringBootTest;
import org.springframework.boot.test.web.client.TestRestTemplate;
import org.springframework.http.HttpEntity;
import org.springframework.http.HttpHeaders;
import org.springframework.http.MediaType;
import org.springframework.http.ResponseEntity;
import org.springframework.test.context.ActiveProfiles;
import org.springframework.test.context.TestPropertySource;

import java.util.HashMap;
import java.util.Map;
import java.util.concurrent.CompletableFuture;
import java.util.concurrent.ExecutorService;
import java.util.concurrent.Executors;
import java.util.concurrent.TimeUnit;
import java.util.concurrent.ExecutionException;

import static org.junit.jupiter.api.Assertions.assertTrue;

/**
 * Бенчмарк для измерения производительности GraphQL API
 */
@SpringBootTest(
    webEnvironment = SpringBootTest.WebEnvironment.RANDOM_PORT,
    classes = VuegeApplication.class
)
@ActiveProfiles("test")
@TestPropertySource(properties = {
    "spring.r2dbc.url=r2dbc:h2:mem:///testdb",
    "logging.level.io.github.bondalen=INFO"
})
public class GraphQLPerformanceBenchmark {

    @Autowired
    private TestRestTemplate restTemplate;

    private static final String GRAPHQL_ENDPOINT = "/api/graphql";
    private static final int WARMUP_ITERATIONS = 10;
    private static final int BENCHMARK_ITERATIONS = 100;
    private static final int CONCURRENT_USERS = 10;

    @Test
    public void benchmarkOrganizationalUnitsQuery() {
        String query = """
            query {
                organizationalUnits {
                    id
                    name
                    type
                    parentUnit {
                        id
                        name
                    }
                    childUnits {
                        id
                        name
                    }
                    positions {
                        id
                        title
                    }
                    location {
                        id
                        latitude
                        longitude
                    }
                    historicalPeriod {
                        id
                        name
                        startDate
                        endDate
                    }
                }
            }
            """;

        // Разогрев
        for (int i = 0; i < WARMUP_ITERATIONS; i++) {
            executeGraphQLQuery(query);
        }

        // Бенчмарк
        long startTime = System.currentTimeMillis();
        for (int i = 0; i < BENCHMARK_ITERATIONS; i++) {
            executeGraphQLQuery(query);
        }
        long endTime = System.currentTimeMillis();

        long totalTime = endTime - startTime;
        double avgTime = (double) totalTime / BENCHMARK_ITERATIONS;
        double throughput = (double) BENCHMARK_ITERATIONS / (totalTime / 1000.0);

        System.out.println("=== ORGANIZATIONAL UNITS QUERY BENCHMARK ===");
        System.out.println("Total time: " + totalTime + "ms");
        System.out.println("Average time: " + avgTime + "ms");
        System.out.println("Throughput: " + throughput + " requests/sec");

        assertTrue(avgTime < 100, "Average response time should be less than 100ms");
        assertTrue(throughput > 10, "Throughput should be more than 10 requests/sec");
    }

    @Test
    public void benchmarkConcurrentQueries() throws InterruptedException {
        String query = """
            query {
                persons {
                    id
                    firstName
                    lastName
                    positions {
                        id
                        title
                        organization {
                            id
                            name
                        }
                    }
                }
            }
            """;

        ExecutorService executor = Executors.newFixedThreadPool(CONCURRENT_USERS);
        @SuppressWarnings("unchecked")
        CompletableFuture<Long>[] futures = new CompletableFuture[CONCURRENT_USERS];

        // Разогрев
        for (int i = 0; i < WARMUP_ITERATIONS; i++) {
            executeGraphQLQuery(query);
        }

        // Конкурентный бенчмарк
        long startTime = System.currentTimeMillis();
        for (int i = 0; i < CONCURRENT_USERS; i++) {
            futures[i] = CompletableFuture.supplyAsync(() -> {
                long queryStart = System.currentTimeMillis();
                for (int j = 0; j < BENCHMARK_ITERATIONS / CONCURRENT_USERS; j++) {
                    executeGraphQLQuery(query);
                }
                return System.currentTimeMillis() - queryStart;
            }, executor);
        }

        // Ожидание завершения
        try {
            CompletableFuture.allOf(futures).get(30, TimeUnit.SECONDS);
        } catch (TimeoutException e) {
            System.err.println("Timeout waiting for concurrent queries to complete");
            throw new RuntimeException(e);
        } catch (ExecutionException e) {
            System.err.println("Error executing concurrent queries: " + e.getMessage());
            throw new RuntimeException(e);
        }
        long endTime = System.currentTimeMillis();

        long totalTime = endTime - startTime;
        double throughput = (double) BENCHMARK_ITERATIONS / (totalTime / 1000.0);

        System.out.println("=== CONCURRENT QUERIES BENCHMARK ===");
        System.out.println("Total time: " + totalTime + "ms");
        System.out.println("Concurrent users: " + CONCURRENT_USERS);
        System.out.println("Throughput: " + throughput + " requests/sec");

        executor.shutdown();
        executor.awaitTermination(5, TimeUnit.SECONDS);

        assertTrue(throughput > 50, "Concurrent throughput should be more than 50 requests/sec");
    }

    @Test
    public void benchmarkMemoryUsage() {
        Runtime runtime = Runtime.getRuntime();
        
        // Сбор мусора перед измерением
        System.gc();
        
        long initialMemory = runtime.totalMemory() - runtime.freeMemory();
        
        String query = """
            query {
                organizationalUnits {
                    id
                    name
                    type
                    parentUnit { id name }
                    childUnits { id name }
                    positions { id title }
                    location { id latitude longitude }
                    historicalPeriod { id name startDate endDate }
                }
            }
            """;

        // Выполнение запросов
        for (int i = 0; i < BENCHMARK_ITERATIONS; i++) {
            executeGraphQLQuery(query);
        }

        // Сбор мусора после выполнения
        System.gc();
        
        long finalMemory = runtime.totalMemory() - runtime.freeMemory();
        long memoryIncrease = finalMemory - initialMemory;
        double memoryIncreaseMB = memoryIncrease / (1024.0 * 1024.0);

        System.out.println("=== MEMORY USAGE BENCHMARK ===");
        System.out.println("Initial memory: " + (initialMemory / (1024 * 1024)) + "MB");
        System.out.println("Final memory: " + (finalMemory / (1024 * 1024)) + "MB");
        System.out.println("Memory increase: " + memoryIncreaseMB + "MB");

        assertTrue(memoryIncreaseMB < 100, "Memory increase should be less than 100MB");
    }

    private ResponseEntity<String> executeGraphQLQuery(String query) {
        HttpHeaders headers = new HttpHeaders();
        headers.setContentType(MediaType.APPLICATION_JSON);

        Map<String, Object> requestBody = new HashMap<>();
        requestBody.put("query", query);

        HttpEntity<Map<String, Object>> request = new HttpEntity<>(requestBody, headers);
        return restTemplate.postForEntity(GRAPHQL_ENDPOINT, request, String.class);
    }
}