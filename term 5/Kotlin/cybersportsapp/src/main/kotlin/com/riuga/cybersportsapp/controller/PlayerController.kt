package com.riuga.cybersportsapp.controller

import com.riuga.cybersportsapp.dto.CreatePlayerDTO
import com.riuga.cybersportsapp.dto.PlayerDTO
import com.riuga.cybersportsapp.entity.Player
import com.riuga.cybersportsapp.entity.Team
import com.riuga.cybersportsapp.repository.TeamRepository
import com.riuga.cybersportsapp.service.PlayerService
import org.springframework.beans.factory.annotation.Autowired
import org.springframework.http.HttpStatus
import org.springframework.http.ResponseEntity
import org.springframework.web.bind.annotation.*

@RestController
@RequestMapping("/api/players")
class PlayerController @Autowired constructor(
    private val playerService: PlayerService,
    private val teamRepository: TeamRepository
) {

    @GetMapping
    fun getAllPlayers(): ResponseEntity<List<PlayerDTO>> {
        val players = playerService.findAll()
        val dtos = players.map { convertToDTO(it) }
        return ResponseEntity.ok(dtos)
    }

    @GetMapping("/{id}")
    fun getPlayerById(@PathVariable id: Long): ResponseEntity<PlayerDTO> {
        val player = playerService.findById(id)
        return if (player != null) {
            ResponseEntity.ok(convertToDTO(player))
        } else {
            ResponseEntity.notFound().build()
        }
    }

    @PostMapping
    fun createPlayer(@RequestBody dto: CreatePlayerDTO): ResponseEntity<PlayerDTO> {
        val player = Player(
            nickname = dto.nickname,
            realName = dto.realName ?: dto.nickname,
            role = dto.role ?: "Unknown"
        )
        player.country = dto.country
        player.joinDate = dto.joinDate

        // Привязываем команду, если указан teamId
        dto.teamId?.let { teamId ->
            val team = teamRepository.findById(teamId).orElse(null)
            if (team != null) {
                player.team = team
            }
        }

        val savedPlayer = playerService.save(player)
        return ResponseEntity.status(HttpStatus.CREATED).body(convertToDTO(savedPlayer))
    }

    @PutMapping("/{id}")
    fun updatePlayer(
        @PathVariable id: Long,
        @RequestBody dto: CreatePlayerDTO
    ): ResponseEntity<PlayerDTO> {
        val player = playerService.findById(id)
        if (player == null) {
            return ResponseEntity.notFound().build()
        }

        player.nickname = dto.nickname
        player.realName = dto.realName
        player.country = dto.country
        player.role = dto.role
        player.joinDate = dto.joinDate

        // Обновляем команду
        dto.teamId?.let { teamId ->
            val team = teamRepository.findById(teamId).orElse(null)
            player.team = team
        } ?: run {
            player.team = null
        }

        val updatedPlayer = playerService.save(player)
        return ResponseEntity.ok(convertToDTO(updatedPlayer))
    }

    @DeleteMapping("/{id}")
    fun deletePlayer(@PathVariable id: Long): ResponseEntity<Void> {
        val player = playerService.findById(id)
        if (player == null) {
            return ResponseEntity.notFound().build()
        }

        playerService.deleteById(id)
        return ResponseEntity.noContent().build()
    }

    @GetMapping("/search")
    fun searchPlayers(@RequestParam nickname: String): ResponseEntity<List<PlayerDTO>> {
        val players = playerService.findByNicknameContaining(nickname)
        val dtos = players.map { convertToDTO(it) }
        return ResponseEntity.ok(dtos)
    }

    @GetMapping("/team/{teamId}")
    fun getPlayersByTeam(@PathVariable teamId: Long): ResponseEntity<List<PlayerDTO>> {
        val players = playerService.findByTeamId(teamId)
        val dtos = players.map { convertToDTO(it) }
        return ResponseEntity.ok(dtos)
    }

    @GetMapping("/country/{country}")
    fun getPlayersByCountry(@PathVariable country: String): ResponseEntity<List<PlayerDTO>> {
        val players = playerService.findByCountry(country)
        val dtos = players.map { convertToDTO(it) }
        return ResponseEntity.ok(dtos)
    }

    @GetMapping("/role/{role}")
    fun getPlayersByRole(@PathVariable role: String): ResponseEntity<List<PlayerDTO>> {
        val players = playerService.findByRole(role)
        val dtos = players.map { convertToDTO(it) }
        return ResponseEntity.ok(dtos)
    }

    private fun convertToDTO(player: Player): PlayerDTO {
        return PlayerDTO(
            id = player.id,
            nickname = player.nickname ?: "",
            realName = player.realName,
            country = player.country,
            role = player.role,
            joinDate = player.joinDate,
            teamId = player.team?.id,
            teamName = player.team?.name
        )
    }
}