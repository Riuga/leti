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
    fun getID(): Long? {return this.id}
    fun setID(id: Long) {this.id = id}

    fun getTeam(): Team? {return this.team}
    fun setTeam(team: Team) {this.team = team}

    fun getRating(): Int {return this.rating}
    fun setRating(rating: Int) {this.rating = rating}

    fun getWins(): Int {return this.wins}
    fun setWins(wins: Int) {this.wins = wins}

    fun getLosses(): Int {return this.losses}
    fun setLosses(losses: Int) {this.losses = losses}

    fun getLastUpdated(): LocalDate {return this.lastUpdated}
    fun setLastUpdated(date: LocalDate) {this.lastUpdated = date}

    fun getGame(): GameType {return this.game}
    fun setGame(game: GameType) {this.game = game}

    fun getWinRate(): Double {
        val totalGames = this.wins + this.losses
        return if (totalGames > 0) this.wins.toDouble() / totalGames else 0.0
    }
}