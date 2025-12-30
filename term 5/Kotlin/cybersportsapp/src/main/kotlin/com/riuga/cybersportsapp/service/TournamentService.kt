package com.riuga.cybersportsapp.service

import com.riuga.cybersportsapp.entity.Tournament

interface TournamentService {
    fun findAll(): List<Tournament>
    fun findById(id: Long): Tournament?
    fun save(tournament: Tournament): Tournament
    fun deleteById(id: Long)
    fun findByNameContaining(name: String): List<Tournament>
    fun findByGame(game: String): List<Tournament>
    fun addTeamToTournament(tournamentId: Long, teamId: Long): Tournament
    fun removeTeamFromTournament(tournamentId: Long, teamId: Long): Tournament
}