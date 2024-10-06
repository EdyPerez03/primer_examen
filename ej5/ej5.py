import csv

def read_csv(file_path):
    """Lee un archivo CSV y devuelve los encabezados y los datos."""
    data = []
    with open(file_path, newline='', encoding='utf-8') as csvfile:
        reader = csv.reader(csvfile)
        headers = next(reader)
        for row in reader:
            data.append(row)
    return headers, data

def clean_numeric_column(val):
    """Limpia y convierte valores a números."""
    if isinstance(val, str) and '/' in val:
        try:
            values = [float(x) for x in val.split('/') if x != '-']
            if values:
                return sum(values) / len(values)
            else:
                return None  
        except ValueError:
            return None
    if val == '-' or val == '--/':
        return None
    try:
        return float(val)
    except ValueError:
        return None

def normalize_data(data):
    """Normaliza las columnas de datos numéricos."""
    normalized_data = []
    for col in range(len(data[0])):
        cleaned_col = [clean_numeric_column(row[col]) for row in data]
        
        # Filtrar solo los valores numéricos (eliminar None)
        numeric_col = [val for val in cleaned_col if val is not None]
        
        # Imprimir valores para depuración
        print(f"Columna {col}: cleaned_col = {cleaned_col}, numeric_col = {numeric_col}")
        
        # Normalización solo si hay datos válidos
        if numeric_col:  
            min_val = min(numeric_col)
            max_val = max(numeric_col)
            # Evitar división por cero al normalizar
            if max_val > min_val:
                normalized_col = [(val - min_val) / (max_val - min_val) if val is not None else 0 for val in cleaned_col]
            else:
                normalized_col = [0] * len(cleaned_col)  # Si todos los valores son iguales
        else:
            normalized_col = [0] * len(cleaned_col)  # Si no hay datos válidos, llenamos con 0
        
        normalized_data.append(normalized_col)
    
    # Transponemos los datos normalizados para que cada fila represente una entrada original
    return list(map(list, zip(*normalized_data)))


def l1_penalty(weights, lambda_l1):
    """Calcula la penalización L1."""
    return lambda_l1 * sum(abs(w) for w in weights)

def l2_penalty(weights, lambda_l2):
    """Calcula la penalización L2."""
    return lambda_l2 * sum(w ** 2 for w in weights)

def write_csv(file_path, headers, data):
    """Escribe los datos en un archivo CSV."""
    with open(file_path, 'w', newline='', encoding='utf-8') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(headers)
        writer.writerows(data)

input_csv = 'C:/Users/59171/Documents/Programacion/examen ia/ej5/DS3_weapon_dataset_clean.csv'
output_csv = 'C:/Users/59171/Documents/Programacion/examen ia/ej5/DS3_weapon_dataset_normalized.csv'

# Leer datos
headers, data = read_csv(input_csv)

# Normalizar datos
normalized_data = normalize_data(data)

# Escribir datos normalizados
write_csv(output_csv, headers, normalized_data)

print("Normalización completa y guardada en 'DS3_weapon_dataset_normalized.csv'")

# Ejemplo de uso de las funciones de penalización
example_weights = [0.5, -1.2, 3.0]
lambda_l1 = 0.1
lambda_l2 = 0.01

l1_result = l1_penalty(example_weights, lambda_l1)
l2_result = l2_penalty(example_weights, lambda_l2)

print(f"Penalización L1: {l1_result}")
print(f"Penalización L2: {l2_result}")
