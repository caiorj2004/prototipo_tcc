import dash
from dash import html, dcc, callback, Input, Output
import plotly.graph_objects as go
import plotly.express as px
import pandas as pd
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from data_pipeline_censo import load_censo_data

# Registra esta página na rota raiz (Página Inicial)
dash.register_page(__name__, path='/', name='Censo Agro 2017')

# Carregar os dados reais
dados_censo = load_censo_data()

# Helpers para gráficos estáticos
def get_df(tipo):
    chave = f"{tipo} | Geral"
    if chave in dados_censo:
        return dados_censo[chave]['df']
    return pd.DataFrame()

# Construção dos gráficos estáticos macro
# 1. Uso da Terra
df_terra_geral = get_df('Terra - Geral')
fig_terra_geral = go.Figure()
if not df_terra_geral.empty:
    fig_terra_geral.add_trace(go.Pie(labels=df_terra_geral.iloc[:,0], values=df_terra_geral.iloc[:,1], marker=dict(colors=['#283618', '#606c38', '#bc6c25']), hole=0.4))
fig_terra_geral.update_layout(margin=dict(t=10, b=10, l=10, r=10), showlegend=True, paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)')

df_terra_matas = get_df('Terra - Matas')
fig_terra_matas = go.Figure()
if not df_terra_matas.empty:
    fig_terra_matas.add_trace(go.Bar(x=df_terra_matas.iloc[:,0], y=df_terra_matas.iloc[:,1], marker_color='#606c38'))
fig_terra_matas.update_layout(margin=dict(t=10, b=10, l=10, r=10), xaxis={'visible': False}, showlegend=False, paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)')

df_terra_past = get_df('Terra - Pastagem')
fig_terra_past = go.Figure()
if not df_terra_past.empty:
    fig_terra_past.add_trace(go.Bar(x=df_terra_past.iloc[:,0], y=df_terra_past.iloc[:,1], marker_color='#dda15e'))
fig_terra_past.update_layout(margin=dict(t=10, b=10, l=10, r=10), xaxis={'visible': False}, showlegend=False, paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)')

df_terra_lav = get_df('Terra - Lavoura')
fig_terra_lav = go.Figure()
if not df_terra_lav.empty:
    fig_terra_lav.add_trace(go.Bar(x=df_terra_lav.iloc[:,0], y=df_terra_lav.iloc[:,1], marker_color='#bc6c25'))
fig_terra_lav.update_layout(margin=dict(t=10, b=10, l=10, r=10), xaxis={'visible': False}, showlegend=False, paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)')

# 2. Mecanização
df_maq_qtd = get_df('Máquinas - Qtd')
fig_maq_qtd = go.Figure()
if not df_maq_qtd.empty:
    fig_maq_qtd = px.treemap(df_maq_qtd, path=[df_maq_qtd.columns[0]], values=df_maq_qtd.columns[1], color_discrete_sequence=['#495057', '#6c757d', '#adb5bd', '#f77f00', '#fcbf49'])
    fig_maq_qtd.update_layout(margin=dict(t=10, b=10, l=10, r=10), paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)')

df_maq_estabs = get_df('Máquinas - Estabs')
fig_maq_estabs = go.Figure()
if not df_maq_estabs.empty:
    fig_maq_estabs.add_trace(go.Bar(y=df_maq_estabs.iloc[:,0], x=df_maq_estabs.iloc[:,1], orientation='h', marker_color='#f77f00'))
fig_maq_estabs.update_layout(margin=dict(t=10, b=10, l=10, r=10), yaxis={'autorange': 'reversed'}, showlegend=False, paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)')

# 3. Financiamento
df_fin_obt = get_df('Financiamento - Obtencao')
fig_fin_obt = go.Figure()
if not df_fin_obt.empty:
    fig_fin_obt.add_trace(go.Pie(labels=df_fin_obt.iloc[:,0], values=df_fin_obt.iloc[:,1], hole=0.5, marker=dict(colors=['#1b4965', '#cae9ff'])))
fig_fin_obt.update_layout(margin=dict(t=10, b=10, l=10, r=10), paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)')

df_fin_gov = get_df('Financiamento - Governo')
fig_fin_gov = go.Figure()
if not df_fin_gov.empty:
    fig_fin_gov.add_trace(go.Pie(labels=df_fin_gov.iloc[:,0], values=df_fin_gov.iloc[:,1], hole=0.5, marker=dict(colors=['#62b6cb', '#5fa8d3'])))
fig_fin_gov.update_layout(margin=dict(t=10, b=10, l=10, r=10), paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)')

df_fin_fin = get_df('Financiamento - Finalidade')
fig_fin_fin = go.Figure()
if not df_fin_fin.empty:
    fig_fin_fin.add_trace(go.Bar(x=df_fin_fin.iloc[:,0], y=df_fin_fin.iloc[:,1], marker_color='#1b4965'))
fig_fin_fin.update_layout(margin=dict(t=10, b=10, l=10, r=10), showlegend=False, paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)')

# 4. Sociodemográfico e Mão de Obra
# Perfil - Sexo
df_perfil_sexo = get_df('Perfil - Sexo')
fig_perfil_sexo = go.Figure()
if not df_perfil_sexo.empty:
    fig_perfil_sexo.add_trace(go.Pie(labels=df_perfil_sexo.iloc[:,0], values=df_perfil_sexo.iloc[:,1], marker=dict(colors=['#5a189a', '#9d4edd']), hole=0.5))
fig_perfil_sexo.update_layout(margin=dict(t=10, b=10, l=10, r=10), paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)')

# Perfil - Idade Sexo (Pirâmide Etária)
df_perfil_idade = get_df('Perfil - Idade Sexo')
fig_perfil_idade = go.Figure()
if not df_perfil_idade.empty:
    y_age = df_perfil_idade.iloc[:,0]
    x_women = df_perfil_idade.iloc[:,1]
    x_men = df_perfil_idade.iloc[:,2] * -1  # Invert men for pyramid
    
    max_val = int(max(x_women.max() if not x_women.empty else 0, abs(x_men.min() if not x_men.empty else 0)))
    if max_val > 0:
        tickvals = [-max_val, -max_val//2, 0, max_val//2, max_val]
        ticktext = [str(abs(v)) for v in tickvals]
    else:
        tickvals = None
        ticktext = None

    fig_perfil_idade.add_trace(go.Bar(y=y_age, x=x_men, name='Homens', orientation='h', marker_color='#3c096c'))
    fig_perfil_idade.add_trace(go.Bar(y=y_age, x=x_women, name='Mulheres', orientation='h', marker_color='#c77dff'))
    fig_perfil_idade.update_layout(
        barmode='relative',
        margin=dict(t=10, b=10, l=10, r=10),
        xaxis=dict(tickvals=tickvals, ticktext=ticktext, title='Valores Absolutos'),
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        showlegend=True,
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
    )

# Perfil - Escolaridade
df_escolaridade = get_df('Perfil - Escolaridade')
fig_escolaridade = go.Figure()
if not df_escolaridade.empty:
    df_escolaridade = df_escolaridade.sort_values(by=df_escolaridade.columns[1], ascending=True)
    fig_escolaridade.add_trace(go.Bar(y=df_escolaridade.iloc[:,0], x=df_escolaridade.iloc[:,1], orientation='h', marker_color='#7b2cbf'))
fig_escolaridade.update_layout(margin=dict(t=10, b=10, l=10, r=10), paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)')

# Mão de Obra - Sem Parentesco
df_mo_sem = get_df('Mão de Obra - Sem Parentesco')
fig_mo_sem = go.Figure()
if not df_mo_sem.empty:
    fig_mo_sem.add_trace(go.Pie(labels=df_mo_sem.iloc[:,0], values=df_mo_sem.iloc[:,1], hole=0.5, marker=dict(colors=['#ff9e00', '#ff6d00', '#e85d04'])))
fig_mo_sem.update_layout(margin=dict(t=10, b=10, l=10, r=10), paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)')

# Mão de Obra - Parentesco
df_mo_com = get_df('Mão de Obra - Parentesco')
fig_mo_com = go.Figure()
if not df_mo_com.empty:
    fig_mo_com.add_trace(go.Bar(x=df_mo_com.iloc[:,0], y=df_mo_com.iloc[:,2], name='Homens', marker_color='#3c096c'))
    fig_mo_com.add_trace(go.Bar(x=df_mo_com.iloc[:,0], y=df_mo_com.iloc[:,1], name='Mulheres', marker_color='#c77dff'))
fig_mo_com.update_layout(barmode='group', margin=dict(t=10, b=10, l=10, r=10), paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', showlegend=True, legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1))

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
    ]),
    
    # === AVISO DE DADOS MACRO ===
    html.Div(className="w-full mt-12 mb-6 border-t border-outline-variant pt-8", children=[
        html.Div(className="flex items-center gap-3 bg-surface-container-low p-4 rounded-xl border border-outline-variant", children=[
            html.Span("info", className="material-symbols-outlined text-primary"),
            html.Div([
                html.H3("Dados Macroestruturais do Distrito Federal", className="font-label-lg text-on-surface"),
                html.P("Os gráficos abaixo apresentam totais estaduais (Uso da Terra, Mecanização e Financiamento) e não sofrem influência dos filtros de Ramo/Produto acima.", className="text-sm text-on-surface-variant")
            ])
        ])
    ]),

    # === SEÇÃO: USO DA TERRA ===
    html.Div(className="w-full mb-8", children=[
        html.H2("Uso da Terra", className="font-h3 text-h3 text-primary mb-4"),
        html.Div(className="grid grid-cols-1 xl:grid-cols-2 gap-6 w-full", children=[
            # Pie Chart
            html.Div(className="bg-surface-container-lowest border border-outline-variant rounded-xl p-card-padding flex flex-col", children=[
                html.H3("Distribuição em Hectares", className="font-label-lg text-on-surface mb-2"),
                html.Div(className="flex-1 min-h-[300px]", children=[
                    dcc.Graph(figure=fig_terra_geral, style={'height': '100%', 'width': '100%'})
                ])
            ]),
            # Bar charts grid
            html.Div(className="grid grid-cols-1 md:grid-cols-3 gap-4", children=[
                html.Div(className="bg-surface-container-lowest border border-outline-variant rounded-xl p-4 flex flex-col", children=[
                    html.H3("Matas ou Florestas", className="font-label-md text-on-surface mb-2 text-center"),
                    html.Div(className="flex-1 min-h-[200px]", children=[
                        dcc.Graph(figure=fig_terra_matas, style={'height': '100%', 'width': '100%'})
                    ])
                ]),
                html.Div(className="bg-surface-container-lowest border border-outline-variant rounded-xl p-4 flex flex-col", children=[
                    html.H3("Pastagens", className="font-label-md text-on-surface mb-2 text-center"),
                    html.Div(className="flex-1 min-h-[200px]", children=[
                        dcc.Graph(figure=fig_terra_past, style={'height': '100%', 'width': '100%'})
                    ])
                ]),
                html.Div(className="bg-surface-container-lowest border border-outline-variant rounded-xl p-4 flex flex-col", children=[
                    html.H3("Lavouras", className="font-label-md text-on-surface mb-2 text-center"),
                    html.Div(className="flex-1 min-h-[200px]", children=[
                        dcc.Graph(figure=fig_terra_lav, style={'height': '100%', 'width': '100%'})
                    ])
                ])
            ])
        ])
    ]),

    # === SEÇÃO: MECANIZAÇÃO ===
    html.Div(className="w-full mb-8", children=[
        html.H2("Mecanização", className="font-h3 text-h3 text-primary mb-4"),
        html.Div(className="grid grid-cols-1 xl:grid-cols-2 gap-6 w-full", children=[
            html.Div(className="bg-surface-container-lowest border border-outline-variant rounded-xl p-card-padding flex flex-col", children=[
                html.H3("Tipos de Máquinas (Qtd)", className="font-label-lg text-on-surface mb-2"),
                html.Div(className="flex-1 min-h-[350px]", children=[
                    dcc.Graph(figure=fig_maq_qtd, style={'height': '100%', 'width': '100%'})
                ])
            ]),
            html.Div(className="bg-surface-container-lowest border border-outline-variant rounded-xl p-card-padding flex flex-col", children=[
                html.H3("Estabelecimentos por Máquina", className="font-label-lg text-on-surface mb-2"),
                html.Div(className="flex-1 min-h-[350px]", children=[
                    dcc.Graph(figure=fig_maq_estabs, style={'height': '100%', 'width': '100%'})
                ])
            ])
        ])
    ]),

    # === SEÇÃO: FINANCIAMENTO ===
    html.Div(className="w-full mb-8", children=[
        html.H2("Financiamento e Crédito", className="font-h3 text-h3 text-primary mb-4"),
        html.Div(className="grid grid-cols-1 md:grid-cols-3 gap-6 w-full", children=[
            html.Div(className="bg-surface-container-lowest border border-outline-variant rounded-xl p-card-padding flex flex-col", children=[
                html.H3("Obtenção de Financiamento", className="font-label-lg text-on-surface mb-2 text-center"),
                html.Div(className="flex-1 min-h-[250px]", children=[
                    dcc.Graph(figure=fig_fin_obt, style={'height': '100%', 'width': '100%'})
                ])
            ]),
            html.Div(className="bg-surface-container-lowest border border-outline-variant rounded-xl p-card-padding flex flex-col", children=[
                html.H3("Financiamento do Governo", className="font-label-lg text-on-surface mb-2 text-center"),
                html.Div(className="flex-1 min-h-[250px]", children=[
                    dcc.Graph(figure=fig_fin_gov, style={'height': '100%', 'width': '100%'})
                ])
            ]),
            html.Div(className="bg-surface-container-lowest border border-outline-variant rounded-xl p-card-padding flex flex-col", children=[
                html.H3("Finalidade do Financiamento", className="font-label-lg text-on-surface mb-2 text-center"),
                html.Div(className="flex-1 min-h-[250px]", children=[
                    dcc.Graph(figure=fig_fin_fin, style={'height': '100%', 'width': '100%'})
                ])
            ])
        ])
    ]),

    # === SEÇÃO: PERFIL SOCIODEMOGRÁFICO E MÃO DE OBRA ===
    html.Div(className="w-full mt-12 mb-8", children=[
        html.Div(className="flex items-center gap-3 mb-6", children=[
            html.Span("group", className="material-symbols-outlined text-primary text-[32px]"),
            html.H2("Perfil do Produtor e Mão de Obra", className="font-h3 text-h3 text-primary")
        ]),
        
        # Grid 1: Sexo e Idade
        html.Div(className="grid grid-cols-1 lg:grid-cols-3 gap-6 w-full mb-6", children=[
            html.Div(className="bg-surface-container-lowest border border-outline-variant rounded-xl p-card-padding flex flex-col lg:col-span-1", children=[
                html.H3("Sexo do Produtor", className="font-label-lg text-on-surface mb-2 text-center"),
                html.Div(className="flex-1 min-h-[250px]", children=[
                    dcc.Graph(figure=fig_perfil_sexo, style={'height': '100%', 'width': '100%'})
                ])
            ]),
            html.Div(className="bg-surface-container-lowest border border-outline-variant rounded-xl p-card-padding flex flex-col lg:col-span-2", children=[
                html.H3("Pirâmide Etária", className="font-label-lg text-on-surface mb-2 text-center"),
                html.Div(className="flex-1 min-h-[250px]", children=[
                    dcc.Graph(figure=fig_perfil_idade, style={'height': '100%', 'width': '100%'})
                ])
            ])
        ]),

        # Grid 2: Escolaridade
        html.Div(className="w-full mb-6 bg-surface-container-lowest border border-outline-variant rounded-xl p-card-padding flex flex-col", children=[
            html.H3("Nível de Escolaridade", className="font-label-lg text-on-surface mb-2"),
            html.Div(className="flex-1 min-h-[300px]", children=[
                dcc.Graph(figure=fig_escolaridade, style={'height': '100%', 'width': '100%'})
            ])
        ]),

        # Grid 3: Mão de Obra
        html.Div(className="grid grid-cols-1 lg:grid-cols-2 gap-6 w-full", children=[
            html.Div(className="bg-surface-container-lowest border border-outline-variant rounded-xl p-card-padding flex flex-col", children=[
                html.H3("Pessoal Ocupado (Sem Parentesco)", className="font-label-lg text-on-surface mb-2 text-center"),
                html.Div(className="flex-1 min-h-[250px]", children=[
                    dcc.Graph(figure=fig_mo_sem, style={'height': '100%', 'width': '100%'})
                ])
            ]),
            html.Div(className="bg-surface-container-lowest border border-outline-variant rounded-xl p-card-padding flex flex-col", children=[
                html.H3("Mão de Obra Familiar por Sexo e Idade", className="font-label-lg text-on-surface mb-2 text-center"),
                html.Div(className="flex-1 min-h-[250px]", children=[
                    dcc.Graph(figure=fig_mo_com, style={'height': '100%', 'width': '100%'})
                ])
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