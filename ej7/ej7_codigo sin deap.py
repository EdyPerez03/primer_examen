import random

# Definimos la función objetivo
def fitness_function(x):
    return x**(2*x) - 1

# Inicializamos la población
def initialize_population(size):
    return [random.uniform(0, 10) for _ in range(size)]  # Cambiar límites según sea necesario

# Selección por torneo
def tournament_selection(population, k=3):
    selected = random.sample(population, k)
    return max(selected, key=fitness_function)

# Cruce
def crossover(parent1, parent2):
    return (parent1 + parent2) / 2  # Cruce promedio

# Mutación
def mutate(individual, mutation_rate=0.1):
    if random.random() < mutation_rate:
        return individual + random.uniform(-1, 1)  # Cambio aleatorio
    return individual

# Algoritmo genético
def genetic_algorithm(population_size, generations):
    population = initialize_population(population_size)
    
    for gen in range(generations):
        new_population = []
        
        for _ in range(population_size):
            parent1 = tournament_selection(population)
            parent2 = tournament_selection(population)
            child = crossover(parent1, parent2)
            child = mutate(child)
            new_population.append(child)
        
        population = new_population
        
        # Evaluamos la población actual y mostramos los resultados
        best_individual = max(population, key=fitness_function)
        best_fitness = fitness_function(best_individual)
        print(f"Generación {gen + 1}: Mejor individuo = {best_individual:.4f}, Fitness = {best_fitness:.4f}")

    # Resultado final
    return best_individual, best_fitness

# Parámetros del algoritmo
population_size = 50
generations = 3

# Ejecución del algoritmo
best_individual, best_fitness = genetic_algorithm(population_size, generations)
print(f"Mejor individuo final: {best_individual:.4f}, Fitness final: {best_fitness:.4f}")
