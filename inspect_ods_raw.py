import pandas as pd
import glob
import os

files = glob.glob('data/*.ods')
for f in files[:2]: # Just the first 2 files to save space
    print(f"--- File: {os.path.basename(f)} ---")
    try:
        # Lê as primeiras 15 linhas sem ignorar nada para ver a estrutura crua
        df = pd.read_excel(f, engine='odf', header=None, nrows=15)
        print(df.to_string())
    except Exception as e:
        print(f"Error reading: {e}")
    print("\n")
