import matplotlib.pyplot as plt

# Функция для вычисления базисного полинома Лагранжа
def lagrange_basis(x, x_points, i):
    """
    Вычисляет i-й базисный полином Лагранжа.
    :param x: Точка, в которой вычисляется полином.
    :param x_points: Список узлов интерполяции.
    :param i: Индекс базисного полинома.
    :return: Значение базисного полинома в точке x.
    """
    basis = 1.0
    for j in range(len(x_points)):
        if j != i:
            basis *= (x - x_points[j]) / (x_points[i] - x_points[j])
    return basis

# Функция для вычисления интерполяционного многочлена Лагранжа
def lagrange_polynomial(x, x_points, y_points):
    """
    Вычисляет значение интерполяционного многочлена Лагранжа в точке x.
    :param x: Точка, в которой вычисляется полином.
    :param x_points: Список узлов интерполяции.
    :param y_points: Список значений функции в узлах интерполяции.
    :return: Значение интерполяционного многочлена в точке x.
    """
    polynomial = 0.0
    for i in range(len(x_points)):
        polynomial += y_points[i] * lagrange_basis(x, x_points, i)
    if x in [1,2,3,4,5]:
        print(x, polynomial)
    return polynomial

# Заданные точки (узлы интерполяции)
x_points = [1, 2, 3, 4, 5]  # Узлы по оси x
y_points = [5.1, 6, 4.0, -10, 0]  # Узлы по оси y

# Генерация точек для построения графика
x_plot = [i * 0.1 for i in range(-10, 90)]  # Точки для построения графика
y_plot = [lagrange_polynomial(x, x_points, y_points) for x in x_plot]  # Значения полинома Лагранжа

# Построение графика
plt.figure(figsize=(100, 60))
plt.plot(x_plot, y_plot, label="Интерполяционный многочлен Лагранжа", color="blue")
plt.scatter(x_points, y_points, color="red", label="Узлы интерполяции")
plt.title("Интерполяционный многочлен Лагранжа")
plt.xlabel("x")
plt.ylabel("y")
plt.legend()
plt.grid(True)
plt.show()
