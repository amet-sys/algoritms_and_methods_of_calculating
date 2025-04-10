import random

# Параметры генетического алгоритма
POPULATION_SIZE = 10
GENES = '01'
TARGET_CHROMOSOME_LENGTH = 5  # Так как 2^5 = 32 (достаточно для интервала [0, 31])
MUTATION_RATE = 0.1
CROSSOVER_RATE = 0.7
GENERATIONS = 100

# Функция, которую мы оптимизируем (ищем максимум)
def fitness_function(x):
    return x * x  # f(x) = x²

# Создание случайной хромосомы
def create_chromosome():
    return ''.join(random.choice(GENES) for _ in range(TARGET_CHROMOSOME_LENGTH))

# Декодирование хромосомы в число
def decode_chromosome(chromosome):
    return int(chromosome, 2)

# Селекция (турнирный отбор)
def selection(population, fitnesses):
    tournament = random.sample(list(zip(population, fitnesses)), 3)
    tournament.sort(key=lambda x: x[1], reverse=True)
    return tournament[0][0]

# Одноточечный кроссовер
def crossover(parent1, parent2):
    if random.random() < CROSSOVER_RATE:
        point = random.randint(1, TARGET_CHROMOSOME_LENGTH - 1)
        child1 = parent1[:point] + parent2[point:]
        child2 = parent2[:point] + parent1[point:]
        return child1, child2
    return parent1, parent2

# Мутация
def mutate(chromosome):
    mutated = list(chromosome)
    for i in range(len(mutated)):
        if random.random() < MUTATION_RATE:
            mutated[i] = '0' if mutated[i] == '1' else '1'
    return ''.join(mutated)

# Основной алгоритм
def genetic_algorithm():
    # Инициализация популяции
    population = [create_chromosome() for _ in range(POPULATION_SIZE)]
    
    for generation in range(GENERATIONS):
        # Оценка приспособленности
        decoded = [decode_chromosome(chrom) for chrom in population]
        fitnesses = [fitness_function(x) for x in decoded]
        
        # Вывод информации о лучшей особи
        best_fitness = max(fitnesses)
        best_index = fitnesses.index(best_fitness)
        best_chromosome = population[best_index]
        best_x = decoded[best_index]
        
        print(f"Поколение {generation}: Лучший x = {best_x}, f(x) = {best_fitness}")
        
        # Создание нового поколения
        new_population = []
        
        while len(new_population) < POPULATION_SIZE:
            # Селекция
            parent1 = selection(population, fitnesses)
            parent2 = selection(population, fitnesses)
            
            # Кроссовер
            child1, child2 = crossover(parent1, parent2)
            
            # Мутация
            child1 = mutate(child1)
            child2 = mutate(child2)
            
            new_population.append(child1)
            if len(new_population) < POPULATION_SIZE:
                new_population.append(child2)
        
        population = new_population
    
    # Возвращаем лучший результат
    decoded = [decode_chromosome(chrom) for chrom in population]
    fitnesses = [fitness_function(x) for x in decoded]
    best_index = fitnesses.index(max(fitnesses))
    return decoded[best_index], fitnesses[best_index]

# Запуск алгоритма
best_solution, best_fitness = genetic_algorithm()
print(f"\nЛучшее решение: x = {best_solution}, f(x) = {best_fitness}")
