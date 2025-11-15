package com.riuga.cybersportsapp.entity
import com.riuga.cybersportsapp.entity.enums.MatchStatus
import jakarta.persistence.*
import java.time.LocalDate

@Entity
@Table(name = "matches")
class Match {
    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    var id: Long? = null

    @ManyToOne(fetch = FetchType.LAZY)
    @JoinColumn(name = "tournament_id", nullable = false)
    var tournament: Tournament? = null

    @ManyToOne(fetch = FetchType.LAZY)
    @JoinColumn(name = "team1_id")
    var team1: Team? = null

    @ManyToOne(fetch = FetchType.LAZY)
    @JoinColumn(name = "team2_id")
    var team2: Team? = null

    @ManyToOne(fetch = FetchType.LAZY)
    @JoinColumn(name = "winner_id")
    var winner: Team? = null

    @Column(name = "match_date")
    var matchDate: LocalDate? = null

    @Column(name = "match_order")
    var matchOrder: Int = 0

    @Enumerated(EnumType.STRING)
    @Column(nullable = false)
    var status: MatchStatus = MatchStatus.SCHEDULED

    @Column(name = "team1_score")
    var team1Score: Int? = null

    @Column(name = "team2_score")
    var team2Score: Int? = null

    // Constructors
    constructor()

    constructor(tournament: Tournament?, team1: Team?, team2: Team?, matchOrder: Int) {
        this.tournament = tournament
        this.team1 = team1
        this.team2 = team2
        this.matchOrder = matchOrder
    }

    // Getters and setters
    fun getID(): Long? {return this.id}
    fun setID(id: Long) {this.id = id}

    fun getTournament(): Tournament? {return this.tournament}
    fun setTournament(tournament: Tournament) {this.tournament = tournament}

    fun getTeam1(): Team? {return this.team1}
    fun setTeam1(team: Team) {this.team1 = team}

    fun getTeam2(): Team? {return this.team2}
    fun setTeam2(team: Team) {this.team2 = team}

    fun getWinner(): Team? {return this.winner}
    fun setWinner(team: Team) {this.winner = team}

    fun getMatchDate(): LocalDate? {return this.matchDate}
    fun setMatchDate(date: LocalDate) {this.matchDate = date}

    fun getMatchOrder(): Int {return this.matchOrder}
    fun setMatchOrder(order: Int) {this.matchOrder = order}

    fun getMatchStatus(): MatchStatus {return this.status}
    fun setMatchStatus(status: MatchStatus) {this.status = status}

    fun getTeam1Score(): Int? {return this.team1Score}
    fun setTeam1Score(score: Int) {this.team1Score = score}

    fun getTeam2Score(): Int? {return this.team2Score}
    fun setTeam2Score(score: Int) {this.team2Score = score}
}