from scipy.sparse import csr_array
from scipy.sparse.csgraph import floyd_warshall
import networkx as nx
import matplotlib.pyplot as plt
import numpy as np

# Создание графа
G = nx.Graph()  # не ориентированный
G = nx.DiGraph(directed=True)  # ориентированный

# Добавление вершин, т.е. задание множества A для прямого произведения A*A
G.add_nodes_from([1, 2, 3, 4, 5])
# Добавление рёбер, то есть задание бинарного отношения, т.е. подмножества A*A
A = [(1, 3), (2, 3), (2, 1), (5, 4), (1, 5), (2, 3)]

G.add_edges_from(A)

# Визуализация графа
nx.draw(G, with_labels=True, node_color='lightblue', node_size=500, font_size=16, font_weight='bold')
plt.title("Граф бинарного отношения")
plt.show()

# Нахождение матрицы смежности B по бинарному отношению
n = 5  # задание числа вершин графа
B = np.zeros((n, n))

for t in A:
    B[t[0] - 1][t[1] - 1] = 1
# матрица смежности графа по заданному бинарному отношению
print("Матрица смежности B:")
print(B)

graph = B
graph = csr_array(graph)
print("\nРазреженная матрица смежности:")
print(graph)

dist_matrix, predecessors = floyd_warshall(csgraph=graph, directed=True, return_predecessors=True)
print("\nМатрица расстояний (кратчайшие пути):")
print(
    dist_matrix)  # Матрица расстояний N x N между узлами графа. dist_matrix[i,j] задает кратчайшее расстояние от точки i до точки j на графе
print("\nМатрица предшественников:")
print(predecessors)


# Функции для проверки свойств бинарного отношения
def check_reflexivity(matrix):
    #Проверка на рефлексивность: все элементы главной диагонали равны 1
    n = len(matrix)
    for i in range(n):
        if matrix[i][i] != 1:
            return False
    return True


def check_antireflexivity(matrix):
    #Проверка на антирефлексивность: все элементы главной диагонали равны 0
    n = len(matrix)
    for i in range(n):
        if matrix[i][i] != 0:
            return False
    return True


def check_symmetry(matrix):
    #Проверка на симметричность: matrix[i][j] = matrix[j][i] для всех i, j
    n = len(matrix)
    for i in range(n):
        for j in range(n):
            if matrix[i][j] != matrix[j][i]:
                return False
    return True


def check_antisymmetry(matrix):
    #Проверка на антисимметричность: если matrix[i][j] = 1 и i != j, то matrix[j][i] = 0
    n = len(matrix)
    for i in range(n):
        for j in range(n):
            if i != j and matrix[i][j] == 1 and matrix[j][i] == 1:
                return False
    return True


def check_transitivity(matrix):
    #Проверка на транзитивность: если есть пути i->j и j->k, то должно быть i->k
    n = len(matrix)
    # Используем алгоритм Уоршелла для нахождения транзитивного замыкания
    tc = matrix.copy()

    # Алгоритм Уоршелла
    for k in range(n):
        for i in range(n):
            for j in range(n):
                if tc[i][k] and tc[k][j]:
                    tc[i][j] = 1

    # Проверяем, что исходная матрица содержит все пути из транзитивного замыкания
    for i in range(n):
        for j in range(n):
            if tc[i][j] == 1 and matrix[i][j] != 1:
                return False
    return True


def check_linearity(matrix):
    #Проверка на линейность (сравнимость): для любых различных i, j либо i->j, либо j->i
    n = len(matrix)
    for i in range(n):
        for j in range(n):
            if i != j and matrix[i][j] == 0 and matrix[j][i] == 0:
                return False
    return True


# Проверка свойств
print("ПРОВЕРКА СВОЙСТВ БИНАРНОГО ОТНОШЕНИЯ")

# Рефлексивность
if check_reflexivity(B):
    print("Рефлексивно")
else:
    print("Нерефлексивно")

# Антирефлексивность
if check_antireflexivity(B):
    print("Антирефлексивно")
else:
    print("Не антирефлексивно")

# Симметричность
if check_symmetry(B):
    print("Симметрично")
else:
    print("Не симметрично")

# Антисимметричность
if check_antisymmetry(B):
    print("Антисимметрично")
else:
    print("Не антисимметрично")

# Транзитивность
if check_transitivity(B):
    print("Транзитивно")
else:
    print("Нетранзитивно")

# Линейность
if check_linearity(B):
    print("Линейно")
else:
    print("Не линейно")