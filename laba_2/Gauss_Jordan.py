def print_matrix(A):
    # Определяем функцию print_matrix, которая принимает матрицу A в качестве аргумента
    for i in A:
        # Проходим по каждой строке матрицы A
        for j in i:
            # Проходим по каждому элементу j в строке i
            print(j, " ", end="")
            # Печатаем элемент j с пробелом, не переходя на новую строку
        print("\n")
        # Печатаем новую строку после завершения печати строки матрицы
    for i in range(len(A) * 10):
        # Печатаем 10 символов "_" для разделения
        print("_", end="")
    print("\n")
    # Печатаем новую строку после завершения печати разделителей
    return
    # Завершаем выполнение функции

def gauss_jordan(matrix):
    """
    Решает систему линейных уравнений методом Гаусса-Жордана.

    Параметры:
        matrix: Расширенная матрица системы (список списков).

    Возвращает:
        Список решений системы.
    """
    n = len(matrix)  # Количество строк (уравнений)

    for i in range(n):
        # Поиск строки с максимальным элементом в текущем столбце
        max_row = i
        for j in range(i + 1, n):
            if abs(matrix[j][i]) > abs(matrix[max_row][i]):
                max_row = j

        # Обмен строк, если необходимо
        if max_row != i:
            matrix[i], matrix[max_row] = matrix[max_row], matrix[i]

        # Нормализация текущей строки
        pivot = matrix[i][i]
        if pivot == 0:
            raise ValueError("Матрица вырождена или система не имеет единственного решения")

        for j in range(i, n + 1):
            matrix[i][j] /= pivot

        # Обнуление элементов в текущем столбце для остальных строк
        for k in range(n):
            if k != i:
                factor = matrix[k][i]
                for j in range(i, n + 1):
                    matrix[k][j] -= factor * matrix[i][j]

    print_matrix(matrix)  # Печать преобразованной матрицы
    solutions = [matrix[i][n] for i in range(n)]  # Извлечение решений
    return solutions

A = [[2, 0, 3], [1, 5, -1], [3, 1, -1]]
# Определяем матрицу A
b = [[1], [8], [-2]]
# Определяем вектор b

for i in range(len(A)):
    # Проходим по каждой строке матрицы A
    A[i].append(b[i][0])
    # Добавляем соответствующий элемент из вектора b в конец строки матрицы A

solutions = gauss_jordan(A)
# Вызываем функцию gauss_jordan с матрицей A и сохраняем решения
print("Решения:", solutions)
# Печатаем найденные решения
