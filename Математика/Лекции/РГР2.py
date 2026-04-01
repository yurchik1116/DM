from collections import deque, defaultdict

def topological_sort(n, edges):
    """
    Выполняет топологическую сортировку ориентированного ациклического графа.

    Параметры:
        n (int): количество вершин (вершины нумеруются от 0 до n-1)
        edges (list of tuple): список рёбер (u, v), означающих, что u < v

    Возвращает:
        list: список вершин в порядке линейного расширения частичного порядка

    Исключения:
        ValueError: если граф содержит цикл (частичный порядок не может быть дополнен до линейного)
    """
    # Строим список смежности и массив степеней захода
    graph = defaultdict(list)
    indegree = [0] * n

    for u, v in edges:
        graph[u].append(v)
        indegree[v] += 1

    # Инициализируем очередь вершинами с нулевой степенью захода
    queue = deque([v for v in range(n) if indegree[v] == 0])
    order = []

    while queue:
        u = queue.popleft()
        order.append(u)

        for v in graph[u]:
            indegree[v] -= 1
            if indegree[v] == 0:
                queue.append(v)

    # Если в порядке не все вершины, значит есть цикл
    if len(order) != n:
        raise ValueError("Граф содержит цикл, частичный порядок не может быть дополнен до линейного.")

    return order


# Пример использования
if __name__ == "__main__":
    # Частичный порядок: 0 < 1, 0 < 2, 1 < 3, 2 < 3
    n = 4
    edges = [(0, 1), (0, 2), (1, 3), (2, 3)]

    try:
        linear_order = topological_sort(n, edges)
        print("Линейное расширение частичного порядка:", linear_order)
    except ValueError as e:
        print(e)