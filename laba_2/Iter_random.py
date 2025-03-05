import random

def dot_product(v1, v2):
    """Вычисляет скалярное произведение двух векторов."""
    return sum(x * y for x, y in zip(v1, v2))

def vector_norm(v):
    """Вычисляет евклидову норму вектора."""
    return sum(x ** 2 for x in v) ** 0.5

def matrix_vector_mult(A, x):
    """Умножает матрицу A на вектор x."""
    return [dot_product(row, x) for row in A]

def randomized_kaczmarz(A, b, max_iter=10000, tol=0.00001):
    """
    Решение СЛАУ Ax = b методом случайных направлений (Randomized Kaczmarz).

    Параметры:
    A : list of lists
        Матрица коэффициентов системы (m x n).
    b : list
        Вектор правой части системы (m x 1).
    max_iter : int, optional
        Максимальное количество итераций (по умолчанию 1000).
    tol : float, optional
        Точность решения (по умолчанию 1e-6).

    Возвращает:
    x : list
        Приближенное решение системы (n x 1).
    residuals : list
        Невязки на каждой итерации.
    """
    m = len(A)  # Количество строк
    n = len(A[0])  # Количество столбцов
    x = [0.0] * n  # Начальное приближение
    residuals = []  # Для хранения невязок

    for k in range(max_iter):
        i = random.randint(0, m - 1)  # Случайный выбор строки
        ai = A[i]
        bi = b[i]

        # Обновление решения
        dot_ai_x = dot_product(ai, x)
        denominator = dot_product(ai, ai)
        if denominator == 0:
            continue  # Избегаем деления на ноль
        x = [x[j] + (bi - dot_ai_x) / denominator * ai[j] for j in range(n)]

        # Вычисление невязки
        Ax = matrix_vector_mult(A, x)
        residual = vector_norm([Ax[j] - b[j] for j in range(m)])
        residuals.append(residual)

        # Проверка на сходимость
        if residual < tol:
            print("Колличество итераций" ,k)
            break

    return x, residuals

A = [[3, 1, -1], [1, 5, -1], [20, 0, 3]]
# Определяем матрицу A
b = [-2, 8, 1]
# Определяем вектор b

x, residuals = randomized_kaczmarz(A, b)
print("Приближенное решение x:", x)
# print("Невязки на каждой итерации:", residuals)