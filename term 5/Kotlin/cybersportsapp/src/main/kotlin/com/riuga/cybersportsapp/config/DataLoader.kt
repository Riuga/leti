package com.riuga.cybersportsapp.config

import com.riuga.cybersportsapp.entity.*
import com.riuga.cybersportsapp.repository.*
import com.riuga.cybersportsapp.service.TeamRatingService
import org.springframework.beans.factory.annotation.Autowired
import org.springframework.boot.CommandLineRunner
import org.springframework.security.crypto.password.PasswordEncoder
import org.springframework.stereotype.Component
import org.springframework.transaction.annotation.Transactional
import java.time.LocalDate
import java.time.LocalDateTime

@Component
@Transactional
class DataLoader @Autowired constructor(
    private val teamRepository: TeamRepository,
    private val playerRepository: PlayerRepository,
    private val tournamentRepository: TournamentRepository,
    private val matchRepository: MatchRepository,
    private val teamRatingRepository: TeamRatingRepository,
    private val teamRatingService: TeamRatingService,
    private val userRepository: UserRepository,
    private val passwordEncoder: PasswordEncoder
) : CommandLineRunner {

    override fun run(vararg args: String) {
        println("Начинаем загрузку тестовых данных...")

        // Проверяем, нужно ли загружать данные
        if (shouldSkipDataLoading()) {
            println("⚠️  Данные уже загружены, пропускаем...")
            return
        }

        // Создание пользователей
        createUsers()
        println("✅ Создано ${userRepository.count()} пользователей")

        // Создание команд
        val teams = createTeams()
        println("✅ Создано ${teams.size} команд")

        // Создание игроков
        val players = createPlayers(teams)
        println("✅ Создано ${players.size} игроков")

        // Создание турниров
        val tournaments = createTournaments()
        println("✅ Создано ${tournaments.size} турниров")

        // Добавление команд к турнирам
        assignTeamsToTournaments(teams, tournaments)
        println("✅ Команды добавлены к турнирам")

        // Создание рейтингов команд
        val ratings = createTeamRatings(teams)
        println("✅ Создано ${ratings.size} рейтингов команд")

        // Создание матчей
        val matches = createMatches(tournaments, teams)
        println("✅ Создано ${matches.size} матчей")

        // Обновление рейтингов после завершенных матчей
        updateRatingsAfterMatches(matches)
        println("✅ Рейтинги обновлены после матчей")

        println("\n📊 ИТОГ:")
        println("Пользователей: ${userRepository.count()}")
        println("Команд: ${teamRepository.count()}")
        println("Игроков: ${playerRepository.count()}")
        println("Турниров: ${tournamentRepository.count()}")
        println("Матчей: ${matchRepository.count()}")
        println("Рейтингов: ${teamRatingRepository.count()}")
        println("\n🎮 Тестовые данные успешно загружены!")
        printTestInfo()
    }

    private fun shouldSkipDataLoading(): Boolean {
        // Проверяем, есть ли уже данные в базе
        return teamRepository.count() > 0 || userRepository.count() > 0
    }

    private fun createUsers() {
        // Проверяем, есть ли уже пользователи
        if (userRepository.count() > 0) {
            println("⚠️  Пользователи уже существуют, пропускаем создание")
            return
        }

        // Создаем администратора
        val admin = User().apply {
            email = "admin@cybersports.ru"
            password = passwordEncoder.encode("admin123")
            firstName = "Администратор"
            lastName = "Системы"
            role = "ADMIN"
            createdAt = LocalDateTime.now()
            isActive = true
        }
        userRepository.save(admin)

        // Создаем модератора
        val moderator = User().apply {
            email = "moderator@cybersports.ru"
            password = passwordEncoder.encode("moderator123")
            firstName = "Модератор"
            lastName = "Системы"
            role = "MODERATOR"
            createdAt = LocalDateTime.now()
            isActive = true
        }
        userRepository.save(moderator)

        // Создаем обычного пользователя
        val user = User().apply {
            email = "user@cybersports.ru"
            password = passwordEncoder.encode("user123")
            firstName = "Обычный"
            lastName = "Пользователь"
            role = "USER"
            createdAt = LocalDateTime.now()
            isActive = true
        }
        userRepository.save(user)

        // Создаем еще несколько тестовых пользователей
        val testUsers = listOf(
            User().apply {
                email = "alex@cybersports.ru"
                password = passwordEncoder.encode("password123")
                firstName = "Александр"
                lastName = "Иванов"
                role = "USER"
                createdAt = LocalDateTime.now()
                isActive = true
            },
            User().apply {
                email = "maria@cybersports.ru"
                password = passwordEncoder.encode("password123")
                firstName = "Мария"
                lastName = "Петрова"
                role = "USER"
                createdAt = LocalDateTime.now()
                isActive = true
            },
            User().apply {
                email = "coach@cybersports.ru"
                password = passwordEncoder.encode("password123")
                firstName = "Тренер"
                lastName = "Профи"
                role = "USER"
                createdAt = LocalDateTime.now()
                isActive = true
            }
        )
        userRepository.saveAll(testUsers)
    }

    private fun createTeams(): List<Team> {
        // Проверяем, есть ли уже команды
        if (teamRepository.count() > 0) {
            println("⚠️  Команды уже существуют, пропускаем создание")
            return teamRepository.findAll()
        }

        val teams = mutableListOf<Team>()

        // Создаем команды с использованием явного конструктора
        val team1 = Team().apply {
            name = "Natus Vincere"
            country = "Украина"
            foundedYear = 2009
            coach = "B1ad3"
            tag = "NaVi"
        }
        teams.add(team1)

        val team2 = Team().apply {
            name = "Team Spirit"
            country = "Россия"
            foundedYear = 2015
            coach = "Silent"
            tag = "TSpirit"
        }
        teams.add(team2)

        val team3 = Team().apply {
            name = "G2 Esports"
            country = "Европа"
            foundedYear = 2013
            coach = "Swani"
            tag = "G2"
        }
        teams.add(team3)

        val team4 = Team().apply {
            name = "Fnatic"
            country = "Швеция"
            foundedYear = 2004
            coach = "Keita"
            tag = "FNC"
        }
        teams.add(team4)

        val team5 = Team().apply {
            name = "Team Liquid"
            country = "США"
            foundedYear = 2000
            coach = "daps"
            tag = "TL"
        }
        teams.add(team5)

        val team6 = Team().apply {
            name = "Virtus.pro"
            country = "Россия"
            foundedYear = 2003
            coach = "dastan"
            tag = "VP"
        }
        teams.add(team6)

        val team7 = Team().apply {
            name = "Cloud9"
            country = "США"
            foundedYear = 2013
            coach = "groove"
            tag = "C9"
        }
        teams.add(team7)

        val team8 = Team().apply {
            name = "FaZe Clan"
            country = "Европа"
            foundedYear = 2010
            coach = "YNk"
            tag = "FaZe"
        }
        teams.add(team8)

        val additionalTeams = listOf(
            Team().apply {
                name = "Ninjas in Pyjamas"
                country = "Швеция"
                foundedYear = 2000
                coach = "djL"
                tag = "NiP"
            },
            Team().apply {
                name = "ENCE"
                country = "Финляндия"
                foundedYear = 2012
                coach = "sAw"
                tag = "ENCE"
            },
            Team().apply {
                name = "Heroic"
                country = "Дания"
                foundedYear = 2016
                coach = "Xizt"
                tag = "Heroic"
            }
        )
        teams.addAll(additionalTeams)

        return teamRepository.saveAll(teams)
    }

    private fun createPlayers(teams: List<Team>): List<Player> {
        if (playerRepository.count() > 0) {
            println("⚠️  Игроки уже существуют, пропускаем создание")
            return playerRepository.findAll()
        }

        val players = mutableListOf<Player>()

        // Игроки NaVi
        players.add(Player().apply {
            nickname = "s1mple"
            realName = "Олександр Костилєв"
            country = "Украина"
            role = "AWPer"
            joinDate = LocalDate.of(2013, 8, 1)
            team = teams[0]
            birthDate = LocalDate.of(1997, 10, 2)
        })

        players.add(Player().apply {
            nickname = "b1t"
            realName = "Валерій Ваховський"
            country = "Украина"
            role = "Rifler"
            joinDate = LocalDate.of(2020, 10, 1)
            team = teams[0]
            birthDate = LocalDate.of(2003, 1, 5)
        })


        return playerRepository.saveAll(players)
    }

    private fun createTournaments(): List<Tournament> {
        if (tournamentRepository.count() > 0) {
            println("⚠️  Турниры уже существуют, пропускаем создание")
            return tournamentRepository.findAll()
        }

        val tournaments = mutableListOf<Tournament>()

        val tournament1 = Tournament().apply {
            name = "PGL Major Copenhagen 2024"
            startDate = LocalDateTime.of(2024, 3, 17, 10, 0)
            game = "Counter-Strike 2"
            endDate = LocalDateTime.of(2024, 3, 31, 22, 0)
            prizePool = 1250000.0
            status = "FINISHED"
            location = "Копенгаген, Дания"
            description = "Крупнейший турнир по Counter-Strike 2 в 2024 году"
        }
        tournaments.add(tournament1)

        val tournament2 = Tournament().apply {
            name = "IEM Katowice 2024"
            startDate = LocalDateTime.of(2024, 2, 3, 12, 0)
            game = "Counter-Strike 2"
            endDate = LocalDateTime.of(2024, 2, 11, 21, 0)
            prizePool = 1000000.0
            status = "FINISHED"
            location = "Катовице, Польша"
            description = "Легендарный турнир в Spodek Arena"
        }
        tournaments.add(tournament2)

        val tournament3 = Tournament().apply {
            name = "BLAST Premier: Spring Finals 2024"
            startDate = LocalDateTime.of(2024, 6, 12, 14, 0)
            game = "Counter-Strike 2"
            endDate = LocalDateTime.of(2024, 6, 16, 23, 0)
            prizePool = 425000.0
            status = "UPCOMING"
            location = "Лондон, Великобритания"
            description = "Весенние финалы BLAST Premier"
        }
        tournaments.add(tournament3)

        val tournament4 = Tournament().apply {
            name = "The International 2024"
            startDate = LocalDateTime.of(2024, 9, 5, 10, 0)
            game = "Dota 2"
            endDate = LocalDateTime.of(2024, 9, 15, 22, 0)
            prizePool = 3000000.0
            status = "UPCOMING"
            location = "Сингапур"
            description = "Чемпионат мира по Dota 2 с самым большим призовым фондом"
        }
        tournaments.add(tournament4)

        val tournament5 = Tournament().apply {
            name = "VALORANT Champions 2024"
            startDate = LocalDateTime.of(2024, 8, 1, 11, 0)
            game = "VALORANT"
            endDate = LocalDateTime.of(2024, 8, 25, 20, 0)
            prizePool = 2000000.0
            status = "UPCOMING"
            location = "Сеул, Южная Корея"
            description = "Чемпионат мира по VALORANT"
        }
        tournaments.add(tournament5)

        return tournamentRepository.saveAll(tournaments)
    }

    private fun assignTeamsToTournaments(teams: List<Team>, tournaments: List<Tournament>) {
        // PGL Major Copenhagen 2024 - все команды CS:GO
        val csgoTeams = teams.take(8)
        tournaments[0].teams = csgoTeams.toMutableSet()

        // IEM Katowice 2024 - топ 4 команды
        tournaments[1].teams = teams.take(4).toMutableSet()

        // BLAST Premier - G2, FaZe, NaVi, Liquid
        val blastTeams = listOf(teams[2], teams[7], teams[0], teams[4])
        tournaments[2].teams = blastTeams.toMutableSet()

        // The International - Dota 2 команды
        tournaments[3].teams = teams.take(5).toMutableSet()

        tournamentRepository.saveAll(tournaments)
    }

    private fun createTeamRatings(teams: List<Team>): List<TeamRating> {
        if (teamRatingRepository.count() > 0) {
            println("⚠️  Рейтинги уже существуют, пропускаем создание")
            return teamRatingRepository.findAll()
        }

        val ratings = mutableListOf<TeamRating>()

        // Создаем рейтинги только для первых 8 команд
        for (i in 0 until minOf(8, teams.size)) {
            val rating = TeamRating().apply {
                team = teams[i]
                rating = (1500 - i * 30).coerceAtLeast(1400)
                points = (100 - i * 10).coerceAtLeast(20)
                wins = (25 - i * 3).coerceAtLeast(5)
                losses = (10 + i * 2).coerceAtMost(25)
                draws = if (i % 2 == 0) 2 else 0
                lastUpdated = LocalDateTime.now()
            }
            ratings.add(rating)
        }

        return teamRatingRepository.saveAll(ratings)
    }

    private fun createMatches(tournaments: List<Tournament>, teams: List<Team>): List<Match> {
        if (matchRepository.count() > 0) {
            println("⚠️  Матчи уже существуют, пропускаем создание")
            return matchRepository.findAll()
        }

        val matches = mutableListOf<Match>()

        // Завершенные матчи PGL Major
        val match1 = Match().apply {
            tournament = tournaments[0]
            team1 = teams[1]
            team2 = teams[2]
            date = LocalDateTime.of(2024, 3, 20, 15, 0)
            stage = "Quarterfinal"
            scoreTeam1 = 2
            scoreTeam2 = 1
            status = "FINISHED"
            winner = teams[1] // Team Spirit победил G2
        }
        matches.add(match1)


        return matchRepository.saveAll(matches)
    }

    private fun updateRatingsAfterMatches(matches: List<Match>) {
        // Обновляем рейтинги для завершенных матчей
        matches.filter { it.status == "FINISHED" }.forEach { match ->
            val winnerId = match.winner?.id
            val isDraw = match.scoreTeam1 == match.scoreTeam2

            val loserId = when {
                isDraw -> null
                winnerId == match.team1?.id -> match.team2?.id
                winnerId == match.team2?.id -> match.team1?.id
                else -> null
            }

            try {
                teamRatingService.updateRatingAfterMatch(winnerId, loserId, isDraw)
            } catch (e: Exception) {
                println("⚠️  Ошибка при обновлении рейтинга для матча ${match.id}: ${e.message}")
            }
        }
    }

    private fun printTestInfo() {
        println("\n📌 ДОСТУПНЫЕ API ЭНДПОИНТЫ:")
        println("🔐 Аутентификация:")
        println("POST /api/auth/register - регистрация")
        println("POST /api/auth/login - вход")
        println("POST /api/auth/logout - выход")
        println("GET  /api/auth/me - информация о текущем пользователе")

        println("\n📊 Тестовые данные:")
        println("GET  /api/teams - все команды")
        println("GET  /api/players - все игроки")
        println("GET  /api/tournaments - все турниры")
        println("GET  /api/matches - все матчи")
        println("GET  /api/ratings/ranking - рейтинг команд")

        println("\n🔐 Тестовые пользователи:")
        println("Администратор: admin@cybersports.ru / admin123")
        println("Модератор: moderator@cybersports.ru / moderator123")
        println("Пользователь: user@cybersports.ru / user123")

        println("\n🔗 Base URL: http://localhost:8080")
        println("\n🚀 Приложение готово к работе!")
    }
}