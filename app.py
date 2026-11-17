import dash
from dash import html, dcc, Input, Output, State, callback_context
import os

# Configuração de scripts e fontes externas
external_scripts = [{"src": "https://cdn.tailwindcss.com?plugins=forms,container-queries"}]
external_stylesheets = [
    "https://fonts.googleapis.com/css2?family=Public+Sans:wght@400;500;600;700&display=swap",
    "https://fonts.googleapis.com/css2?family=Material+Symbols+Outlined:wght,FILL@100..700,0..1&display=swap"
]

# INICIALIZAÇÃO MULTI-PAGE
app = dash.Dash(__name__, use_pages=True, external_scripts=external_scripts, external_stylesheets=external_stylesheets)
server = app.server  # usado pelo gunicorn: gunicorn app:server
app.title = "AgroTec-DF | Painel de Inteligência para Agricultura Familiar"

# Customização do HTML base (Tailwind e cores do protótipo com WCAG AA)
app.index_string = '''
<!DOCTYPE html>
<html lang="pt-BR" class="light">
    <head>
        {%metas%}
        <title>AgroTec-DF - Painel Analítico Institucional</title>
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
                  "label-sm": ["Public Sans"],
                  "public-sans": ["Public Sans", "sans-serif"]
                }
              }
            }
          }
        </script>
        <style>
          body { background-color: #f8faf9; font-family: 'Public Sans', sans-serif; overflow-x: hidden; }
          .sidebar-transition { transition: transform 0.3s ease-in-out, width 0.3s ease-in-out, margin 0.3s ease-in-out; }
        </style>
    </head>
    <body class="font-public-sans text-slate-800 bg-slate-50 min-h-screen">
        {%app_entry%}
        <footer>
            {%config%}
            {%scripts%}
            {%renderer%}
        </footer>
    </body>
</html>
'''

# Store para o estado da sidebar (aberta/fechada)
sidebar_store = dcc.Store(id='sidebar-state', data={'is_open': True, 'is_mobile_open': False})

# ----------------- SIDEBAR RECOLHÍVEL (MOBILE-FIRST) -----------------
sidebar = html.Aside(
    id="app-sidebar",
    className="fixed left-0 top-0 h-full w-72 bg-emerald-950 text-white shadow-2xl flex flex-col z-50 sidebar-transition -translate-x-full md:translate-x-0 border-r border-emerald-900/60",
    children=[
        # Sidebar Header
        html.Div(className="p-5 border-b border-emerald-900/80 flex items-center justify-between", children=[
            html.Div(className="flex items-center gap-3", children=[
                html.Div(className="w-10 h-10 rounded-xl bg-emerald-800/80 flex items-center justify-center text-emerald-300 font-bold shrink-0 shadow-inner", children=[
                    html.Span("eco", className="material-symbols-outlined text-2xl")
                ]),
                html.Div(id="sidebar-brand-text", className="flex flex-col overflow-hidden whitespace-nowrap", children=[
                    html.H2("AgroTec-DF", className="font-bold text-base text-white tracking-tight leading-tight"),
                    html.P("Suporte Institucional", className="text-xs text-emerald-300/80 font-medium")
                ])
            ]),
            html.Button(
                id="btn-close-sidebar-mobile",
                className="md:hidden text-emerald-300 hover:text-white p-1 rounded-lg hover:bg-emerald-900/50 transition-colors",
                children=[html.Span("close", className="material-symbols-outlined")]
            )
        ]),

        # Navigation Links
        html.Nav(className="flex-1 flex flex-col gap-1.5 p-3 overflow-y-auto mt-2", children=[
            dcc.Link(href="/", className="text-emerald-100/80 hover:text-white hover:bg-emerald-900/60 px-3.5 py-2.5 flex items-center gap-3 text-sm font-medium transition-all rounded-xl", children=[
                html.Span("analytics", className="material-symbols-outlined text-emerald-400 shrink-0"),
                html.Span("Censo Agro 2017", className="sidebar-link-text whitespace-nowrap")
            ]),
            dcc.Link(href="/ibge", className="text-emerald-100/80 hover:text-white hover:bg-emerald-900/60 px-3.5 py-2.5 flex items-center gap-3 text-sm font-medium transition-all rounded-xl", children=[
                html.Span("data_exploration", className="material-symbols-outlined text-emerald-400 shrink-0"),
                html.Span("IBGE 2024", className="sidebar-link-text whitespace-nowrap")
            ]),
            dcc.Link(href="/cnpo", className="text-emerald-100/80 hover:text-white hover:bg-emerald-900/60 px-3.5 py-2.5 flex items-center gap-3 text-sm font-medium transition-all rounded-xl", children=[
                html.Span("eco", className="material-symbols-outlined text-emerald-400 shrink-0"),
                html.Span("CNPO Orgânicos", className="sidebar-link-text whitespace-nowrap")
            ]),
            dcc.Link(href="/caf", className="text-emerald-100/80 hover:text-white hover:bg-emerald-900/60 px-3.5 py-2.5 flex items-center gap-3 text-sm font-medium transition-all rounded-xl", children=[
                html.Span("badge", className="material-symbols-outlined text-emerald-400 shrink-0"),
                html.Span("CAF", className="sidebar-link-text whitespace-nowrap")
            ]),
            dcc.Link(href="/credito-rural", className="text-emerald-100/80 hover:text-white hover:bg-emerald-900/60 px-3.5 py-2.5 flex items-center gap-3 text-sm font-medium transition-all rounded-xl", children=[
                html.Span("account_balance", className="material-symbols-outlined text-emerald-400 shrink-0"),
                html.Span("Crédito Rural (MCDR)", className="sidebar-link-text whitespace-nowrap")
            ]),
            html.Div(className="my-2 border-t border-emerald-900/60"),
            dcc.Link(href="/tipologia", className="text-emerald-100/80 hover:text-white hover:bg-emerald-900/60 px-3.5 py-2.5 flex items-center gap-3 text-sm font-medium transition-all rounded-xl", children=[
                html.Span("grid_view", className="material-symbols-outlined text-teal-400 shrink-0"),
                html.Span("Tipologia Rural (TCC)", className="sidebar-link-text whitespace-nowrap")
            ]),
            dcc.Link(href="/pdad-rural", className="text-emerald-100/80 hover:text-white hover:bg-emerald-900/60 px-3.5 py-2.5 flex items-center gap-3 text-sm font-medium transition-all rounded-xl", children=[
                html.Span("house", className="material-symbols-outlined text-teal-400 shrink-0"),
                html.Span("PDAD Rural 2022", className="sidebar-link-text whitespace-nowrap")
            ])
        ]),
        
        # Sidebar Footer
        html.Div(className="p-4 border-t border-emerald-900/80 flex flex-col gap-2 mt-auto", children=[
            html.A(id="btn-ajuda", n_clicks=0, className="text-emerald-200 hover:text-white py-2 px-3 flex items-center gap-3 text-sm font-medium hover:bg-emerald-900/60 transition-all rounded-xl cursor-pointer", children=[
                html.Span("help_outline", className="material-symbols-outlined text-emerald-400 shrink-0"),
                html.Span("Guia Institucional & Ajuda", className="sidebar-link-text whitespace-nowrap")
            ])
        ])
    ]
)

# ----------------- TOPBAR -----------------
topbar = html.Header(className="bg-white dark:bg-slate-900 border-b border-slate-200 dark:border-slate-800 w-full z-40 sticky top-0 shadow-sm", children=[
    html.Div(className="flex justify-between items-center w-full px-4 md:px-8 py-3", children=[
        html.Div(className="flex items-center gap-3 md:gap-4", children=[
            html.Button(
                id="btn-toggle-sidebar",
                className="text-slate-600 dark:text-slate-300 hover:text-emerald-800 dark:hover:text-emerald-400 p-2 rounded-xl hover:bg-slate-100 dark:hover:bg-slate-800 transition-colors cursor-pointer",
                children=[html.Span("menu", className="material-symbols-outlined text-2xl")]
            ),
            html.Div(className="flex flex-col", children=[
                html.Span("AgroTec-DF", className="text-base md:text-lg font-bold text-emerald-950 dark:text-emerald-400 tracking-tight leading-tight"),
                html.Span("Sistema de Inteligência para Agricultura Familiar do DF", className="text-xs text-slate-500 dark:text-slate-400 hidden sm:inline-block")
            ])
        ]),
        html.Div(className="flex items-center gap-2 md:gap-4", children=[
            html.Div(className="flex items-center gap-2 bg-emerald-50 dark:bg-emerald-950/60 border border-emerald-200 dark:border-emerald-800 px-3 py-1.5 rounded-full text-xs text-emerald-900 dark:text-emerald-200 font-medium", children=[
                html.Span("account_balance", className="material-symbols-outlined text-emerald-700 dark:text-emerald-400 text-base"),
                html.Span("Suporte: FAPDF, IESB e AgroTec")
            ])
        ])
    ])
])

# ----------------- OVERLAY PARA MOBILE -----------------
sidebar_overlay = html.Div(
    id="sidebar-overlay",
    className="hidden fixed inset-0 bg-slate-900/50 backdrop-blur-sm z-40 transition-opacity"
)

# ----------------- MODAL DE AJUDA & METODOLOGIA -----------------
modal_ajuda = html.Div(
    id="modal-ajuda",
    className="hidden fixed inset-0 bg-black/50 z-[100] items-center justify-center p-4",
    children=[
        html.Div(
            className="bg-white dark:bg-slate-900 rounded-2xl shadow-2xl max-w-2xl w-full max-h-[85vh] flex flex-col overflow-hidden relative border border-slate-200 dark:border-slate-800 animate-in fade-in zoom-in-95 duration-200",
            children=[
                # Header do Modal
                html.Div(
                    className="flex justify-between items-center px-6 py-4 border-b border-slate-200 dark:border-slate-800 bg-emerald-950 text-white",
                    children=[
                        html.Div(className="flex items-center gap-2", children=[
                            html.Span("school", className="material-symbols-outlined text-emerald-400 text-2xl"),
                            html.H2("Guia Institucional & Ajuda", className="text-lg font-bold text-white font-public-sans")
                        ]),
                    ]
                ),
                
                # Conteúdo do Modal com Scroll
                html.Div(
                    className="flex-1 overflow-y-auto p-6 space-y-6 text-slate-700 dark:text-slate-300 font-public-sans text-sm leading-relaxed",
                    children=[
                        html.Div(className="bg-amber-50 dark:bg-amber-950/40 p-4 rounded-xl border border-amber-200 dark:border-amber-800 text-amber-900 dark:text-amber-200", children=[
                            html.H3("⚠️ Realidade Institucional e Espacial do DF", className="text-sm font-bold text-amber-950 dark:text-amber-100 mb-2 flex items-center gap-2"),
                            html.P("O Distrito Federal é cadastrado e tratado como um único município pelo IBGE e Banco Central. As bases oficiais de Crédito Rural (MCDR) e CAF não descem nativamente ao nível de Região Administrativa (RA). O AgroTec-DF foi projetado exclusivamente para suporte institucional aos gestores e extensionistas (EMATER-DF, IPEDF, SEAGRI-DF).")
                        ]),
                        html.Div(children=[
                            html.H3("Propósito do Sistema", className="text-base font-bold text-emerald-900 dark:text-emerald-400 mb-2"),
                            html.P(
                                "O AgroTec-DF visa combater a assimetria de informação no setor rural do Distrito Federal, oferecendo suporte à governança pública baseada em evidências. Ele integra dados demográficos, crédito rural, produtores orgânicos, cadastros da agricultura familiar e tipologia territorial socioespacial."
                            )
                        ]),
                        html.Div(children=[
                            html.H3("Bases de Dados Governamentais Integradas", className="text-base font-bold text-emerald-900 dark:text-emerald-400 mb-3"),
                            html.Ul(className="space-y-2 pl-2 list-disc list-inside text-slate-600 dark:text-slate-400", children=[
                                html.Li([html.Strong("Censo Agro 2017 (IBGE): "), "Perfil demográfico, uso do solo, mecanização e financiamento."]),
                                html.Li([html.Strong("IBGE 2024: "), "Estimativas de produção agrícola (PAM) e pecuária (PPM)."]),
                                html.Li([html.Strong("CNPO (MAPA): "), "Cadastro Nacional de Produtores Orgânicos e escopos."]),
                                html.Li([html.Strong("CAF (MDA): "), "Cadastro Nacional da Agricultura Familiar, gênero, jovens e renda."]),
                                html.Li([html.Strong("Crédito Rural (BCB/MCDR): "), "Matriz de crédito por modalidade e instituição financeira."]),
                                html.Li([html.Strong("PDAD Rural 2022 (IPE-DF): "), "5.075 domicílios e 15.357 moradores; base da análise exploratória e da tipologia dos territórios rurais do TCC (49 segmentos RA × subpopulação, modelo M2, K = 3). A estrutura é um gradiente de urbanização formal, não tipos naturais; os grupos são hipóteses para investigar."])
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
                            className="bg-emerald-800 hover:bg-emerald-900 text-white font-medium rounded-xl px-5 py-2.5 text-sm transition-colors cursor-pointer",
                            n_clicks=0
                        )
                    ]
                )
            ]
        )
    ]
)

# Layout Principal com suporte a Collapsible Sidebar
app.layout = html.Div(
    className="min-h-screen bg-slate-50 dark:bg-slate-950 flex flex-col font-public-sans",
    children=[
        sidebar_store,
        sidebar_overlay,
        sidebar,
        html.Div(
            id="app-main-content",
            className="flex-1 flex flex-col md:ml-72 sidebar-transition min-w-0",
            children=[
                topbar,
                html.Main(
                    className="flex-1 overflow-y-auto bg-slate-50 dark:bg-slate-950",
                    children=[
                        dash.page_container 
                    ]
                )
            ]
        ),
        modal_ajuda
    ]
)

# Callback para controlar abertura/fechamento da Sidebar e Overlay (Desktop & Mobile)
@app.callback(
    Output("sidebar-state", "data"),
    Input("btn-toggle-sidebar", "n_clicks"),
    Input("btn-close-sidebar-mobile", "n_clicks"),
    Input("sidebar-overlay", "n_clicks"),
    State("sidebar-state", "data"),
    prevent_initial_call=True
)
def toggle_sidebar_state(n_toggle, n_close, n_overlay, current_data):
    ctx = callback_context
    if not ctx.triggered:
        return current_data
        
    trigger_id = ctx.triggered[0]["prop_id"].split(".")[0]
    is_open = current_data.get('is_open', True)
    is_mobile_open = current_data.get('is_mobile_open', False)
    
    if trigger_id == "btn-toggle-sidebar":
        return {'is_open': not is_open, 'is_mobile_open': not is_mobile_open}
    elif trigger_id in ["btn-close-sidebar-mobile", "sidebar-overlay"]:
        return {'is_open': is_open, 'is_mobile_open': False}
        
    return current_data

@app.callback(
    Output("app-sidebar", "className"),
    Output("app-main-content", "className"),
    Output("sidebar-overlay", "className"),
    Output("sidebar-brand-text", "className"),
    Input("sidebar-state", "data")
)
def render_sidebar_layout(state):
    is_open = state.get('is_open', True)
    is_mobile = state.get('is_mobile_open', False)
    
    base_sidebar = "fixed left-0 top-0 h-full bg-emerald-950 text-white shadow-2xl flex flex-col z-50 sidebar-transition border-r border-emerald-900/60"
    base_content = "flex-1 flex flex-col sidebar-transition min-w-0"
    base_overlay = "fixed inset-0 bg-slate-900/50 backdrop-blur-sm z-40 transition-opacity"
    
    brand_class = "flex flex-col overflow-hidden whitespace-nowrap"
    
    if is_open:
        sidebar_cls = f"{base_sidebar} w-72 " + ("translate-x-0" if is_mobile else "-translate-x-full md:translate-x-0")
        content_cls = f"{base_content} md:ml-72"
    else:
        sidebar_cls = f"{base_sidebar} w-20 " + ("translate-x-0" if is_mobile else "-translate-x-full md:translate-x-0")
        content_cls = f"{base_content} md:ml-20"
        brand_class += " hidden"
        
    overlay_cls = f"{base_overlay} block md:hidden" if is_mobile else f"{base_overlay} hidden"
    
    return sidebar_cls, content_cls, overlay_cls, brand_class

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
        return "fixed inset-0 bg-black/50 z-[100] flex items-center justify-center p-4 animate-in fade-in duration-200"
    elif trigger_id == "btn-fechar-ajuda":
        return "hidden fixed inset-0 bg-black/50 z-[100] items-center justify-center p-4"
    
    return current_class

if __name__ == '__main__':
    debug_mode = os.getenv("DASH_DEBUG", "False").lower() in ["true", "1"]
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 7860)), debug=debug_mode)