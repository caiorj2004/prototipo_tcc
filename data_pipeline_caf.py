import pandas as pd
import os
from functools import lru_cache

@lru_cache(maxsize=1)
def load_caf_data(data_dir='data/'):
    """
    Carrega o arquivo CAF consolidado e retorna um dicionário de DataFrames limpos.
    """
    filepath = os.path.join(data_dir, 'CAF_TRATADO_COMPLETO.xlsx')
    data_dict = {}
    
    if not os.path.exists(filepath):
        # Fallback
        filepath = os.path.join(data_dir, 'CAF 02 2026.ods')
        if not os.path.exists(filepath):
            print(f"File not found: CAF_TRATADO_COMPLETO.xlsx or fallback")
            return data_dict
            
    try:
        if filepath.endswith('.xlsx'):
            xl = pd.ExcelFile(filepath)
        else:
            xl = pd.ExcelFile(filepath, engine='odf')
            
        sheet_names = xl.sheet_names
        cols_to_drop = ['ARQUIVO', 'ABA', 'TITULO', 'NENHUMA OPÇÃO', 'PREENCHIMENTO']
        
        def get_sheet(target_sheet, key_name):
            for s in sheet_names:
                # Ignorar resumos como solicitado
                if s.upper() in ['RESUMO UF', 'RESUMO - REGIÃO']:
                    continue
                    
                if target_sheet.upper() in s.upper():
                    if filepath.endswith('.xlsx'):
                        df = pd.read_excel(filepath, sheet_name=s)
                    else:
                        df = pd.read_excel(filepath, engine='odf', sheet_name=s)
                        
                    # Drop colunas de controle interno
                    df = df.drop(columns=[c for c in cols_to_drop if c in df.columns], errors='ignore')
                    
                    # Remover colunas unnamed
                    df = df.loc[:, ~df.columns.str.contains('^Unnamed')]
                    
                    # Padronizar colunas ANO e MES para string e tirar .0
                    for c in ['ANO', 'MES']:
                        if c in df.columns:
                            df[c] = df[c].fillna(0).astype(str).str.replace(r'\.0$', '', regex=True)
                            df[c] = df[c].replace(['0', 'nan', '0.0'], 'Desconhecido')
                    
                    if 'UF' in df.columns:
                        df = df[df['UF'] == 'DF'].copy()
                        
                    data_dict[key_name] = df
                    return
            data_dict[key_name] = pd.DataFrame()

        get_sheet('LOCALIDADE AREA PF', 'pf')
        get_sheet('LOCALIDADE AREA PJ', 'pj_area')
        get_sheet('CARACTERIZA', 'caracterizacao')
        get_sheet('ATIVIDADE', 'atividade')
        get_sheet('GENERO', 'genero')
        get_sheet('JOVENS', 'jovens')
        get_sheet('JURÍDICO', 'pj')
        get_sheet('ENTIDADES', 'entidade')
        get_sheet('RENDA QUANTIDADE', 'renda_qtd')
        get_sheet('RENDA VALOR', 'renda_valor')
        
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
