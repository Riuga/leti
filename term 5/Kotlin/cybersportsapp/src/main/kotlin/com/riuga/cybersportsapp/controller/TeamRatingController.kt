package com.riuga.cybersportsapp.controller

import com.riuga.cybersportsapp.dto.TeamRatingDTO
import com.riuga.cybersportsapp.service.TeamRatingService
import org.springframework.beans.factory.annotation.Autowired
import org.springframework.http.ResponseEntity
import org.springframework.web.bind.annotation.*

@RestController
@RequestMapping("/api/ratings")
class TeamRatingController @Autowired constructor(
    private val teamRatingService: TeamRatingService
) {

    @GetMapping
    fun getAllRatings(): ResponseEntity<List<TeamRatingDTO>> {
        val ratings = teamRatingService.findAll()
        val dtos = ratings.map { convertToDTO(it) }
        return ResponseEntity.ok(dtos)
    }

    @GetMapping("/{id}")
    fun getRatingById(@PathVariable id: Long): ResponseEntity<TeamRatingDTO> {
        val rating = teamRatingService.findById(id)
        return if (rating != null) {
            ResponseEntity.ok(convertToDTO(rating))
        } else {
            ResponseEntity.notFound().build()
        }
    }

    @GetMapping("/team/{teamId}")
    fun getRatingByTeamId(@PathVariable teamId: Long): ResponseEntity<TeamRatingDTO> {
        val rating = teamRatingService.findByTeamId(teamId)
        return if (rating != null) {
            ResponseEntity.ok(convertToDTO(rating))
        } else {
            ResponseEntity.notFound().build()
        }
    }

    @GetMapping("/top/{limit}")
    fun getTopTeams(@PathVariable limit: Int): ResponseEntity<List<TeamRatingDTO>> {
        val ratings = teamRatingService.getTopTeams(limit)
        val dtos = ratings.map { convertToDTO(it) }
        return ResponseEntity.ok(dtos)
    }

    @GetMapping("/ranking")
    fun getTeamRanking(): ResponseEntity<List<TeamRatingDTO>> {
        val ratings = teamRatingService.getTeamRanking()
        val dtos = ratings.map { convertToDTO(it) }
        return ResponseEntity.ok(dtos)
    }

    @DeleteMapping("/{id}")
    fun deleteRating(@PathVariable id: Long): ResponseEntity<Void> {
        val rating = teamRatingService.findById(id)
        if (rating == null) {
            return ResponseEntity.notFound().build()
        }

        teamRatingService.deleteById(id)
        return ResponseEntity.noContent().build()
    }

    private fun convertToDTO(rating: com.riuga.cybersportsapp.entity.TeamRating): TeamRatingDTO {
        return TeamRatingDTO(
            id = rating.id,
            teamId = rating.team?.id,
            teamName = rating.team?.name,
            rating = rating.rating ?: 1000,
            points = rating.points ?: 0,
            wins = rating.wins ?: 0,
            losses = rating.losses ?: 0,
            draws = rating.draws ?: 0,
            lastUpdated = rating.lastUpdated
        )
    }
}