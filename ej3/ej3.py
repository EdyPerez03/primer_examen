import csv


def read_csv(file_path):
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


def one_hot_encode(data, columns):
    """Realiza One-Hot Encoding en las columnas especificadas."""
    new_data = []
    for row in data:
        new_row = row[:]
        for col in columns:
            unique_vals = sorted(set(r[col] for r in data))
            for unique_val in unique_vals:
                new_row.append(1 if row[col] == unique_val else 0)
        new_data.append(new_row)
    return new_data


def label_encode(data, columns):
    """Realiza Label Encoding en las columnas especificadas."""
    for col in columns:
        unique_vals = {val: i for i, val in enumerate(sorted(set(row[col] for row in data)))}
        for row in data:
            row[col] = unique_vals[row[col]]
    return data


def discretize_column(data, col, n_bins=5):
    """Discretiza la columna numérica especificada."""
    numeric_values = [row[col] for row in data if isinstance(row[col], (int, float))]

    if not numeric_values:
        print(f"No hay valores válidos en la columna {col} para discretizar.")
        return data

    min_val, max_val = min(numeric_values), max(numeric_values)
    bin_size = (max_val - min_val) / n_bins

    for row in data:
        if isinstance(row[col], (int, float)):
            row[col] = min(int((row[col] - min_val) / bin_size), n_bins - 1)
    return data


def normalize_column(data, col):
    """Normaliza la columna numérica especificada."""
    numeric_values = [row[col] for row in data if isinstance(row[col], (int, float))]

    if not numeric_values:
        print(f"No hay valores válidos en la columna {col} para normalizar.")
        return data

    min_val, max_val = min(numeric_values), max(numeric_values)

    for row in data:
        if isinstance(row[col], (int, float)):
            row[col] = (row[col] - min_val) / (max_val - min_val)
    return data


def write_arff(file_path, headers, data):
    """Escribe el conjunto de datos procesado en un archivo ARFF."""
    with open(file_path, 'w', newline='', encoding='utf-8') as arff_file:
        arff_file.write('@RELATION dark_souls_3_weapons_processed\n\n')
        for header in headers:
            arff_file.write(f"@ATTRIBUTE {header} REAL\n")
        arff_file.write('\n@DATA\n')
        for row in data:
            arff_file.write(','.join([str(val) if val is not None else '?' for val in row]) + '\n')


input_csv = 'C:/Users/59171/Documents/Programacion/examen ia/ej2/DS3_weapon_dataset_clean.csv'
output_arff = 'C:/Users/59171/Documents/Programacion/examen ia/ej3/DS_finalizado_weapon_dataset_processed.arff'

headers, data = read_csv(input_csv)

numeric_cols = ['Damage', 'Damage Reduction', 'Stat Requirements', 'Stat Bonuses', 'Critical', 
                'Weight', 'Stability', 'Durability', 'Sell Price', 'Spell Buff', 'Range']

for col in numeric_cols:
    col_index = headers.index(col)
    for row in data:
        row[col_index] = clean_numeric_column(row[col_index])

# 1. One-Hot Encoding
categorical_cols = ['Name', 'Category', 'Reinforcement', 'Aux Effects', 'Buffable', 'Infusable']
categorical_col_indexes = [headers.index(col) for col in categorical_cols]
data = one_hot_encode(data, categorical_col_indexes)

# 2. Label Encoding
data = label_encode(data, categorical_col_indexes)

# 3. Discretización de las columnas numéricas
for col in numeric_cols:
    col_index = headers.index(col)
    data = discretize_column(data, col_index, n_bins=5)

# 4. Normalización de las columnas numéricas
for col in numeric_cols:
    col_index = headers.index(col)
    data = normalize_column(data, col_index)

write_arff(output_arff, headers, data)

print("Procesamiento completo y guardado en 'DS3_weapon_dataset_processed.arff'")
