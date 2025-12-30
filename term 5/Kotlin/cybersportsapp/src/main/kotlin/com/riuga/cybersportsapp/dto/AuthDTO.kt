package com.riuga.cybersportsapp.dto

import jakarta.validation.constraints.Email
import jakarta.validation.constraints.NotBlank
import jakarta.validation.constraints.Size

data class LoginRequest(
    @field:NotBlank(message = "Email обязателен")
    @field:Email(message = "Некорректный email")
    val email: String,

    @field:NotBlank(message = "Пароль обязателен")
    val password: String
)

data class RegisterRequest(
    @field:NotBlank(message = "Email обязателен")
    @field:Email(message = "Некорректный email")
    val email: String,

    @field:NotBlank(message = "Пароль обязателен")
    @field:Size(min = 6, message = "Пароль должен быть минимум 6 символов")
    val password: String,

    @field:NotBlank(message = "Имя обязательно")
    val firstName: String,

    @field:NotBlank(message = "Фамилия обязательна")
    val lastName: String
)

data class AuthResponse(
    val message: String,
    val userId: Long?,
    val email: String?,
    val firstName: String?,
    val lastName: String?,
    val role: String
)

data class UserResponse(
    val id: Long?,
    val email: String,
    val firstName: String,
    val lastName: String,
    val role: String,
    val createdAt: String?,
    val isActive: Boolean
)