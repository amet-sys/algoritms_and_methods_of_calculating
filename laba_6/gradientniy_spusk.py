"""
Я реализую метод градиентного спуска (метод первого порядка) для минимизации известной тестовой функции Розенброка.
Этот метод хорошо подходит для демонстрации, так как:

    Прост в реализации

    Не требует вычисления матрицы Гессе (в отличие от методов второго порядка)

    Хорошо работает на гладких функциях
"""

"""
Функция Розенброка

Функция Розенброка - это классическая тестовая функция для оптимизации:
f(x, y) = (a - x)² + b(y - x²)²

Глобальный минимум находится в точке (a, a²). Для стандартных параметров a=1, b=100 минимум равен 0 в точке (1, 1).
"""

import math

def rosenbrock(x, a=1, b=100):
    """Функция Розенброка"""
    return (a - x[0])**2 + b * (x[1] - x[0]**2)**2

def gradient_rosenbrock(x, a=1, b=100):
    """Аналитический градиент функции Розенброка"""
    dx0 = -2*(a - x[0]) - 4*b*(x[1] - x[0]**2)*x[0]
    dx1 = 2*b*(x[1] - x[0]**2)
    return [dx0, dx1]

def gradient_descent(f, grad_f, x0, learning_rate=0.001, max_iter=10000, tol=1e-6):
    """
    Метод градиентного спуска для минимизации функции
    
    Параметры:
    f - целевая функция
    grad_f - функция вычисления градиента
    x0 - начальная точка [x, y]
    learning_rate - начальный размер шага
    max_iter - максимальное число итераций
    tol - критерий остановки (по норме градиента)
    
    Возвращает:
    x - найденную точку минимума
    history - историю значений функции и точек
    """
    x = x0.copy()
    history = {'points': [], 'values': []}
    
    for i in range(max_iter):
        # Вычисляем градиент
        grad = grad_f(x)
        
        # Критерий остановки
        if math.sqrt(grad[0]**2 + grad[1]**2) < tol:
            break
            
        # Обновляем точку
        x[0] -= learning_rate * grad[0]
        x[1] -= learning_rate * grad[1]
        
        # Сохраняем историю
        history['points'].append(x.copy())
        history['values'].append(f(x))
        
        # Адаптивное изменение learning_rate (простое правило)
        if i > 0 and history['values'][-1] > history['values'][-2]:
            learning_rate *= 0.9  # уменьшаем шаг если функция растет
    
    return x, history

def line_search(f, x, direction, max_alpha=1.0, max_iter=100, tol=1e-6):
    """Поиск оптимального шага вдоль направления (метод золотого сечения)"""
    gr = (math.sqrt(5) + 1) / 2  # золотое сечение
    
    a = 0
    b = max_alpha
    
    c = b - (b - a) / gr
    d = a + (b - a) / gr
    
    phi = lambda alpha: f([x[0] + alpha * direction[0], 
                          x[1] + alpha * direction[1]])
    
    for _ in range(max_iter):
        if phi(c) < phi(d):
            b = d
        else:
            a = c
            
        if abs(b - a) < tol:
            break
            
        c = b - (b - a) / gr
        d = a + (b - a) / gr
    
    return (a + b) / 2

def gradient_descent_with_line_search(f, grad_f, x0, max_iter=10000, tol=1e-6):
    """
    Метод градиентного спуска с поиском оптимального шага
    
    Параметры:
    f - целевая функция
    grad_f - функция вычисления градиента
    x0 - начальная точка [x, y]
    max_iter - максимальное число итераций
    tol - критерий остановки
    
    Возвращает:
    x - найденную точку минимума
    history - историю значений
    """
    x = x0.copy()
    history = {'points': [], 'values': []}
    
    for i in range(max_iter):
        grad = grad_f(x)
        norm_grad = math.sqrt(grad[0]**2 + grad[1]**2)
        
        if norm_grad < tol:
            break
            
        # Направление антиградиента
        direction = [-g/norm_grad for g in grad]  # нормализованный
        
        # Оптимальный шаг
        alpha = line_search(f, x, direction)
        
        # Обновление точки
        x[0] += alpha * direction[0]
        x[1] += alpha * direction[1]
        
        history['points'].append(x.copy())
        history['values'].append(f(x))
    
    return x, history

# Начальная точка (обычно выбирают [-1.5, 2.0] для тестирования)
x0 = [-1.5, 2.0]

# Простой градиентный спуск с фиксированным шагом
print("Градиентный спуск с фиксированным шагом:")
x_gd, hist_gd = gradient_descent(rosenbrock, gradient_rosenbrock, x0, learning_rate=0.001)
print(f"Найденный минимум: ({x_gd[0]:.6f}, {x_gd[1]:.6f})")
print(f"Значение функции: {rosenbrock(x_gd):.6f}")
print(f"Количество итераций: {len(hist_gd['values'])}")

# Градиентный спуск с поиском оптимального шага
print("\nГрадиентный спуск с поиском оптимального шага:")
x_ls, hist_ls = gradient_descent_with_line_search(rosenbrock, gradient_rosenbrock, x0)
print(f"Найденный минимум: ({x_ls[0]:.6f}, {x_ls[1]:.6f})")
print(f"Значение функции: {rosenbrock(x_ls):.6f}")
print(f"Количество итераций: {len(hist_ls['values'])}")

import matplotlib.pyplot as plt

# Траектория для метода с фиксированным шагом
points_gd = hist_gd['points']
x_vals = [p[0] for p in points_gd]
y_vals = [p[1] for p in points_gd]

# Траектория для метода с поиском шага
points_ls = hist_ls['points']
x_ls_vals = [p[0] for p in points_ls]
y_ls_vals = [p[1] for p in points_ls]

# Создаем график
plt.figure(figsize=(10, 6))
plt.plot(x_vals, y_vals, 'b-', label='Фиксированный шаг', alpha=0.5)
plt.plot(x_ls_vals, y_ls_vals, 'r-', label='Оптимальный шаг', alpha=0.8)
plt.scatter([1], [1], c='g', marker='*', s=200, label='Глобальный минимум')
plt.xlabel('x')
plt.ylabel('y')
plt.title('Траектории градиентного спуска для функции Розенброка')
plt.legend()
plt.grid(True)
plt.show()