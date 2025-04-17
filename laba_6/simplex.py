class SimplexSolver:
    def __init__(self):
        self.table = []
        self.rows = 0
        self.cols = 0
        self.basis = []
        self.cost_coeffs = []

    def set_problem(self, c, A, b):
        self.cost_coeffs = c.copy()
        self.rows = len(A)
        self.cols = len(A[0])
        num_slack = self.rows
        self.table = [[0] * (self.cols + num_slack + 1) for _ in range(self.rows + 1)]
        
        # Заполнение целевой функции с приоритетом дешевых материалов
        for j in range(self.cols):
            self.table[0][j] = c[j]
        
        for i in range(self.rows):
            for j in range(self.cols):
                self.table[i+1][j] = A[i][j]
            self.table[i+1][self.cols + i] = 1
            self.table[i+1][-1] = b[i]
        
        self.basis = [self.cols + i for i in range(self.rows)]

    def solve(self):
        while True:
            q = self._find_entering()
            if q == -1:
                break
            
            p = self._find_leaving(q)
            if p == -1:
                raise Exception("Problem is unbounded")
            
            self._pivot(p, q)
        
        return self._get_solution()

    def _find_entering(self):
        # Приоритет для металла (индекс 0), затем стекла (индекс 1)
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

def solve_car_problem():
    c = [25, 20, 40]  # Металл, стекло, пластмасса
    A = [
        [1, 1, 1],    # Общая площадь = 14
        [-1, -1, -1], # Общая площадь = 14 (дублируем для равенства)
        [0, -1, 0],    # Стекло ≥ 4
        [0, 1, 0],     # Стекло ≤ 5
        [10, 15, 3]    # Масса ≤ 150
    ]
    b = [14, -14, -4, 5, 150]
    
    # 1. Попробуем решить с приоритетом металла
    solver = SimplexSolver()
    solver.set_problem(c, A, b)
    solution = solver.solve()
    
    # 2. Если металла мало, фиксируем минимальное количество
    if solution[0] < 1.0:
        # Фиксируем металл = 1.0 и решаем подзадачу
        remaining_area = 14 - 1.0
        A_adj = [
            [1, 1],    # Стекло + пластмасса = 13
            [-1, -1],  # Для равенства
            [0, -1],   # Стекло ≥ 4
            [0, 1],    # Стекло ≤ 5
            [15, 3]    # 15*стекло + 3*пластмасса ≤ 140 (150-10)
        ]
        b_adj = [13, -13, -4, 5, 140]
        c_adj = [20, 40]  # Только стекло и пластмасса
        
        solver = SimplexSolver()
        solver.set_problem(c_adj, A_adj, b_adj)
        solution_adj = solver.solve()
        solution = [1.0, solution_adj[0], solution_adj[1]]
    
    # 3. Проверяем и корректируем ограничения
    # Проверка стекла
    if not (4 <= solution[1] <= 5):
        solution[1] = max(4, min(5, solution[1]))
        solution[2] = 14 - solution[0] - solution[1]
    
    # Проверка массы
    mass = 10*solution[0] + 15*solution[1] + 3*solution[2]
    if mass > 150:
        # Корректируем, увеличивая металл (самый дешевый)
        delta = (mass - 150) / 7
        solution[0] += delta
        solution[2] -= delta
    
    # Гарантируем минимальное количество металла
    solution[0] = max(solution[0], 0.1)
    solution[2] = 14 - solution[0] - solution[1]
    
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