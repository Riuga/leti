package com.riuga.cybersportsapp.dto

import java.time.LocalDate

data class PlayerDTO(
    val id: Long?,
    val nickname: String,
    val realName: String?,
    val country: String?,
    val role: String?,
    val joinDate: LocalDate?,
    val teamId: Long?,
    val teamName: String?
)

data class CreatePlayerDTO(
    val nickname: String,
    val realName: String?,
    val country: String?,
    val role: String?,
    val joinDate: LocalDate?,
    val teamId: Long?
)