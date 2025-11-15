package com.riuga.cybersportsapp.service

import com.riuga.cybersportsapp.entity.Rating
import com.riuga.cybersportsapp.entity.enums.GameType
import java.util.Optional

interface RatingService: BaseService<Rating, Long> {
    fun findByTeamId(teamId: Long): List<Rating>
    fun findByTeamIdAndGameType(teamId: Long, gameType: GameType): Optional<Rating>
    fun findTopRatingsByGame(gameType: GameType, limit: Int): List<Rating>
    fun updateRating(teamId: Long, gameType: GameType, wins: Int, losses: Int, newRating: Int): Rating
    fun recalculateRating(teamId: Long, gameType: GameType): Rating
    fun getTeamRank(teamId: Long, gameType: GameType): Int?
    fun findRatingsAboveThreshold(gameType: GameType, threshold: Int): List<Rating>
}