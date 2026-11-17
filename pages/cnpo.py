import dash
from dash import html, dcc, dash_table, callback, Input, Output, State
import plotly.express as px
import pandas as pd
import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from data_pipeline_cnpo import load_cnpo_data
from components import render_chart_footer

dash.register_page(__name__, path='/cnpo', name='Produtores Orgânicos')

df_cnpo = load_cnpo_data()

if 'CIDADE' in df_cnpo.columns and not df_cnpo.empty:
    cidades = sorted([c for c in df_cnpo['CIDADE'].unique() if c])
else:
    cidades = []

cidades_options = [{'label': 'Todas as Cidades', 'value': 'ALL'}] + [{'label': c, 'value': c} for c in cidades]

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

layout = html.Div(className="w-full p-6 md:p-8 bg-background font-public-sans", children=[
    
    # Header com especificidade do dataset
    html.Div(className="mb-8 flex flex-col md:flex-row md:items-end justify-between gap-4", children=[
        html.Div([
            html.H1("Cadastro Nacional de Produtores Orgânicos (CNPO)", className="text-2xl md:text-3xl font-bold text-primary tracking-tight"),
            html.P("Análise de atividades e escopos de certificação orgânica de unidades produtoras cadastradas no Distrito Federal (MAPA / CNPO).", className="text-sm md:text-base text-on-surface-variant mt-2")
        ]),
        html.Div(className="flex items-center gap-2 text-sm text-on-surface-variant font-data-tabular shrink-0", children=[
            html.Span("eco", className="material-symbols-outlined text-[18px] text-emerald-700 dark:text-emerald-400"),
            html.Span("Fonte: MAPA / CNPO")
        ])
    ]),
    
    # Global Filters
    html.Div(className="w-full bg-surface-container-lowest border border-outline-variant rounded-xl p-card-padding mb-8 flex flex-wrap items-center gap-6 shadow-sm", children=[
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
        html.Div(className="w-full bg-surface-container-lowest border border-outline-variant rounded-xl flex flex-col relative overflow-hidden shadow-sm p-card-padding", children=[
            html.Div(className="border-b border-surface-variant pb-4 flex justify-between items-center mb-4", children=[
                html.Div([
                    html.H2("Top 10 Atividades Orgânicas", className="text-lg font-bold text-primary"),
                    html.P("Culturas/produtos mais frequentes na região.", className="text-xs text-on-surface-variant mt-0.5")
                ]),
                html.Button(html.Span("psychiatry", className="material-symbols-outlined"), className="text-emerald-800 bg-emerald-100 dark:bg-emerald-950 p-2 rounded-lg cursor-default")
            ]),
            html.Div(className="min-h-[350px] relative bg-surface-container-low/30 rounded-lg p-2 mb-4", children=[
                dcc.Graph(id='cnpo-atividades-bar', style={'height': '350px', 'width': '100%'})
            ]),
            render_chart_footer(source="MAPA / CNPO", ref_date="2024", note="Ranking de culturas em conformidade orgânica.", download_id="btn-download-cnpo-atividades")
        ]),
        
        # Gráfico 2: Tipos de Entidade (Donut)
        html.Div(className="w-full bg-surface-container-lowest border border-outline-variant rounded-xl flex flex-col relative overflow-hidden shadow-sm p-card-padding", children=[
            html.Div(className="border-b border-surface-variant pb-4 flex justify-between items-center mb-4", children=[
                html.Div([
                    html.H2("Distribuição por Tipo de Entidade", className="text-lg font-bold text-primary"),
                    html.P("Proporção das naturezas de certificação.", className="text-xs text-on-surface-variant mt-0.5")
                ]),
                html.Button(html.Span("verified", className="material-symbols-outlined"), className="text-teal-800 bg-teal-100 dark:bg-teal-950 p-2 rounded-lg cursor-default")
            ]),
            html.Div(className="min-h-[350px] relative bg-surface-container-low/30 rounded-lg p-2 mb-4", children=[
                dcc.Graph(id='cnpo-entidades-pie', style={'height': '350px', 'width': '100%'})
            ]),
            render_chart_footer(source="MAPA / CNPO", ref_date="2024", note="Contagem por tipo de certificadora (OCS/OPAC).", download_id="btn-download-cnpo-entidades-pie")
        ])
    ]),
    
    # Tabela Inferior: Lista de Entidades
    html.Div(className="w-full bg-surface-container-lowest border border-outline-variant rounded-xl flex flex-col relative overflow-hidden pb-4 shadow-sm p-card-padding", children=[
        html.Div(className="border-b border-surface-variant pb-4 flex justify-between items-center mb-4", children=[
            html.Div([
                html.H2("Relação de Entidades Ativas", className="text-lg font-bold text-primary"),
                html.P("Lista detalhada de produtores e seus escopos.", className="text-xs text-on-surface-variant mt-0.5")
            ])
        ]),
        html.Div(id='cnpo-entidades-table-container', className="mb-4"),
        render_chart_footer(source="MAPA / CNPO", ref_date="2024", note="Tabela completa de produtores orgânicos no DF.", download_id="btn-download-cnpo-tabela")
    ])
])

def get_filtered_cnpo(cidade, ano, mes):
    dff = df_cnpo.copy()
    if cidade and cidade != 'ALL':
        dff = dff[dff['CIDADE'] == cidade]
    if ano and ano != 'ALL' and 'ANO_REFERÊNCIA' in dff.columns:
        dff = dff[dff['ANO_REFERÊNCIA'] == str(ano)]
    if mes and mes != 'ALL' and 'MÊS_REFERÊNCIA' in dff.columns:
        dff = dff[dff['MÊS_REFERÊNCIA'] == str(mes)]
    return dff

@callback(
    Output('cnpo-atividades-bar', 'figure'),
    Output('cnpo-entidades-pie', 'figure'),
    Output('cnpo-entidades-table-container', 'children'),
    Input('cnpo-cidade-dropdown', 'value'),
    Input('cnpo-ano-dropdown', 'value'),
    Input('cnpo-mes-dropdown', 'value')
)
def update_cnpo_dashboard(cidade, ano, mes):
    dff = get_filtered_cnpo(cidade, ano, mes)
        
    if dff.empty:
        return px.bar(title="Sem dados"), px.pie(title="Sem dados"), []

    # 1. Processamento das Atividades
    atividades_series = dff['ATIVIDADES'].dropna().astype(str)
    atividades_list = atividades_series.str.split(';')
    atividades_exploded = atividades_list.explode()
    atividades_exploded = atividades_exploded.str.strip().str.title()
    atividades_exploded = atividades_exploded[atividades_exploded != '']
    
    top_atividades = atividades_exploded.value_counts().head(10).reset_index()
    top_atividades.columns = ['Atividade', 'Contagem']
    top_atividades = top_atividades.sort_values(by='Contagem', ascending=True)
    
    fig_bar = px.bar(
        top_atividades,
        x='Contagem',
        y='Atividade',
        orientation='h',
        text='Contagem',
        color='Contagem',
        color_continuous_scale='Viridis'
    )
    fig_bar.update_traces(textposition='outside')
    fig_bar.update_layout(
        margin=dict(t=10, l=10, r=40, b=10),
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        coloraxis_showscale=False,
        xaxis_title="Número de Ocorrências",
        yaxis_title="",
        font=dict(family="Public Sans")
    )
    
    # 2. Processamento Tipos de Entidade
    entidades_count = dff['TIPO DE ENTIDADE'].value_counts().reset_index()
    entidades_count.columns = ['Tipo', 'Contagem']
    
    fig_pie = px.pie(
        entidades_count,
        names='Tipo',
        values='Contagem',
        hole=0.5,
        color_discrete_sequence=['#440154', '#3b528b', '#21908d', '#5dc963', '#fde725']
    )
    fig_pie.update_traces(textinfo='percent+label', textposition='inside')
    fig_pie.update_layout(
        margin=dict(t=10, l=10, r=10, b=10),
        paper_bgcolor='rgba(0,0,0,0)',
        showlegend=False,
        font=dict(family="Public Sans")
    )
    
    # 3. Tabela de Entidades
    cols_tabela = ['ENTIDADE', 'TIPO DE ENTIDADE', 'ESCOPO']
    if 'ANO_REFERÊNCIA' in dff.columns: cols_tabela.append('ANO_REFERÊNCIA')
    if 'MÊS_REFERÊNCIA' in dff.columns: cols_tabela.append('MÊS_REFERÊNCIA')
    
    table_data = dff[cols_tabela].fillna('')
    
    tabela = dash_table.DataTable(
        data=table_data.to_dict('records'),
        columns=[{"name": i, "id": i} for i in table_data.columns],
        page_size=50,
        style_table={'overflowX': 'auto', 'width': '100%'},
        style_header={'backgroundColor': '#012d1d', 'color': 'white', 'fontWeight': 'bold'},
        style_data={'backgroundColor': 'white', 'color': '#191c1c', 'whiteSpace': 'normal', 'height': 'auto'},
        style_cell={'textAlign': 'left', 'padding': '10px', 'fontFamily': 'Public Sans, sans-serif'}
    ) if not table_data.empty else html.P("Sem dados.", className="text-on-surface-variant p-4")
        
    return fig_bar, fig_pie, tabela

# Callbacks para Download CSV Isolados e Granulares
@callback(
    Output("dcc-btn-download-cnpo-atividades", "data"),
    Input("btn-download-cnpo-atividades", "n_clicks"),
    State('cnpo-cidade-dropdown', 'value'),
    State('cnpo-ano-dropdown', 'value'),
    State('cnpo-mes-dropdown', 'value'),
    prevent_initial_call=True
)
def download_cnpo_atividades(n_clicks, cidade, ano, mes):
    dff = get_filtered_cnpo(cidade, ano, mes)
    if not dff.empty:
        atividades_exploded = dff['ATIVIDADES'].dropna().astype(str).str.split(';').explode().str.strip().str.title()
        atividades_exploded = atividades_exploded[atividades_exploded != '']
        top_atividades = atividades_exploded.value_counts().head(10).reset_index()
        top_atividades.columns = ['Atividade', 'Contagem']
        return dcc.send_data_frame(top_atividades.to_csv, "cnpo_top10_atividades.csv", index=False)
    return None

@callback(
    Output("dcc-btn-download-cnpo-entidades-pie", "data"),
    Input("btn-download-cnpo-entidades-pie", "n_clicks"),
    State('cnpo-cidade-dropdown', 'value'),
    State('cnpo-ano-dropdown', 'value'),
    State('cnpo-mes-dropdown', 'value'),
    prevent_initial_call=True
)
def download_cnpo_entidades_pie(n_clicks, cidade, ano, mes):
    dff = get_filtered_cnpo(cidade, ano, mes)
    if not dff.empty:
        entidades_count = dff['TIPO DE ENTIDADE'].value_counts().reset_index()
        entidades_count.columns = ['Tipo de Entidade', 'Contagem']
        return dcc.send_data_frame(entidades_count.to_csv, "cnpo_tipos_de_entidade.csv", index=False)
    return None

@callback(
    Output("dcc-btn-download-cnpo-tabela", "data"),
    Input("btn-download-cnpo-tabela", "n_clicks"),
    State('cnpo-cidade-dropdown', 'value'),
    State('cnpo-ano-dropdown', 'value'),
    State('cnpo-mes-dropdown', 'value'),
    prevent_initial_call=True
)
def download_cnpo_tabela(n_clicks, cidade, ano, mes):
    dff = get_filtered_cnpo(cidade, ano, mes)
    if not dff.empty:
        cols_tabela = ['ENTIDADE', 'TIPO DE ENTIDADE', 'ESCOPO']
        if 'ANO_REFERÊNCIA' in dff.columns: cols_tabela.append('ANO_REFERÊNCIA')
        if 'MÊS_REFERÊNCIA' in dff.columns: cols_tabela.append('MÊS_REFERÊNCIA')
        return dcc.send_data_frame(dff[cols_tabela].to_csv, "cnpo_produtores_organicos_tabela.csv", index=False)
    return None
