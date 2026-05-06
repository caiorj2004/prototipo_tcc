import dash
from dash import html, dcc

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
        ])
    ]),
    
    html.Div(className="px-6 mt-auto flex flex-col gap-4", children=[
        html.Button(className="w-full border border-secondary text-secondary hover:bg-secondary/10 transition-colors rounded-lg py-2 font-label-sm text-label-sm flex items-center justify-center gap-2", children=[
            html.Span("download", className="material-symbols-outlined text-[18px]"),
            "Exportar Relatório"
        ]),
        html.Div(className="flex flex-col gap-1 mt-4", children=[
            html.A(className="text-emerald-100/70 hover:text-white py-2 flex items-center gap-3 font-public-sans text-sm font-medium hover:bg-emerald-800/50 transition-all px-2 rounded", href="#", children=[
                html.Span("help", className="material-symbols-outlined"), "Ajuda"
            ]),
            html.A(className="text-emerald-100/70 hover:text-white py-2 flex items-center gap-3 font-public-sans text-sm font-medium hover:bg-emerald-800/50 transition-all px-2 rounded", href="#", children=[
                html.Span("logout", className="material-symbols-outlined"), "Sair"
            ])
        ])
    ])
])

# ----------------- TOPBAR -----------------
topbar = html.Header(className="bg-white dark:bg-slate-900 border-b border-slate-200 dark:border-slate-800 w-full z-40 sticky top-0", children=[
    html.Div(className="flex justify-between items-center w-full px-8 py-3", children=[
        html.Div(className="flex items-center gap-4", children=[
            html.Span("Painel de Indicadores", className="text-xl font-bold text-emerald-900 dark:text-emerald-400 font-public-sans tracking-tight")
        ]),
        html.Div(className="flex items-center gap-6", children=[
            html.Div(className="relative hidden md:block", children=[
                html.Span("search", className="material-symbols-outlined absolute left-3 top-1/2 -translate-y-1/2 text-slate-400 text-[20px]"),
                dcc.Input(className="pl-10 pr-4 py-2 bg-surface-container-low border border-outline-variant rounded-full text-sm font-public-sans focus:outline-none focus:border-primary-container focus:ring-1 focus:ring-primary-container transition-colors w-64", placeholder="Buscar dados...", type="text")
            ]),
            html.Div(className="flex items-center gap-2", children=[
                html.Button(className="w-10 h-10 rounded-full flex items-center justify-center text-slate-500 dark:text-slate-400 hover:bg-slate-50 dark:hover:bg-slate-800 transition-colors", children=[
                    html.Span("notifications", className="material-symbols-outlined")
                ]),
                html.Button(className="w-10 h-10 rounded-full flex items-center justify-center text-slate-500 dark:text-slate-400 hover:bg-slate-50 dark:hover:bg-slate-800 transition-colors", children=[
                    html.Span("settings", className="material-symbols-outlined")
                ])
            ])
        ])
    ])
])

# ----------------- LAYOUT PRINCIPAL -----------------
app.layout = html.Div(className="font-body-md text-body-md text-on-background min-h-screen flex", children=[
    sidebar,
    html.Div(className="flex-1 ml-[280px] flex flex-col min-w-0 h-screen overflow-hidden", children=[
        topbar,
        dash.page_container 
    ])
])

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=7860, debug=True)
