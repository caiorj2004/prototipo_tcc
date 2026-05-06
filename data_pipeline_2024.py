import pandas as pd
import os

def clean_valor_pecuaria(x):
    if pd.isna(x):
        return x
    # Fix for thousands parsed as decimals (e.g. 160.664 -> 160664)
    if x < 1000 and (x % 1 != 0):
        return int(round(x * 1000))
    return int(x)

def load_data_2024():
    """
    Carrega e limpa os dados de Agricultura e Pecuária de 2024.
    Retorna um dicionário com os DataFrames prontos para uso.
    """
    base_dir = os.path.dirname(os.path.abspath(__file__))
    data_dir = os.path.join(base_dir, 'data')
    
    file_agri = os.path.join(data_dir, 'Agricultura - Valor da produção (2024).xlsx')
    file_pec = os.path.join(data_dir, 'Pecuária - Rebanhos (2024).xlsx')
    
    try:
        df_agri = pd.read_excel(file_agri)
        # Ordenar do maior para o menor valor e pegar top 10
        if 'Valor' in df_agri.columns:
            df_agri = df_agri.sort_values(by='Valor', ascending=False).reset_index(drop=True)
            
    except Exception as e:
        print(f"Erro ao ler {file_agri}: {e}")
        df_agri = pd.DataFrame(columns=['Produto', 'Valor'])
        
    try:
        df_pec = pd.read_excel(file_pec)
        # Tratar os valores de cabeças de gado
        if 'Valor' in df_pec.columns:
            df_pec['Valor'] = df_pec['Valor'].apply(clean_valor_pecuaria)
        # Limpeza visual de caracteres, se necessário (o pandas geralmente já faz o handle correto de utf-8 via openpyxl)
            
    except Exception as e:
        print(f"Erro ao ler {file_pec}: {e}")
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
