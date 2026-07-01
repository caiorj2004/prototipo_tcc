import dash
from dash import html, dcc, Input, Output, State, callback_context

# Configuração de scripts e fontes externas
external_scripts = [{"src": "https://cdn.tailwindcss.com?plugins=forms,container-queries"}]
external_stylesheets = [
    "https://fonts.googleapis.com/css2?family=Public+Sans:wght@400;500;600;700&display=swap",
    "https://fonts.googleapis.com/css2?family=Material+Symbols+Outlined:wght,FILL@100..700,0..1&display=swap"
]

# INICIALIZAÇÃO MULTI-PAGE
app = dash.Dash(__name__, use_pages=True, external_scripts=external_scripts, external_stylesheets=external_stylesheets)

# Customização do HTML base (Tailwind e cores do protótipo)
app.index_string = '''
<!DOCTYPE html>
<html lang="pt-BR" class="light">
    <head>
        {%metas%}
        <title>Protótipo Sistema de Inteligência para Agricultura Familiar</title>
        {%favicon%}
        {%css%}
        <script>
          tailwind.config = {
            darkMode: "class",
            theme: {
              extend: {
                "colors": {
                  "primary-container": "#1b4332",
                  "tertiary-fixed-dim": "#89ceff",
                  "inverse-surface": "#2e3131",
                  "secondary-fixed-dim": "#ffb59b",
                  "surface-container-lowest": "#ffffff",
                  "primary": "#012d1d",
                  "outline": "#717973",
                  "on-error": "#ffffff",
                  "on-secondary": "#ffffff",
                  "on-primary-fixed-variant": "#274e3d",
                  "secondary-fixed": "#ffdbcf",
                  "tertiary-fixed": "#c9e6ff",
                  "on-tertiary-fixed-variant": "#004c6e",
                  "on-surface-variant": "#414844",
                  "on-primary": "#ffffff",
                  "on-secondary-fixed-variant": "#783114",
                  "inverse-on-surface": "#eff1f0",
                  "error": "#ba1a1a",
                  "surface-bright": "#f8faf9",
                  "surface-dim": "#d8dada",
                  "secondary-container": "#fe9974",
                  "surface-variant": "#e1e3e2",
                  "primary-fixed-dim": "#a5d0b9",
                  "on-error-container": "#93000a",
                  "on-secondary-container": "#762f13",
                  "inverse-primary": "#a5d0b9",
                  "secondary": "#974729",
                  "surface": "#f8faf9",
                  "background": "#f8faf9",
                  "error-container": "#ffdad6",
                  "surface-container-low": "#f2f4f3",
                  "tertiary": "#00293e",
                  "on-surface": "#191c1c",
                  "primary-fixed": "#c1ecd4",
                  "on-secondary-fixed": "#380d00",
                  "on-tertiary-container": "#2bb0f5",
                  "surface-container-highest": "#e1e3e2",
                  "surface-container-high": "#e6e9e8",
                  "surface-tint": "#3f6653",
                  "tertiary-container": "#00405e",
                  "outline-variant": "#c1c8c2",
                  "on-primary-fixed": "#002114",
                  "surface-container": "#eceeed",
                  "on-background": "#191c1c",
                  "on-tertiary": "#ffffff",
                  "on-tertiary-fixed": "#001e2f",
                  "on-primary-container": "#86af99"
                },
                "borderRadius": {
                  "DEFAULT": "0.125rem",
                  "lg": "0.25rem",
                  "xl": "0.5rem",
                  "full": "0.75rem"
                },
                "spacing": {
                  "card-padding": "20px",
                  "gutter": "24px",
                  "sidebar-width": "280px",
                  "unit": "4px",
                  "container-margin": "32px"
                },
                "fontFamily": {
                  "h1": ["Public Sans"],
                  "data-tabular": ["Public Sans"],
                  "h3": ["Public Sans"],
                  "body-lg": ["Public Sans"],
                  "body-md": ["Public Sans"],
                  "h2": ["Public Sans"],
                  "label-sm": ["Public Sans"]
                }
              }
            }
          }
        </script>
        <style>
          body { background-color: #f8faf9; }
        </style>
    </head>
    <body class="font-body-md text-body-md text-on-background min-h-screen flex">
        {%app_entry%}
        <footer>
            {%config%}
            {%scripts%}
            {%renderer%}
        </footer>
    </body>
</html>
'''

# ----------------- SIDEBAR -----------------
sidebar = html.Aside(className="fixed left-0 top-0 h-full w-[280px] bg-emerald-900 dark:bg-emerald-950 border-r border-emerald-800 shadow-xl dark:shadow-none flex flex-col py-6 z-50", children=[
    html.Div(className="px-6 mb-8 flex flex-col", children=[
        html.H2("Protótipo Sistema de Inteligência", className="text-white font-bold text-sm leading-tight tracking-tight"),
        html.P("para Agricultura Familiar", className="font-public-sans text-xs font-medium text-emerald-100/70 mt-1")
    ]),
    
    # Links de Navegação usando dcc.Link para roteamento
    html.Nav(className="flex-1 flex flex-col gap-1 px-2", children=[
        dcc.Link(href="/", className="text-emerald-100/70 hover:text-white hover:bg-emerald-800/50 px-4 py-3 flex items-center gap-3 font-public-sans text-sm font-medium transition-all rounded", children=[
            html.Span("analytics", className="material-symbols-outlined"),
            "Censo Agro 2017"
        ]),
        dcc.Link(href="/ibge", className="text-emerald-100/70 hover:text-white hover:bg-emerald-800/50 px-4 py-3 flex items-center gap-3 font-public-sans text-sm font-medium transition-all rounded", children=[
            html.Span("data_exploration", className="material-symbols-outlined"),
            "IBGE 2024"
        ]),
        dcc.Link(href="/cnpo", className="text-emerald-100/70 hover:text-white hover:bg-emerald-800/50 px-4 py-3 flex items-center gap-3 font-public-sans text-sm font-medium transition-all rounded", children=[
            html.Span("corporate_fare", className="material-symbols-outlined"),
            "CNPO"
        ]),
        dcc.Link(href="/caf", className="text-emerald-100/70 hover:text-white hover:bg-emerald-800/50 px-4 py-3 flex items-center gap-3 font-public-sans text-sm font-medium transition-all rounded", children=[
            html.Span("badge", className="material-symbols-outlined"),
            "CAF"
        ]),
        dcc.Link(href="/credito-rural", className="text-emerald-100/70 hover:text-white hover:bg-emerald-800/50 px-4 py-3 flex items-center gap-3 font-public-sans text-sm font-medium transition-all rounded", children=[
            html.Span("account_balance", className="material-symbols-outlined"),
            "Crédito Rural"
        ])
    ]),
    
    html.Div(className="px-6 mt-auto flex flex-col gap-4", children=[
        html.Div(className="flex flex-col gap-1 mt-4", children=[
            html.A(id="btn-ajuda", n_clicks=0, className="text-emerald-100/70 hover:text-white py-2 flex items-center gap-3 font-public-sans text-sm font-medium hover:bg-emerald-800/50 transition-all px-2 rounded cursor-pointer", children=[
                html.Span("help", className="material-symbols-outlined"), "Ajuda"
            ])
        ])
    ])
])

# ----------------- TOPBAR -----------------
topbar = html.Header(className="bg-white dark:bg-slate-900 border-b border-slate-200 dark:border-slate-800 w-full z-40 sticky top-0", children=[
    html.Div(className="flex justify-between items-center w-full px-10 py-3", children=[
        html.Div(className="flex items-center gap-4", children=[
            html.Span("Painel de Indicadores", className="text-xl font-bold text-emerald-900 dark:text-emerald-400 font-public-sans tracking-tight")
        ])
    ])
])

# ----------------- LAYOUT PRINCIPAL -----------------
# ----------------- MODAL DE AJUDA -----------------
modal_ajuda = html.Div(
    id="modal-ajuda",
    className="hidden fixed inset-0 bg-black/50 z-[100] items-center justify-center p-4",
    children=[
        html.Div(
            className="bg-white dark:bg-slate-900 rounded-xl shadow-2xl max-w-2xl w-full max-h-[85vh] flex flex-col overflow-hidden relative border border-slate-200 dark:border-slate-800 animate-in fade-in zoom-in-95 duration-200",
            children=[
                # Header do Modal
                html.Div(
                    className="flex justify-between items-center px-6 py-4 border-b border-slate-200 dark:border-slate-800",
                    children=[
                        html.H2("Guia do Painel de Indicadores (TCC)", className="text-xl font-bold text-emerald-900 dark:text-emerald-400 font-public-sans"),
                    ]
                ),
                
                # Conteúdo do Modal com Scroll
                html.Div(
                    className="flex-1 overflow-y-auto p-6 space-y-6 text-slate-700 dark:text-slate-300 font-public-sans",
                    children=[
                        html.Div(children=[
                            html.H3("Propósito", className="text-lg font-semibold text-emerald-800 dark:text-emerald-300 mb-2"),
                            html.P(
                                "Este painel interativo foi desenvolvido para combater a assimetria de informação no meio rural do Distrito Federal, servindo como uma ferramenta de transparência e suporte à governança baseada em dados (data-driven policymaking). O projeto visa auxiliar gestores públicos (GDF, Emater-DF) e a sociedade civil na alocação otimizada de recursos e na calibração de políticas públicas de assistência técnica e compras institucionais.",
                                className="text-sm leading-relaxed mb-4"
                            ),
                            html.P(
                                "Paralelamente, este dashboard integra os resultados da pesquisa de Trabalho de Conclusão de Curso (TCC) em Ciência de Dados e IA (IESB), que aplica técnicas de aprendizado não supervisionado (Clustering Socioespacial) para criar uma tipologia inédita dos territórios rurais do DF, revelando disparidades socioeconômicas frequentemente camufladas por indicadores agregados.",
                                className="text-sm leading-relaxed"
                            )
                        ]),
                        html.Div(children=[
                            html.H3("Como Navegar", className="text-lg font-semibold text-emerald-800 dark:text-emerald-300 mb-2"),
                            html.P(
                                "Utilize o menu lateral para transitar entre as diferentes bases de dados governamentais. Utilize os filtros no topo de cada página para selecionar o recorte temporal desejado.",
                                className="text-sm leading-relaxed"
                            )
                        ]),
                        html.Div(children=[
                            html.H3("Bases de Dados (Fontes)", className="text-lg font-semibold text-emerald-800 dark:text-emerald-300 mb-3"),
                            html.Div(className="space-y-4 pl-1", children=[
                                html.Div(children=[
                                    html.H4("Censo Agro (2017)", className="text-sm font-bold text-slate-800 dark:text-slate-200"),
                                    html.P("Dados demográficos e estruturais da base produtiva (IBGE).", className="text-sm text-slate-600 dark:text-slate-400")
                                ]),
                                html.Div(children=[
                                    html.H4("IBGE (2024)", className="text-sm font-bold text-slate-800 dark:text-slate-200"),
                                    html.P("Estimativas e projeções recentes do setor.", className="text-sm text-slate-600 dark:text-slate-400")
                                ]),
                                html.Div(children=[
                                    html.H4("CNPO", className="text-sm font-bold text-slate-800 dark:text-slate-200"),
                                    html.P("Cadastro Nacional de Produtores Orgânicos (MAPA).", className="text-sm text-slate-600 dark:text-slate-400")
                                ]),
                                html.Div(children=[
                                    html.H4("CAF", className="text-sm font-bold text-slate-800 dark:text-slate-200"),
                                    html.P("Cadastro Nacional da Agricultura Familiar, evidenciando formalização, gênero, juventude e renda (MDA).", className="text-sm text-slate-600 dark:text-slate-400")
                                ]),
                                html.Div(children=[
                                    html.H4("Crédito Rural (MCDR)", className="text-sm font-bold text-slate-800 dark:text-slate-200"),
                                    html.P("Matriz de Dados do Crédito Rural do Banco Central, demonstrando a alocação de recursos, concentração bancária e finalidade do crédito.", className="text-sm text-slate-600 dark:text-slate-400")
                                ])
                            ])
                        ])
                    ]
                ),
                
                # Rodapé do Modal
                html.Div(
                    className="px-6 py-4 bg-slate-50 dark:bg-slate-800/50 border-t border-slate-200 dark:border-slate-800 flex justify-end",
                    children=[
                        html.Button(
                            "Fechar",
                            id="btn-fechar-ajuda",
                            className="bg-emerald-800 hover:bg-emerald-950 text-white font-medium rounded-lg px-5 py-2.5 text-sm transition-colors cursor-pointer",
                            n_clicks=0
                        )
                    ]
                )
            ]
        )
    ]
)

app.layout = html.Div(
    className="font-body-md text-body-md text-on-background min-h-screen bg-background flex",
    # Usamos 100vw para forçar a largura a ser EXATAMENTE o tamanho da janela do navegador
    style={"width": "100vw", "overflowX": "hidden"},
    children=[
        sidebar,
        html.Div(
            className="flex flex-col h-screen",
            # A MÁGICA DE VERDADE: Calculamos o espaço exato da tela menos os 280px da barra verde lateral
            style={"marginLeft": "280px", "width": "calc(100vw - 280px)"},
            children=[
                topbar,
                html.Main(
                    className="flex-1 overflow-y-auto bg-background",
                    style={"width": "100%"},
                    children=[
                        dash.page_container 
                    ]
                )
            ]
        ),
        modal_ajuda
    ]
)

# Callback para alternar a visibilidade do modal de ajuda
@app.callback(
    Output("modal-ajuda", "className"),
    Input("btn-ajuda", "n_clicks"),
    Input("btn-fechar-ajuda", "n_clicks"),
    State("modal-ajuda", "className"),
    prevent_initial_call=True
)
def toggle_modal(n_ajuda, n_fechar, current_class):
    ctx = callback_context
    if not ctx.triggered:
        return current_class
    
    trigger_id = ctx.triggered[0]["prop_id"].split(".")[0]
    
    if trigger_id == "btn-ajuda":
        return "fixed inset-0 bg-black/50 z-[100] flex items-center justify-center p-4"
    elif trigger_id == "btn-fechar-ajuda":
        return "hidden fixed inset-0 bg-black/50 z-[100] items-center justify-center p-4"
    
    return current_class

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=7860, debug=True)