package com.riuga.cybersportsapp.dto

import java.time.LocalDateTime

data class TournamentDTO(
    val id: Long?,
    val name: String,
    val startDate: LocalDateTime,
    val endDate: LocalDateTime?,
    val prizePool: Double,
    val game: String,
    val status: String,
    val location: String?,
    val description: String?,
    val teamCount: Int
)

data class CreateTournamentDTO(
    val name: String,
    val startDate: LocalDateTime,
    val endDate: LocalDateTime?,
    val prizePool: Double,
    val game: String,
    val location: String?,
    val description: String?
)