import pandas as pd

# 1. Cargar tu archivo original (el de 29MB o más)
df = pd.read_csv('all_trips_clean.csv', low_memory=False)

# 2. Tomar una muestra aleatoria (150,000 filas suelen pesar unos 15-18MB)
# Esto mantiene la proporción de datos para que los gráficos se vean igual de bien
df_sample = df.sample(n=150000, random_state=42)

# 3. Guardar el archivo nuevo para GitHub
df_sample.to_csv('all_trips_github.csv', index=False)

print("¡Listo! El archivo 'all_trips_github.csv' ya debería pesar menos de 25MB.")