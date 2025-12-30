package com.riuga.cybersportsapp.repository

import com.riuga.cybersportsapp.entity.Match
import org.springframework.data.jpa.repository.JpaRepository
import org.springframework.data.jpa.repository.Query
import org.springframework.data.repository.query.Param
import org.springframework.stereotype.Repository
import java.time.LocalDateTime

@Repository
interface MatchRepository : JpaRepository<Match, Long> {
    fun findByTournamentId(tournamentId: Long): List<Match>
    fun findByTeam1IdOrTeam2Id(team1Id: Long, team2Id: Long): List<Match>
    fun findByStatus(status: String): List<Match>
    fun findByDateBetween(startDate: LocalDateTime, endDate: LocalDateTime): List<Match>

    @Query("SELECT m FROM Match m WHERE (m.team1.id = :teamId OR m.team2.id = :teamId) AND m.status = 'FINISHED'")
    fun findFinishedMatchesByTeamId(@Param("teamId") teamId: Long): List<Match>
}