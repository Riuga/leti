package com.riuga.cybersportsapp.service

import com.riuga.cybersportsapp.entity.Match
import com.riuga.cybersportsapp.entity.enums.MatchStatus
import java.time.LocalDate

interface MatchService: BaseService<Match, Long> {
    fun findByTournamentId(tournamentId: Long): List<Match>
    fun findByTeamId(teamId: Long): List<Match>
    fun findByStatus(status: MatchStatus): List<Match>
    fun findByMatchDate(date: LocalDate): List<Match>
    fun findUpcomingMatches(days: Int): List<Match>
    fun updateMatchScore(matchId: Long, team1Score: Int, team2Score: Int): Match
    fun startMatch(matchId: Long): Match
    fun completeMatch(matchId: Long, winnerId: Long?): Match
    fun findMatchesBetweenTeams(team1Id: Long, team2Id: Long): List<Match>
}