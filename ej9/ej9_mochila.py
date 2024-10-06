import pandas as pd
import numpy as np

# Cargar el dataset
df = pd.read_csv("C:/Users/59171/Documents/Programacion/examen ia/ej9/DS3_weapon_dataset_clean.csv")
pesos = df['Weight'].values
valores = df['Sell Price'].values
capacidad_max = 200

def knapsack(pesos, valores, capacidad):
    n = len(valores)
    dp = np.zeros((n + 1, capacidad + 1))

    # Construir la tabla dp
    for i in range(1, n + 1):
        for w in range(1, capacidad + 1):
            if int(pesos[i - 1]) <= w:
                dp[i][w] = max(dp[i - 1][w], dp[i - 1][w - int(pesos[i - 1])] + valores[i - 1])
            else:
                dp[i][w] = dp[i - 1][w]

    valor_maximo = dp[n][capacidad]
    w = capacidad
    items_seleccionados = []

    # Identificar los artículos seleccionados
    for i in range(n, 0, -1):
        if dp[i][w] != dp[i - 1][w]:
            items_seleccionados.append(i - 1)  # Guardar índice
            w -= int(pesos[i - 1])  # Reducir el peso

    return valor_maximo, items_seleccionados

def ajustar_peso(articulos, capacidad_max):
    peso_total = articulos['Weight'].sum()
    # Mientras el peso total exceda la capacidad máxima, eliminar el artículo de mayor peso
    while peso_total > capacidad_max:
        # Encontrar el índice del artículo con el mayor peso
        max_peso_index = articulos['Weight'].idxmax()
        articulos = articulos.drop(index=max_peso_index)  # Eliminar el artículo más pesado
        peso_total = articulos['Weight'].sum()  # Actualizar el peso total
    return articulos

valor_maximo, items_seleccionados = knapsack(pesos, valores, capacidad_max)

# Seleccionar artículos del DataFrame
articulos_seleccionados = df.iloc[items_seleccionados]
articulos_ajustados = ajustar_peso(articulos_seleccionados, capacidad_max)
peso_total = articulos_ajustados['Weight'].sum()

print("Artículos seleccionados y sus pesos:")
for index in articulos_ajustados.index:
    print(f"{df.iloc[index]['Name']}: Peso = {df.iloc[index]['Weight']}")

if peso_total <= capacidad_max:
    print(f'Valor máximo que se puede llevar: {valor_maximo}')
    print(f'Peso total de los artículos seleccionados: {peso_total}')
    print(articulos_ajustados)
else:
    print("El peso total excede la capacidad máxima permitida.")
