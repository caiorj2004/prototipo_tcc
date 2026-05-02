import dash
from dash import html, dcc

# Configuração de scripts e fontes externas
external_scripts = [{"src": "https://cdn.tailwindcss.com?plugins=forms,container-queries"}]
external_stylesheets = [
    "https://fonts.googleapis.com/css2?family=Public+Sans:wght@400;500;600;700&display=swap",
    "https://fonts.googleapis.com/css2?family=Material+Symbols+Outlined:wght,FILL@100..700,0..1&display=swap"
]

app = dash.Dash(__name__, external_scripts=external_scripts, external_stylesheets=external_stylesheets)

# Customização do HTML base para injetar as configurações do Tailwind e o background global
app.index_string = '''
<!DOCTYPE html>
<html lang="pt-BR" class="light">
    <head>
        {%metas%}
        <title>AgriSteward - Dashboard Geral</title>
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
                },
                "fontSize": {
                  "h1": ["2.5rem", {"lineHeight": "1.2", "letterSpacing": "-0.02em", "fontWeight": "700"}],
                  "data-tabular": ["0.9375rem", {"lineHeight": "1.4", "letterSpacing": "0", "fontWeight": "500"}],
                  "h3": ["1.5rem", {"lineHeight": "1.4", "letterSpacing": "0", "fontWeight": "600"}],
                  "body-lg": ["1.125rem", {"lineHeight": "1.6", "letterSpacing": "0", "fontWeight": "400"}],
                  "body-md": ["1rem", {"lineHeight": "1.5", "letterSpacing": "0", "fontWeight": "400"}],
                  "h2": ["1.875rem", {"lineHeight": "1.3", "letterSpacing": "-0.01em", "fontWeight": "600"}],
                  "label-sm": ["0.875rem", {"lineHeight": "1.2", "letterSpacing": "0.05em", "fontWeight": "600"}]
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

# Componente da Barra Lateral (Sidebar)
sidebar = html.Aside(className="fixed left-0 top-0 h-full w-[280px] bg-emerald-900 dark:bg-emerald-950 border-r border-emerald-800 shadow-xl dark:shadow-none flex flex-col py-6 z-50", children=[
    html.Div(className="px-6 mb-8 flex items-center gap-4", children=[
        html.Div(className="w-10 h-10 rounded-lg bg-surface-container-lowest flex items-center justify-center overflow-hidden", children=[
            html.Img(src="https://lh3.googleusercontent.com/aida-public/AB6AXuD-Krp1h-nZuElAjxteizE1E2QVreLPf3KjwXTftrsqjJpSWSec_o77vrFuzu_9llYlOFlQyNeVYUeyVyHDfIy-Oe_NKovbfaqzckCmTzJzIrgr9Xqr0h-zjAdHnje5XY1RxvuZ9fn4EeZhhqd9YKUYEtGf6s-2SHhhCvIzr0dx_7VeLT6VuCGd-I5prfHoygAAj6ODDRzxf5v1N3M7yPQCV8qihKmiWzSVNvkJzRMml32ZeQ4oTomjskCvITrDM7GmWA858oPXCxw", className="w-full h-full object-cover")
        ]),
        html.Div([
            html.H2("Stewardship Portal", className="text-white font-bold text-lg leading-tight tracking-tight"),
            html.P("Family Heritage Data", className="font-public-sans text-sm font-medium text-emerald-100/70")
        ])
    ]),
    html.Nav(className="flex-1 flex flex-col gap-1 px-2", children=[
        html.A(className="bg-emerald-800 text-white border-l-4 border-orange-600 px-4 py-3 flex items-center gap-3 font-public-sans text-sm font-medium translate-x-1 transition-transform", href="#", children=[
            html.Span("dashboard", className="material-symbols-outlined", style={'fontVariationSettings': "'FILL' 1"}),
            "General Overview"
        ]),
        html.A(className="text-emerald-100/70 hover:text-white px-4 py-3 flex items-center gap-3 font-public-sans text-sm font-medium hover:bg-emerald-800/50 transition-all", href="#", children=[
            html.Span("landscape", className="material-symbols-outlined"),
            "Farm Profile"
        ]),
        html.A(className="text-emerald-100/70 hover:text-white px-4 py-3 flex items-center gap-3 font-public-sans text-sm font-medium hover:bg-emerald-800/50 transition-all", href="#", children=[
            html.Span("trending_up", className="material-symbols-outlined"),
            "Market Prices"
        ]),
        html.A(className="text-emerald-100/70 hover:text-white px-4 py-3 flex items-center gap-3 font-public-sans text-sm font-medium hover:bg-emerald-800/50 transition-all", href="#", children=[
            html.Span("assignment", className="material-symbols-outlined"),
            "Registries"
        ])
    ]),
    html.Div(className="px-6 mt-auto flex flex-col gap-4", children=[
        html.Button(className="w-full border border-secondary text-secondary hover:bg-secondary/10 transition-colors rounded-lg py-2 font-label-sm text-label-sm flex items-center justify-center gap-2", children=[
            html.Span("download", className="material-symbols-outlined text-[18px]"),
            "Export Report"
        ]),
        html.Div(className="flex flex-col gap-1 mt-4", children=[
            html.A(className="text-emerald-100/70 hover:text-white py-2 flex items-center gap-3 font-public-sans text-sm font-medium hover:bg-emerald-800/50 transition-all px-2 rounded", href="#", children=[
                html.Span("help", className="material-symbols-outlined"),
                "Help Center"
            ]),
            html.A(className="text-emerald-100/70 hover:text-white py-2 flex items-center gap-3 font-public-sans text-sm font-medium hover:bg-emerald-800/50 transition-all px-2 rounded", href="#", children=[
                html.Span("logout", className="material-symbols-outlined"),
                "Logout"
            ])
        ])
    ])
])

# Componente do Cabeçalho Superior
topbar = html.Header(className="bg-white dark:bg-slate-900 border-b border-slate-200 dark:border-slate-800 w-full z-40 sticky top-0", children=[
    html.Div(className="flex justify-between items-center w-full px-8 py-3", children=[
        html.Div(className="flex items-center gap-4", children=[
            html.Span("AgriSteward", className="text-xl font-bold text-emerald-900 dark:text-emerald-400 font-public-sans tracking-tight")
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
            ]),
            html.Div(className="w-9 h-9 rounded-full bg-surface-variant overflow-hidden cursor-pointer border border-outline-variant", children=[
                html.Img(src="https://lh3.googleusercontent.com/aida-public/AB6AXuBu323VhDRrGc7LVawcDIuk35GKHDNj6hRMVt1ES9TRIIst2yshrTXQfqL6KbckeTq1com_TChxLAMMRwn1zfTbLKHpzE6zkHrmiJH9lN9BXm-VCR1Vb4KEFY3kbThbuy-31k3YtQAgyu_0TEmxIYANrwch3JbJsHnz6LkXGmYfSv_AXftgRCbzE7DX4FGg8TX9xfSqSCh33rcBiDN5SxQuLEAPNNgDVMq6mDPAfu1mWodhBBcOAvow_fuL1ZBBg3wEqgNsnB2EIoA", className="w-full h-full object-cover")
            ])
        ])
    ])
])

# Componentes de KPIs
kpi_1 = html.Div(className="bg-surface-container-lowest border border-outline-variant rounded-xl p-card-padding flex flex-col relative overflow-hidden group", children=[
    html.Div(className="flex justify-between items-start mb-4 relative z-10", children=[
        html.H3("Estabelecimentos Familiares", className="font-label-sm text-label-sm text-on-surface-variant uppercase tracking-wider"),
        html.Div(className="w-8 h-8 rounded-full bg-tertiary-fixed flex items-center justify-center text-tertiary-container", children=[
            html.Span("real_estate_agent", className="material-symbols-outlined text-[18px]")
        ])
    ]),
    html.Div(className="relative z-10 flex items-baseline gap-3", children=[
        html.Span("3.8M", className="font-h2 text-h2 text-primary"),
        html.Span(className="flex items-center text-sm font-medium text-[#166534] bg-[#dcfce7] px-2 py-0.5 rounded", children=[
            html.Span("arrow_upward", className="material-symbols-outlined text-[14px]"), " 2.4%"
        ])
    ]),
    html.P("Total de propriedades ativas no ciclo", className="font-data-tabular text-data-tabular text-outline mt-1 relative z-10"),
    html.Div(className="absolute -right-6 -bottom-6 opacity-[0.03] text-primary transition-transform group-hover:scale-110 duration-500", children=[
        html.Span("landscape", className="material-symbols-outlined text-[120px]", style={'fontVariationSettings': "'FILL' 1"})
    ])
])

kpi_2 = html.Div(className="bg-surface-container-lowest border border-outline-variant rounded-xl p-card-padding flex flex-col relative overflow-hidden group", children=[
    html.Div(className="flex justify-between items-start mb-4 relative z-10", children=[
        html.H3("Área Total Ocupada (ha)", className="font-label-sm text-label-sm text-on-surface-variant uppercase tracking-wider"),
        html.Div(className="w-8 h-8 rounded-full bg-secondary-fixed flex items-center justify-center text-on-secondary-container", children=[
            html.Span("aspect_ratio", className="material-symbols-outlined text-[18px]")
        ])
    ]),
    html.Div(className="relative z-10 flex items-baseline gap-3", children=[
        html.Span("80.9M", className="font-h2 text-h2 text-primary"),
        html.Span(className="flex items-center text-sm font-medium text-outline bg-surface-container py-0.5 px-2 rounded", children=[
            html.Span("horizontal_rule", className="material-symbols-outlined text-[14px]"), " 0.0%"
        ])
    ]),
    html.P("Hectares dedicados à produção", className="font-data-tabular text-data-tabular text-outline mt-1 relative z-10"),
    html.Div(className="absolute -right-6 -bottom-6 opacity-[0.03] text-primary transition-transform group-hover:scale-110 duration-500", children=[
        html.Span("grid_on", className="material-symbols-outlined text-[120px]", style={'fontVariationSettings': "'FILL' 1"})
    ])
])

kpi_3 = html.Div(className="bg-surface-container-lowest border border-outline-variant rounded-xl p-card-padding flex flex-col relative overflow-hidden group", children=[
    html.Div(className="flex justify-between items-start mb-4 relative z-10", children=[
        html.H3("Valor Bruto de Produção", className="font-label-sm text-label-sm text-on-surface-variant uppercase tracking-wider"),
        html.Div(className="w-8 h-8 rounded-full bg-primary-fixed flex items-center justify-center text-primary-container", children=[
            html.Span("payments", className="material-symbols-outlined text-[18px]")
        ])
    ]),
    html.Div(className="relative z-10 flex items-baseline gap-3", children=[
        html.Span("R$ 106.5B", className="font-h2 text-h2 text-primary"),
        html.Span(className="flex items-center text-sm font-medium text-[#166534] bg-[#dcfce7] px-2 py-0.5 rounded", children=[
            html.Span("arrow_upward", className="material-symbols-outlined text-[14px]"), " 8.1%"
        ])
    ]),
    html.P("Estimativa anualizada (BRL)", className="font-data-tabular text-data-tabular text-outline mt-1 relative z-10"),
    html.Div(className="absolute -right-6 -bottom-6 opacity-[0.03] text-primary transition-transform group-hover:scale-110 duration-500", children=[
        html.Span("monitoring", className="material-symbols-outlined text-[120px]", style={'fontVariationSettings': "'FILL' 1"})
    ])
])

# Layout Principal
app.layout = html.Div(className="flex-1 ml-[280px] flex flex-col min-w-0 h-screen overflow-hidden", children=[
    sidebar,
    topbar,
    html.Main(className="flex-1 overflow-y-auto p-container-margin bg-background", children=[
        # Cabeçalho da Página
        html.Div(className="mb-8 flex items-end justify-between", children=[
            html.Div([
                html.H1("Dashboard Geral", className="font-h1 text-h1 text-primary"),
                html.P("Visão consolidada do agronegócio familiar e indicadores de performance.", className="font-body-lg text-body-lg text-on-surface-variant mt-2")
            ]),
            html.Div(className="flex items-center gap-2 text-sm text-on-surface-variant font-data-tabular", children=[
                html.Span("calendar_today", className="material-symbols-outlined text-[18px]"),
                html.Span("Atualizado hoje, 08:30 BRT")
            ])
        ]),
        
        # Grid de KPIs
        html.Div(className="grid grid-cols-1 md:grid-cols-3 gap-gutter mb-gutter", children=[kpi_1, kpi_2, kpi_3]),
        
        # Grid de Gráficos com os placeholders estruturados para receberem os dcc.Graph do Plotly
        html.Div(className="grid grid-cols-1 xl:grid-cols-12 gap-gutter pb-12", children=[
            # Gráfico de Mapa (Heatmap)
            html.Div(className="xl:col-span-7 bg-surface-container-lowest border border-outline-variant rounded-xl flex flex-col relative", children=[
                html.Div(className="p-card-padding border-b border-surface-variant flex justify-between items-center", children=[
                    html.Div([
                        html.H2("Distribuição de Produtores", className="font-h3 text-h3 text-primary"),
                        html.P("Mapa de calor da densidade de unidades produtivas pelo Brasil.", className="font-data-tabular text-data-tabular text-on-surface-variant mt-1")
                    ]),
                    html.Button(html.Span("more_vert", className="material-symbols-outlined"), className="text-outline hover:text-primary transition-colors")
                ]),
                html.Div(className="p-card-padding flex-1 min-h-[400px] flex items-center justify-center relative bg-surface-container-low/30", children=[
                    dcc.Graph(id='mapa-distribuicao', style={'height': '100%', 'width': '100%'})
                ])
            ]),
            
            # Gráfico de Barras
            html.Div(className="xl:col-span-5 bg-surface-container-lowest border border-outline-variant rounded-xl flex flex-col relative", children=[
                html.Div(className="p-card-padding border-b border-surface-variant flex justify-between items-center", children=[
                    html.Div([
                        html.H2("Produção por Região", className="font-h3 text-h3 text-primary"),
                        html.P("Comparativo de volume (toneladas) nas 5 macrorregiões.", className="font-data-tabular text-data-tabular text-on-surface-variant mt-1")
                    ]),
                    html.Button(html.Span("filter_list", className="material-symbols-outlined"), className="text-outline hover:text-primary transition-colors")
                ]),
                html.Div(className="p-card-padding flex-1 min-h-[400px] flex flex-col justify-end relative bg-surface-container-low/30", children=[
                    dcc.Graph(id='grafico-producao-regiao', style={'height': '100%', 'width': '100%'})
                ])
            ])
        ])
    ])
])

if __name__ == '__main__':
    # host='0.0.0.0' permite que a nuvem acesse o app, e port=7860 é a porta do HF
    app.run(host='0.0.0.0', port=7860, debug=False)
