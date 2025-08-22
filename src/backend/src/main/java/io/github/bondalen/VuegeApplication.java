package io.github.bondalen;

import org.springframework.boot.SpringApplication;
import org.springframework.boot.autoconfigure.SpringBootApplication;

/**
 * Основной класс Spring Boot приложения Vuege
 * 
 * CRUD веб-сервис для учета организационных единиц с исторической перспективой 
 * и ГИС-функциональностью
 */
@SpringBootApplication
public class VuegeApplication {

    public static void main(String[] args) {
        SpringApplication.run(VuegeApplication.class, args);
    }
}
