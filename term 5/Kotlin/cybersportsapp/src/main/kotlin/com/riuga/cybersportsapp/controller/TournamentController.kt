package com.riuga.cybersportsapp.controller

import com.riuga.cybersportsapp.dto.CreateTournamentDTO
import com.riuga.cybersportsapp.dto.TournamentDTO
import com.riuga.cybersportsapp.entity.Tournament
import com.riuga.cybersportsapp.service.TournamentService
import org.springframework.beans.factory.annotation.Autowired
import org.springframework.http.HttpStatus
import org.springframework.http.ResponseEntity
import org.springframework.web.bind.annotation.*

@RestController
@RequestMapping("/api/tournaments")
class TournamentController @Autowired constructor(
    private val tournamentService: TournamentService
) {

    @GetMapping
    fun getAllTournaments(): ResponseEntity<List<TournamentDTO>> {
        val tournaments = tournamentService.findAll()
        val dtos = tournaments.map { convertToDTO(it) }
        return ResponseEntity.ok(dtos)
    }

    @GetMapping("/{id}")
    fun getTournamentById(@PathVariable id: Long): ResponseEntity<TournamentDTO> {
        val tournament = tournamentService.findById(id)
        return if (tournament != null) {
            ResponseEntity.ok(convertToDTO(tournament))
        } else {
            ResponseEntity.notFound().build()
        }
    }

    @PostMapping
    fun createTournament(@RequestBody dto: CreateTournamentDTO): ResponseEntity<TournamentDTO> {
        val tournament = Tournament()
        tournament.name = dto.name
        tournament.startDate = dto.startDate
        tournament.endDate = dto.endDate
        tournament.prizePool = dto.prizePool
        tournament.game = dto.game
        tournament.location = dto.location
        tournament.description = dto.description
        tournament.endDate = dto.endDate
        tournament.prizePool = dto.prizePool

        val savedTournament = tournamentService.save(tournament)
        return ResponseEntity.status(HttpStatus.CREATED).body(convertToDTO(savedTournament))
    }

    @PutMapping("/{id}")
    fun updateTournament(
        @PathVariable id: Long,
        @RequestBody dto: CreateTournamentDTO
    ): ResponseEntity<TournamentDTO> {
        val tournament = tournamentService.findById(id)
        if (tournament == null) {
            return ResponseEntity.notFound().build()
        }

        tournament.name = dto.name
        tournament.startDate = dto.startDate
        tournament.endDate = dto.endDate
        tournament.prizePool = dto.prizePool
        tournament.game = dto.game
        tournament.location = dto.location
        tournament.description = dto.description

        val updatedTournament = tournamentService.save(tournament)
        return ResponseEntity.ok(convertToDTO(updatedTournament))
    }

    @DeleteMapping("/{id}")
    fun deleteTournament(@PathVariable id: Long): ResponseEntity<Void> {
        val tournament = tournamentService.findById(id) ?: return ResponseEntity.notFound().build()

        tournamentService.deleteById(id)
        return ResponseEntity.noContent().build()
    }

    @GetMapping("/search")
    fun searchTournaments(@RequestParam name: String): ResponseEntity<List<TournamentDTO>> {
        val tournaments = tournamentService.findByNameContaining(name)
        val dtos = tournaments.map { convertToDTO(it) }
        return ResponseEntity.ok(dtos)
    }

    @GetMapping("/game/{game}")
    fun getTournamentsByGame(@PathVariable game: String): ResponseEntity<List<TournamentDTO>> {
        val tournaments = tournamentService.findByGame(game)
        val dtos = tournaments.map { convertToDTO(it) }
        return ResponseEntity.ok(dtos)
    }

    @PostMapping("/{tournamentId}/teams/{teamId}")
    fun addTeamToTournament(
        @PathVariable tournamentId: Long,
        @PathVariable teamId: Long
    ): ResponseEntity<TournamentDTO> {
        try {
            val tournament = tournamentService.addTeamToTournament(tournamentId, teamId)
            return ResponseEntity.ok(convertToDTO(tournament))
        } catch (e: RuntimeException) {
            return ResponseEntity.badRequest().build()
        }
    }

    @DeleteMapping("/{tournamentId}/teams/{teamId}")
    fun removeTeamFromTournament(
        @PathVariable tournamentId: Long,
        @PathVariable teamId: Long
    ): ResponseEntity<TournamentDTO> {
        try {
            val tournament = tournamentService.removeTeamFromTournament(tournamentId, teamId)
            return ResponseEntity.ok(convertToDTO(tournament))
        } catch (e: RuntimeException) {
            return ResponseEntity.badRequest().build()
        }
    }

    private fun convertToDTO(tournament: Tournament): TournamentDTO {
        return TournamentDTO(
            id = tournament.id,
            name = tournament.name ?: "",
            startDate = tournament.startDate ?: throw IllegalStateException("Start date is required"),
            endDate = tournament.endDate,
            prizePool = tournament.prizePool ?: 0.0,
            game = tournament.game ?: "",
            status = tournament.status ?: "UPCOMING",
            location = tournament.location,
            description = tournament.description,
            teamCount = tournament.teams.size
        )
    }
}