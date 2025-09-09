def dfs(vertex, graph, visited):
    """Функция для выполнения обхода в глубину (DFS)."""
    visited.add(vertex)  # Помечаем вершину как посещенную
    for neighbor in graph[vertex]:  # Проходим по всем соседям
        if neighbor not in visited:  # Если сосед еще не посещен
            dfs(neighbor, graph, visited)  # Рекурсивно вызываем DFS для соседа


def count_connected_components(graph):
    """Функция для подсчета компонент связности в графе."""
    visited = set()  # Множество для хранения посещенных вершин
    component_count = 0  # Счетчик компонент связности

    for vertex in range(len(graph)):
        if vertex not in visited:  # Если вершина еще не посещена
            dfs(vertex, graph, visited)  # Запускаем DFS
            component_count += 1  # Увеличиваем счетчик компонент

    return component_count


# Чтение входных данных
n = int(input("Введите количество вершин: "))  # Количество вершин
graph = []

for i in range(n):
    line = input().strip()  # Читаем строку
    if line == "-1":
        graph.append([])  # Если -1, добавляем пустой список
    else:
        neighbors = list(map(int, line.split()))  # Разбиваем строку на соседей
        graph.append(neighbors)  # Добавляем список соседей в граф

# Подсчет компонент связности
result = count_connected_components(graph)
print(result)  # Вывод результата
