package io.github.bondalen.graphql.security.input;

import lombok.Data;
import lombok.Builder;
import lombok.NoArgsConstructor;
import lombok.AllArgsConstructor;

@Data
@Builder
@NoArgsConstructor
@AllArgsConstructor
public class RegisterInput {
    private String username;
    private String email;
    private String password;
    private String firstName;
    private String lastName;
}