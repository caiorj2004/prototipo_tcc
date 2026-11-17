import dash
from data_pipeline_tcc import dados_disponiveis

dash.register_page(__name__, path='/pdad-rural', name='PDAD Rural 2022')

if dados_disponiveis():
    from pages._pdad_rural_conteudo import layout  # noqa: F401  (registra também os callbacks)
else:
    from pages._tcc_guard import indisponivel
    layout = indisponivel("PDAD Rural 2022 · análise exploratória")
