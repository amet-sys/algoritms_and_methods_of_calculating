import itertools
import math
import random

def generate_random_points(num_points, max_x=100, max_y=100):
    """Генерация случайных точек на плоскости"""
    return [(random.randint(0, max_x), random.randint(0, max_y)) for _ in range(num_points)]

def calculate_distance(p1, p2):
    """Вычисление евклидова расстояния между двумя точками"""
    return math.sqrt((p1[0] - p2[0])**2 + (p1[1] - p2[1])**2)

def create_distance_matrix(points):
    """Создание матрицы расстояний между всеми точками"""
    n = len(points)
    matrix = [[0] * n for _ in range(n)]
    for i in range(n):
        for j in range(i+1, n):
            dist = calculate_distance(points[i], points[j])
            matrix[i][j] = dist
            matrix[j][i] = dist
    return matrix

def brute_force_tsp(points):
    """Решение задачи коммивояжера методом полного перебора"""
    n = len(points)
    if n <= 1:
        return points, 0
    
    # Создаем матрицу расстояний
    distance_matrix = create_distance_matrix(points)
    
    min_path = None
    min_distance = float('inf')
    
    # Перебираем все возможные перестановки точек (кроме первой, которую фиксируем)
    for permutation in itertools.permutations(range(1, n)):
        current_distance = 0
        # Добавляем первую точку в начало и конец маршрута
        path = [0] + list(permutation) + [0]
        
        # Вычисляем общее расстояние маршрута
        for i in range(len(path)-1):
            current_distance += distance_matrix[path[i]][path[i+1]]
        
        # Обновляем минимальное расстояние и путь
        if current_distance < min_distance:
            min_distance = current_distance
            min_path = path
    
    # Преобразуем индексы в точки
    result_path = [points[i] for i in min_path[:-1]]  # Убираем дублирование начальной точки
    return result_path, min_distance

def nearest_neighbor_tsp(points):
    """Решение задачи коммивояжера методом ближайшего соседа"""
    n = len(points)
    if n <= 1:
        return points, 0
    
    distance_matrix = create_distance_matrix(points)
    unvisited = set(range(n))
    path = []
    total_distance = 0
    
    # Начинаем с первой точки
    current = 0
    path.append(current)
    unvisited.remove(current)
    
    while unvisited:
        # Находим ближайшего непосещенного соседа
        nearest = None
        min_dist = float('inf')
        for neighbor in unvisited:
            if distance_matrix[current][neighbor] < min_dist:
                min_dist = distance_matrix[current][neighbor]
                nearest = neighbor
        
        # Переходим к ближайшему соседу
        path.append(nearest)
        unvisited.remove(nearest)
        total_distance += min_dist
        current = nearest
    
    # Возвращаемся в начальную точку
    total_distance += distance_matrix[current][0]
    path.append(0)
    
    # Преобразуем индексы в точки
    result_path = [points[i] for i in path[:-1]]  # Убираем дублирование начальной точки
    return result_path, total_distance

def print_path(path, distance):
    """Вывод маршрута и расстояния"""
    print("Оптимальный маршрут:")
    for point in path:
        print(f"({point[0]}, {point[1]})", end=" -> ")
    print(f"({path[0][0]}, {path[0][1]})")  # Замыкаем цикл
    print(f"Общее расстояние: {distance:.2f}")

def main():
    # Генерируем случайные точки
    num_points = 6  # Для brute force лучше не больше 8-9 точек (из-за факториального роста)
    points = generate_random_points(num_points)
    print(f"Точки: {points}")
    
    print("\nМетод ближайшего соседа:")
    path_nn, dist_nn = nearest_neighbor_tsp(points)
    print_path(path_nn, dist_nn)
    
    if num_points <= 8:
        print("\nМетод полного перебора:")
        path_bf, dist_bf = brute_force_tsp(points)
        print_path(path_bf, dist_bf)
        print(f"\nРазница в расстоянии: {dist_nn - dist_bf:.2f} (метод ближ. соседа хуже на {((dist_nn/dist_bf)-1)*100:.2f}%)")
    else:
        print("\nМетод полного перебора не выполняется из-за большого количества точек.")

if __name__ == "__main__":
    main()
