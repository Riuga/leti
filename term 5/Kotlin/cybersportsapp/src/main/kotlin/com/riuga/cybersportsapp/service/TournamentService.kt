package com.riuga.cybersportsapp.service

import com.riuga.cybersportsapp.entity.Tournament
import com.riuga.cybersportsapp.entity.enums.GameType
import com.riuga.cybersportsapp.entity.enums.TournamentStatus
import java.time.LocalDate

interface TournamentService: BaseService<Tournament, Long> {
    fun findByTitleContaining(title: String): List<Tournament>
    fun findByStatus(status: TournamentStatus): List<Tournament>
    fun findByGameType(gameType: GameType): List<Tournament>
    fun findByStartDateBetween(startDate: LocalDate, endDate: LocalDate): List<Tournament>
    fun findActiveTournaments(): List<Tournament>
    fun findByTeamId(teamId: Long): List<Tournament>
    fun registerTeam(tournamentId: Long, teamId: Long): Tournament
    fun unregisterTeam(tournamentId: Long, teamId: Long): Tournament
    fun startTournament(tournamentId: Long): Tournament
    fun completeTournament(tournamentId: Long): Tournament
}