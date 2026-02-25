def boolean_matrix_operations(A, B, operation):
    """
    Выполняет одну из пяти операций над булевыми матрицами A и B.

    Параметры:
    A, B: списки списков (матрицы) с элементами 0 или 1.
    operation: строка, указывающая операцию:
        'or'       — дизъюнкция (R1 ∨ R2)
        'transpose'— транспонирование (только A)
        'invert'   — инвертирование (только A)
        'subtract' — вычитание (A - B)
        'multiply' — умножение (A × B)

    Возвращает:
        Результирующую матрицу (список списков) или None, если операция неверна.
    """

    def ensure_boolean(value):
        #Гарантирует, что результат будет 0 или 1
        return 1 if value else 0

    if operation == 'or':
        # Проверка размеров
        if len(A) != len(B) or any(len(rowA) != len(rowB) for rowA, rowB in zip(A, B)):
            raise ValueError("Матрицы должны быть одинакового размера для дизъюнкции")
        rows = len(A)
        cols = len(A[0])
        result = [[0] * cols for _ in range(rows)]
        for i in range(rows):
            for j in range(cols):
                result[i][j] = A[i][j] | B[i][j]
        return result

    elif operation == 'transpose':
        rows = len(A)
        cols = len(A[0])
        result = [[0] * rows for _ in range(cols)]
        for i in range(rows):
            for j in range(cols):
                result[j][i] = A[i][j]
        return result

    elif operation == 'invert':
        rows = len(A)
        cols = len(A[0])
        result = [[0] * cols for _ in range(rows)]
        for i in range(rows):
            for j in range(cols):
                result[i][j] = 1 - A[i][j]  # или ~A[i][j] & 1
        return result

    elif operation == 'subtract':
        if len(A) != len(B) or any(len(rowA) != len(rowB) for rowA, rowB in zip(A, B)):
            raise ValueError("Матрицы должны быть одинакового размера для вычитания")
        rows = len(A)
        cols = len(A[0])
        result = [[0] * cols for _ in range(rows)]
        for i in range(rows):
            for j in range(cols):
                # A[i,j] & (1 - B[i,j])
                result[i][j] = A[i][j] & (1 - B[i][j])
        return result

    elif operation == 'multiply':
        # Проверка: число столбцов A должно равняться числу строк B
        if len(A[0]) != len(B):
            raise ValueError("Число столбцов A должно равняться числу строк B для умножения")
        rowsA = len(A)
        colsA = len(A[0])
        colsB = len(B[0]) if B else 0
        result = [[0] * colsB for _ in range(rowsA)]
        for i in range(rowsA):
            for j in range(colsB):
                s = 0
                for k in range(colsA):
                    # A[i,k] & B[k,j]
                    s |= (A[i][k] & B[k][j])
                result[i][j] = ensure_boolean(s)
        return result

    else:
        print(f"Неизвестная операция: {operation}")
        return None


def print_matrix(matrix, title=""):
    #Выводит матрицу в читаемом виде
    if title:
        print(title)
    for row in matrix:
        print(" ".join(map(str, row)))
    print()


# Пример
if __name__ == "__main__":
    A = [
        [1, 0, 1],
        [0, 1, 0],
        [1, 1, 0]
    ]

    B = [
        [0, 1, 0],
        [1, 1, 1],
        [0, 0, 1]
    ]

    print_matrix(A, "Матрица A:")
    print_matrix(B, "Матрица B:")

    # 1. Дизъюнкция
    C_or = boolean_matrix_operations(A, B, 'or')
    print_matrix(C_or, "A ∨ B (дизъюнкция):")

    # 2. Транспонирование A
    C_trans = boolean_matrix_operations(A, None, 'transpose')
    print_matrix(C_trans, "Транспонированная A^T:")

    # 3. Инвертирование A
    C_inv = boolean_matrix_operations(A, None, 'invert')
    print_matrix(C_inv, "Инвертированная ¬A:")

    # 4. Вычитание A - B
    C_sub = boolean_matrix_operations(A, B, 'subtract')
    print_matrix(C_sub, "A - B (вычитание):")

    # 5. Умножение A × B
    C_mul = boolean_matrix_operations(A, B, 'multiply')
    print_matrix(C_mul, "A × B (булево умножение):")