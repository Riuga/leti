package com.riuga.cybersportsapp.dto

import java.time.LocalDateTime

data class MatchDTO(
    val id: Long?,
    val tournamentId: Long?,
    val tournamentName: String?,
    val team1Id: Long?,
    val team1Name: String?,
    val team2Id: Long?,
    val team2Name: String?,
    val date: LocalDateTime,
    val scoreTeam1: Int,
    val scoreTeam2: Int,
    val winnerId: Long?,
    val winnerName: String?,
    val status: String,
    val stage: String?
)

data class CreateMatchDTO(
    val tournamentId: Long,
    val team1Id: Long,
    val team2Id: Long,
    val date: LocalDateTime,
    val stage: String?
)

data class UpdateMatchScoreDTO(
    val scoreTeam1: Int,
    val scoreTeam2: Int
)