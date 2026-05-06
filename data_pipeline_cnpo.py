import pandas as pd
import os

def load_cnpo_data():
    """
    Carrega e limpa os dados do Cadastro Nacional de Produtores Orgânicos (CNPO).
    Filtra especificamente para UF == 'DF'.
    """
    base_dir = os.path.dirname(os.path.abspath(__file__))
    file_path = os.path.join(base_dir, 'data', 'CNPO 27-04-2026.ods')
    
    try:
        df = pd.read_excel(file_path, engine='odf')
        # Filtra para DF
        if 'UF' in df.columns:
            df = df[df['UF'] == 'DF'].copy()
            
        # Trata Nulos em colunas vitais
        cols_str = ['TIPO DE ENTIDADE', 'ENTIDADE', 'CIDADE', 'ESCOPO', 'ATIVIDADES']
        for c in cols_str:
            if c in df.columns:
                df[c] = df[c].fillna('').astype(str).str.strip()
                
        return df
    except Exception as e:
        print(f"Erro ao carregar dados do CNPO: {e}")
        # Retorna DF vazio com as colunas esperadas para não quebrar a UI
        return pd.DataFrame(columns=['TIPO DE ENTIDADE', 'ENTIDADE', 'PAIS', 'UF', 'CIDADE', 'SITUAÇÃO', 'CNPF/CNPJ/NIF', 'ESCOPO', 'ATIVIDADES'])

if __name__ == "__main__":
    df = load_cnpo_data()
    print(df.head())
    print(f"Total rows (DF): {len(df)}")
