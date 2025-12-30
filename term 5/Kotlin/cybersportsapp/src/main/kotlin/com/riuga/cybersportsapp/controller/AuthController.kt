package com.riuga.cybersportsapp.controller

import com.riuga.cybersportsapp.dto.AuthResponse
import com.riuga.cybersportsapp.dto.LoginRequest
import com.riuga.cybersportsapp.dto.RegisterRequest
import com.riuga.cybersportsapp.dto.UserResponse
import com.riuga.cybersportsapp.entity.User
import com.riuga.cybersportsapp.repository.UserRepository
import jakarta.validation.Valid
import org.springframework.beans.factory.annotation.Autowired
import org.springframework.http.ResponseEntity
import org.springframework.security.authentication.AuthenticationManager
import org.springframework.security.authentication.UsernamePasswordAuthenticationToken
import org.springframework.security.core.Authentication
import org.springframework.security.core.context.SecurityContextHolder
import org.springframework.security.crypto.password.PasswordEncoder
import org.springframework.web.bind.annotation.*
import java.time.LocalDateTime

@RestController
@RequestMapping("/api/auth")
class AuthController {

    @Autowired
    private lateinit var authenticationManager: AuthenticationManager

    @Autowired
    private lateinit var userRepository: UserRepository

    @Autowired
    private lateinit var passwordEncoder: PasswordEncoder

    @PostMapping("/login")
    fun login(@Valid @RequestBody loginRequest: LoginRequest): ResponseEntity<*> {
        return try {
            // Аутентификация пользователя
            val authentication: Authentication = authenticationManager.authenticate(
                UsernamePasswordAuthenticationToken(
                    loginRequest.email,
                    loginRequest.password
                )
            )

            // Установка аутентификации в контекст
            SecurityContextHolder.getContext().authentication = authentication

            // Получение информации о пользователе
            val user = userRepository.findByEmail(loginRequest.email)

            if (user.isPresent) {
                val response = AuthResponse(
                    message = "Успешный вход в систему",
                    userId = user.get().id,
                    email = user.get().email,
                    firstName = user.get().firstName,
                    lastName = user.get().lastName,
                    role = user.get().role
                )
                ResponseEntity.ok(response)
            } else {
                ResponseEntity.badRequest().body(mapOf("error" to "Пользователь не найден"))
            }
        } catch (e: Exception) {
            ResponseEntity.badRequest().body(mapOf("error" to "Неверный email или пароль"))
        }
    }

    @PostMapping("/register")
    fun register(@Valid @RequestBody request: RegisterRequest): ResponseEntity<*> {
        return try {
            // Проверяем, существует ли пользователь с таким email
            if (userRepository.existsByEmail(request.email)) {
                return ResponseEntity.badRequest()
                    .body(mapOf("error" to "Пользователь с таким email уже существует"))
            }

            // Создаем нового пользователя
            val user = User(
                email = request.email,
                password = passwordEncoder.encode(request.password),
                firstName = request.firstName,
                lastName = request.lastName
            )
            user.role = "USER"
            user.createdAt = LocalDateTime.now()
            user.isActive = true

            val savedUser = userRepository.save(user)

            val response = AuthResponse(
                message = "Регистрация прошла успешно",
                userId = savedUser.id,
                email = savedUser.email,
                firstName = savedUser.firstName,
                lastName = savedUser.lastName,
                role = savedUser.role
            )

            ResponseEntity.ok(response)
        } catch (e: Exception) {
            ResponseEntity.badRequest().body(mapOf("error" to "Ошибка при регистрации: ${e.message}"))
        }
    }

    @PostMapping("/logout")
    fun logout(): ResponseEntity<Map<String, String>> {
        SecurityContextHolder.clearContext()
        return ResponseEntity.ok(mapOf("message" to "Успешный выход из системы"))
    }

    @GetMapping("/me")
    fun getCurrentUser(): ResponseEntity<*> {
        val authentication = SecurityContextHolder.getContext().authentication
        val email = authentication!!.name

        return try {
            val user = userRepository.findByEmail(email)
                .orElseThrow { RuntimeException("Пользователь не найден") }

            val response = UserResponse(
                id = user.id,
                email = user.email ?: "",
                firstName = user.firstName ?: "",
                lastName = user.lastName ?: "",
                role = user.role,
                createdAt = user.createdAt?.toString(),
                isActive = user.isActive
            )

            ResponseEntity.ok(response)
        } catch (e: RuntimeException) {
            ResponseEntity.status(401).body(mapOf("error" to "Пользователь не аутентифицирован"))
        }
    }
}