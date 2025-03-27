import matplotlib.pyplot as plt
import math

# Узлы интерполяции от -10 до 10 с шагом 0.1
x_points = [x * 0.5 for x in range(-10, 10)]  # Генерация узлов
y_points = [math.sin(x) for x in x_points]  # Значения функции sin(x) в узлах
y_derivatives = [math.cos(x) for x in x_points]  # Производные функции sin(x) в узлах

# Базисные функции Эрмита
def h00(t):
    return 2 * t**3 - 3 * t**2 + 1

def h01(t):
    return -2 * t**3 + 3 * t**2

def h10(t):
    return t**3 - 2 * t**2 + t

def h11(t):
    return t**3 - t**2

# Функция для вычисления сплайна Эрмита
def hermite_spline(x, x_points, y_points, y_derivatives):
    for i in range(len(x_points) - 1):
        if x_points[i] <= x < x_points[i + 1]:
            h = x_points[i + 1] - x_points[i]
            t = (x - x_points[i]) / h
            return (
                y_points[i] * h00(t) +
                y_points[i + 1] * h01(t) +
                y_derivatives[i] * h10(t) * h +
                y_derivatives[i + 1] * h11(t) * h
            )
    
    return y_points[-1]

# Генерация точек для построения графика
x_plot = [x * 0.01 for x in range(-1000, 1001)]  # Точки для графика с шагом 0.01
y_spline = [hermite_spline(x, x_points, y_points, y_derivatives) for x in x_plot]
y_exact = [math.sin(x) for x in x_plot]\

print(hermite_spline(3.8,x_points, y_points, y_derivatives))

# Построение графика
plt.figure(figsize=(14, 8))
plt.plot(x_plot, y_spline, label="Сплайн Эрмита", color="blue")
plt.plot(x_plot, y_exact, label="Точная функция sin(x)", color="red", linestyle="--")
plt.scatter(x_points, y_points, color="green", label="Узлы интерполяции", s=18)
plt.title("Сплайн Эрмита для функции sin(x) на интервале [-10, 10]")
plt.xlabel("x")
plt.ylabel("y")
plt.legend()
plt.grid(True)
plt.show()