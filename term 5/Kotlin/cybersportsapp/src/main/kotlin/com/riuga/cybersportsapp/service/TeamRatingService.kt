package com.riuga.cybersportsapp.service

import com.riuga.cybersportsapp.entity.TeamRating

interface TeamRatingService {
    fun findAll(): List<TeamRating>
    fun findById(id: Long): TeamRating?
    fun save(rating: TeamRating): TeamRating
    fun deleteById(id: Long)
    fun findByTeamId(teamId: Long): TeamRating?
    fun getTopTeams(limit: Int): List<TeamRating>
    fun updateRatingAfterMatch(winnerId: Long?, loserId: Long?, isDraw: Boolean = false)
    fun getTeamRanking(): List<TeamRating>
}