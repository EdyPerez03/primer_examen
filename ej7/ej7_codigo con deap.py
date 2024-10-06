import random
from deap import base, creator, tools

# Definimos la función objetivo
def fitness_function(x):
    return x[0]**(2*x[0]) - 1,

# Definimos el tipo de problema como maximización
creator.create("FitnessMax", base.Fitness, weights=(1.0,))
creator.create("Individual", list, fitness=creator.FitnessMax)

# Inicializamos los elementos del algoritmo genético
toolbox = base.Toolbox()
toolbox.register("x", random.uniform, 0, 10)  # Cambiar los límites según sea necesario
toolbox.register("individual", tools.initRepeat, creator.Individual, toolbox.x, n=1)
toolbox.register("population", tools.initRepeat, list, toolbox.individual)
toolbox.register("evaluate", fitness_function)
toolbox.register("mate", tools.cxBlend, alpha=0.5)
toolbox.register("mutate", tools.mutGaussian, mu=0, sigma=1, indpb=0.2)
toolbox.register("select", tools.selTournament, tournsize=3)

# Algoritmo genético
def genetic_algorithm(population_size, generations):
    # Creamos la población inicial
    population = toolbox.population(n=population_size)

    for gen in range(generations):
        # Evaluamos la población
        fitnesses = list(map(toolbox.evaluate, population))
        for ind, fit in zip(population, fitnesses):
            ind.fitness.values = fit

        # Seleccionamos los individuos para la nueva generación
        offspring = toolbox.select(population, len(population))
        offspring = list(map(toolbox.clone, offspring))

        # Aplicamos cruce y mutación
        for child1, child2 in zip(offspring[::2], offspring[1::2]):
            if random.random() < 0.5:  # Probabilidad de cruce
                toolbox.mate(child1, child2)
                del child1.fitness.values  # Se requiere volver a evaluar
                del child2.fitness.values  # Se requiere volver a evaluar

        for mutant in offspring:
            if random.random() < 0.2:  # Probabilidad de mutación
                toolbox.mutate(mutant)
                del mutant.fitness.values  # Se requiere volver a evaluar

        # Evaluamos nuevamente los individuos que han cambiado
        fitnesses = list(map(toolbox.evaluate, offspring))
        for ind, fit in zip(offspring, fitnesses):
            ind.fitness.values = fit

        # Actualizamos la población
        population[:] = offspring

        # Evaluamos la población actual y mostramos los resultados
        best_individual = max(population, key=lambda ind: ind.fitness.values[0])
        best_fitness = best_individual.fitness.values[0]
        print(f"Generación {gen + 1}: Mejor individuo = {best_individual[0]:.4f}, Fitness = {best_fitness:.4f}")

    # Resultado final
    return best_individual, best_fitness

# Parámetros del algoritmo
population_size = 50
generations = 3

# Ejecución del algoritmo
best_individual, best_fitness = genetic_algorithm(population_size, generations)
print(f"Mejor individuo final: {best_individual[0]:.4f}, Fitness final: {best_fitness:.4f}")
