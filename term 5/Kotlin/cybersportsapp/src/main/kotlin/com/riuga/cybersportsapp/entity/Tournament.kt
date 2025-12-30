package com.riuga.cybersportsapp.entity

import jakarta.persistence.*
import java.time.LocalDateTime

@Entity
@Table(name = "tournaments")
class Tournament {
    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    var id: Long? = null

    @Column(nullable = false)
    var name: String? = null

    @Column(name = "start_date", nullable = false)
    var startDate: LocalDateTime? = null

    @Column(name = "end_date")
    var endDate: LocalDateTime? = null

    @Column(name = "prize_pool")
    var prizePool: Double? = 0.0

    @Column(nullable = false)
    var game: String? = null

    @Column
    var status: String? = "UPCOMING" // UPCOMING, ONGOING, FINISHED

    @Column
    var location: String? = null

    @Column
    var description: String? = null

    @ManyToMany
    @JoinTable(
        name = "tournament_teams",
        joinColumns = [JoinColumn(name = "tournament_id")],
        inverseJoinColumns = [JoinColumn(name = "team_id")]
    )
    var teams: MutableSet<Team> = mutableSetOf()

    @OneToMany(mappedBy = "tournament", cascade = [CascadeType.ALL])
    var matches: MutableList<Match> = mutableListOf()

    constructor()

    constructor(name: String, startDate: LocalDateTime, game: String) {
        this.name = name
        this.startDate = startDate
        this.game = game
    }
}