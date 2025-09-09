import sys


def find_bridges(n, graph):
    visited = [False] * n
    disc = [float('inf')] * n  # Время открытия вершины
    low = [float('inf')] * n  # Наименьшее время доступа
    parent = [-1] * n  # Родительская вершина
    bridges = []  # Список мостов
    # Временная метка, обернута в список для изменения внутри вложенной функции
    time = [0]

    def dfs(u):
        visited[u] = True
        disc[u] = low[u] = time[0]
        time[0] += 1

        for v in graph[u]:
            if not visited[v]:  # Если v еще не посещена
                parent[v] = u
                dfs(v)

                # Проверка условия для моста
                low[u] = min(low[u], low[v])
                if low[v] > disc[u]:
                    bridges.append((u, v))

            elif v != parent[u]:  # Обновление low[u] для обратного ребра
                low[u] = min(low[u], disc[v])

    for i in range(n):
        if not visited[i]:
            dfs(i)

    return len(bridges)


# Чтение входных данных из stdin
input_data = sys.stdin.read().strip().splitlines()
n = int(input_data[0])  # Количество вершин
graph = [[] for _ in range(n)]

for i in range(1, n + 1):
    line = input_data[i].strip()  # Читаем строку
    if line != "-1":
        neighbors = list(map(int, line.split()))  # Разбиваем строку на соседей
        graph[i - 1].extend(neighbors)  # Добавляем соседей к графу

# Подсчет мостов
result = find_bridges(n, graph)
print(result)  # Вывод результата
