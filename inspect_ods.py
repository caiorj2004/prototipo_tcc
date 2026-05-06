import pandas as pd
import glob
import os

files = glob.glob('data/*.ods')
for f in files:
    print(f"--- File: {os.path.basename(f)} ---")
    try:
        # Pula as primeiras 4 linhas (geralmente metadados do IBGE) e lê 5 linhas
        df = pd.read_excel(f, engine='odf', skiprows=4, nrows=5)
        print("Columns:")
        print(df.columns.tolist())
        print("First row:")
        print(df.iloc[0].values)
    except Exception as e:
        print(f"Error reading: {e}")
    print("\n")
