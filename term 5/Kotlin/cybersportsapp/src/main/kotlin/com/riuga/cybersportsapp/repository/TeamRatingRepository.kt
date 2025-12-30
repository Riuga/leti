package com.riuga.cybersportsapp.repository

import com.riuga.cybersportsapp.entity.TeamRating
import org.springframework.data.jpa.repository.JpaRepository
import org.springframework.stereotype.Repository

@Repository
interface TeamRatingRepository : JpaRepository<TeamRating, Long> {
    fun findByTeamId(teamId: Long): TeamRating?
    fun findAllByOrderByRatingDesc(): List<TeamRating>
    fun findByRatingGreaterThanEqual(rating: Int): List<TeamRating>
}