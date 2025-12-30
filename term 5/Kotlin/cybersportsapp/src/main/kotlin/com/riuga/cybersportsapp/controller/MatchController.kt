package com.riuga.cybersportsapp.controller

import com.riuga.cybersportsapp.dto.CreateMatchDTO
import com.riuga.cybersportsapp.dto.MatchDTO
import com.riuga.cybersportsapp.dto.UpdateMatchScoreDTO
import com.riuga.cybersportsapp.entity.Match
import com.riuga.cybersportsapp.entity.Team
import com.riuga.cybersportsapp.entity.Tournament
import com.riuga.cybersportsapp.repository.TeamRepository
import com.riuga.cybersportsapp.repository.TournamentRepository
import com.riuga.cybersportsapp.service.MatchService
import com.riuga.cybersportsapp.service.TeamRatingService
import org.springframework.beans.factory.annotation.Autowired
import org.springframework.http.HttpStatus
import org.springframework.http.ResponseEntity
import org.springframework.web.bind.annotation.*

@RestController
@RequestMapping("/api/matches")
class MatchController @Autowired constructor(
    private val matchService: MatchService,
    private val tournamentRepository: TournamentRepository,
    private val teamRepository: TeamRepository,
    private val teamRatingService: TeamRatingService
) {

    @GetMapping
    fun getAllMatches(): ResponseEntity<List<MatchDTO>> {
        val matches = matchService.findAll()
        val dtos = matches.map { convertToDTO(it) }
        return ResponseEntity.ok(dtos)
    }

    @GetMapping("/{id}")
    fun getMatchById(@PathVariable id: Long): ResponseEntity<MatchDTO> {
        val match = matchService.findById(id)
        return if (match != null) {
            ResponseEntity.ok(convertToDTO(match))
        } else {
            ResponseEntity.notFound().build()
        }
    }

    @PostMapping
    fun createMatch(@RequestBody dto: CreateMatchDTO): ResponseEntity<MatchDTO> {
        val tournament = tournamentRepository.findById(dto.tournamentId)
            .orElseThrow { RuntimeException("Tournament not found") }
        val team1 = teamRepository.findById(dto.team1Id)
            .orElseThrow { RuntimeException("Team 1 not found") }
        val team2 = teamRepository.findById(dto.team2Id)
            .orElseThrow { RuntimeException("Team 2 not found") }

        val match = Match(tournament, team1, team2, dto.date)
        match.stage = dto.stage

        val savedMatch = matchService.save(match)
        return ResponseEntity.status(HttpStatus.CREATED).body(convertToDTO(savedMatch))
    }

    @PutMapping("/{id}")
    fun updateMatch(
        @PathVariable id: Long,
        @RequestBody dto: CreateMatchDTO
    ): ResponseEntity<MatchDTO> {
        val match = matchService.findById(id)
        if (match == null) {
            return ResponseEntity.notFound().build()
        }

        val tournament = tournamentRepository.findById(dto.tournamentId)
            .orElseThrow { RuntimeException("Tournament not found") }
        val team1 = teamRepository.findById(dto.team1Id)
            .orElseThrow { RuntimeException("Team 1 not found") }
        val team2 = teamRepository.findById(dto.team2Id)
            .orElseThrow { RuntimeException("Team 2 not found") }

        match.tournament = tournament
        match.team1 = team1
        match.team2 = team2
        match.date = dto.date
        match.stage = dto.stage

        val updatedMatch = matchService.save(match)
        return ResponseEntity.ok(convertToDTO(updatedMatch))
    }

    @DeleteMapping("/{id}")
    fun deleteMatch(@PathVariable id: Long): ResponseEntity<Void> {
        val match = matchService.findById(id)
        if (match == null) {
            return ResponseEntity.notFound().build()
        }

        matchService.deleteById(id)
        return ResponseEntity.noContent().build()
    }

    @GetMapping("/tournament/{tournamentId}")
    fun getMatchesByTournament(@PathVariable tournamentId: Long): ResponseEntity<List<MatchDTO>> {
        val matches = matchService.findByTournamentId(tournamentId)
        val dtos = matches.map { convertToDTO(it) }
        return ResponseEntity.ok(dtos)
    }

    @GetMapping("/team/{teamId}")
    fun getMatchesByTeam(@PathVariable teamId: Long): ResponseEntity<List<MatchDTO>> {
        val matches = matchService.findByTeamId(teamId)
        val dtos = matches.map { convertToDTO(it) }
        return ResponseEntity.ok(dtos)
    }

    @GetMapping("/status/{status}")
    fun getMatchesByStatus(@PathVariable status: String): ResponseEntity<List<MatchDTO>> {
        val matches = matchService.findByStatus(status)
        val dtos = matches.map { convertToDTO(it) }
        return ResponseEntity.ok(dtos)
    }

    @PutMapping("/{id}/score")
    fun updateMatchScore(
        @PathVariable id: Long,
        @RequestBody scoreDto: UpdateMatchScoreDTO
    ): ResponseEntity<MatchDTO> {
        try {
            val match = matchService.updateMatchScore(id, scoreDto.scoreTeam1, scoreDto.scoreTeam2)
            return ResponseEntity.ok(convertToDTO(match))
        } catch (e: RuntimeException) {
            return ResponseEntity.badRequest().build()
        }
    }

    @PutMapping("/{id}/complete")
    fun completeMatch(@PathVariable id: Long): ResponseEntity<MatchDTO> {
        try {
            val match = matchService.completeMatch(id)

            // Обновляем рейтинги команд
            val winnerId = match.winner?.id
            val loserId = when {
                winnerId == match.team1?.id -> match.team2?.id
                winnerId == match.team2?.id -> match.team1?.id
                else -> null // ничья
            }

            val isDraw = winnerId == null && match.scoreTeam1 == match.scoreTeam2
            teamRatingService.updateRatingAfterMatch(winnerId, loserId, isDraw)

            return ResponseEntity.ok(convertToDTO(match))
        } catch (e: RuntimeException) {
            return ResponseEntity.badRequest().build()
        }
    }

    @GetMapping("/upcoming")
    fun getUpcomingMatches(): ResponseEntity<List<MatchDTO>> {
        val matches = matchService.findByStatus("SCHEDULED")
        val dtos = matches.map { convertToDTO(it) }
        return ResponseEntity.ok(dtos)
    }

    @GetMapping("/live")
    fun getLiveMatches(): ResponseEntity<List<MatchDTO>> {
        val matches = matchService.findByStatus("LIVE")
        val dtos = matches.map { convertToDTO(it) }
        return ResponseEntity.ok(dtos)
    }

    private fun convertToDTO(match: Match): MatchDTO {
        return MatchDTO(
            id = match.id,
            tournamentId = match.tournament?.id,
            tournamentName = match.tournament?.name,
            team1Id = match.team1?.id,
            team1Name = match.team1?.name,
            team2Id = match.team2?.id,
            team2Name = match.team2?.name,
            date = match.date ?: throw IllegalStateException("Match date is required"),
            scoreTeam1 = match.scoreTeam1 ?: 0,
            scoreTeam2 = match.scoreTeam2 ?: 0,
            winnerId = match.winner?.id,
            winnerName = match.winner?.name,
            status = match.status ?: "SCHEDULED",
            stage = match.stage
        )
    }
}