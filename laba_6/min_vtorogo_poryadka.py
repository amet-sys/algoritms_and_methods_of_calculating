import math
import matplotlib.pyplot as plt

def rosenbrock(x, a=1, b=100):
    """Функция Розенброка"""
    return (a - x[0])**2 + b * (x[1] - x[0]**2)**2

def gradient_rosenbrock(x, a=1, b=100):
    """Аналитический градиент функции Розенброка"""
    dx0 = -2*(a - x[0]) - 4*b*(x[1] - x[0]**2)*x[0]
    dx1 = 2*b*(x[1] - x[0]**2)
    return [dx0, dx1]

def hessian_rosenbrock(x, a=1, b=100):
    """Аналитическая матрица Гессе для функции Розенброка"""
    # Вторые производные
    d2x0x0 = 2 - 4*b*(x[1] - x[0]**2) + 8*b*x[0]**2
    d2x0x1 = -4*b*x[0]
    d2x1x0 = -4*b*x[0]
    d2x1x1 = 2*b
    
    return [[d2x0x0, d2x0x1],
            [d2x1x0, d2x1x1]]

def solve_2x2(A, b):
    """Решение системы 2x2 линейных уравнений"""
    det = A[0][0]*A[1][1] - A[0][1]*A[1][0]
    if abs(det) < 1e-10:
        return [0, 0]  # вырожденный случай
    
    x0 = (A[1][1]*b[0] - A[0][1]*b[1]) / det
    x1 = (A[0][0]*b[1] - A[1][0]*b[0]) / det
    return [x0, x1]

def newton_method(f, grad_f, hess_f, x0, max_iter=100, tol=1e-6):
    """
    Метод Ньютона для минимизации функции
    
    Параметры:
    f - целевая функция
    grad_f - функция вычисления градиента
    hess_f - функция вычисления матрицы Гессе
    x0 - начальная точка [x, y]
    max_iter - максимальное число итераций
    tol - критерий остановки
    
    Возвращает:
    x - найденную точку минимума
    history - историю значений функции и точек
    """
    x = x0.copy()
    history = {'points': [], 'values': []}
    
    for i in range(max_iter):
        grad = grad_f(x)
        H = hess_f(x)
        
        # Критерий остановки
        if math.sqrt(grad[0]**2 + grad[1]**2) < tol:
            break
            
        # Решаем систему H*d = -grad
        direction = solve_2x2(H, [-g for g in grad])
        
        # Обновляем точку
        x[0] += direction[0]
        x[1] += direction[1]
        
        # Сохраняем историю
        history['points'].append(x.copy())
        history['values'].append(f(x))
    
    return x, history

# Начальная точка
x0 = [-1.5, 2.0]

# Применяем метод Ньютона
x_opt, history = newton_method(rosenbrock, gradient_rosenbrock, hessian_rosenbrock, x0)

# Результаты
print("Метод Ньютона для функции Розенброка:")
print(f"Найденный минимум: ({x_opt[0]:.8f}, {x_opt[1]:.8f})")
print(f"Значение функции в минимуме: {rosenbrock(x_opt):.10f}")
print(f"Количество итераций: {len(history['values'])}")

# Вывод истории сходимости
print("\nИстория сходимости:")
for i, (point, value) in enumerate(zip(history['points'], history['values'])):
    print(f"Iter {i+1}: x={point[0]:.6f}, y={point[1]:.6f}, f(x,y)={value:.6f}")


# Траектория метода
points = history['points']
x_vals = [p[0] for p in points]
y_vals = [p[1] for p in points]

# Создаем график
plt.figure(figsize=(10, 6))
plt.plot(x_vals, y_vals, 'bo-', label='Траектория метода Ньютона')
plt.scatter([1], [1], c='r', marker='*', s=200, label='Глобальный минимум')
plt.xlabel('x')
plt.ylabel('y')
plt.title('Траектория метода Ньютона для функции Розенброка')
plt.legend()
plt.grid(True)
plt.show()