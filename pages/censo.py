import dash
from dash import html, dcc, callback, Input, Output
import plotly.graph_objects as go
import pandas as pd
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from data_pipeline_censo import load_censo_data

# Registra esta página na rota raiz (Página Inicial)
dash.register_page(__name__, path='/', name='Censo Agro 2017')

# Carregar os dados reais
dados_censo = load_censo_data()

# Obter lista de Ramos
ramos = list(set([v['ramo'] for v in dados_censo.values() if v['ramo'] != 'Geral']))
ramos.sort()

# Cores do Tailwind config para o Plotly
cores_raca = {
    'Branca': '#1b4332',      # primary-container
    'Parda': '#fe9974',       # secondary-container
    'Preta': '#00405e',       # tertiary-container
    'Amarela': '#ffdbcf',     # secondary-fixed
    'Indígena': '#a5d0b9',    # primary-fixed-dim
    'Não se aplica': '#e1e3e2'# surface-variant
}

layout = html.Div(className="w-full p-6 md:p-8 bg-background", children=[
    
    # Page Header
    html.Div(className="mb-8 flex items-end justify-between", children=[
        html.Div([
            html.H1("Censo Agropecuário 2017", className="font-h1 text-h1 text-primary"),
            html.P("Análise demográfica e socioeconômica dos estabelecimentos por cor ou raça.", className="font-body-lg text-body-lg text-on-surface-variant mt-2")
        ]),
        html.Div(className="flex items-center gap-2 text-sm text-on-surface-variant font-data-tabular", children=[
            html.Span("calendar_today", className="material-symbols-outlined text-[18px]"),
            html.Span("Fonte: IBGE/Censo Agro 2017 (DF)")
        ])
    ]),
    
    # Controles de Filtro (Para respeitar a regra de não agregação indevida)
    html.Div(className="w-full bg-surface-container-lowest border border-outline-variant rounded-xl p-card-padding mb-8 flex flex-col md:flex-row gap-8", children=[
        html.Div(className="flex-1", children=[
            html.Label("Selecione o Ramo:", className="block font-label-sm text-label-sm text-on-surface-variant mb-2 uppercase tracking-wider"),
            dcc.Dropdown(
                id='dropdown-ramo-censo',
                options=[{'label': r, 'value': r} for r in ramos],
                value='Horticultura' if 'Horticultura' in ramos else ramos[0] if ramos else None,
                clearable=False,
                className="font-public-sans text-sm"
            )
        ]),
        html.Div(className="flex-1", children=[
            html.Label("Selecione o Produto:", className="block font-label-sm text-label-sm text-on-surface-variant mb-2 uppercase tracking-wider"),
            dcc.Dropdown(
                id='dropdown-produto-censo',
                clearable=False,
                className="font-public-sans text-sm"
            )
        ])
    ]),
    
    # Data Grid
    html.Div(className="w-full mb-6", children=[
        
        # 1. Distribution of establishments by color/race
        html.Div(className="w-full bg-surface-container-lowest border border-outline-variant rounded-xl flex flex-col relative overflow-hidden", children=[
            html.Div(className="p-card-padding border-b border-surface-variant flex justify-between items-center", children=[
                html.Div([
                    html.H2("Distribuição de Estabelecimentos por Cor ou Raça", className="font-h3 text-h3 text-primary"),
                    html.P("Frequência absoluta de produtores para o produto selecionado.", className="font-data-tabular text-data-tabular text-on-surface-variant mt-1")
                ]),
                html.Div(className="flex gap-2", children=[
                    html.Button("Distrito Federal", className="px-3 py-1 text-xs font-label-sm border border-outline-variant rounded-lg bg-surface-container-low transition-colors cursor-default"),
                    html.Button(html.Span("more_vert", className="material-symbols-outlined"), className="text-outline hover:text-primary transition-colors")
                ])
            ]),
            html.Div(className="p-card-padding grid grid-cols-1 md:grid-cols-2 gap-8", children=[
                html.Div(className="min-h-[300px] flex items-center justify-center relative bg-surface-container-low/30 rounded-lg", children=[
                    dcc.Graph(id='censo-distribuicao-raca', style={'height': '100%', 'width': '100%'})
                ]),
                html.Div(className="flex flex-col justify-center gap-4", children=[
                    html.Div(className="space-y-4", children=[
                        html.Div(className="flex items-center justify-between", children=[
                            html.Div(className="flex items-center gap-2", children=[html.Div(className="w-3 h-3 rounded-full bg-primary-container"), html.Span("Branca", className="font-body-md text-on-surface")]),
                            html.Span("-", id='val-branca', className="font-data-tabular font-bold text-primary")
                        ]),
                        html.Div(className="flex items-center justify-between", children=[
                            html.Div(className="flex items-center gap-2", children=[html.Div(className="w-3 h-3 rounded-full bg-secondary-container"), html.Span("Parda", className="font-body-md text-on-surface")]),
                            html.Span("-", id='val-parda', className="font-data-tabular font-bold text-primary")
                        ]),
                        html.Div(className="flex items-center justify-between", children=[
                            html.Div(className="flex items-center gap-2", children=[html.Div(className="w-3 h-3 rounded-full bg-tertiary-container"), html.Span("Preta", className="font-body-md text-on-surface")]),
                            html.Span("-", id='val-preta', className="font-data-tabular font-bold text-primary")
                        ]),
                        html.Div(className="flex items-center justify-between", children=[
                            html.Div(className="flex items-center gap-2", children=[
                                html.Div(className="w-3 h-3 rounded-full", style={'backgroundColor': cores_raca['Amarela']}), 
                                html.Span("Outras (Amarela/Indígena)", className="font-body-md text-on-surface")
                            ]),
                            html.Span("-", id='val-outras', className="font-data-tabular font-bold text-primary")
                        ])
                    ])
                ])
            ])
        ])
    ]),
    
    # Seção Inferior (Tabela e Gráfico de Barras)
    html.Div(className="grid grid-cols-1 xl:grid-cols-2 gap-6 w-full pb-12", children=[
        
        # 2. Value of production by color/race (Table/Comparison)
        html.Div(className="w-full bg-surface-container-lowest border border-outline-variant rounded-xl flex flex-col relative overflow-hidden", children=[
            html.Div(className="p-card-padding border-b border-surface-variant flex justify-between items-center", children=[
                html.Div([
                    html.H2("Valor de Produção por Cor ou Raça", className="font-h3 text-h3 text-primary"),
                    html.P("Comparativo entre o Somatório Total e a Média por estabelecimento.", className="font-data-tabular text-data-tabular text-on-surface-variant mt-1")
                ]),
                html.Button(html.Span("filter_alt", className="material-symbols-outlined"), className="text-outline hover:text-primary transition-colors")
            ]),
            html.Div(className="overflow-x-auto", children=[
                html.Table(className="w-full text-left border-collapse", children=[
                    html.Thead(html.Tr(className="bg-surface-container-low border-b border-outline-variant", children=[
                        html.Th("Cor ou Raça", className="p-4 font-label-sm text-on-surface-variant uppercase tracking-wider"),
                        html.Th("Soma (R$)", className="p-4 font-label-sm text-on-surface-variant uppercase tracking-wider text-right"),
                        html.Th("Média (R$)", className="p-4 font-label-sm text-on-surface-variant uppercase tracking-wider text-right")
                    ])),
                    html.Tbody(id='tabela-valor-producao', className="divide-y divide-outline-variant", children=[])
                ])
            ])
        ]),
        
        # 3. Quantity produced by color/race (Chart)
        html.Div(className="w-full bg-surface-container-lowest border border-outline-variant rounded-xl flex flex-col relative overflow-hidden", children=[
            html.Div(className="p-card-padding border-b border-surface-variant flex justify-between items-center", children=[
                html.Div([
                    html.H2("Quantidade Produzida", className="font-h3 text-h3 text-primary"),
                    html.P("Volume de produção física estimada por grupo (Kg).", className="font-data-tabular text-data-tabular text-on-surface-variant mt-1")
                ]),
                html.Button(html.Span("analytics", className="material-symbols-outlined"), className="text-outline hover:text-primary transition-colors")
            ]),
            html.Div(className="p-card-padding flex-1 min-h-[300px] flex flex-col justify-end relative bg-surface-container-low/30", children=[
                dcc.Graph(id='censo-quantidade-raca', style={'height': '100%', 'width': '100%'})
            ])
        ])
    ])
])

# Helpers
def get_row_for_product(tipo, ramo, produto):
    chave = f"{tipo} | {ramo}"
    if chave in dados_censo:
        df = dados_censo[chave]['df']
        linha = df[df['Produto'] == produto]
        if not linha.empty:
            return linha.iloc[0]
    return None

# Callbacks
@callback(
    Output('dropdown-produto-censo', 'options'),
    Output('dropdown-produto-censo', 'value'),
    Input('dropdown-ramo-censo', 'value')
)
def update_produtos(ramo):
    if not ramo:
        return [], None
    produtos = set()
    for k, v in dados_censo.items():
        if v['ramo'] == ramo:
            produtos.update(v['df']['Produto'].dropna().tolist())
            
    lista_produtos = sorted(list(produtos))
    valor_padrao = lista_produtos[0] if lista_produtos else None
    return [{'label': p, 'value': p} for p in lista_produtos], valor_padrao

@callback(
    Output('censo-distribuicao-raca', 'figure'),
    Output('val-branca', 'children'),
    Output('val-parda', 'children'),
    Output('val-preta', 'children'),
    Output('val-outras', 'children'),
    Output('tabela-valor-producao', 'children'),
    Output('censo-quantidade-raca', 'figure'),
    Input('dropdown-ramo-censo', 'value'),
    Input('dropdown-produto-censo', 'value')
)
def update_censo_dashboard(ramo, produto):
    if not ramo or not produto:
        return go.Figure(), "-", "-", "-", "-", [], go.Figure()
        
    cols_raca = ['Branca', 'Preta', 'Amarela', 'Parda', 'Indígena']
    
    row_est = get_row_for_product('Qtd Estabelecimentos', ramo, produto)
    row_kg = get_row_for_product('Qtd Kg', ramo, produto)
    row_vs = get_row_for_product('Valor Soma', ramo, produto)
    row_vm = get_row_for_product('Valor Média', ramo, produto)
    
    # 1. Indicadores de Estabelecimentos
    v_branca = v_parda = v_preta = v_outras = 0
    total_est = 0
    
    if row_est is not None:
        v_branca = row_est.get('Branca', 0)
        v_parda = row_est.get('Parda', 0)
        v_preta = row_est.get('Preta', 0)
        v_outras = row_est.get('Amarela', 0) + row_est.get('Indígena', 0)
        total_est = sum([row_est.get(c, 0) for c in cols_raca])
    
    def formata_perc(valor, total):
        if total == 0: return "0 (0%)"
        perc = (valor / total) * 100
        return f"{int(valor)} ({perc:.1f}%)".replace('.', ',')
        
    str_branca = formata_perc(v_branca, total_est)
    str_parda = formata_perc(v_parda, total_est)
    str_preta = formata_perc(v_preta, total_est)
    str_outras = formata_perc(v_outras, total_est)

    # Gráfico de Rosca
    fig_rosca = go.Figure()
    if total_est > 0:
        labels = ['Branca', 'Parda', 'Preta', 'Outras']
        values = [v_branca, v_parda, v_preta, v_outras]
        
        # Filtra > 0
        l_filt = [l for l, v in zip(labels, values) if v > 0]
        v_filt = [v for v in values if v > 0]
        c_filt = [cores_raca.get(l.split()[0], '#000') if l != 'Outras' else cores_raca['Amarela'] for l in l_filt]
        
        fig_rosca.add_trace(go.Pie(
            labels=l_filt,
            values=v_filt,
            hole=0.6,
            marker=dict(colors=c_filt),
            textinfo='label+percent',
            hoverinfo='label+value'
        ))
        
    fig_rosca.update_layout(margin=dict(t=10, b=10, l=10, r=10), showlegend=False, paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)')

    # 2. Tabela de Valor de Produção
    linhas_tabela = []
    for raca in cols_raca:
        vs = row_vs.get(raca, 0) if row_vs is not None else 0
        vm = row_vm.get(raca, 0) if row_vm is not None else 0
        
        # Mostra na tabela se tiver qualquer valor
        if vs > 0 or vm > 0:
            linhas_tabela.append(
                html.Tr(className="hover:bg-surface-container-low/50 transition-colors", children=[
                    html.Td(raca, className="p-4 font-medium text-primary"),
                    html.Td(f"{vs:,.2f}".replace(",", "X").replace(".", ",").replace("X", "."), className="p-4 text-right font-data-tabular"),
                    html.Td(f"{vm:,.2f}".replace(",", "X").replace(".", ",").replace("X", "."), className="p-4 text-right font-data-tabular")
                ])
            )
            
    if not linhas_tabela:
        linhas_tabela.append(
            html.Tr(children=[html.Td("Sem dados", colSpan=3, className="p-4 text-center text-outline")])
        )

    # 3. Gráfico de Barras (Quantidade em Kg)
    fig_barras = go.Figure()
    if row_kg is not None:
        valores_kg = [row_kg.get(c, 0) for c in cols_raca]
        
        fig_barras.add_trace(go.Bar(
            x=cols_raca,
            y=valores_kg,
            marker_color=[cores_raca.get(c, '#000') for c in cols_raca],
            text=[f"{v:,.0f}".replace(",", ".") if v > 0 else "" for v in valores_kg],
            textposition='auto'
        ))
        
    fig_barras.update_layout(
        margin=dict(t=10, b=10, l=10, r=10),
        xaxis_title="Cor ou Raça",
        yaxis_title="Kg",
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        showlegend=False
    )
    
    return fig_rosca, str_branca, str_parda, str_preta, str_outras, linhas_tabela, fig_barras