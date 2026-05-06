import pandas as pd
import glob
import os

def load_censo_data(data_dir='data/'):
    """
    Carrega os arquivos .ods do IBGE mantendo cada tabela intacta,
    sem agregar ou mesclar indevidamente, conforme diretrizes.
    Retorna um dicionário onde a chave é um nome claro (métrica + escopo)
    e o valor é o DataFrame.
    """
    files = glob.glob(os.path.join(data_dir, '*.ods'))
    data_dict = {}
    
    for f in files:
        basename = os.path.basename(f)
        
        # Lê o arquivo. As planilhas fornecidas estão com o cabeçalho na linha 0.
        try:
            df = pd.read_excel(f, engine='odf', header=0)
            
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
            if 'Quantidade de estabelecimentos' in basename:
                tipo = 'Qtd Estabelecimentos'
            elif 'Média da quantidade' in basename or 'Total da quantidade' in basename:
                tipo = 'Qtd Kg'
            elif 'Valor de produção (soma)' in basename:
                tipo = 'Valor Soma'
            elif 'Valor de produção (média)' in basename:
                tipo = 'Valor Média'
                
            ramo = 'Geral'
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
