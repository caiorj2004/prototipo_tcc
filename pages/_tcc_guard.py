from dash import html
from data_pipeline_tcc import PASTA

def indisponivel(titulo):
    return html.Div(className="w-full p-6 md:p-8 bg-background", children=[
        html.H1(titulo, className="font-h1 text-h1 text-primary text-2xl font-bold"),
        html.Div(className="mt-6 border-l-4 border-secondary bg-secondary-fixed/40 rounded p-4 text-sm text-on-secondary-fixed-variant", children=[
            html.Strong("Dados indisponíveis: "),
            f"as tabelas do TCC não foram encontradas em '{PASTA}'. Sincronize a pasta dados_tcc/ (por exemplo, com aws s3 sync) "
            "ou defina a variável DADOS_TCC_DIR e reinicie o app."])])
