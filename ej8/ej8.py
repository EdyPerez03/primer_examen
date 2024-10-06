import pandas as pd
import numpy as np

ruta_dataset = r"C:\Users\59171\Documents\Programacion\examen ia\ej8\ejer8_dataset.csv"
data = pd.read_csv(ruta_dataset)

print("Primeras filas del dataset:")
print(data.head())

print("\nTipos de datos:")
print(data.dtypes)

print("\nNombres de las columnas:")
print(data.columns.tolist())  
data.columns = data.columns.str.strip()

print("\nClase: medidas corporales")

def calcular_entropia(clase):
    conteos = clase.value_counts(normalize=True)
    entropia = -sum(conteos * np.log2(conteos))
    return entropia

# Calcular entropía para la columna Talla
entropia_talla = calcular_entropia(data['Talla (M/L/S/XL)'])
print(f"\nEntropía de Talla (M/L/S/XL): {entropia_talla:.4f}")

# Calcular entropía para la columna Altura (cm)
def calcular_entropia_numerica(columna):
    return calcular_entropia(pd.cut(columna, bins=10))  # Dividir en 10 bins

entropia_altura = calcular_entropia_numerica(data['Altura (cm)'])
print(f"Entropía de Altura (cm): {entropia_altura:.4f}")

# Calcular entropía para la columna Peso (kg)
entropia_peso = calcular_entropia_numerica(data['Peso (kg)'])
print(f"Entropía de Peso (kg): {entropia_peso:.4f}")

def calcular_ganancia_informacion(data, atributo, clase):
    entropia_total = calcular_entropia(data[clase])
    valores = data[atributo].unique()
    entropia_atributo = 0

    for valor in valores:
        subgrupo = data[data[atributo] == valor]
        probabilidad = len(subgrupo) / len(data)
        entropia_atributo += probabilidad * calcular_entropia(subgrupo[clase])

    ganancia = entropia_total - entropia_atributo
    return ganancia

atributos = data.columns.drop('Talla (M/L/S/XL)')

for atributo in atributos:
    ganancia = calcular_ganancia_informacion(data, atributo, 'Talla (M/L/S/XL)')
    print(f"Ganancia de Información ({atributo}): {ganancia:.4f}")

