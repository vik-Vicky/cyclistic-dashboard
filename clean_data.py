import pandas as pd

# 1. Load your original file (file of 123MB)
df = pd.read_csv('all_trips_clean.csv', low_memory=False)

# 2. Take a random sample (150,000 rows usually weigh around 15-18MB)
# This preserves the data proportion so that the charts look just as good
df_sample = df.sample(n=150000, random_state=42)

# 3. Save the new file for GitHub
df_sample.to_csv('all_trips_github.csv', index=False)

print("Done! The file 'all_trips_github.csv' should now weigh less than 25MB.")

print("¡Listo! El archivo 'all_trips_github.csv' ya debería pesar menos de 25MB.")
