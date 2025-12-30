package com.riuga.cybersportsapp.service

import com.riuga.cybersportsapp.entity.Team

interface TeamService {
    fun findAll(): List<Team>
    fun findById(id: Long): Team?
    fun save(team: Team): Team
    fun deleteById(id: Long)
    fun findByNameContaining(name: String): List<Team>
    fun findByCountry(country: String): List<Team>
}