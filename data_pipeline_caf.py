import os
import unicodedata
import pandas as pd
from functools import lru_cache

COLS_DROP = ['ARQUIVO', 'ABA', 'TITULO', 'NENHUMA OPÇÃO', 'PREENCHIMENTO']
ALVOS = [('LOCALIDADE AREA PF', 'pf'), ('LOCALIDADE AREA PJ', 'pj_area'), ('CARACTERIZA', 'caracterizacao'),
         ('ATIVIDADE', 'atividade'), ('GENERO', 'genero'), ('JOVENS', 'jovens'), ('JURÍDICO', 'pj'),
         ('ENTIDADES', 'entidade'), ('RENDA QUANTIDADE', 'renda_qtd'), ('RENDA VALOR', 'renda_valor')]

def _nfc(s):
    return unicodedata.normalize('NFC', s).upper()

def _limpa(df):
    df = df.drop(columns=[c for c in COLS_DROP if c in df.columns], errors='ignore')
    df = df.loc[:, ~df.columns.str.contains('^Unnamed')]
    for c in ['ANO', 'MES']:
        if c in df.columns:
            df[c] = df[c].fillna(0).astype(str).str.replace(r'\.0$', '', regex=True)
            df[c] = df[c].replace(['0', 'nan', '0.0'], 'Desconhecido')
    if 'UF' in df.columns:
        df = df[df['UF'] == 'DF'].copy()
    return df

def _fontes(data_dir):
    """Retorna {nome da aba (maiúsculo): função que lê a aba}. Usa Parquet (caf_sheet_*.parquet) se existir; senão o Excel/ODS."""
    pq = {}
    if os.path.isdir(data_dir):
        for f in sorted(os.listdir(data_dir)):
            if f.startswith('caf_sheet_') and f.endswith('.parquet'):
                nome = _nfc(f[len('caf_sheet_'):-len('.parquet')].replace('_', ' '))
                pq[nome] = (lambda p: (lambda: pd.read_parquet(p)))(os.path.join(data_dir, f))
    if pq:
        return pq
    caminho = os.path.join(data_dir, 'CAF_TRATADO_COMPLETO.xlsx')
    eng = None
    if not os.path.exists(caminho):
        caminho = os.path.join(data_dir, 'CAF 02 2026.ods'); eng = 'odf'
        if not os.path.exists(caminho):
            return {}
    xl = pd.ExcelFile(caminho, engine=eng)
    return {_nfc(s): (lambda s=s: pd.read_excel(caminho, sheet_name=s, engine=eng)) for s in xl.sheet_names}

@lru_cache(maxsize=1)
def load_caf_data(data_dir='data/'):
    """Carrega a base CAF (abas em Parquet ou Excel/ODS) e retorna um dicionário de DataFrames limpos."""
    data_dict = {}
    try:
        fontes = _fontes(data_dir)
        if not fontes:
            print("CAF: arquivo não encontrado (CAF_TRATADO_COMPLETO.xlsx ou parquet).")
            return data_dict
        for alvo, chave in ALVOS:
            data_dict[chave] = pd.DataFrame()
            for nome, leitor in fontes.items():
                if nome in ('RESUMO UF', 'RESUMO - REGIÃO'):
                    continue
                if _nfc(alvo) in nome:
                    data_dict[chave] = _limpa(leitor())
                    break
    except Exception as e:
        print(f"Erro ao carregar CAF: {e}")
    return data_dict

if __name__ == '__main__':
    for k, v in load_caf_data().items():
        print(f"--- {k} ---")
        print(v.head(2) if not v.empty else "Empty DataFrame")
