"""Carrega as tabelas agregadas do TCC (dados_tcc/*.csv) usadas pelas páginas /tipologia e /pdad-rural.

Todas as tabelas estão em nível de segmento, RA, grupo ou subpopulação (sem microdados).
Para regenerá-las: `app/gerar_tabelas_dash.py` no repositório pdad_tipologia_cluster.
Pasta configurável por DADOS_TCC_DIR.
"""
import os, re
from functools import lru_cache
from pathlib import Path
import pandas as pd

PASTA = Path(os.environ.get('DADOS_TCC_DIR', Path(__file__).parent / 'dados_tcc'))

COR_GRUPO = {'A': '#1b6ca8', 'B': '#b5432a', 'C': '#e0a43f'}
COR_NEUTRA = '#c9cfcb'
ROTULO_SUB = {'Características Urbanas': 'Moradia e Lazer'}   # nome usado no TCC
ROTULO_VAR = {
    'renda_domiciliar_pc': 'Renda domiciliar per capita (R$)', 'escolaridade_adulto': 'Escolaridade do adulto (anos)',
    'internet_banda_larga_fixa': 'Banda larga fixa', 'possui_computador': 'Possui computador', 'agua_rede': 'Água da rede',
    'solucao_sanitaria_estruturada': 'Solução sanitária estruturada', 'rua_pavimentada': 'Rua pavimentada',
    'trabalhou_30d': 'Trabalhou nos últimos 30 dias', 'contribui_previdencia': 'Contribui à previdência',
    'possui_automovel': 'Possui automóvel', 'ivs_df': 'IVS-DF', 'ebia_insegur_qualquer': 'Insegurança alimentar (EBIA, qualquer)',
    'ebia_mod_grave': 'Insegurança alimentar moderada/grave', 'beneficio_social': 'Recebe benefício social',
    'cadunico': 'Inscrito no CadÚnico', 'escritura_registrada': 'Escritura registrada', 'doc_formal': 'Documento formal do imóvel',
    'outorga_agua': 'Outorga de água', 'internet_domiciliar': 'Internet no domicílio', 'tem_ctps': 'Tem CTPS',
    'recebe_beneficios_sociais': 'Recebe benefícios sociais', 'internet_uso_3m': 'Usou internet (3 meses)',
}

def _ler(nome):
    return pd.read_csv(PASTA / nome)

def _sub(s):
    return s.replace(ROTULO_SUB) if hasattr(s, 'replace') else s

@lru_cache(maxsize=None)
def tipologia():
    t = {k: _ler(f'tipologia_{k}.csv') for k in ('grupos', 'perfil_grupos', 'segmentos', 'mapa_ras', 'modelos', 'ari_modelos',
                                                 'estabilidade_resumo', 'estabilidade_nulo_cov', 'escolha_k', 'sem_uma_ra',
                                                 'sem_uma_subpopulacao', 'coligacao_segmentos', 'totais', 'mapa_dim')}
    t['segmentos']['subpopulacao'] = _sub(t['segmentos']['subpopulacao'])
    t['coligacao_segmentos']['seg'] = t['coligacao_segmentos']['seg'].str.replace('Características Urbanas', 'Moradia e Lazer')
    return t

@lru_cache(maxsize=None)
def pdad():
    d = {k: _ler(f'pdad_{k}.csv') for k in ('subpopulacao', 'ra', 'faixa_etaria', 'piramide', 'renda_resumo', 'renda_escolaridade',
                                           'renda_beneficio', 'renda_sem_renda', 'indicadores_subpopulacao', 'totais', 'segmentos', 'spearman_segmentos')}
    for k in ('subpopulacao', 'indicadores_subpopulacao', 'segmentos'):
        d[k]['subpopulacao'] = _sub(d[k]['subpopulacao'])
    return d

def centroide(caminho):
    """Centroide aproximado (média dos vértices) de um caminho SVG."""
    n = [float(x) for x in re.findall(r'-?\d+\.?\d*', caminho)]
    xs, ys = n[0::2], n[1::2]
    return sum(xs) / len(xs), sum(ys) / len(ys)

def dados_disponiveis():
    """False quando a pasta dados_tcc/ não existe (ex.: ambiente sem dados no repositório, antes do sync do S3)."""
    return (PASTA / 'tipologia_grupos.csv').exists() and (PASTA / 'pdad_totais.csv').exists()
