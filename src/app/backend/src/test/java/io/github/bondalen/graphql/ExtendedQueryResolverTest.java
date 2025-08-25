package io.github.bondalen.graphql;

import org.junit.jupiter.api.Test;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.test.autoconfigure.graphql.GraphQlTest;
import org.springframework.context.annotation.Import;
import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Primary;
import org.springframework.boot.test.context.TestConfiguration;
import org.springframework.graphql.test.tester.GraphQlTester;
import reactor.core.publisher.Flux;
import static org.mockito.Mockito.mock;
import static org.mockito.Mockito.when;

@GraphQlTest(controllers = {
    io.github.bondalen.graphql.resolver.QueryResolver.class
})
@Import({io.github.bondalen.config.GraphQLConfig.class, ExtendedQueryResolverTest.TestConfig.class})
class ExtendedQueryResolverTest {

    @Autowired
    private GraphQlTester graphQlTester;

    @TestConfiguration
    static class TestConfig {
        
        @Bean
        @Primary
        public io.github.bondalen.graphql.service.OrganizationalUnitService organizationalUnitService() {
            io.github.bondalen.graphql.service.OrganizationalUnitService mock = mock(io.github.bondalen.graphql.service.OrganizationalUnitService.class);
            when(mock.findAll()).thenReturn(Flux.empty());
            return mock;
        }
        
        @Bean
        @Primary
        public io.github.bondalen.graphql.service.PositionService positionService() {
            return mock(io.github.bondalen.graphql.service.PositionService.class);
        }
        
        @Bean
        @Primary
        public io.github.bondalen.graphql.service.PersonService personService() {
            return mock(io.github.bondalen.graphql.service.PersonService.class);
        }
        
        @Bean
        @Primary
        public io.github.bondalen.graphql.service.HistoricalPeriodService historicalPeriodService() {
            return mock(io.github.bondalen.graphql.service.HistoricalPeriodService.class);
        }
    }

    @Test
    void testSchemaValidation() {
        // Тестируем только валидность GraphQL схемы
        graphQlTester.document("""
            query IntrospectionQuery {
                __schema {
                    types {
                        name
                        kind
                    }
                }
            }
            """)
            .execute()
            .path("data.__schema.types")
            .entityList(Object.class)
            .hasSizeGreaterThan(0);
    }

    @Test
    void testQueryTypeExists() {
        // Проверяем что тип Query существует в схеме
        graphQlTester.document("""
            query {
                __type(name: "Query") {
                    name
                    fields {
                        name
                        type {
                            name
                        }
                    }
                }
            }
            """)
            .execute()
            .path("data.__type.name")
            .entity(String.class)
            .isEqualTo("Query");
    }


}