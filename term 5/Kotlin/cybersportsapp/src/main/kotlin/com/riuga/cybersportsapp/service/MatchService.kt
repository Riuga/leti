package com.riuga.cybersportsapp.service

import com.riuga.cybersportsapp.entity.Match

interface MatchService {
    fun findAll(): List<Match>
    fun findById(id: Long): Match?
    fun save(match: Match): Match
    fun deleteById(id: Long)
    fun findByTournamentId(tournamentId: Long): List<Match>
    fun findByTeamId(teamId: Long): List<Match>
    fun findByStatus(status: String): List<Match>
    fun updateMatchScore(matchId: Long, scoreTeam1: Int, scoreTeam2: Int): Match
    fun completeMatch(matchId: Long): Match
}