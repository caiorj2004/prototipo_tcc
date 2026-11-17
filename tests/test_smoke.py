"""Teste de fumaça: todas as páginas respondem e as abas/filtros das páginas do TCC geram figuras.
Rodar: pytest -q   (ou python tests/test_smoke.py)"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from app import app, server  # noqa: E402

ROTAS = ['/', '/ibge', '/cnpo', '/caf', '/credito-rural', '/tipologia', '/pdad-rural']

def test_rotas():
    c = server.test_client()
    for r in ROTAS:
        assert c.get(r).status_code == 200, r

def test_callbacks_tcc():
    from pages import tipologia, pdad_rural
    for v in ('mapa', 'perfil', 'seg', 'modelos', 'estab'):
        assert tipologia.troca_aba(v) is not None
    g, t = tipologia.atualiza_seg(['A'], None)
    assert g is not None and t is not None
    for v in ('perfil', 'renda', 'sub', 'corr'):
        assert pdad_rural.troca(v) is not None

def test_numeros_tcc():
    from data_pipeline_tcc import tipologia as T
    t = T()
    assert len(t['segmentos']) == 49
    assert t['grupos'].n_seg.tolist() == [12, 20, 17]
    assert int(t['totais'].iloc[0].amostra) == 5067

if __name__ == '__main__':
    test_rotas(); test_callbacks_tcc(); test_numeros_tcc(); print('ok')
