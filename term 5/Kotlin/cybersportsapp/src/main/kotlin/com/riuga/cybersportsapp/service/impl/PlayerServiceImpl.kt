package com.riuga.cybersportsapp.service.impl

import com.riuga.cybersportsapp.entity.Player
import com.riuga.cybersportsapp.repository.PlayerRepository
import com.riuga.cybersportsapp.service.PlayerService
import org.springframework.beans.factory.annotation.Autowired
import org.springframework.stereotype.Service
import org.springframework.transaction.annotation.Transactional

@Service
@Transactional
class PlayerServiceImpl @Autowired constructor(
    private val playerRepository: PlayerRepository
) : PlayerService {

    override fun findAll(): List<Player> {
        return playerRepository.findAll()
    }

    override fun findById(id: Long): Player? {
        return playerRepository.findById(id).orElse(null)
    }

    override fun save(player: Player): Player {
        return playerRepository.save(player)
    }

    override fun deleteById(id: Long) {
        playerRepository.deleteById(id)
    }

    override fun findByNicknameContaining(nickname: String): List<Player> {
        return playerRepository.findByNicknameContainingIgnoreCase(nickname)
    }

    override fun findByTeamId(teamId: Long): List<Player> {
        return playerRepository.findByTeamId(teamId)
    }

    override fun findByCountry(country: String): List<Player> {
        return playerRepository.findByCountry(country)
    }

    override fun findByRole(role: String): List<Player> {
        return playerRepository.findByRole(role)
    }
}