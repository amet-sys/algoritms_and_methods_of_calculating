import matplotlib.pyplot as plt
import math

# Узлы интерполяции
x_points = [1.00, 1.04, 1.08, 1.12, 1.16, 1.20]
y_points = [math.sin(x) for x in x_points]

# Функция для вычисления кубического сплайна
def cubic_spline(x, x_points, y_points):
    n = len(x_points)
    h = [x_points[i+1] - x_points[i] for i in range(n-1)]
    alpha = [0] * n
    for i in range(1, n-1):
        alpha[i] = (3/h[i]) * (y_points[i+1] - y_points[i]) - (3/h[i-1]) * (y_points[i] - y_points[i-1])
    
    # Решение системы уравнений для нахождения коэффициентов c
    l = [1] * n
    mu = [0] * n
    z = [0] * n
    for i in range(1, n-1):
        l[i] = 2 * (x_points[i+1] - x_points[i-1]) - h[i-1] * mu[i-1]
        mu[i] = h[i] / l[i]
        z[i] = (alpha[i] - h[i-1] * z[i-1]) / l[i]
    
    c = [0] * n
    l[-1] = 1
    z[-1] = 0
    c[-1] = 0
    for j in range(n-2, -1, -1):
        c[j] = z[j] - mu[j] * c[j+1]
    
    # Нахождение коэффициентов b и d
    b = [0] * (n-1)
    d = [0] * (n-1)
    for i in range(n-1):
        b[i] = (y_points[i+1] - y_points[i]) / h[i] - h[i] * (c[i+1] + 2 * c[i]) / 3
        d[i] = (c[i+1] - c[i]) / (3 * h[i])
    
    # Поиск интервала, в который попадает x
    for i in range(n-1):
        if x_points[i] <= x < x_points[i+1]:
            dx = x - x_points[i]
            return y_points[i] + b[i] * dx + c[i] * dx**2 + d[i] * dx**3
    
    
    return y_points[-1]

# Генерация точек для построения графика
x_plot = [i * 0.001 for i in range(1000, 1201)]
y_spline = [cubic_spline(x, x_points, y_points) for x in x_plot]
y_exact = [math.sin(x) for x in x_plot]

print(cubic_spline(1.17,x_points, y_points))

# Построение графика
plt.figure(figsize=(10, 6))
plt.plot(x_plot, y_spline, label="Кубический сплайн", color="blue")
plt.plot(x_plot, y_exact, label="Точная функция sin(x)", color="red", linestyle="--")
plt.scatter(x_points, y_points, color="green", label="Узлы интерполяции")
plt.title("Кубический сплайн для функции sin(x)")
plt.xlabel("x")
plt.ylabel("y")
plt.legend()
plt.grid(True)
plt.show()