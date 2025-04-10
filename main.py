import matplotlib.pyplot as plt
from tabulate import tabulate  # Для красивого вывода таблиц

# Определяем функцию f(x)
def f(x):
    return np.sin(x) + 0.5 * np.cos(2*x)

# Метод трапеций для численного интегрирования
def integrate_trapezoidal(func, a, b, N):
    x = np.linspace(a, b, N)
    h = (b - a) / (N - 1)
    integral = h * (func(x[0]) + func(x[-1])) / 2
    integral += h * np.sum(func(x[1:-1]))
    return integral

# Вычисление коэффициентов Фурье
def fourier_coefficients(func, L, N_terms, num_points=1000):
    a0 = (1 / (2 * L)) * integrate_trapezoidal(func, -L, L, num_points)
    an = []
    bn = []
    for n in range(1, N_terms + 1):
        # a_n = (1/L) * ∫ f(x) * cos(nπx/L) dx
        integrand_cos = lambda x: func(x) * np.cos(n * np.pi * x / L)
        an.append((1 / L) * integrate_trapezoidal(integrand_cos, -L, L, num_points))

        # b_n = (1/L) * ∫ f(x) * sin(nπx/L) dx
        integrand_sin = lambda x: func(x) * np.sin(n * np.pi * x / L)
        bn.append((1 / L) * integrate_trapezoidal(integrand_sin, -L, L, num_points))

    return a0, an, bn

# Построение частичной суммы ряда Фурье
def fourier_series_approximation(a0, an, bn, L, N_terms, x):
    approximation = a0
    for n in range(1, N_terms + 1):
        approximation += an[n - 1] * np.cos(n * np.pi * x / L)
        approximation += bn[n - 1] * np.sin(n * np.pi * x / L)
    return approximation

# Основная программа
import numpy as np
    # Параметры
a, b = -np.pi, np.pi  # Интервал
L = (b - a) / 2  # Полупериод
N_terms = 10  # Количество членов ряда
num_points = 1000  # Точки для графика и интегрирования

    # Вычисляем коэффициенты Фурье
a0, an, bn = fourier_coefficients(f, L, N_terms, num_points)

    # Создаем таблицу коэффициентов
table_data = [["n", "a_n", "b_n"]]
table_data.append([0, f"{a0:.6f}", "-"])  # a0 не имеет b0
for n in range(1, N_terms + 1):
    table_data.append([n, f"{an[n - 1]:.6f}", f"{bn[n - 1]:.6f}"])

# Выводим таблицу в консоль
print("Коэффициенты Фурье:")
print(tabulate(table_data, headers="firstrow", tablefmt="grid"))

    # График исходной функции
x_vals = np.linspace(a, b, num_points)
y_vals = f(x_vals)

    # График аппроксимации рядом Фурье
y_fourier = fourier_series_approximation(a0, an, bn, L, N_terms, x_vals)

    # Визуализация
plt.figure(figsize=(10, 6))
plt.plot(x_vals, y_vals, label="Исходная функция", color="blue")
plt.plot(x_vals, y_fourier, label=f"Ряд Фурье (N={N_terms})", color="red", linestyle="--")
plt.title("Разложение в ряд Фурье")
plt.xlabel("x")
plt.ylabel("f(x)")
plt.legend()

    # Добавляем легенду с кратким описанием коэффициентов
plt.text(0.05, 0.95, f"a0 = {a0:.4f}", transform=plt.gca().transAxes, fontsize=10, verticalalignment='top',
         bbox=dict(facecolor='white', alpha=0.8))
plt.text(0.05, 0.90, "Остальные коэффициенты a_n и b_n:", transform=plt.gca().transAxes, fontsize=10,
             verticalalignment='top', bbox=dict(facecolor='white', alpha=0.8))
for i, (a, b) in enumerate(zip(an[:5], bn[:5]), start=1):  # Показываем первые 5 коэффициентов
    plt.text(0.05, 0.85 - i * 0.05, f"a{i} = {a:.4f}, b{i} = {b:.4f}", transform=plt.gca().transAxes, fontsize=10,
                 verticalalignment='top')

plt.grid()
plt.show()

# Разложение функции f(x) в ряд Фурье позволяет представить её как сумму синусоидальных и косинусоидальных функций (гармоник).

# Разложение в ряд Фурье — основывается на представлении функции как суммы тригонометрических составляющих,
# где коэффициенты находятся через численное интегрирование.
# Метод эффективен для анализа периодических сигналов и аппроксимации произвольных функций.

# 1. Задать пользовательскую функцию f(x), которую нужно разложить в ряд Фурье.
# 2. Указать интервал [a, b], на котором определена функция.
# 3. Выбрать количество членов ряда N.
# 4. Численно вычислить коэффициенты a0, an и bn.
# 5. Построить частичную сумму ряда Фурье для заданного числа членов.
# 6. Вывести результат: график исходной