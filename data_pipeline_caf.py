import pandas as pd
import os
from functools import lru_cache

@lru_cache(maxsize=1)
def load_caf_data(data_dir='data/'):
    """
    Carrega o arquivo CAF consolidado e retorna um dicionário de DataFrames limpos
    apenas para o Distrito Federal.
    """
    filepath = os.path.join(data_dir, 'CAF 02 2026.ods')
    data_dict = {}
    
    if not os.path.exists(filepath):
        print(f"File not found: {filepath}")
        return data_dict
        
    try:
        xl = pd.ExcelFile(filepath, engine='odf')
        sheet_names = xl.sheet_names
        
        # Helper function to find sheet by substring to avoid encoding mismatch
        def get_sheet(substring):
            for s in sheet_names:
                if substring in s:
                    df = pd.read_excel(filepath, engine='odf', sheet_name=s)
                    # Remover colunas vazias de artefatos de planilha
                    df = df.loc[:, ~df.columns.str.contains('^Unnamed')]
                    # Filtrar apenas para DF caso existam outras UFs
                    if 'UF' in df.columns:
                        df = df[df['UF'] == 'DF'].copy()
                    return df
            return pd.DataFrame()

        data_dict['geral'] = get_sheet('GERAL')
        data_dict['caracterizacao'] = get_sheet('CARACTERIZA')
        data_dict['genero_jovens'] = get_sheet('GENERO E JOVENS')
        data_dict['atividade'] = get_sheet('ATIVIDADE')
        data_dict['renda_qtd'] = get_sheet('RENDA POR QUANTIDADE')
        data_dict['renda_valor'] = get_sheet('RENDA POR VALOR TOTAL')
        data_dict['pj'] = get_sheet('PESSOA JURIDICA')
        data_dict['entidade'] = get_sheet('ENTIDADE EMISSORA')
        
    except Exception as e:
        print(f"Error loading CAF data: {e}")
        
    return data_dict

if __name__ == '__main__':
    dados = load_caf_data()
    for k, v in dados.items():
        print(f"--- {k} ---")
        if not v.empty:
            print(v.head(2))
        else:
            print("Empty DataFrame")
