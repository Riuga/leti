package com.riuga.cybersportsapp.service.impl

import com.riuga.cybersportsapp.entity.Team
import com.riuga.cybersportsapp.repository.TeamRepository
import com.riuga.cybersportsapp.service.TeamService
import org.springframework.beans.factory.annotation.Autowired
import org.springframework.stereotype.Service
import org.springframework.transaction.annotation.Transactional

@Service
@Transactional
class TeamServiceImpl @Autowired constructor(
    private val teamRepository: TeamRepository
) : TeamService {

    override fun findAll(): List<Team> {
        return teamRepository.findAll()
    }

    override fun findById(id: Long): Team? {
        return teamRepository.findById(id).orElse(null)
    }

    override fun save(team: Team): Team {
        return teamRepository.save(team)
    }

    override fun deleteById(id: Long) {
        teamRepository.deleteById(id)
    }

    override fun findByNameContaining(name: String): List<Team> {
        return teamRepository.findByNameContainingIgnoreCase(name)
    }

    override fun findByCountry(country: String): List<Team> {
        return teamRepository.findByCountry(country)
    }
}