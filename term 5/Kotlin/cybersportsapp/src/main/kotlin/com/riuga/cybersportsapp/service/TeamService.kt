package com.riuga.cybersportsapp.service

import com.riuga.cybersportsapp.entity.Team
import com.riuga.cybersportsapp.entity.enums.GameType
import java.util.Optional

interface TeamService: BaseService<Team, Long> {
    fun findByNameContaining(name: String): List<Team>
    fun findByTag(tag: String): Optional<Team>
    fun findByName(name: String): Optional<Team>
    fun findActiveTeams(): List<Team>
    fun findTeamsByGameType(gameType: GameType): List<Team>
    fun findTopRatedTeams(gameType: GameType, limit: Int): List<Team>
    fun updateTeamRating(teamId: Long, gameType: GameType, newRating: Int): Team
    fun addTeamMember(teamId: Long, playerId: Long): Team
}