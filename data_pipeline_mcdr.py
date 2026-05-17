import pandas as pd
import os
from functools import lru_cache

@lru_cache(maxsize=1)
def load_mcdr_data(data_dir='data/'):
    """
    Carrega o arquivo de Crédito Rural (MCDR), 
    trata os formatos numéricos pt-BR e retorna o DataFrame centralizado e limpo.
    """
    # Procura pela base em múltiplos formatos
    filepath = None
    for ext in ['.csv', '.xlsx', '.ods']:
        path_test = os.path.join(data_dir, f'Matriz_Credito_Rural_DF_2017_2025{ext}')
        if os.path.exists(path_test):
            filepath = path_test
            break
            
    if not filepath:
        # Fallback
        filepath = os.path.join(data_dir, 'mcdr_2024.csv')
        if not os.path.exists(filepath):
            print("Nenhum arquivo MCDR encontrado.")
            return pd.DataFrame()
        
    try:
        if filepath.endswith('.csv'):
            df = pd.read_csv(filepath, sep=';', encoding='utf-8-sig', decimal=',', thousands='.', low_memory=False)
            if len(df.columns) == 1:
                df = pd.read_csv(filepath, sep=',', encoding='utf-8-sig', decimal=',', thousands='.', low_memory=False)
        elif filepath.endswith('.xlsx'):
            df = pd.read_excel(filepath)
        else:
            df = pd.read_excel(filepath, engine='odf')
            
        # Colunas financeiras e quantitativas esperadas
        cols_num = ['VLCUSTEIO', 'VLINVESTIMENTO', 'VLCOMERCIALIZACAO', 'VLINDUSTRIALIZACAO', 'AREATOTAL', 'QTDTOTAL', 'VALORTOTAL']
        
        # Limpar espaços extras em nomes de colunas por garantia
        df.columns = df.columns.str.strip()
        
        # O Ano pode vir em várias colunas, vamos tentar padronizar para uma coluna "ANO"
        ano_cols = [c for c in df.columns if c.upper() in ['ANO', 'ANO_EMISSAO', 'DATA_EMISSAO', 'ANO_REFERÊNCIA']]
        if ano_cols:
            col_ano = ano_cols[0]
            # Se for data, tenta extrair o ano
            if 'DATA' in col_ano.upper():
                df['ANO'] = pd.to_datetime(df[col_ano], errors='coerce').dt.year
            else:
                df['ANO'] = df[col_ano]
        else:
            df['ANO'] = 2024 # Valor padrão se não existir
            
        df['ANO'] = df['ANO'].fillna(0).astype(int).astype(str)
        df['ANO'] = df['ANO'].replace('0', 'Desconhecido')
        
        for col in cols_num:
            if col in df.columns:
                # Trata caso a leitura do excel/csv não tenha aplicado o decimal/milhares
                if df[col].dtype == object:
                    df[col] = df[col].astype(str).str.replace('.', '', regex=False).str.replace(',', '.', regex=False)
                df[col] = pd.to_numeric(df[col], errors='coerce').fillna(0)
                
        # Removendo a agregação estática, retornamos o DataFrame limpo.
        return df

    except Exception as e:
        print(f"Error loading MCDR data: {e}")
        return pd.DataFrame()

if __name__ == '__main__':
    df = load_mcdr_data()
    print("DataFrame MCDR:")
    print(df.head())
    print(df.columns)
