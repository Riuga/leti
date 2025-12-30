package com.riuga.cybersportsapp.service.impl

import com.riuga.cybersportsapp.entity.TeamRating
import com.riuga.cybersportsapp.repository.TeamRatingRepository
import com.riuga.cybersportsapp.service.TeamRatingService
import org.springframework.beans.factory.annotation.Autowired
import org.springframework.stereotype.Service
import org.springframework.transaction.annotation.Transactional
import java.time.LocalDateTime

@Service
@Transactional
class TeamRatingServiceImpl @Autowired constructor(
    private val teamRatingRepository: TeamRatingRepository
) : TeamRatingService {

    override fun findAll(): List<TeamRating> {
        return teamRatingRepository.findAll()
    }

    override fun findById(id: Long): TeamRating? {
        return teamRatingRepository.findById(id).orElse(null)
    }

    override fun save(rating: TeamRating): TeamRating {
        rating.lastUpdated = LocalDateTime.now()
        return teamRatingRepository.save(rating)
    }

    override fun deleteById(id: Long) {
        teamRatingRepository.deleteById(id)
    }

    override fun findByTeamId(teamId: Long): TeamRating? {
        return teamRatingRepository.findByTeamId(teamId)
    }

    override fun getTopTeams(limit: Int): List<TeamRating> {
        return teamRatingRepository.findAllByOrderByRatingDesc().take(limit)
    }

    override fun updateRatingAfterMatch(winnerId: Long?, loserId: Long?, isDraw: Boolean) {
        if (winnerId == null && loserId == null && !isDraw) return

        if (isDraw) {
            // Ничья - оба получают немного очков
            winnerId?.let { updateTeamRating(it, pointsChange = 5, isWin = false, isDraw = true) }
            loserId?.let { updateTeamRating(it, pointsChange = 5, isWin = false, isDraw = true) }
        } else {
            // Победитель и проигравший
            winnerId?.let { updateTeamRating(it, pointsChange = 20, isWin = true) }
            loserId?.let { updateTeamRating(it, pointsChange = -10, isWin = false) }
        }
    }

    private fun updateTeamRating(teamId: Long, pointsChange: Int, isWin: Boolean, isDraw: Boolean = false) {
        val rating = findByTeamId(teamId) ?: return

        rating.points = rating.points?.plus(pointsChange) ?: pointsChange
        rating.rating = rating.rating?.plus(pointsChange) ?: (1000 + pointsChange)

        if (isDraw) {
            rating.draws = rating.draws?.plus(1) ?: 1
        } else if (isWin) {
            rating.wins = rating.wins?.plus(1) ?: 1
        } else {
            rating.losses = rating.losses?.plus(1) ?: 1
        }

        save(rating)
    }

    override fun getTeamRanking(): List<TeamRating> {
        return teamRatingRepository.findAllByOrderByRatingDesc()
    }
}