def solve_ilp():
    max_value = -float('inf')
    best_solution = None
    
    # Определяем границы для перебора
    # Из первого ограничения x1 + x2 + x3 ≤ 1 и x1,x2 ≥ 0, x1,x2 ∈ ℤ
    # x3 может быть нецелым, но x1 и x2 целые и ≥0
    
    # Перебираем возможные целые значения x1 и x2
    for x1 in range(0, 2):  # x1 может быть 0 или 1 (т.к. x1 + x2 + x3 ≤ 1)
        for x2 in range(0, 2):  # x2 может быть 0 или 1
            # Для данных x1 и x2 находим максимально возможное x3 из ограничений
            x3_max_from_1 = 1 - x1 - x2  # из первого ограничения
            x3_max_from_2 = (10 - 5*x1 - 3*x2) / 10  # из второго ограничения
            x3_max_from_3 = (3 - 2*x1 - x2) / 4  # из третьего ограничения
            
            # Находим минимальное из верхних границ для x3
            x3_max = min(x3_max_from_1, x3_max_from_2, x3_max_from_3)
            
            # x3 должен быть ≥0
            if x3_max >= 0:
                # Для данного x1 и x2 оптимальное x3 будет максимально возможным
                x3 = x3_max
                current_value = 3*x1 + 2*x2 + 5*x3
                
                # Проверяем, является ли это решение лучше найденных ранее
                if current_value > max_value:
                    max_value = current_value
                    best_solution = (x1, x2, x3)
    
    return best_solution, max_value

# Решаем задачу
solution, max_f = solve_ilp()

# Выводим результаты
if solution:
    x1, x2, x3 = solution
    print("Оптимальное решение найдено:")
    print(f"x1 = {x1} (целое)")
    print(f"x2 = {x2} (целое)")
    print(f"x3 = {x3:.2f}")
    print(f"Максимальное значение целевой функции F = {max_f:.2f}")
else:
    print("Допустимое решение не найдено.")
