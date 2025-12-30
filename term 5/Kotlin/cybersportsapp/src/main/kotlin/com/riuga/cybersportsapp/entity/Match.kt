package com.riuga.cybersportsapp.entity

import jakarta.persistence.*
import java.time.LocalDateTime

@Entity
@Table(name = "matches")
class Match {
    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    var id: Long? = null

    @ManyToOne
    @JoinColumn(name = "tournament_id")
    var tournament: Tournament? = null

    @ManyToOne
    @JoinColumn(name = "team1_id")
    var team1: Team? = null

    @ManyToOne
    @JoinColumn(name = "team2_id")
    var team2: Team? = null

    @Column(nullable = false)
    var date: LocalDateTime? = null

    @Column(name = "score_team1")
    var scoreTeam1: Int? = 0

    @Column(name = "score_team2")
    var scoreTeam2: Int? = 0

    @ManyToOne
    @JoinColumn(name = "winner_id")
    var winner: Team? = null

    @Column
    var status: String? = "SCHEDULED" // SCHEDULED, LIVE, FINISHED

    @Column
    var stage: String? = null // Group Stage, Quarterfinal, Semifinal, Final

    constructor()

    constructor(tournament: Tournament, team1: Team, team2: Team, date: LocalDateTime) {
        this.tournament = tournament
        this.team1 = team1
        this.team2 = team2
        this.date = date
    }
}