package com.riuga.cybersportsapp.service

import java.util.Optional

interface BaseService<T, ID> {
    fun findAll(): List<T>
    fun findById(id: ID): Optional<T>
    fun save(entity: T): T
    fun deleteById(id: ID)
}