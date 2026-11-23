"""Teste de fumaça: todas as páginas respondem e as abas/filtros das páginas do TCC geram figuras.
Rodar: pytest -q   (ou python tests/test_smoke.py)"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from app import app, server  # noqa: E402
import subprocess, os, tempfile

ROTAS = ['/', '/ibge', '/cnpo', '/caf', '/credito-rural', '/tipologia', '/pdad-rural']

def test_rotas():
    c = server.test_client()
    for r in ROTAS:
        assert c.get(r).status_code == 200, r

def test_sem_dados_tcc():
    """Sem dados_tcc/ o app sobe e as páginas do TCC mostram aviso (não derrubam o app)."""
    vazio = tempfile.mkdtemp()
    cod = ("import sys; sys.path.insert(0, %r); from app import server; c = server.test_client();"
           "r = [c.get(p).status_code for p in ('/', '/tipologia', '/pdad-rural')]; assert r == [200, 200, 200], r; print('ok')") % str(Path(__file__).resolve().parent.parent)
    out = subprocess.run([sys.executable, '-c', cod], env={**os.environ, 'DADOS_TCC_DIR': vazio}, capture_output=True, text=True)
    assert out.returncode == 0 and 'ok' in out.stdout, out.stderr[-500:]

def test_callbacks_tcc():
    from pages import _tipologia_conteudo as tipologia, _pdad_rural_conteudo as pdad_rural
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

def test_export_mcdr_top15_sao_as_maiores():
    """O CSV de instituições financeiras deve trazer as 15 MAIORES, como o gráfico."""
    import pandas as pd
    import app  # noqa: F401  (registra as páginas)
    from pages import mcdr
    dff = mcdr.get_filtered_mcdr('ALL')
    esperado = (dff.groupby('NOMEIF')['VALORTOTAL'].sum().sort_values(ascending=False).head(15))
    out = mcdr.download_mcdr_if(1, 'ALL')
    import io
    df = pd.read_csv(io.StringIO(out['content']))
    assert set(df['Instituição Financeira']) == set(esperado.index)
    assert df['Valor Total (R$)'].min() >= esperado.min() - 1e-6

def test_export_caf_percapita_difere_do_total():
    """O CSV per capita é agregado (média) e não repete os dados brutos do total."""
    import pandas as pd
    import app  # noqa: F401
    from pages import caf
    for chave in ('renda_valor', 'renda_qtd'):
        df = caf.dados_caf.get(chave, pd.DataFrame())
        if df.empty:
            continue
        tot, prod, col_t = caf.agrega_renda(df, 'total')
        per, _, col_p = caf.agrega_renda(df, 'percapita')
        assert tot is not None and per is not None
        assert col_t != col_p
        assert tot[prod].is_unique and per[prod].is_unique  # uma linha por produto

if __name__ == '__main__':
    test_rotas(); test_callbacks_tcc(); test_numeros_tcc(); test_export_mcdr_top15_sao_as_maiores(); test_export_caf_percapita_difere_do_total(); print('ok')
