package com.riuga.cybersportsapp.config

import com.riuga.cybersportsapp.service.CustomUserDetailsService
import org.springframework.beans.factory.annotation.Autowired
import org.springframework.context.annotation.Bean
import org.springframework.context.annotation.Configuration
import org.springframework.security.authentication.AuthenticationManager
import org.springframework.security.config.annotation.authentication.configuration.AuthenticationConfiguration
import org.springframework.security.config.annotation.method.configuration.EnableMethodSecurity
import org.springframework.security.config.annotation.web.builders.HttpSecurity
import org.springframework.security.config.annotation.web.configuration.EnableWebSecurity
import org.springframework.security.config.http.SessionCreationPolicy
import org.springframework.security.crypto.bcrypt.BCryptPasswordEncoder
import org.springframework.security.crypto.password.PasswordEncoder
import org.springframework.security.web.SecurityFilterChain

@Configuration
@EnableWebSecurity
@EnableMethodSecurity
class SecurityConfig {

    @Autowired
    private lateinit var userDetailsService: CustomUserDetailsService

    @Bean
    fun passwordEncoder(): PasswordEncoder {
        return BCryptPasswordEncoder()
    }

    @Bean
    fun authenticationManager(config: AuthenticationConfiguration): AuthenticationManager {
        return config.authenticationManager
    }

    @Bean
    @Throws(Exception::class)
    fun securityFilterChain(http: HttpSecurity): SecurityFilterChain {
        http
            .csrf { csrf -> csrf.disable() }
            .authorizeHttpRequests { auth ->
                auth
                    // Разрешаем доступ к эндпоинтам аутентификации
                    .requestMatchers("/api/auth/**").permitAll()
                    // Разрешаем доступ к публичным эндпоинтам (опционально)
                    .requestMatchers("/api/test/public").permitAll()
                    .requestMatchers("/api/teams").permitAll()
                    .requestMatchers("/api/players").permitAll()
                    .requestMatchers("/api/tournaments").permitAll()
                    .requestMatchers("/api/matches").permitAll()
                    // Защищаем все остальные эндпоинты
                    .requestMatchers("/api/**").authenticated()
                    .anyRequest().authenticated()
            }
            .sessionManagement { session ->
                session.sessionCreationPolicy(SessionCreationPolicy.IF_REQUIRED)
            }
            .userDetailsService(userDetailsService)

        return http.build()
    }
}