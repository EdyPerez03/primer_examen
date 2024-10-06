import pandas as pd
import numpy as np
import arff
from sklearn.preprocessing import OneHotEncoder, LabelEncoder, KBinsDiscretizer, MinMaxScaler

data = arff.load(open('C:/Users/59171/Documents/Programacion/examen ia/ej3/DS3_weapon_dataset.arff', 'r'))
df = pd.DataFrame(data['data'], columns=[attr[0] for attr in data['attributes']])

categorical_cols = ['Name', 'Category', 'Reinforcement', 'Aux Effects', 'Buffable', 'Infusable']
numeric_cols = ['Damage', 'Damage Reduction', 'Stat Requirements', 'Stat Bonuses', 'Critical',
                'Weight', 'Stability', 'Durability', 'Sell Price', 'Spell Buff', 'Range']

def clean_numeric_column(column):
    def clean_value(val):
        if isinstance(val, str) and '/' in val:
            try:
                return np.mean([float(x) for x in val.split('/') if x != '-'])
            except ValueError:
                return np.nan  
        if val == '-' or val == '--/':
            return np.nan  
        try:
           
            return float(val)
        except ValueError:
           
            return np.nan
    return column.apply(clean_value)

# Limpiar las columnas numéricas
for col in numeric_cols:
    df[col] = clean_numeric_column(df[col])

# 1. One-Hot Encoding para columnas categóricas
onehot_encoder = OneHotEncoder(sparse_output=False)
onehot_encoded = onehot_encoder.fit_transform(df[categorical_cols])
onehot_encoded_df = pd.DataFrame(onehot_encoded, columns=onehot_encoder.get_feature_names_out(categorical_cols))

# 2. Label Encoding 
label_encoder = LabelEncoder()
label_encoded_df = df[categorical_cols].apply(label_encoder.fit_transform)

# 3. Discretización de las columnas numéricas
discretizer = KBinsDiscretizer(n_bins=5, encode='ordinal', strategy='uniform', subsample=None)
discretized = discretizer.fit_transform(df[numeric_cols].fillna(0))  # Reemplazar NaN con 0 (puedes usar otro valor si prefieres)
discretized_df = pd.DataFrame(discretized, columns=[f'{col}_discretized' for col in numeric_cols])

# 4. Normalización de las columnas numéricas
scaler = MinMaxScaler()
normalized = scaler.fit_transform(df[numeric_cols].fillna(0))  # Reemplazar NaN con 0 para normalización
normalized_df = pd.DataFrame(normalized, columns=[f'{col}_normalized' for col in numeric_cols])


final_df = pd.concat([df.reset_index(drop=True), onehot_encoded_df.reset_index(drop=True), 
                      discretized_df.reset_index(drop=True), normalized_df.reset_index(drop=True)], axis=1)

final_df.columns = pd.Index([f"{col}_{i}" if col in final_df.columns[:i].to_list() else col for i, col in enumerate(final_df.columns)])

arff_data = {
    'description': 'Dataset procesado de armas de Dark Souls 3',
    'relation': 'dark_souls_3_weapons_processed',
    'attributes': [(str(col), 'REAL' if pd.api.types.is_numeric_dtype(final_df[col]) else 'STRING') for col in final_df.columns],
    'data': final_df.values.tolist()
}

with open('C:/Users/59171/Documents/Programacion/examen ia/ej3/DS3_weapon_dataset_processed.arff', 'w') as f:
    arff.dump(arff_data, f)

print("Procesamiento completo y guardado en 'DS_weapon_dataset_processed.arff'")
