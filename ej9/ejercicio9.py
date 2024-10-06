import pandas as pd
import random

class Articulo:
    def __init__(self, id, nombre, peso, precio_venta):
        self.id = id
        self.nombre = nombre
        self.peso = peso
        self.precio_venta = precio_venta

def parserArticulos(articulos_df):
    articulos = []
    for index, row in articulos_df.iterrows():
        articulos.append(Articulo(index, row['Name'], row['Weight'], row['Sell Price']))
    return articulos

def evaluar_solucion(solucion, peso_maximo):
    peso_total = sum(articulo.peso for articulo in solucion)
    if peso_total <= peso_maximo:
        return len(solucion), peso_total  # Devuelve la cantidad de artículos y el peso total
    else:
        return 0, 0  # Solución inválida

def peso_total(solucion):
    return sum(articulo.peso for articulo in solucion)

def imprimir_pesos(articulos):
    print("Pesos de los artículos en el dataset:")
    for articulo in articulos:
        print(f"Nombre: {articulo.nombre}, Peso: {articulo.peso}, Precio de venta: {articulo.precio_venta}")

def generar_poblacion(articulos, tam_poblacion):
    return [random.sample(articulos, random.randint(1, len(articulos))) for _ in range(tam_poblacion)]

def seleccion(poblacion, peso_maximo):
    poblacion = sorted(poblacion, key=lambda x: evaluar_solucion(x, peso_maximo)[0], reverse=True)
    return poblacion[:len(poblacion) // 2]

def cruzar(padre1, padre2):
    if len(padre1) < 2 or len(padre2) < 2:
        return padre1, padre2  # No se puede cruzar, devolver los padres sin cambios
    
    punto_cruce = random.randint(1, min(len(padre1), len(padre2)) - 1)
    hijo1 = padre1[:punto_cruce] + padre2[punto_cruce:]
    hijo2 = padre2[:punto_cruce] + padre1[punto_cruce:]
    return hijo1, hijo2

def mutar(solucion, prob_mutacion):
    if random.random() < prob_mutacion and len(solucion) > 0:
        articulo = random.choice(solucion)
        return [a for a in solucion if a != articulo]
    return solucion

def algoritmo_genetico(articulos, peso_maximo, tam_poblacion, prob_mutacion, iteraciones):
    poblacion = generar_poblacion(articulos, tam_poblacion)
    
    for _ in range(iteraciones):
        poblacion = seleccion(poblacion, peso_maximo)
        nueva_poblacion = []
        while len(nueva_poblacion) < tam_poblacion:
            padre1 = random.choice(poblacion)
            padre2 = random.choice(poblacion)
            hijos = cruzar(padre1, padre2)
            nueva_poblacion.extend(hijos)
        poblacion = [mutar(solucion, prob_mutacion) for solucion in nueva_poblacion]

    # Filtramos soluciones válidas
    poblacion_validas = [solucion for solucion in poblacion if evaluar_solucion(solucion, peso_maximo)[0] > 0]
    
    if poblacion_validas:
        mejor_solucion = max(poblacion_validas, key=lambda x: evaluar_solucion(x, peso_maximo)[0])
    else:
        mejor_solucion = []

    return mejor_solucion

def main():
    articulos_df = pd.read_csv("C:\\Users\\59171\\Documents\\Programacion\\examen ia\\ej9\\DS3_weapon_dataset_clean.csv")
    articulos = parserArticulos(articulos_df)
    
    imprimir_pesos(articulos)  # Imprimir los pesos de los artículos
    
    peso_maximo = 150
    tam_poblacion = 50
    prob_mutacion = 0.1
    iteraciones = 100
    
    mejor_solucion = algoritmo_genetico(articulos, peso_maximo, tam_poblacion, prob_mutacion, iteraciones)

    print("\nMejor solución encontrada:")
    if mejor_solucion:
        for articulo in mejor_solucion:
            print(f"Nombre: {articulo.nombre}, Peso: {articulo.peso}, Precio de venta: {articulo.precio_venta}")

        peso_total_mejor_solucion = peso_total(mejor_solucion)
        print(f"\nPeso total de la mejor solución: {peso_total_mejor_solucion}")
    else:
        print("No se encontró una solución válida.")

if __name__ == "__main__":
    main()
