import pandas as pd
import glob
import os
from functools import lru_cache

@lru_cache(maxsize=1)
def load_censo_data(data_dir='data/'):
    """
    Carrega os arquivos .ods do IBGE mantendo cada tabela intacta,
    sem agregar ou mesclar indevidamente, conforme diretrizes.
    Retorna um dicionário onde a chave é um nome claro (métrica + escopo)
    e o valor é o DataFrame.
    """
    files_ods = glob.glob(os.path.join(data_dir, '*.ods'))
    files_xlsx = glob.glob(os.path.join(data_dir, '*.xlsx'))
    files = files_ods + files_xlsx
    data_dict = {}
    
    for f in files:
        basename = os.path.basename(f)
        
        # Lê o arquivo. As planilhas fornecidas estão com o cabeçalho na linha 0.
        try:
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
            nome_amigavel = basename.replace(' - Distrito Federal 2017.ods', '')
            
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
            elif 'Utilização das terras em hectares' in basename:
                tipo = 'Terra - Geral'
            elif 'Utilização das terras de matas ou florestas' in basename:
                tipo = 'Terra - Matas'
            elif 'Utilização das terras de pastagem' in basename:
                tipo = 'Terra - Pastagem'
            elif 'Utilização das terras de lavoura' in basename:
                tipo = 'Terra - Lavoura'
                
            # Novos Dados - Mecanização
            elif 'Número de máquinas, tratores ou equipamentos' in basename:
                tipo = 'Máquinas - Qtd'
            elif 'Número de estabelecimentos que usam máquinas' in basename:
                tipo = 'Máquinas - Estabs'
                
            # Novos Dados - Financiamento
            elif 'Estabelecimentos que obtiveram financiamento do governo' in basename:
                tipo = 'Financiamento - Governo'
            elif 'Estabelecimentos que obtiveram financiamento' in basename:
                tipo = 'Financiamento - Obtencao'
            elif 'Finalidade do financiamento' in basename:
                tipo = 'Financiamento - Finalidade'
                
            # Novos Dados - Sociodemográfico e Mão de Obra
            elif 'Número de estabelecimentos agropecuários por sexo e idade do produtor' in basename:
                tipo = 'Perfil - Idade Sexo'
            elif 'Número de estabelecimentos agropecuários por sexo do produtor' in basename:
                tipo = 'Perfil - Sexo'
            elif 'Número de estabelecimentos agropecuários por escolaridade' in basename:
                tipo = 'Perfil - Escolaridade'
            elif 'Pessoal ocupado sem parentesco' in basename:
                tipo = 'Mão de Obra - Sem Parentesco'
            elif 'Sexo e idade do pessoal ocupado com parentesco com o produtor' in basename:
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
