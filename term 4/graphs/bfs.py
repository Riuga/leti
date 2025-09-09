from collections import deque

graph2 = {
    0: [1, 4, 5],
    1: [0, 6],
    2: [3, 5],
    3: [2, 7],
    4: [0, 5, 9],
    5: [0, 2, 4, 9, 10],
    6: [1, 11],
    7: [3, 10],
    8: [9, 13],
    9: [4, 5, 8, 10, 12],
    10: [5, 7, 9, 15],
    11: [6, 14],
    12: [9],
    13: [8, 14],
    14: [11, 13],
    15: [10]
}


def bfs_shortest_path(graph, start, end):
    # очередь для BFS, хранящая кортежи (вершина, путь до нее)
    queue = deque([(start, [start])])
    visited = set()  # множество посещенных вершин

    while queue:
        # извлекаем текущую вершину и путь до нее
        current, path = queue.popleft()

        if current == end:  # если достигли конечной вершины
            return path  # возвращаем путь

        visited.add(current)  # добавляем текущую вершину в посещенные

        # проходим по всем соседям текущей вершины
        for neighbor in graph[current]:
            if neighbor not in visited:  # если сосед еще не посещен
                # добавляем соседа и обновленный путь в очередь
                queue.append((neighbor, path + [neighbor]))

    return None  # если путь не найден


start = int(input("Введите номер начальной вершины: "))
end = int(input("Введите номер конечной вершины: "))

# Находим кратчайший путь
shortest_path = bfs_shortest_path(graph2, start, end)

if shortest_path is not None:
    print(' '.join(map(str, shortest_path)))
else:
    print(f"Нет пути между вершинами {start} и {end}.")
