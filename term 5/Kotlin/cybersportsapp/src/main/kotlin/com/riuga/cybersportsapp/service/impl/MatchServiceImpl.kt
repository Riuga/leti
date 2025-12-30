package com.riuga.cybersportsapp.service.impl

import com.riuga.cybersportsapp.entity.Match
import com.riuga.cybersportsapp.repository.MatchRepository
import com.riuga.cybersportsapp.service.MatchService
import org.springframework.beans.factory.annotation.Autowired
import org.springframework.stereotype.Service
import org.springframework.transaction.annotation.Transactional
import java.time.LocalDateTime

@Service
@Transactional
class MatchServiceImpl @Autowired constructor(
    private val matchRepository: MatchRepository
) : MatchService {

    override fun findAll(): List<Match> {
        return matchRepository.findAll()
    }

    override fun findById(id: Long): Match? {
        return matchRepository.findById(id).orElse(null)
    }

    override fun save(match: Match): Match {
        return matchRepository.save(match)
    }

    override fun deleteById(id: Long) {
        matchRepository.deleteById(id)
    }

    override fun findByTournamentId(tournamentId: Long): List<Match> {
        return matchRepository.findByTournamentId(tournamentId)
    }

    override fun findByTeamId(teamId: Long): List<Match> {
        return matchRepository.findByTeam1IdOrTeam2Id(teamId, teamId)
    }

    override fun findByStatus(status: String): List<Match> {
        return matchRepository.findByStatus(status)
    }

    override fun updateMatchScore(matchId: Long, scoreTeam1: Int, scoreTeam2: Int): Match {
        val match = findById(matchId) ?: throw RuntimeException("Match not found")

        match.scoreTeam1 = scoreTeam1
        match.scoreTeam2 = scoreTeam2
        match.status = "LIVE"

        return save(match)
    }

    override fun completeMatch(matchId: Long): Match {
        val match = findById(matchId) ?: throw RuntimeException("Match not found")

        if (match.scoreTeam1 == null || match.scoreTeam2 == null) {
            throw RuntimeException("Match score must be set before completing")
        }

        match.status = "FINISHED"

        // Определяем победителя
        when {
            match.scoreTeam1!! > match.scoreTeam2!! -> match.winner = match.team1
            match.scoreTeam2!! > match.scoreTeam1!! -> match.winner = match.team2
            else -> match.winner = null // ничья
        }

        return save(match)
    }
}