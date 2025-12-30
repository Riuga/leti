package com.riuga.cybersportsapp.repository

import com.riuga.cybersportsapp.entity.Player
import org.springframework.data.jpa.repository.JpaRepository
import org.springframework.stereotype.Repository

@Repository
interface PlayerRepository : JpaRepository<Player, Long> {
    fun findByNicknameContainingIgnoreCase(nickname: String): List<Player>
    fun findByTeamId(teamId: Long): List<Player>
    fun findByCountry(country: String): List<Player>
    fun findByRole(role: String): List<Player>
}