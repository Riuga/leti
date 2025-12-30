package com.riuga.cybersportsapp.repository

import com.riuga.cybersportsapp.entity.Tournament
import org.springframework.data.jpa.repository.JpaRepository
import org.springframework.data.jpa.repository.Query
import org.springframework.data.repository.query.Param
import org.springframework.stereotype.Repository
import java.time.LocalDateTime

@Repository
interface TournamentRepository : JpaRepository<Tournament, Long> {
    fun findByNameContainingIgnoreCase(name: String): List<Tournament>
    fun findByGame(game: String): List<Tournament>
    fun findByStatus(status: String): List<Tournament>

    @Query("SELECT t FROM Tournament t WHERE t.startDate BETWEEN :start AND :end")
    fun findTournamentsBetweenDates(
        @Param("start") start: LocalDateTime,
        @Param("end") end: LocalDateTime
    ): List<Tournament>

    fun findByPrizePoolGreaterThan(prizePool: Double): List<Tournament>
}