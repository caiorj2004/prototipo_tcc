import dash
from dash import html, dcc, dash_table, callback, Input, Output
import plotly.express as px
import pandas as pd
from data_pipeline_cnpo import load_cnpo_data

dash.register_page(__name__, path='/cnpo', name='Produtores Orgânicos')

# Carrega os dados brutos (apenas DF)
df_cnpo = load_cnpo_data()

# Prepara as opções do Dropdown de Cidades
if 'CIDADE' in df_cnpo.columns and not df_cnpo.empty:
    cidades = sorted([c for c in df_cnpo['CIDADE'].unique() if c])
else:
    cidades = []

cidades_options = [{'label': 'Todas as Cidades', 'value': 'ALL'}] + [{'label': c, 'value': c} for c in cidades]

# Prepara as opções de Ano e Mês
anos_options = [{'label': 'Todos', 'value': 'ALL'}]
if 'ANO_REFERÊNCIA' in df_cnpo.columns and not df_cnpo.empty:
    anos = sorted([a for a in df_cnpo['ANO_REFERÊNCIA'].unique() if a])
    anos_options += [{'label': str(a), 'value': a} for a in anos]

meses_nomes = {
    '1': 'Janeiro', '2': 'Fevereiro', '3': 'Março', '4': 'Abril',
    '5': 'Maio', '6': 'Junho', '7': 'Julho', '8': 'Agosto',
    '9': 'Setembro', '10': 'Outubro', '11': 'Novembro', '12': 'Dezembro',
    '01': 'Janeiro', '02': 'Fevereiro', '03': 'Março', '04': 'Abril',
    '05': 'Maio', '06': 'Junho', '07': 'Julho', '08': 'Agosto', '09': 'Setembro'
}

meses_options = [{'label': 'Todos', 'value': 'ALL'}]
if 'MÊS_REFERÊNCIA' in df_cnpo.columns and not df_cnpo.empty:
    meses = [str(m) for m in df_cnpo['MÊS_REFERÊNCIA'].unique() if str(m).strip() and str(m) != 'nan']
    try:
        meses = sorted(meses, key=lambda x: int(x))
    except:
        meses = sorted(meses)
    meses_options += [{'label': meses_nomes.get(m, m), 'value': m} for m in meses]

layout = html.Div(className="w-full p-6 md:p-8 bg-background", children=[
    
    # Page Header
    html.Div(className="mb-8 flex items-end justify-between", children=[
        html.Div([
            html.H1("Cadastro Nacional de Produtores Orgânicos", className="font-h1 text-h1 text-primary"),
            html.P("Análise de atividades e escopos de certificação orgânica no DF.", className="font-body-lg text-body-lg text-on-surface-variant mt-2")
        ]),
        html.Div(className="flex items-center gap-2 text-sm text-on-surface-variant font-data-tabular", children=[
            html.Span("eco", className="material-symbols-outlined text-[18px] text-[#558b2f]"),
            html.Span("Fonte: MAPA / CNPO")
        ])
    ]),
    
    # Global Filters
    html.Div(className="w-full bg-surface-container-lowest border border-outline-variant rounded-xl p-card-padding mb-8 flex flex-wrap items-center gap-6", children=[
        html.Div(className="flex items-center gap-4", children=[
            html.Label("Ano:", className="font-label-sm text-label-sm text-on-surface-variant uppercase tracking-wider"),
            html.Div(className="w-32", children=[
                dcc.Dropdown(
                    id='cnpo-ano-dropdown',
                    options=anos_options,
                    value='ALL',
                    clearable=False,
                    className="font-public-sans text-sm"
                )
            ])
        ]),
        
        html.Div(className="flex items-center gap-4", children=[
            html.Label("Mês:", className="font-label-sm text-label-sm text-on-surface-variant uppercase tracking-wider"),
            html.Div(className="w-32", children=[
                dcc.Dropdown(
                    id='cnpo-mes-dropdown',
                    options=meses_options,
                    value='ALL',
                    clearable=False,
                    className="font-public-sans text-sm"
                )
            ])
        ]),

        html.Div(className="flex items-center gap-4", children=[
            html.Label("Cidade:", className="font-label-sm text-label-sm text-on-surface-variant uppercase tracking-wider"),
            html.Div(className="w-64", children=[
                dcc.Dropdown(
                    id='cnpo-cidade-dropdown',
                    options=cidades_options,
                    value='ALL',
                    clearable=False,
                    className="font-public-sans text-sm"
                )
            ])
        ])
    ]),
    
    # Grid Superior (Gráficos)
    html.Div(className="grid grid-cols-1 xl:grid-cols-2 gap-6 w-full mb-6", children=[
        
        # Gráfico 1: Top Atividades (Barras Horizontais)
        html.Div(className="w-full bg-surface-container-lowest border border-outline-variant rounded-xl flex flex-col relative overflow-hidden", children=[
            html.Div(className="p-card-padding border-b border-surface-variant flex justify-between items-center", children=[
                html.Div([
                    html.H2("Top 10 Atividades Orgânicas", className="font-h3 text-h3 text-primary"),
                    html.P("Culturas/produtos mais frequentes na região.", className="font-data-tabular text-data-tabular text-on-surface-variant mt-1")
                ]),
                html.Button(html.Span("psychiatry", className="material-symbols-outlined"), className="text-[#33691e] bg-[#aed581]/30 p-2 rounded-lg cursor-default")
            ]),
            html.Div(className="p-card-padding min-h-[350px] relative bg-surface-container-low/30", children=[
                dcc.Graph(id='cnpo-atividades-bar', style={'height': '350px', 'width': '100%'})
            ])
        ]),
        
        # Gráfico 2: Tipos de Entidade (Donut)
        html.Div(className="w-full bg-surface-container-lowest border border-outline-variant rounded-xl flex flex-col relative overflow-hidden", children=[
            html.Div(className="p-card-padding border-b border-surface-variant flex justify-between items-center", children=[
                html.Div([
                    html.H2("Distribuição por Tipo de Entidade", className="font-h3 text-h3 text-primary"),
                    html.P("Proporção das naturezas de certificação.", className="font-data-tabular text-data-tabular text-on-surface-variant mt-1")
                ]),
                html.Button(html.Span("verified", className="material-symbols-outlined"), className="text-[#558b2f] bg-[#f1f8e9] p-2 rounded-lg cursor-default")
            ]),
            html.Div(className="p-card-padding min-h-[350px] relative bg-surface-container-low/30", children=[
                dcc.Graph(id='cnpo-entidades-pie', style={'height': '350px', 'width': '100%'})
            ])
        ])
    ]),
    
    # Tabela Inferior: Lista de Entidades
    html.Div(className="w-full bg-surface-container-lowest border border-outline-variant rounded-xl flex flex-col relative overflow-hidden pb-4", children=[
        html.Div(className="p-card-padding border-b border-surface-variant flex justify-between items-center", children=[
            html.Div([
                html.H2("Relação de Entidades Ativas", className="font-h3 text-h3 text-primary"),
                html.P("Lista detalhada de produtores e seus escopos.", className="font-data-tabular text-data-tabular text-on-surface-variant mt-1")
            ])
        ]),
        html.Div(id='cnpo-entidades-table-container', className="p-card-padding")
    ])
])

@callback(
    Output('cnpo-atividades-bar', 'figure'),
    Output('cnpo-entidades-pie', 'figure'),
    Output('cnpo-entidades-table-container', 'children'),
    Input('cnpo-cidade-dropdown', 'value'),
    Input('cnpo-ano-dropdown', 'value'),
    Input('cnpo-mes-dropdown', 'value')
)
def update_cnpo_dashboard(cidade, ano, mes):
    dff = df_cnpo.copy()
    
    if cidade and cidade != 'ALL':
        dff = dff[dff['CIDADE'] == cidade]
    if ano and ano != 'ALL' and 'ANO_REFERÊNCIA' in dff.columns:
        dff = dff[dff['ANO_REFERÊNCIA'] == str(ano)]
    if mes and mes != 'ALL' and 'MÊS_REFERÊNCIA' in dff.columns:
        dff = dff[dff['MÊS_REFERÊNCIA'] == str(mes)]
        
    if dff.empty:
        return px.bar(title="Sem dados"), px.pie(title="Sem dados"), []

    # 1. Processamento das Atividades (split e explode)
    atividades_series = dff['ATIVIDADES'].dropna().astype(str)
    # Separa por ponto e vírgula
    atividades_list = atividades_series.str.split(';')
    # Transforma lista de listas em uma única série (explode)
    atividades_exploded = atividades_list.explode()
    # Remove espaços em branco e capitaliza
    atividades_exploded = atividades_exploded.str.strip().str.title()
    # Remove strings vazias
    atividades_exploded = atividades_exploded[atividades_exploded != '']
    
    # Contagem Top 10
    top_atividades = atividades_exploded.value_counts().head(10).reset_index()
    top_atividades.columns = ['Atividade', 'Contagem']
    top_atividades = top_atividades.sort_values(by='Contagem', ascending=True) # Para barras horizontais
    
    fig_bar = px.bar(
        top_atividades,
        x='Contagem',
        y='Atividade',
        orientation='h',
        text='Contagem',
        color_discrete_sequence=['#558b2f'] # Verde Oliva
    )
    fig_bar.update_traces(textposition='outside')
    fig_bar.update_layout(
        margin=dict(t=10, l=10, r=40, b=10),
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        xaxis_title="Número de Ocorrências",
        yaxis_title="",
        font=dict(family="Public Sans")
    )
    
    # 2. Processamento Tipos de Entidade (Donut)
    entidades_count = dff['TIPO DE ENTIDADE'].value_counts().reset_index()
    entidades_count.columns = ['Tipo', 'Contagem']
    
    fig_pie = px.pie(
        entidades_count,
        names='Tipo',
        values='Contagem',
        hole=0.5,
        color_discrete_sequence=['#33691e', '#558b2f', '#aed581', '#f1f8e9']
    )
    fig_pie.update_traces(textinfo='percent+label', textposition='inside')
    fig_pie.update_layout(
        margin=dict(t=10, l=10, r=10, b=10),
        paper_bgcolor='rgba(0,0,0,0)',
        showlegend=False,
        font=dict(family="Public Sans")
    )
    
    # 3. Tabela de Entidades
    table_data = dff[['ENTIDADE', 'TIPO DE ENTIDADE', 'ESCOPO']].fillna('')
    
    tabela = dash_table.DataTable(
        data=table_data.to_dict('records'),
        columns=[{"name": i, "id": i} for i in table_data.columns],
        page_size=30,
        style_table={'overflowX': 'auto', 'width': '100%'},
        style_header={'backgroundColor': '#f1f5f9', 'color': 'black', 'fontWeight': 'bold'},
        style_data={'backgroundColor': 'white', 'color': 'black', 'whiteSpace': 'normal', 'height': 'auto'},
        style_cell={'textAlign': 'left', 'padding': '10px', 'fontFamily': 'Public Sans, sans-serif'}
    ) if not table_data.empty else html.P("Sem dados.", className="text-on-surface-variant p-4")
        
    return fig_bar, fig_pie, tabela
