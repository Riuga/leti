package com.riuga.cybersportsapp.dto

import java.time.LocalDateTime

data class TeamRatingDTO(
    val id: Long?,
    val teamId: Long?,
    val teamName: String?,
    val rating: Int,
    val points: Int,
    val wins: Int,
    val losses: Int,
    val draws: Int,
    val lastUpdated: LocalDateTime?
)