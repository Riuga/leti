package com.riuga.cybersportsapp.service

import com.riuga.cybersportsapp.repository.UserRepository
import org.springframework.beans.factory.annotation.Autowired
import org.springframework.security.core.GrantedAuthority
import org.springframework.security.core.authority.SimpleGrantedAuthority
import org.springframework.security.core.userdetails.User
import org.springframework.security.core.userdetails.UserDetails
import org.springframework.security.core.userdetails.UserDetailsService
import org.springframework.security.core.userdetails.UsernameNotFoundException
import org.springframework.stereotype.Service

@Service
class CustomUserDetailsService : UserDetailsService {

    @Autowired
    private lateinit var userRepository: UserRepository

    override fun loadUserByUsername(email: String): UserDetails {
        val user = userRepository.findByEmail(email)
            .orElseThrow { UsernameNotFoundException("Пользователь не найден: $email") }

        if (!user.isActive) {
            throw UsernameNotFoundException("Учетная запись заблокирована")
        }

        val authorities = listOf(SimpleGrantedAuthority("ROLE_${user.role}"))

        return User(
            user.email ?: "",
            user.password ?: "",
            authorities
        )
    }
}