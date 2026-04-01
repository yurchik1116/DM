import math

def continued_fraction(num, den):
    """Возвращает список неполных частных цепной дроби для num/den (num, den > 0)."""
    res = []
    while den != 0:
        q = num // den
        res.append(q)
        num, den = den, num - q * den
    return res

def convergents(frac):
    """Возвращает список подходящих дробей (числитель, знаменатель) для цепной дроби."""
    p_prev2, p_prev1 = 0, 1
    q_prev2, q_prev1 = 1, 0
    convs = []
    for a in frac:
        p = a * p_prev1 + p_prev2
        q = a * q_prev1 + q_prev2
        convs.append((p, q))
        p_prev2, p_prev1 = p_prev1, p
        q_prev2, q_prev1 = q_prev1, q
    return convs

def solve_diophantine(a, b, c):
    # Обработка случаев, когда один из коэффициентов ноль
    if a == 0 and b == 0:
        if c == 0:
            return "Бесконечно много решений: x, y любые целые."
        else:
            return "Решений нет."
    if a == 0:
        if c % b != 0:
            return "Решений нет."
        y = c // b
        return f"Частное решение: x любое, y = {y}\nОбщее решение: x = t, y = {y}"
    if b == 0:
        if c % a != 0:
            return "Решений нет."
        x = c // a
        return f"Частное решение: x = {x}, y любое\nОбщее решение: x = {x}, y = t"

    g = math.gcd(a, b)
    if c % g != 0:
        return "Решений нет."

    # Сокращаем уравнение
    a1 = a // g
    b1 = b // g
    c1 = c // g

    # Работаем с положительными коэффициентами для цепной дроби
    a_abs = abs(a1)
    b_abs = abs(b1)

    # Находим частное решение для a_abs * x + b_abs * y = 1
    if b_abs == 1:
        # Случай, когда знаменатель 1: цепная дробь [a_abs], нет предпоследней
        x0_abs = 0
        y0_abs = 1
    else:
        frac = continued_fraction(a_abs, b_abs)
        convs = convergents(frac)
        n = len(frac) - 1          # индекс последней подходящей дроби
        p_prev, q_prev = convs[n-1]  # предпоследняя подходящая дробь
        if n % 2 == 1:             # n нечётное
            x0_abs = q_prev
            y0_abs = -p_prev
        else:                      # n чётное
            x0_abs = -q_prev
            y0_abs = p_prev

    # Умножаем на c1
    x0_abs *= c1
    y0_abs *= c1

    # Корректируем знаки в соответствии с a1, b1
    x0 = x0_abs if a1 > 0 else -x0_abs
    y0 = y0_abs if b1 > 0 else -y0_abs

    # Формируем ответ
    result = f"Частное решение: x0 = {x0}, y0 = {y0}\n"
    result += f"Общее решение: x = {x0} + {b1} * t, y = {y0} - {a1} * t\n\n"
    result += "Несколько решений:\n"
    for t in range(-2, 3):
        x_val = x0 + b1 * t
        y_val = y0 - a1 * t
        result += f"t = {t}: x = {x_val}, y = {y_val}\n"
    return result

def main():
    print("Решение линейных диофантовых уравнений вида ax + by = c с помощью цепных дробей.")
    try:
        a = int(input("Введите a: "))
        b = int(input("Введите b: "))
        c = int(input("Введите c: "))
    except ValueError:
        print("Ошибка ввода. Введите целые числа.")
        return

    result = solve_diophantine(a, b, c)
    print(result)


if __name__ == "__main__":
    test_cases = [
        (13, 7, 3),  # обычный случай
        (6, 9, 15),  # коэффициенты с общим делителем
        (2, 4, 5),  # нет решений
        (0, 5, 10),  # a = 0
        (3, 0, 9),  # b = 0
    ]

    for a, b, c in test_cases:
        print(f"\nУравнение: {a}x + {b}y = {c}")
        print(solve_diophantine(a, b, c))
        print("-" * 50)