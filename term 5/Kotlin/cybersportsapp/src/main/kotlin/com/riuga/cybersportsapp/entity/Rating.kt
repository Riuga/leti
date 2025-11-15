package com.riuga.cybersportsapp.entity

import com.riuga.cybersportsapp.entity.enums.GameType
import jakarta.persistence.*
import java.time.LocalDate

@Entity
@Table(name = "ratings")
class Rating {
    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    var id: Long? = null

    @ManyToOne(fetch = FetchType.LAZY)
    @JoinColumn(name = "team_id", nullable = false)
    var team: Team? = null

    @Column(nullable = false)
    var rating: Int = 1000

    @Column(nullable = false)
    var wins: Int = 0

    @Column(nullable = false)
    var losses: Int = 0

    @Column(name = "last_updated")
    var lastUpdated: LocalDate = LocalDate.now()

    @Enumerated(EnumType.STRING)
    @Column(nullable = false)
    var game: GameType = GameType.UNKNOWN

    // Constructors
    constructor()

    constructor(team: Team?, game: GameType) {
        this.team = team
        this.game = game
    }

    // Getters and setters

    fun getWinRate(): Double {
        val totalGames = this.wins + this.losses
        return if (totalGames > 0) this.wins.toDouble() / totalGames else 0.0
    }
}