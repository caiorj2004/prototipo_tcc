import pandas as pd
import os
from functools import lru_cache

@lru_cache(maxsize=1)
def load_cnpo_data():
    """
    Carrega e limpa os dados do Cadastro Nacional de Produtores Orgânicos (CNPO).
    Filtra especificamente para UF == 'DF'.
    """
    base_dir = os.path.dirname(os.path.abspath(__file__))
    
    file_path = None
    for ext in ['.csv', '.xlsx', '.ods']:
        path_test = os.path.join(base_dir, 'data', f'Dados_CNPO_DF_Final{ext}')
        if os.path.exists(path_test):
            file_path = path_test
            break
            
    if not file_path:
        file_path = os.path.join(base_dir, 'data', 'CNPO 27-04-2026.ods')
        if not os.path.exists(file_path):
             print("Nenhum arquivo CNPO encontrado.")
             return pd.DataFrame(columns=['TIPO DE ENTIDADE', 'ENTIDADE', 'PAIS', 'UF', 'CIDADE', 'SITUAÇÃO', 'CNPF/CNPJ/NIF', 'ESCOPO', 'ATIVIDADES', 'ANO_REFERÊNCIA', 'MÊS_REFERÊNCIA'])
    
    try:
        if file_path.endswith('.csv'):
            df = pd.read_csv(file_path, sep=';', encoding='utf-8-sig', low_memory=False)
            if len(df.columns) == 1:
                df = pd.read_csv(file_path, sep=',', encoding='utf-8-sig', low_memory=False)
        elif file_path.endswith('.xlsx'):
            df = pd.read_excel(file_path)
        else:
            df = pd.read_excel(file_path, engine='odf')
            
        # Filtra para DF
        if 'UF' in df.columns:
            df = df[df['UF'] == 'DF'].copy()
            
        # Trata Nulos em colunas vitais
        cols_str = ['TIPO DE ENTIDADE', 'ENTIDADE', 'CIDADE', 'ESCOPO', 'ATIVIDADES', 'ANO_REFERÊNCIA', 'MÊS_REFERÊNCIA']
        for c in cols_str:
            if c in df.columns:
                df[c] = df[c].fillna('').astype(str).str.strip()
                if 'ANO' in c.upper() or 'MÊS' in c.upper() or 'MES' in c.upper():
                    df[c] = df[c].str.replace(r'\.0$', '', regex=True)
                    df[c] = df[c].replace('nan', '')
                
        return df
    except Exception as e:
        print(f"Erro ao carregar dados do CNPO: {e}")
        return pd.DataFrame(columns=['TIPO DE ENTIDADE', 'ENTIDADE', 'PAIS', 'UF', 'CIDADE', 'SITUAÇÃO', 'CNPF/CNPJ/NIF', 'ESCOPO', 'ATIVIDADES', 'ANO_REFERÊNCIA', 'MÊS_REFERÊNCIA'])

if __name__ == "__main__":
    df = load_cnpo_data()
    print(df.head())
    print(f"Total rows (DF): {len(df)}")
