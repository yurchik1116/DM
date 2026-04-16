# Программа для исследования группы симметрий правильного шестиугольника (D6)

def compose(p, q):
    """Композиция p и q: сначала q, затем p."""
    return tuple(p[q[i]] for i in range(len(p)))

def perm_to_cycles(perm, vertices_1based=True):
    """Преобразует перестановку в строку циклов (вершины 1..6)."""
    n = len(perm)
    visited = [False] * n
    cycles = []
    for i in range(n):
        if not visited[i]:
            cycle = []
            j = i
            while not visited[j]:
                visited[j] = True
                cycle.append(j + 1 if vertices_1based else j)
                j = perm[j]
            if len(cycle) > 1 or (len(cycle) == 1 and cycle[0] != 1):
                cycles.append(cycle)
    if not cycles:
        return '(' + ')('.join(str(v) for v in range(1, n+1)) + ')'
    return ''.join('(' + ''.join(str(v) for v in cycle) + ')' for cycle in cycles)

# Базовые перестановки (вершины 0..5)
e = (0, 1, 2, 3, 4, 5)          # тождество
r = (1, 2, 3, 4, 5, 0)          # поворот на 60 градусов
s = (0, 5, 4, 3, 2, 1)          # отражение через вершины 0 и 3

# Генерируем все 12 элементов D6
elements = []
names = []

# Повороты r^i
for i in range(6):
    el = e
    for _ in range(i):
        el = compose(r, el)
    elements.append(el)
    names.append('e' if i == 0 else f'r^{i}')

# Отражения r^i и s
for i in range(6):
    ri = elements[i]
    el = compose(ri, s)
    elements.append(el)
    names.append('s' if i == 0 else f'r^{i}s')

# Построение таблицы умножения
size = len(elements)
mult_table = [[None] * size for _ in range(size)]
for i, a in enumerate(elements):
    for j, b in enumerate(elements):
        mult_table[i][j] = compose(a, b)

# Проверка свойств группы
closed = all(mult_table[i][j] in elements for i in range(size) for j in range(size))
has_identity = e in elements
has_inverses = all(any(compose(a, b) == e for b in elements) for a in elements)
is_group = closed and has_identity and has_inverses

# Проверка коммутативности
is_abelian = True
counterexample = None
for i in range(size):
    for j in range(size):
        if compose(elements[i], elements[j]) != compose(elements[j], elements[i]):
            is_abelian = False
            counterexample = (names[i], names[j])
            break
    if not is_abelian:
        break

# Вывод элементов в виде подстановок
print("Все самосовмещения правильного шестиугольника (вершины 1..6):")
for name, perm in zip(names, elements):
    print(f"{name:4} = {perm_to_cycles(perm)}")

# Вывод таблицы умножения (имена элементов)
print("\nТаблица умножения (строки × столбцы):")
# Сопоставление перестановки → имя
perm_to_name = {perm: name for perm, name in zip(elements, names)}
# Заголовок
header = "     " + " ".join(f"{name:>4}" for name in names)
print(header)
for i, name_row in enumerate(names):
    row = [perm_to_name[mult_table[i][j]] for j in range(size)]
    print(f"{name_row:4} | " + " ".join(f"{x:>4}" for x in row))

# Результаты
print("\n--- Проверка свойств ---")
print(f"Замкнутость: {'Да' if closed else 'Нет'}")
print(f"Наличие единицы: {'Да' if has_identity else 'Нет'}")
print(f"Наличие обратных: {'Да' if has_inverses else 'Нет'}")
print("Ассоциативность: Да (композиция перестановок ассоциативна)")
print(f"Получилась группа? {'Да' if is_group else 'Нет'}")
print(f"Группа Абелева? {'Да' if is_abelian else 'Нет'}")
if not is_abelian and counterexample:
    print(f"  Контрпример: {counterexample[0]} ∘ {counterexample[1]} ≠ {counterexample[1]} ∘ {counterexample[0]}")