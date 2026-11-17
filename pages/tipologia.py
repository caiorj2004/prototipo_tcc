import dash
from data_pipeline_tcc import dados_disponiveis

dash.register_page(__name__, path='/tipologia', name='Tipologia Rural (TCC)')

if dados_disponiveis():
    from pages._tipologia_conteudo import layout  # noqa: F401  (registra também os callbacks)
else:
    from pages._tcc_guard import indisponivel
    layout = indisponivel("Tipologia dos Territórios Rurais do DF")
