package io.github.bondalen.graphql.batch;

import io.github.bondalen.entity.OrganizationalUnit;
import io.github.bondalen.graphql.input.OrganizationalUnitInput;
import io.github.bondalen.graphql.batch.service.BatchService;
import lombok.RequiredArgsConstructor;
import lombok.extern.slf4j.Slf4j;
import org.springframework.graphql.data.method.annotation.Argument;
import org.springframework.graphql.data.method.annotation.MutationMapping;
import org.springframework.stereotype.Controller;
import reactor.core.publisher.Flux;
import reactor.core.publisher.Mono;

import java.util.List;
import java.util.Map;

@Controller
@RequiredArgsConstructor
@Slf4j
public class BatchMutationResolver {

    private final BatchService batchService;

    @MutationMapping
    public Flux<OrganizationalUnit> batchCreateOrganizations(@Argument List<OrganizationalUnitInput> inputs) {
        log.info("Batch creating {} organizations", inputs.size());
        return batchService.batchCreateOrganizations(inputs);
    }

    @MutationMapping
    public Flux<OrganizationalUnit> batchUpdateOrganizations(@Argument List<Map<String, Object>> inputs) {
        log.info("Batch updating {} organizations", inputs.size());
        return batchService.batchUpdateOrganizations(inputs);
    }

    @MutationMapping
    public Mono<Map<String, Object>> batchDeleteOrganizations(@Argument List<String> ids) {
        log.info("Batch deleting {} organizations", ids.size());
        return batchService.batchDeleteOrganizations(ids);
    }
}