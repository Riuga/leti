package com.riuga.cybersportsapp.service.impl

import com.riuga.cybersportsapp.entity.Team
import com.riuga.cybersportsapp.entity.Tournament
import com.riuga.cybersportsapp.repository.TeamRepository
import com.riuga.cybersportsapp.repository.TournamentRepository
import com.riuga.cybersportsapp.service.TournamentService
import org.springframework.beans.factory.annotation.Autowired
import org.springframework.stereotype.Service
import org.springframework.transaction.annotation.Transactional

@Service
@Transactional
class TournamentServiceImpl @Autowired constructor(
    private val tournamentRepository: TournamentRepository,
    private val teamRepository: TeamRepository
) : TournamentService {

    override fun findAll(): List<Tournament> {
        return tournamentRepository.findAll()
    }

    override fun findById(id: Long): Tournament? {
        return tournamentRepository.findById(id).orElse(null)
    }

    override fun save(tournament: Tournament): Tournament {
        return tournamentRepository.save(tournament)
    }

    override fun deleteById(id: Long) {
        tournamentRepository.deleteById(id)
    }

    override fun findByNameContaining(name: String): List<Tournament> {
        return tournamentRepository.findByNameContainingIgnoreCase(name)
    }

    override fun findByGame(game: String): List<Tournament> {
        return tournamentRepository.findByGame(game)
    }

    override fun addTeamToTournament(tournamentId: Long, teamId: Long): Tournament {
        val tournament = findById(tournamentId) ?: throw RuntimeException("Tournament not found")
        val team = teamRepository.findById(teamId).orElseThrow { RuntimeException("Team not found") }

        tournament.teams.add(team)
        return tournamentRepository.save(tournament)
    }

    override fun removeTeamFromTournament(tournamentId: Long, teamId: Long): Tournament {
        val tournament = findById(tournamentId) ?: throw RuntimeException("Tournament not found")
        val team = teamRepository.findById(teamId).orElseThrow { RuntimeException("Team not found") }

        tournament.teams.remove(team)
        return tournamentRepository.save(tournament)
    }
}