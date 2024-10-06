import pandas as pd
import arff

# Cargar el dataset CSV
df = pd.read_csv('C:/Users/59171/Documents/Programacion/examen ia/ej2/DS3_weapon_dataset_clean.csv')

# Convertir a ARFF
arff_data = {
    'description': 'Dataset de armas de Dark Souls 3',
    'relation': 'dark_souls_3_weapons',
    'attributes': [(col, 'REAL' if df[col].dtype in ['int64', 'float64'] else 'STRING') for col in df.columns],
    'data': df.values.tolist()
}

# Guardar como archivo ARFF
with open('C:/Users/59171/Documents/Programacion/examen ia/ejr3/DS3_weapon_dataset.arff', 'w') as f:
    arff.dump(arff_data, f)
