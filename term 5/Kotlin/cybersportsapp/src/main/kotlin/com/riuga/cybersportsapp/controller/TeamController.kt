package com.riuga.cybersportsapp.controller

import com.riuga.cybersportsapp.dto.CreateTeamDTO
import com.riuga.cybersportsapp.dto.TeamDTO
import com.riuga.cybersportsapp.entity.Team
import com.riuga.cybersportsapp.service.TeamService
import org.springframework.beans.factory.annotation.Autowired
import org.springframework.http.HttpStatus
import org.springframework.http.ResponseEntity
import org.springframework.web.bind.annotation.*

@RestController
@RequestMapping("/api/teams")
class TeamController @Autowired constructor(
    private val teamService: TeamService
) {

    @GetMapping
    fun getAllTeams(): ResponseEntity<List<TeamDTO>> {
        val teams = teamService.findAll()
        val dtos = teams.map { convertToDTO(it) }
        return ResponseEntity.ok(dtos)
    }

    @GetMapping("/{id}")
    fun getTeamById(@PathVariable id: Long): ResponseEntity<TeamDTO> {
        val team = teamService.findById(id)
        return if (team != null) {
            ResponseEntity.ok(convertToDTO(team))
        } else {
            ResponseEntity.notFound().build()
        }
    }

    @PostMapping
    fun createTeam(@RequestBody dto: CreateTeamDTO): ResponseEntity<TeamDTO> {
        val team = Team(
            name = dto.name,
            country = dto.country ?: ""
        )
        team.foundedYear = dto.foundedYear
        team.coach = dto.coach

        val savedTeam = teamService.save(team)
        return ResponseEntity.status(HttpStatus.CREATED).body(convertToDTO(savedTeam))
    }

    @PutMapping("/{id}")
    fun updateTeam(
        @PathVariable id: Long,
        @RequestBody dto: CreateTeamDTO
    ): ResponseEntity<TeamDTO> {
        val team = teamService.findById(id)
        if (team == null) {
            return ResponseEntity.notFound().build()
        }

        team.name = dto.name
        team.country = dto.country
        team.foundedYear = dto.foundedYear
        team.coach = dto.coach

        val updatedTeam = teamService.save(team)
        return ResponseEntity.ok(convertToDTO(updatedTeam))
    }

    @DeleteMapping("/{id}")
    fun deleteTeam(@PathVariable id: Long): ResponseEntity<Void> {
        val team = teamService.findById(id)
        if (team == null) {
            return ResponseEntity.notFound().build()
        }

        teamService.deleteById(id)
        return ResponseEntity.noContent().build()
    }

    @GetMapping("/search")
    fun searchTeams(@RequestParam name: String): ResponseEntity<List<TeamDTO>> {
        val teams = teamService.findByNameContaining(name)
        val dtos = teams.map { convertToDTO(it) }
        return ResponseEntity.ok(dtos)
    }

    @GetMapping("/country/{country}")
    fun getTeamsByCountry(@PathVariable country: String): ResponseEntity<List<TeamDTO>> {
        val teams = teamService.findByCountry(country)
        val dtos = teams.map { convertToDTO(it) }
        return ResponseEntity.ok(dtos)
    }

    private fun convertToDTO(team: Team): TeamDTO {
        return TeamDTO(
            id = team.id,
            name = team.name ?: "",
            country = team.country,
            foundedYear = team.foundedYear,
            coach = team.coach,
            playerCount = team.players.size,
            rating = team.rating?.rating
        )
    }
}