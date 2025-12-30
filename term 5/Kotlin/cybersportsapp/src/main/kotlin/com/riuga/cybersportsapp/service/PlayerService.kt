package com.riuga.cybersportsapp.service

import com.riuga.cybersportsapp.entity.Player

interface PlayerService {
    fun findAll(): List<Player>
    fun findById(id: Long): Player?
    fun save(player: Player): Player
    fun deleteById(id: Long)
    fun findByNicknameContaining(nickname: String): List<Player>
    fun findByTeamId(teamId: Long): List<Player>
    fun findByCountry(country: String): List<Player>
    fun findByRole(role: String): List<Player>
}