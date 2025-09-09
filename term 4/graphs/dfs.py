graph = {
    0: [1, 2, 3],
    1: [0, 4, 5],
    2: [0, 6, 7],
    3: [0, 8, 9],
    4: [1, 10, 11, 12],
    5: [1, 13, 14],
    6: [2, 15],
    7: [2, 16, 17],
    8: [3],
    9: [3, 18],
    10: [4],
    11: [4],
    12: [4, 19, 20],
    13: [5],
    14: [5],
    15: [6, 21, 22, 23],
    16: [7, 24, 25],
    17: [7, 26, 27],
    18: [9, 28, 29],
    19: [12],
    20: [12],
    21: [15],
    22: [15],
    23: [15],
    24: [16],
    25: [16],
    26: [17],
    27: [17],
    28: [18],
    29: [18]}


def dfs(graph, start, end, visited, depth):
    if start == end:
        return depth

    visited.add(start)

    for neighbor in graph[start]:
        if neighbor not in visited:
            result = dfs(graph, neighbor, end, visited, depth + 1)
            if result is not None:
                return result

    visited.remove(start)
    return None


def find_distance(graph, start, end):
    visited = set()
    distance = dfs(graph, start, end, visited, 0)
    return distance


start, end = map(int,
                 input("Введите номера начальной и конечной вершины: ").split())

distance = find_distance(graph, start, end)

if distance is not None:
    print(distance)
else:
    print(f"Нет пути между вершинами {start} и {end}.")
