import sys
from collections import defaultdict


def kosaraju(n, graph):
    visited = [False] * n
    finish_stack = []

    # Первый проход DFS для заполнения стека завершения
    def dfs_first(v):
        visited[v] = True
        for neighbor in graph[v]:
            if not visited[neighbor]:
                dfs_first(neighbor)
        finish_stack.append(v)

    # Создание транспонированного графа
    transposed_graph = defaultdict(list)
    for v in range(n):
        for neighbor in graph[v]:
            transposed_graph[neighbor].append(v)

    # Второй проход DFS на транспонированном графе
    def dfs_second(v):
        visited[v] = True
        for neighbor in transposed_graph[v]:
            if not visited[neighbor]:
                dfs_second(neighbor)

    # Заполнение стека завершения
    for i in range(n):
        if not visited[i]:
            dfs_first(i)

    # Сброс посещенных вершин для второго прохода
    visited = [False] * n
    count_scc = 0

    # Обработка вершин в порядке убывания времени завершения
    while finish_stack:
        v = finish_stack.pop()
        if not visited[v]:
            dfs_second(v)
            count_scc += 1

    return count_scc


# Чтение входных данных из stdin
input_data = sys.stdin.read().strip().splitlines()
n = int(input_data[0])  # Количество вершин
graph = [[] for _ in range(n)]

for i in range(1, n + 1):
    line = input_data[i].strip()  # Читаем строку
    if line != "-1":
        neighbors = list(map(int, line.split()))  # Разбиваем строку на соседей
        graph[i - 1].extend(neighbors)  # Добавляем соседей к графу

# Подсчет компонент сильной связности
result = kosaraju(n, graph)
print(result)  # Вывод результата
