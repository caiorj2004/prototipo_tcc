import pandas as pd
import os
from functools import lru_cache

@lru_cache(maxsize=1)
def load_mcdr_data(data_dir='data/'):
    """
    Carrega o arquivo de Crédito Rural (MCDR) de 2024 (Distrito Federal), 
    trata os formatos numéricos pt-BR e cria os DataFrames agregados para a UI.
    """
    filepath = os.path.join(data_dir, 'mcdr_2024.csv')
    data_dict = {}
    
    if not os.path.exists(filepath):
        print(f"File not found: {filepath}")
        return data_dict
        
    try:
        # Lê usando separador vírgula, encoding utf-8-sig e formato brasileiro de milhares e decimais
        df = pd.read_csv(filepath, sep=',', encoding='utf-8-sig', decimal=',', thousands='.')
        
        # Colunas financeiras e quantitativas esperadas
        cols_num = ['VLCUSTEIO', 'VLINVESTIMENTO', 'VLCOMERCIALIZACAO', 'VLINDUSTRIALIZACAO', 'AREATOTAL', 'QTDTOTAL', 'VALORTOTAL']
        
        # Limpar espaços extras em nomes de colunas por garantia
        df.columns = df.columns.str.strip()
        
        for col in cols_num:
            if col in df.columns:
                df[col] = pd.to_numeric(df[col], errors='coerce').fillna(0)
                
        # 1. Totais por Finalidade (Soma geral das 4 variáveis)
        finalidade_data = {
            'Finalidade': ['Custeio', 'Investimento', 'Comercialização', 'Industrialização'],
            'Valor': [
                df['VLCUSTEIO'].sum() if 'VLCUSTEIO' in df.columns else 0,
                df['VLINVESTIMENTO'].sum() if 'VLINVESTIMENTO' in df.columns else 0,
                df['VLCOMERCIALIZACAO'].sum() if 'VLCOMERCIALIZACAO' in df.columns else 0,
                df['VLINDUSTRIALIZACAO'].sum() if 'VLINDUSTRIALIZACAO' in df.columns else 0
            ]
        }
        data_dict['finalidade'] = pd.DataFrame(finalidade_data)
        
        # 2. Totais por IF (Instituição Financeira)
        if 'NOMEIF' in df.columns and 'VALORTOTAL' in df.columns:
            df_if = df.groupby('NOMEIF', as_index=False)['VALORTOTAL'].sum().sort_values(by='VALORTOTAL', ascending=True)
            data_dict['if'] = df_if
        else:
            data_dict['if'] = pd.DataFrame()
            
        # 3. Totais por Categoria e Atividade
        if 'NOMESEGMENTOCATEGORIA' in df.columns and 'ATIVIDADE' in df.columns and 'VALORTOTAL' in df.columns:
            df_cat = df.groupby(['NOMESEGMENTOCATEGORIA', 'ATIVIDADE'], as_index=False)['VALORTOTAL'].sum()
            data_dict['categoria'] = df_cat
        else:
            data_dict['categoria'] = pd.DataFrame()
            
        # 4. Dados Dispersão
        if all(c in df.columns for c in ['VALORTOTAL', 'AREATOTAL', 'QTDTOTAL', 'ATIVIDADE']):
            df_disp = df[['VALORTOTAL', 'AREATOTAL', 'QTDTOTAL', 'ATIVIDADE']].copy()
            # Remover zeros na área para não aglomerar distorções no eixo zero do gráfico logarítmico (se usado)
            df_disp = df_disp[(df_disp['VALORTOTAL'] > 0) & (df_disp['AREATOTAL'] > 0)]
            data_dict['dispersao'] = df_disp
        else:
            data_dict['dispersao'] = pd.DataFrame()

    except Exception as e:
        print(f"Error loading MCDR data: {e}")
        
    return data_dict

if __name__ == '__main__':
    dados = load_mcdr_data()
    for k, v in dados.items():
        print(f"--- {k} ---")
        if not v.empty:
            print(v.head())
        else:
            print("Empty DataFrame")
