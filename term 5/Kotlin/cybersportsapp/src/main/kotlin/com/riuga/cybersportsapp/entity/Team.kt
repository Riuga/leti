package com.riuga.cybersportsapp.entity

import jakarta.persistence.*

@Entity
@Table(name = "teams")
class Team {
    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    var id: Long? = null

    @Column(nullable = false, unique = true)
    var name: String? = null

    @Column
    var tag: String? = null // Сокращенное название (NaVi, G2 и т.д.)

    @Column
    var country: String? = null

    @Column(name = "founded_year")
    var foundedYear: Int? = null

    @Column
    var coach: String? = null

    @Column
    var logoUrl: String? = null

    @OneToMany(mappedBy = "team", cascade = [CascadeType.ALL])
    var players: MutableList<Player> = mutableListOf()

    @OneToOne(mappedBy = "team", cascade = [CascadeType.ALL])
    var rating: TeamRating? = null

    @ManyToMany(mappedBy = "teams")
    var tournaments: MutableSet<Tournament> = mutableSetOf()

    constructor()

    constructor(name: String, country: String) {
        this.name = name
        this.country = country
    }
}