package com.riuga.cybersportsapp.entity

import jakarta.persistence.*
import java.time.LocalDateTime

@Entity
@Table(name = "users")
class User {
    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    var id: Long? = null

    @Column(nullable = false, unique = true)
    var email: String? = null

    @Column(nullable = false)
    var password: String? = null

    @Column(name = "first_name", nullable = false)
    var firstName: String? = null

    @Column(name = "last_name", nullable = false)
    var lastName: String? = null

    @Column(name = "created_at")
    var createdAt: LocalDateTime? = null

    @Column
    var role: String = "USER" // USER, ADMIN, LIBRARIAN

    @Column(name = "is_active")
    var isActive: Boolean = true

    constructor()

    constructor(email: String, password: String?, firstName: String, lastName: String) {
        this.email = email
        this.password = password
        this.firstName = firstName
        this.lastName = lastName
        this.createdAt = LocalDateTime.now()
        this.role = "USER"
        this.isActive = true
    }
}