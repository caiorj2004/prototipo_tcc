import pandas as pd
import os

from functools import lru_cache

def clean_valor_pecuaria(x):
    if pd.isna(x):
        return x
    # Fix for thousands parsed as decimals (e.g. 160.664 -> 160664)
    if x < 1000 and (x % 1 != 0):
        return int(round(x * 1000))
    return int(x)

@lru_cache(maxsize=1)
def load_data_2024():
    """
    Carrega e limpa os dados de Agricultura e Pecuária de 2024 em Parquet ou Excel.
    Retorna um dicionário com os DataFrames prontos para uso.
    """
    base_dir = os.path.dirname(os.path.abspath(__file__))
    data_dir = os.path.join(base_dir, 'data')
    
    file_agri_pq = os.path.join(data_dir, 'Agricultura_Valor_producao_2024.parquet')
    file_agri_xl = os.path.join(data_dir, 'Agricultura - Valor da produção (2024).xlsx')
    
    file_pec_pq = os.path.join(data_dir, 'Pecuaria_Rebanhos_2024.parquet')
    file_pec_xl = os.path.join(data_dir, 'Pecuária - Rebanhos (2024).xlsx')
    
    try:
        if os.path.exists(file_agri_pq):
            df_agri = pd.read_parquet(file_agri_pq)
        else:
            df_agri = pd.read_excel(file_agri_xl)
        if 'Valor' in df_agri.columns:
            df_agri = df_agri.sort_values(by='Valor', ascending=False).reset_index(drop=True)
    except Exception as e:
        print(f"Erro ao ler agricultura 2024: {e}")
        df_agri = pd.DataFrame(columns=['Produto', 'Valor'])
        
    try:
        if os.path.exists(file_pec_pq):
            df_pec = pd.read_parquet(file_pec_pq)
        else:
            df_pec = pd.read_excel(file_pec_xl)
        if 'Valor' in df_pec.columns:
            df_pec['Valor'] = df_pec['Valor'].apply(clean_valor_pecuaria)
    except Exception as e:
        print(f"Erro ao ler pecuária 2024: {e}")
        df_pec = pd.DataFrame(columns=['Produto', 'Valor', 'Unidade'])
        
    return {
        'agricultura': df_agri,
        'pecuaria': df_pec
    }

if __name__ == "__main__":
    dados = load_data_2024()
    print("Agricultura:")
    print(dados['agricultura'].head())
    print("\nPecuária:")
    print(dados['pecuaria'].head())
