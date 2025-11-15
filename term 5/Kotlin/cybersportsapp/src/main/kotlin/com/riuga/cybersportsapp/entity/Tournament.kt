package com.riuga.cybersportsapp.entity

import com.riuga.cybersportsapp.entity.enums.GameType
import com.riuga.cybersportsapp.entity.enums.TournamentStatus
import jakarta.persistence.*
import java.time.LocalDate

@Entity
@Table(name = "tournaments")
class Tournament {
    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    var id: Long? = null

    @Column(nullable = false)
    var title: String? = null

    @Enumerated(EnumType.STRING)
    @Column(nullable = false)
    var game: GameType = GameType.UNKNOWN

    @Column(nullable = false)
    var prizePool: Int = 0

    @Column(name = "start_date")
    var startDate: LocalDate? = null

    @Column(name = "end_date")
    var endDate: LocalDate? = null

    @Enumerated(EnumType.STRING)
    @Column(nullable = false)
    var status: TournamentStatus = TournamentStatus.UPCOMING

    @OneToMany(mappedBy = "tournament", cascade = [CascadeType.ALL], fetch = FetchType.LAZY)
    var matches: MutableList<Match> = mutableListOf()

    @ManyToMany(fetch = FetchType.LAZY)
    @JoinTable(
        name = "tournament_teams",
        joinColumns = [JoinColumn(name = "tournament_id")],
        inverseJoinColumns = [JoinColumn(name = "team_id")]
    )
    var teams: MutableList<Team> = mutableListOf()

    @Column(length = 1000)
    var description: String? = null

    @Column(name = "max_teams")
    var maxTeams: Int? = null

    // Constructors
    constructor()
    constructor(title: String?) {
        this.title = title
    }

    constructor(title: String?, game: GameType, startDate: LocalDate?, endDate: LocalDate?, description: String?) {
        this.title = title
        this.game = game
        this.startDate = startDate
        this.endDate = endDate
        this.description = description
    }

    constructor(title: String?, game: GameType, startDate: LocalDate?, endDate: LocalDate?, description: String?, maxTeams: Int, teams: MutableList<Team>, status: TournamentStatus, matches: MutableList<Match>) {
        this.title = title
        this.game = game
        this.startDate = startDate
        this.endDate = endDate
        this.description = description
        this.maxTeams = maxTeams
        this.teams = teams
        this.status = status
        this.matches = matches
    }

    // Getters and setters
    fun addTeam(team: Team) {
        if (team !in this.teams) {
            team.addTournament(this)
            this.teams.add(team)
        }
    }

    fun addMatch(match: Match) {
        match.tournament = this
        this.matches.add(match)
    }
}