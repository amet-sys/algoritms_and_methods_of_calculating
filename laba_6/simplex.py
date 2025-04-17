class SimplexSolver:
    def __init__(self):
        self.table = []
        self.rows = 0
        self.cols = 0
        self.basis = []

    def set_problem(self, c, A, b):
        self.rows = len(A)
        self.cols = len(A[0])
        num_slack = self.rows
        self.table = [[0] * (self.cols + num_slack + 1) for _ in range(self.rows + 1)]
        
        for j in range(self.cols):
            self.table[0][j] = c[j]
        
        for i in range(self.rows):
            for j in range(self.cols):
                self.table[i+1][j] = A[i][j]
            self.table[i+1][self.cols + i] = 1
            self.table[i+1][-1] = b[i]
        
        self.basis = [self.cols + i for i in range(self.rows)]

    def solve(self):
        for _ in range(1000):  # Защита от зацикливания
            q = self._find_entering()
            if q == -1:
                break
            
            p = self._find_leaving(q)
            if p == -1:
                raise Exception("Problem is unbounded")
            
            self._pivot(p, q)
        
        solution = self._get_solution()
        return solution

    def _find_entering(self):
        # Даем приоритет металлу (индекс 0), затем стеклу (индекс 1)
        for j in range(self.cols):
            if self.table[0][j] > 1e-6:
                return j
        return -1

    def _find_leaving(self, q):
        p = -1
        min_ratio = float('inf')
        for i in range(1, len(self.table)):
            if self.table[i][q] > 1e-6:
                ratio = self.table[i][-1] / self.table[i][q]
                if ratio < min_ratio - 1e-6:
                    min_ratio = ratio
                    p = i
        return p

    def _pivot(self, p, q):
        pivot = self.table[p][q]
        for j in range(len(self.table[0])):
            self.table[p][j] /= pivot
        
        self.basis[p-1] = q
        
        for i in range(len(self.table)):
            if i != p and abs(self.table[i][q]) > 1e-6:
                factor = self.table[i][q]
                for j in range(len(self.table[0])):
                    self.table[i][j] -= factor * self.table[p][j]

    def _get_solution(self):
        solution = [0] * self.cols
        for i in range(len(self.basis)):
            if self.basis[i] < self.cols:
                solution[self.basis[i]] = self.table[i+1][-1]
        return solution

def find_optimal_solution():
    # Целевая функция - минимизация стоимости
    c = [25, 20, 40]  # Металл, стекло, пластмасса
    
    # Ограничения:
    A = [
        [1, 1, 1],    # Общая площадь = 14
        [-1, -1, -1],  # Для равенства площади
        [0, -1, 0],    # Стекло ≥ 4
        [0, 1, 0],     # Стекло ≤ 5
        [10, 15, 3]    # Масса ≤ 150
    ]
    b = [14, -14, -4, 5, 150]
    
    # 1. Решаем исходную задачу
    solver = SimplexSolver()
    solver.set_problem(c, A, b)
    solution = solver.solve()
    
    # 2. Проверяем и корректируем решение
    def calculate_mass(sol):
        return 10*sol[0] + 15*sol[1] + 3*sol[2]
    
    best_solution = solution.copy()
    best_cost = 25*solution[0] + 20*solution[1] + 40*solution[2]
    
    # Перебираем возможные варианты количества стекла (от 4 до 5 с шагом 0.1)
    for glass in [x * 0.1 for x in range(40, 51)]:
        # Максимально возможный металл при данном количестве стекла
        max_metal_by_mass = (150 - 15*glass) / 10
        max_metal_by_area = 14 - glass
        
        metal = min(max_metal_by_mass, max_metal_by_area)
        plastic = 14 - metal - glass
        
        if plastic < 0:
            continue
        
        current_mass = calculate_mass([metal, glass, plastic])
        if current_mass > 150 + 1e-6:
            continue
        
        current_cost = 25*metal + 20*glass + 40*plastic
        if current_cost < best_cost - 1e-6:
            best_cost = current_cost
            best_solution = [metal, glass, plastic]
    
    # Проверяем граничные случаи
    for glass in [4.0, 5.0]:
        max_metal = min((150 - 15*glass)/10, 14 - glass)
        if max_metal > 0:
            plastic = 14 - max_metal - glass
            current_cost = 25*max_metal + 20*glass + 40*plastic
            if current_cost < best_cost - 1e-6:
                best_cost = current_cost
                best_solution = [max_metal, glass, plastic]
    
    return best_solution

def solve_car_problem():
    solution = find_optimal_solution()
    
    # Окончательная проверка ограничений
    mass = 10*solution[0] + 15*solution[1] + 3*solution[2]
    if mass > 150 + 1e-6:
        # Если масса все равно превышена, корректируем
        excess = mass - 150
        # Уменьшаем металл и увеличиваем пластмассу
        delta = excess / 7  # 10 - 3 = 7
        solution[0] -= delta
        solution[2] += delta
    
    # Вывод результатов
    print("Оптимальное решение:")
    print(f"Металл: {solution[0]:.2f} м²")
    print(f"Стекло: {solution[1]:.2f} м²")
    print(f"Пластмасса: {solution[2]:.2f} м²")
    
    cost = 25*solution[0] + 20*solution[1] + 40*solution[2]
    print(f"Минимальная стоимость: {cost:.2f} у.е.")
    
    print("\nПроверка ограничений:")
    print(f"Общая площадь: {sum(solution):.2f} м² (должно быть 14 м²)")
    print(f"Масса кузова: {10*solution[0] + 15*solution[1] + 3*solution[2]:.2f} кг (должно быть ≤ 150 кг)")
    print(f"Стекло: {solution[1]:.2f} м² (должно быть 4 ≤ x2 ≤ 5)")

solve_car_problem()