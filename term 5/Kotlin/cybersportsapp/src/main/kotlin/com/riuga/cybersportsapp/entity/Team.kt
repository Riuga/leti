package com.riuga.cybersportsapp.entity

import jakarta.persistence.*
import org.springframework.context.annotation.Description
import org.springframework.data.annotation.CreatedDate
import java.time.LocalDate

@Entity
@Table(name = "teams")
class Team {
    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    var id: Long? = null

    @Column(nullable = false, unique = true)
    var name: String? = null

    @Column
    var tag: String? = null

    @Column(length = 1000)
    var description: String? = null

    @Column(name = "logo_url")
    var logoUrl: String? = null

    @Column(name = "created_date")
    var createdDate: LocalDate = LocalDate.now()

    @OneToMany(mappedBy = "team", cascade = [CascadeType.ALL], fetch = FetchType.LAZY)
    var ratings: MutableList<Rating> = mutableListOf()

    @ManyToMany(mappedBy = "teams", fetch = FetchType.LAZY)
    var tournaments: MutableList<Tournament> = mutableListOf()

    // Constructors
    constructor()

    constructor(name: String?, tag: String?) {
        this.name = name
        this.tag = tag
    }
    constructor(name: String?, tag: String?, description: String?, logoUrl: String?, createdDate: LocalDate) {
        this.name = name
        this.tag = tag
        this.description = description
        this.logoUrl = logoUrl
        this.createdDate = createdDate
    }
    constructor(name: String?, tag: String?, description: String?, logoUrl: String?, createdDate: LocalDate, ratings: MutableList<Rating>, tournaments:MutableList<Tournament>) {
        this.name = name
        this.tag = tag
        this.description = description
        this.logoUrl = logoUrl
        this.createdDate = createdDate
        this.ratings = ratings
        this.tournaments = tournaments
    }

    // Getters and setters
    fun getID(): Long? {return this.id}
    fun setID(id: Long) {this.id = id}

    fun getName(): String? {return this.name}
    fun setName(name: String) {this.name = name}

    fun getTag(): String? {return this.tag}
    fun setTag(tag: String) {this.tag = tag}

    fun getDescription(): String? {return this.description}
    fun setDescription(description: String) {this.description = description}

    fun getLogoUrl(): String? {return this.logoUrl}
    fun setLogoUrl(logoUrl: String) {this.logoUrl = logoUrl}

    fun getCreatedDate(): LocalDate? {return this.createdDate}
    fun setCreatedDate(date: LocalDate) {this.createdDate = date}

    fun getRatings(): MutableList<Rating> {return this.ratings}
    fun setRatings(ratings: MutableList<Rating>) {this.ratings = ratings}

    fun getTournaments(): MutableList<Tournament> {return this.tournaments}
    fun setTournaments(tournaments: MutableList<Tournament>) {this.tournaments = tournaments}
    fun addTournament(tournament: Tournament) {
        if (tournament !in this.tournaments) {
            tournament.addTeam(this)
            this.tournaments.add(tournament)
        }
    }
}