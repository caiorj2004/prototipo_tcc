import pandas as pd
import glob
import os
from functools import lru_cache

@lru_cache(maxsize=1)
def load_censo_data(data_dir='data/'):
    """
    Carrega os dados pré-agregados em Parquet (ou fallback .ods/.xlsx) do IBGE
    mantendo cada tabela intacta com lru_cache para máxima performance.
    """
    files_parquet = glob.glob(os.path.join(data_dir, '*.parquet'))
    censo_parquet = [f for f in files_parquet if not any(k in os.path.basename(f) for k in ['CAF', 'CNPO', 'Matriz', '2024', 'caf_sheet', 'Agricultura', 'Pecuaria'])]
    
    files = censo_parquet
    if not files:
        files = glob.glob(os.path.join(data_dir, '*.ods')) + glob.glob(os.path.join(data_dir, '*.xlsx'))
        
    data_dict = {}
    
    for f in files:
        basename = os.path.basename(f)
        
        try:
            if f.endswith('.parquet'):
                df = pd.read_parquet(f)
            else:
                eng = 'odf' if f.endswith('.ods') else None
                df = pd.read_excel(f, engine=eng, header=0)
            
            # Limpeza básica (remover colunas não nomeadas se houver lixo)
            df = df.loc[:, ~df.columns.str.contains('^Unnamed')]
            
            # Converter colunas de valores para numérico, ignorando erros
            cols_raca = ['Branca', 'Preta', 'Amarela', 'Parda', 'Indígena', 'Não se aplica']
            for col in cols_raca:
                if col in df.columns:
                    df[col] = pd.to_numeric(df[col], errors='coerce').fillna(0)
            
            # Preencher NaN em Produto
            if 'Produto' in df.columns:
                df['Produto'] = df['Produto'].fillna('Desconhecido')
                
            # Identificar a métrica e escopo a partir do nome
            nome_amigavel = basename.replace(' - Distrito Federal 2017.ods', '').replace('.parquet', '').replace('.ods', '')
            
            # Categorizar o tipo de dado para a UI
            tipo = 'Outros'
            ramo = 'Geral'
            
            # 1. Dados antigos com granularidade (Ramo/Produto/Raça)
            if 'Quantidade de estabelecimentos' in basename:
                tipo = 'Qtd Estabelecimentos'
            elif 'Média da quantidade' in basename or 'Total da quantidade' in basename:
                tipo = 'Qtd Kg'
            elif 'Valor de produção (soma)' in basename:
                tipo = 'Valor Soma'
            elif 'Valor de produção (média)' in basename:
                tipo = 'Valor Média'
            
            # Novos Dados - Uso da Terra
            elif 'Utilização das terras em hectares' in basename or 'Utilizacao das terras em hectares' in basename:
                tipo = 'Terra - Geral'
            elif 'Utilização das terras de matas' in basename or 'Utilizacao das terras de matas' in basename:
                tipo = 'Terra - Matas'
            elif 'Utilização das terras de pastagem' in basename or 'Utilizacao das terras de pastagem' in basename:
                tipo = 'Terra - Pastagem'
            elif 'Utilização das terras de lavoura' in basename or 'Utilizacao das terras de lavoura' in basename:
                tipo = 'Terra - Lavoura'
                
            # Novos Dados - Mecanização
            elif 'Número de máquinas' in basename or 'Numero de maquinas' in basename:
                tipo = 'Máquinas - Qtd'
            elif 'Número de estabelecimentos que usam máquinas' in basename or 'Numero de estabelecimentos que usam maquinas' in basename:
                tipo = 'Máquinas - Estabs'
                
            # Novos Dados - Financiamento
            elif 'obveram financiamento do governo' in basename or 'obtiveram financiamento do governo' in basename:
                tipo = 'Financiamento - Governo'
            elif 'obveram financiamento' in basename or 'obtiveram financiamento' in basename:
                tipo = 'Financiamento - Obtencao'
            elif 'Finalidade do financiamento' in basename:
                tipo = 'Financiamento - Finalidade'
                
            # Novos Dados - Sociodemográfico e Mão de Obra
            elif 'sexo e idade do produtor' in basename:
                tipo = 'Perfil - Idade Sexo'
            elif 'sexo do produtor' in basename:
                tipo = 'Perfil - Sexo'
            elif 'escolaridade' in basename:
                tipo = 'Perfil - Escolaridade'
            elif 'sem parentesco' in basename:
                tipo = 'Mão de Obra - Sem Parentesco'
            elif 'com parentesco' in basename:
                tipo = 'Mão de Obra - Parentesco'
                
            if 'Horticultura' in basename:
                ramo = 'Horticultura'
            elif 'Lavoura Permanente' in basename:
                ramo = 'Lavoura Permanente'
            elif 'Lavoura Temporária' in basename:
                ramo = 'Lavoura Temporária'
                
            chave = f"{tipo} | {ramo}"
            
            data_dict[chave] = {
                'df': df,
                'tipo': tipo,
                'ramo': ramo,
                'nome_original': basename
            }
            
        except Exception as e:
            print(f"Erro ao ler {basename}: {e}")
            
    return data_dict

if __name__ == '__main__':
    dados = load_censo_data()
    for k, v in dados.items():
        print(f"--- {k} ---")
        print(v['df'].head(3))
        print("\n")
