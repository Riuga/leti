package com.riuga.cybersportsapp.dto

data class TeamDTO(
    val id: Long?,
    val name: String,
    val country: String?,
    val foundedYear: Int?,
    val coach: String?,
    val playerCount: Int,
    val rating: Int?
)

data class CreateTeamDTO(
    val name: String,
    val country: String?,
    val foundedYear: Int?,
    val coach: String?
)