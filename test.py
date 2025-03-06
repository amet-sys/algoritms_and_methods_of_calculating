import numpy as np # type: ignore
import matplotlib.pyplot as plt # type: ignore
import math

# Определение функций
def eq1(x, y):
    return np.cos(y - 1) + x - 0.5

def eq2(x, y):
    return y - np.cos(x) - 3

# Создание сетки значений x и y
x = np.linspace(-10, 10, 400)
y = np.linspace(-10, 10, 400)
X, Y = np.meshgrid(x, y)

# Вычисление значений функций на сетке
Z1 = eq1(X, Y)
Z2 = eq2(X, Y)

# Построение графиков
plt.figure(figsize=(50, 50))

# График первого уравнения: cos(y-1) + x = 0.5
plt.contour(X, Y, Z1, levels=[0], colors='blue', label=r'$\cos(y-1) + x = 0.5$')

# График второго уравнения: y - cos(x) = 3
plt.contour(X, Y, Z2, levels=[0], colors='red', label=r'$y - \cos(x) = 3$')

# Настройка графика
plt.xlabel('x')
plt.ylabel('y')
plt.title('График системы уравнений')
plt.axhline(0, color='black', linewidth=0.5)
plt.axvline(0, color='black', linewidth=0.5)
plt.grid(True)
plt.legend()

# Отображение графика
plt.show()


# Определение системы уравнений
def equations(vars):
    x, y = vars
    eq1 = math.cos(y - 1) + x - 0.5
    eq2 = y - math.cos(x) - 3
    return [eq1, eq2]

# Вычисление матрицы Якоби (частные производные)
def jacobian(vars):
    x, y = vars
    # Частные производные для первого уравнения
    df1_dx = 1
    df1_dy = -math.sin(y - 1)
    # Частные производные для второго уравнения
    df2_dx = math.sin(x)
    df2_dy = 1
    return [[df1_dx, df1_dy], [df2_dx, df2_dy]]

# Метод Ньютона-Рафсона
def newton_raphson(equations, jacobian, initial_guess, tol=1e-6, max_iter=100):
    vars = initial_guess
    for i in range(max_iter):
        # Вычисляем значения уравнений и матрицы Якоби
        F = equations(vars)
        J = jacobian(vars)
        
        # Решаем систему линейных уравнений J * delta = -F
        # Используем метод Крамера для 2x2 системы
        det = J[0][0] * J[1][1] - J[0][1] * J[1][0]
        if det == 0:
            raise ValueError("Матрица Якоби вырождена")
        
        delta_x = (-F[0] * J[1][1] + F[1] * J[0][1]) / det
        delta_y = (F[0] * J[1][0] - F[1] * J[0][0]) / det
        
        # Обновляем переменные
        vars = [vars[0] + delta_x, vars[1] + delta_y]
        
        # Проверка на сходимость
        if math.sqrt(delta_x**2 + delta_y**2) < tol:
            print(f"Решение сошлось за {i + 1} итераций.")
            return vars
    
    print("Метод не сошелся за максимальное количество итераций.")
    return vars

# Начальное приближение
initial_guess = [1.0, 1.0]

# Решение системы
solution = newton_raphson(equations, jacobian, initial_guess)
print("Решение:", solution)