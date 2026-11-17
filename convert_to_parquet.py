"""Converte as bases de data/ (CSV/XLSX/ODS) em Parquet para carregamento mais rápido.
Os pipelines usam o Parquet quando existe e, senão, o arquivo original.
Uso: python convert_to_parquet.py   (requer pyarrow)"""
import pandas as pd
import glob
import os

data_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'data')
print(f"Data directory: {data_dir}")

# 1. Convert CNPO
cnpo_csv = os.path.join(data_dir, 'Dados_CNPO_DF_Final.csv')
cnpo_parquet = os.path.join(data_dir, 'Dados_CNPO_DF_Final.parquet')
if os.path.exists(cnpo_csv):
    print("Converting CNPO CSV to Parquet...")
    try:
        df = pd.read_csv(cnpo_csv, sep=';', encoding='utf-8-sig', low_memory=False)
        if len(df.columns) == 1:
            df = pd.read_csv(cnpo_csv, sep=',', encoding='utf-8-sig', low_memory=False)
        df.to_parquet(cnpo_parquet, index=False)
        print(f"Saved {cnpo_parquet} ({os.path.getsize(cnpo_parquet)} bytes)")
    except Exception as e:
        print(f"Error CNPO parquet: {e}")

# 2. Convert MCDR
mcdr_xlsx = os.path.join(data_dir, 'Matriz_Credito_Rural_DF_2017_2025.xlsx')
mcdr_parquet = os.path.join(data_dir, 'Matriz_Credito_Rural_DF_2017_2025.parquet')
if os.path.exists(mcdr_xlsx):
    print("Converting MCDR Excel to Parquet...")
    try:
        df = pd.read_excel(mcdr_xlsx)
        df.to_parquet(mcdr_parquet, index=False)
        print(f"Saved {mcdr_parquet} ({os.path.getsize(mcdr_parquet)} bytes)")
    except Exception as e:
        print(f"Error MCDR parquet: {e}")

# 3. Convert CAF sheets
caf_xlsx = os.path.join(data_dir, 'CAF_TRATADO_COMPLETO.xlsx')
if os.path.exists(caf_xlsx):
    print("Converting CAF Excel sheets to Parquet...")
    xl = pd.ExcelFile(caf_xlsx)
    for sheet in xl.sheet_names:
        clean_name = sheet.strip().replace(' ', '_').lower()
        sheet_parquet = os.path.join(data_dir, f'caf_sheet_{clean_name}.parquet')
        df = pd.read_excel(caf_xlsx, sheet_name=sheet)
        df.to_parquet(sheet_parquet, index=False)
        print(f"Saved {sheet_parquet}")

# 4. Convert IBGE 2024
agri_xlsx = os.path.join(data_dir, 'Agricultura - Valor da produção (2024).xlsx')
agri_parquet = os.path.join(data_dir, 'Agricultura_Valor_producao_2024.parquet')
if os.path.exists(agri_xlsx):
    pd.read_excel(agri_xlsx).to_parquet(agri_parquet, index=False)
    print(f"Saved {agri_parquet}")

pec_xlsx = os.path.join(data_dir, 'Pecuária - Rebanhos (2024).xlsx')
pec_parquet = os.path.join(data_dir, 'Pecuaria_Rebanhos_2024.parquet')
if os.path.exists(pec_xlsx):
    pd.read_excel(pec_xlsx).to_parquet(pec_parquet, index=False)
    print(f"Saved {pec_parquet}")

# 5. Convert Censo files (.ods/.xlsx)
censo_files = glob.glob(os.path.join(data_dir, '*.ods')) + glob.glob(os.path.join(data_dir, '*.xlsx'))
for f in censo_files:
    fname = os.path.basename(f)
    if 'CAF' in fname or 'CNPO' in fname or 'Matriz' in fname or '2024' in fname:
        continue
    pq_name = os.path.splitext(fname)[0] + '.parquet'
    pq_path = os.path.join(data_dir, pq_name)
    try:
        eng = 'odf' if f.endswith('.ods') else None
        df = pd.read_excel(f, engine=eng, header=0)
        df.to_parquet(pq_path, index=False)
        print(f"Saved {pq_name}")
    except Exception as e:
        print(f"Error converting {fname}: {e}")

print("Parquet conversion completed!")
