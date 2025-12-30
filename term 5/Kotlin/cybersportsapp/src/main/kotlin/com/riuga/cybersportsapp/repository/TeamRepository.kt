package com.riuga.cybersportsapp.repository

import com.riuga.cybersportsapp.entity.Team
import org.springframework.data.jpa.repository.JpaRepository
import org.springframework.stereotype.Repository

@Repository
interface TeamRepository : JpaRepository<Team, Long> {
    fun findByNameContainingIgnoreCase(name: String): List<Team>
    fun findByCountry(country: String): List<Team>
    fun existsByName(name: String): Boolean
}