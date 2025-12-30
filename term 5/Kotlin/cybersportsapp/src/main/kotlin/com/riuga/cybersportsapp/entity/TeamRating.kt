package com.riuga.cybersportsapp.entity

import jakarta.persistence.*
import java.time.LocalDateTime

@Entity
@Table(name = "team_ratings")
class TeamRating {
    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    var id: Long? = null

    @OneToOne
    @JoinColumn(name = "team_id", unique = true)
    var team: Team? = null

    @Column(nullable = false)
    var rating: Int? = 1000

    @Column
    var points: Int? = 0

    @Column
    var wins: Int? = 0

    @Column
    var losses: Int? = 0

    @Column
    var draws: Int? = 0

    @Column(name = "last_updated")
    var lastUpdated: LocalDateTime? = null

    constructor()

    constructor(team: Team) {
        this.team = team
    }
}