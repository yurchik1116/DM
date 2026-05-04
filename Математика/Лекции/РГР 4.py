import math
from typing import List, Tuple

# 1. Решение системы сравнений
def egcd(a: int, b: int) -> Tuple[int, int, int]:
    #Расширенный алгоритм Евклида: возвращает (gcd, x, y), где a*x + b*y = gcd
    if b == 0:
        return (a, 1, 0)
    else:
        g, x1, y1 = egcd(b, a % b)
        return (g, y1, x1 - (a // b) * y1)

def modinv(a: int, m: int) -> int:
    #Обратное число к a по модулю m (если существует)
    g, x, _ = egcd(a, m)
    if g != 1:
        raise ValueError(f"Обратного элемента для {a} по модулю {m} не существует")
    return x % m

def solve_crt(remainders: List[int], moduli: List[int]) -> int:
    """
    Решает систему сравнений:
        x = remainders[i] (mod moduli[i])
    Используется китайская теорема об остатках.
    Проверяется совместность.
    Возвращает наименьшее неотрицательное решение.
    """
    if not remainders or not moduli or len(remainders) != len(moduli):
        raise ValueError("Списки остатков и модулей должны быть непустыми и одинаковой длины")

    # Нормализация остатков
    for i in range(len(moduli)):
        remainders[i] %= moduli[i]

    x = remainders[0]
    M = moduli[0]

    for i in range(1, len(moduli)):
        r2 = remainders[i]
        m2 = moduli[i]

        # Решаем: x = r1 (mod M) и x = r2 (mod m2)
        g = math.gcd(M, m2)
        if (r2 - x) % g != 0:
            raise ValueError("Система несовместна")

        # Приводим к виду: x + k*M = r2 (mod m2)  =>  k*M = r2 - x (mod m2)
        m2_div = m2 // g
        rhs = (r2 - x) // g
        M_div = M // g

        # Находим обратное к M_div по модулю m2_div
        inv = modinv(M_div, m2_div)
        k = (rhs * inv) % m2_div

        # Новое решение
        x = x + k * M
        M = M * m2_div
        x %= M

    return x

# Пример использования
if __name__ == "__main__":
    # Система: x = 2 (mod 3), x = 3 (mod 5), x = 2 (mod 7)
    rem = [2, 3, 2]
    mod = [3, 5, 7]
    sol = solve_crt(rem, mod)
    print(f"Решение системы {list(zip(rem, mod))}: x = {sol} (mod {math.prod(mod)})")
    # Проверка
    for r, m in zip(rem, mod):
        print(f"  {sol} = {r} (mod {m}): {sol % m == r}")

# 2. Шифрование RSA фразы
def rsa_encrypt(text: str, e: int, n: int) -> List[int]:
    """
    Шифрует текст с помощью RSA.
    Каждый символ преобразуется в его Unicode-код и шифруется: c = m^e mod n.
    """
    encrypted = []
    for ch in text:
        m = ord(ch)          # числовое представление символа
        if m >= n:
            raise ValueError(f"Символ '{ch}' (код {m}) превышает модуль n={n}. Используйте больший модуль.")
        c = pow(m, e, n)
        encrypted.append(c)
    return encrypted

def rsa_decrypt(cipher: List[int], d: int, n: int) -> str:
    # Расшифровывает список чисел обратно в строку.
    decrypted_chars = []
    for c in cipher:
        m = pow(c, d, n)
        decrypted_chars.append(chr(m))
    return ''.join(decrypted_chars)

# Параметры RSA
p = 61
q = 53
n = p * q                     # 3233
phi = (p - 1) * (q - 1)       # 3120
e = 17                        # открытая экспонента
d = modinv(e, phi)            # 2753

print("\n RSA шифрование")
print(f"Открытый ключ: (n={n}, e={e})")
print(f"Закрытый ключ: (n={n}, d={d})")

phrase = "Четные числа - питательны, а нечетные - просто вкусные"
print(f"Исходная фраза: {phrase}")

# Шифрование
ciphertext = rsa_encrypt(phrase, e, n)
print(f"Зашифрованная фраза (числа): {ciphertext}")

# Дешифрование (для проверки)
decrypted = rsa_decrypt(ciphertext, d, n)
print(f"Расшифрованная фраза: {decrypted}")
assert phrase == decrypted, "Ошибка: расшифрованный текст не совпадает с исходным!"