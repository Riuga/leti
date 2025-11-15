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
    fun getID(): Long? { return this.id }
    fun setID(id: Long) {this.id = id}

    fun getTitle():String? { return this.title }
    fun setTitle(title: String) {this.title = title}

    fun getPrizePool():Int {return this.prizePool}
    fun setPrizePool(prizePool: Int) {this.prizePool = prizePool}

    fun getDescription(): String? {return this.description}
    fun setDescription(description: String) {this.description = description}

    fun getGame(): GameType {return this.game}
    fun setGame(game: GameType) {this.game = game}

    fun getStartDate(): LocalDate? {return this.startDate}
    fun setStartDate(startDate: LocalDate) {this.startDate = startDate}

    fun getEndDate(): LocalDate? {return this.endDate}
    fun setEndDate(endDate: LocalDate) {this.endDate = endDate}

    fun getStatus(): TournamentStatus {return this.status}
    fun setStatus(status: TournamentStatus) {this.status = status}

    fun getTeams(): MutableList<Team> {return this.teams}
    fun setTeams(teams: MutableList<Team>) {this.teams = teams}
    fun addTeam(team: Team) {
        if (team !in this.teams) {
            team.addTournament(this)
            this.teams.add(team)
        }
    }

    fun getMatches(): MutableList<Match> {return this.matches}
    fun setMatches(matches: MutableList<Match>) {this.matches = matches}
    fun addMatch(match: Match) {
        match.setTournament(this)
        this.matches.add(match)
    }

    fun getMaxTeams(): Int? {return this.maxTeams}
    fun setMaxTeams(maxTeams: Int) {this.maxTeams = maxTeams}

}