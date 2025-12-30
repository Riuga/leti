package com.riuga.cybersportsapp.entity

import jakarta.persistence.*
import java.time.LocalDate

@Entity
@Table(name = "players")
class Player {
    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    var id: Long? = null

    @Column(nullable = false)
    var nickname: String? = null

    @Column(name = "real_name")
    var realName: String? = null

    @Column
    var country: String? = null

    @Column
    var role: String? = null // например: AWPer, Rifler, IGL, Support

    @Column(name = "birth_date")
    var birthDate: LocalDate? = null

    @Column(name = "join_date")
    var joinDate: LocalDate? = null

    @Column(name = "player_photo")
    var photoUrl: String? = null

    @ManyToOne
    @JoinColumn(name = "team_id")
    var team: Team? = null

    @Column
    var isActive: Boolean = true

    constructor()

    constructor(nickname: String, realName: String, role: String) {
        this.nickname = nickname
        this.realName = realName
        this.role = role
    }
}