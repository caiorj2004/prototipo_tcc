import dash
from dash import html, dcc, dash_table, callback, Input, Output
import plotly.graph_objects as go
import plotly.express as px
import pandas as pd
import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from data_pipeline_caf import load_caf_data

dash.register_page(__name__, path='/caf', name='Módulo CAF')

# Carregar os dados reais
dados_caf = load_caf_data()

# Função auxiliar para extrair Anos e Meses únicos de uma lista de DFs
def get_unique_options(df_dict, keys, col_name):
    opts = set()
    for k in keys:
        df = df_dict.get(k, pd.DataFrame())
        if not df.empty and col_name in df.columns:
            opts.update(df[col_name].dropna().unique().tolist())
    opts = sorted([str(x) for x in opts if str(x) not in ['Desconhecido', 'nan', '']], reverse=True)
    return [{'label': 'Todos', 'value': 'ALL'}] + [{'label': o, 'value': o} for o in opts]

keys_gerais = ['pf', 'pj_area', 'caracterizacao', 'atividade', 'genero', 'jovens', 'pj', 'entidade']
anos_gerais = get_unique_options(dados_caf, keys_gerais, 'ANO')
meses_gerais = get_unique_options(dados_caf, keys_gerais, 'MES')

keys_renda = ['renda_qtd', 'renda_valor']
anos_renda = get_unique_options(dados_caf, keys_renda, 'ANO')
meses_renda = get_unique_options(dados_caf, keys_renda, 'MES')

layout = html.Div(className="w-full p-6 md:p-8 bg-background", children=[
    
    # Header
    html.Div(className="mb-8 flex items-end justify-between", children=[
        html.Div([
            html.H1("Cadastro Nacional da Agricultura Familiar (CAF)", className="font-h1 text-h1 text-primary"),
            html.P("Painel de acompanhamento do perfil, atividade e renda dos inscritos no CAF.", className="font-body-lg text-body-lg text-on-surface-variant mt-2")
        ]),
        html.Div(className="flex items-center gap-2 text-sm text-on-surface-variant font-data-tabular", children=[
            html.Span("assignment", className="material-symbols-outlined text-[18px]"),
            html.Span("Fonte: MDA / CAF (Distrito Federal)")
        ])
    ]),
    
    # Filtros Gerais
    html.Div(className="w-full bg-surface-container-lowest border border-outline-variant rounded-xl p-card-padding mb-8", children=[
        html.H3("Filtros Gerais (Perfil e Atividade)", className="font-label-lg text-on-surface mb-4"),
        html.Div(className="flex flex-wrap items-center gap-6", children=[
            html.Div(className="flex items-center gap-4", children=[
                html.Label("Ano:", className="font-label-sm text-label-sm text-on-surface-variant uppercase tracking-wider"),
                html.Div(className="w-32", children=[
                    dcc.Dropdown(id='caf-geral-ano', options=anos_gerais, value='ALL', clearable=False, className="font-public-sans text-sm")
                ])
            ]),
            html.Div(className="flex items-center gap-4", children=[
                html.Label("Mês:", className="font-label-sm text-label-sm text-on-surface-variant uppercase tracking-wider"),
                html.Div(className="w-32", children=[
                    dcc.Dropdown(id='caf-geral-mes', options=meses_gerais, value='ALL', clearable=False, className="font-public-sans text-sm")
                ])
            ])
        ])
    ]),
    
    # Linha 1: Geral e Caracterização
    html.Div(className="grid grid-cols-1 xl:grid-cols-2 gap-6 w-full mb-6", children=[
        html.Div(className="bg-surface-container-lowest border border-outline-variant rounded-xl p-card-padding flex flex-col", children=[
            html.H3("Geral: Pessoa Física vs Jurídica", className="font-label-lg text-on-surface mb-2"),
            html.Div(className="flex-1 min-h-[300px]", children=[
                dcc.Graph(id='caf-fig-geral', style={'height': '100%', 'width': '100%'})
            ])
        ]),
        html.Div(className="bg-surface-container-lowest border border-outline-variant rounded-xl p-card-padding flex flex-col", children=[
            html.H3("Caracterização: Minorias e Assentados", className="font-label-lg text-on-surface mb-2"),
            html.Div(className="flex-1 min-h-[300px]", children=[
                dcc.Graph(id='caf-fig-carac', style={'height': '100%', 'width': '100%'})
            ])
        ])
    ]),
    
    # Linha 2: Gênero, Jovens e Atividade
    html.Div(className="grid grid-cols-1 md:grid-cols-3 gap-6 w-full mb-6", children=[
        html.Div(className="bg-surface-container-lowest border border-outline-variant rounded-xl p-card-padding flex flex-col", children=[
            html.H3("Gênero Global", className="font-label-lg text-on-surface mb-2 text-center"),
            html.Div(className="flex-1 min-h-[250px]", children=[
                dcc.Graph(id='caf-fig-genero-global', style={'height': '100%', 'width': '100%'})
            ])
        ]),
        html.Div(className="bg-surface-container-lowest border border-outline-variant rounded-xl p-card-padding flex flex-col", children=[
            html.H3("Distribuição de Jovens (16-29)", className="font-label-lg text-on-surface mb-2 text-center"),
            html.Div(className="flex-1 min-h-[250px]", children=[
                dcc.Graph(id='caf-fig-genero-jovens', style={'height': '100%', 'width': '100%'})
            ])
        ]),
        html.Div(className="bg-surface-container-lowest border border-outline-variant rounded-xl p-card-padding flex flex-col", children=[
            html.H3("Áreas de Atividade", className="font-label-lg text-on-surface mb-2 text-center"),
            html.Div(className="flex-1 min-h-[250px]", children=[
                dcc.Graph(id='caf-fig-atividade', style={'height': '100%', 'width': '100%'})
            ])
        ])
    ]),
    
    # DataTables
    html.Div(className="w-full mb-10", children=[
        html.H2("Detalhamento Institucional", className="font-h3 text-h3 text-primary mb-4"),
        html.Div(className="grid grid-cols-1 gap-6 w-full", children=[
            html.Div(className="bg-surface-container-lowest border border-outline-variant rounded-xl p-card-padding flex flex-col overflow-hidden", children=[
                html.H3("Pessoas Jurídicas Registradas", className="font-label-lg text-on-surface mb-4"),
                html.Div(id='caf-table-pj')
            ]),
            html.Div(className="bg-surface-container-lowest border border-outline-variant rounded-xl p-card-padding flex flex-col overflow-hidden", children=[
                html.H3("Entidades Emissoras", className="font-label-lg text-on-surface mb-4"),
                html.Div(id='caf-table-entidade')
            ])
        ])
    ]),

    # Filtros de Renda
    html.Div(className="w-full bg-surface-container-lowest border border-outline-variant rounded-xl p-card-padding mb-8", children=[
        html.H3("Filtros de Renda", className="font-label-lg text-on-surface mb-4"),
        html.Div(className="flex flex-wrap items-center gap-6", children=[
            html.Div(className="flex items-center gap-4", children=[
                html.Label("Ano:", className="font-label-sm text-label-sm text-on-surface-variant uppercase tracking-wider"),
                html.Div(className="w-32", children=[
                    dcc.Dropdown(id='caf-renda-ano', options=anos_renda, value='ALL', clearable=False, className="font-public-sans text-sm")
                ])
            ]),
            html.Div(className="flex items-center gap-4", children=[
                html.Label("Mês:", className="font-label-sm text-label-sm text-on-surface-variant uppercase tracking-wider"),
                html.Div(className="w-32", children=[
                    dcc.Dropdown(id='caf-renda-mes', options=meses_renda, value='ALL', clearable=False, className="font-public-sans text-sm")
                ])
            ])
        ])
    ]),
    
    # Linha 3: Renda (Produção Total)
    html.Div(className="grid grid-cols-1 xl:grid-cols-2 gap-6 w-full mb-6", children=[
        html.Div(className="bg-surface-container-lowest border border-outline-variant rounded-xl p-card-padding flex flex-col", children=[
            html.H3("Produção Total (Por Valor Total de Produção)", className="font-label-lg text-on-surface mb-2"),
            html.Div(className="flex-1 min-h-[350px]", children=[
                dcc.Graph(id='caf-fig-renda-valor-total', style={'height': '100%', 'width': '100%'})
            ])
        ]),
        html.Div(className="bg-surface-container-lowest border border-outline-variant rounded-xl p-card-padding flex flex-col", children=[
            html.H3("Produção Total (Por Quantidade de Cadastros)", className="font-label-lg text-on-surface mb-2"),
            html.Div(className="flex-1 min-h-[350px]", children=[
                dcc.Graph(id='caf-fig-renda-qtd-total', style={'height': '100%', 'width': '100%'})
            ])
        ])
    ]),
    
    # Linha 4: Renda (Produção Per-capita)
    html.Div(className="grid grid-cols-1 xl:grid-cols-2 gap-6 w-full mb-8", children=[
        html.Div(className="bg-surface-container-lowest border border-outline-variant rounded-xl p-card-padding flex flex-col", children=[
            html.H3("Produção Per-capita (Por Valor Total de Produção)", className="font-label-lg text-on-surface mb-2"),
            html.Div(className="flex-1 min-h-[350px]", children=[
                dcc.Graph(id='caf-fig-renda-valor-percapita', style={'height': '100%', 'width': '100%'})
            ])
        ]),
        html.Div(className="bg-surface-container-lowest border border-outline-variant rounded-xl p-card-padding flex flex-col", children=[
            html.H3("Produção Per-capita (Por Quantidade de Cadastros)", className="font-label-lg text-on-surface mb-2"),
            html.Div(className="flex-1 min-h-[350px]", children=[
                dcc.Graph(id='caf-fig-renda-qtd-percapita', style={'height': '100%', 'width': '100%'})
            ])
        ])
    ])
])

def filter_df(df, ano, mes):
    if df.empty: return df
    dff = df.copy()
    if ano != 'ALL' and 'ANO' in dff.columns:
        dff = dff[dff['ANO'] == str(ano)]
    if mes != 'ALL' and 'MES' in dff.columns:
        dff = dff[dff['MES'] == str(mes)]
    return dff

@callback(
    Output('caf-fig-geral', 'figure'),
    Output('caf-fig-carac', 'figure'),
    Output('caf-fig-genero-global', 'figure'),
    Output('caf-fig-genero-jovens', 'figure'),
    Output('caf-fig-atividade', 'figure'),
    Output('caf-table-pj', 'children'),
    Output('caf-table-entidade', 'children'),
    Input('caf-geral-ano', 'value'),
    Input('caf-geral-mes', 'value')
)
def update_gerais(ano, mes):
    empty_fig = go.Figure().update_layout(margin=dict(t=10, b=10, l=10, r=10), paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)')
    
    # Geral (Pessoa Física vs Jurídica)
    df_pf = filter_df(dados_caf.get('pf', pd.DataFrame()), ano, mes)
    df_pj_area = filter_df(dados_caf.get('pj_area', pd.DataFrame()), ano, mes)
    
    fig_geral = go.Figure(empty_fig)
    val_pf = df_pf.select_dtypes(include='number').sum().sum() if not df_pf.empty else 0
    val_pj = df_pj_area.select_dtypes(include='number').sum().sum() if not df_pj_area.empty else 0
    if val_pf + val_pj > 0:
        fig_geral.add_trace(go.Pie(labels=['Pessoa Física', 'Pessoa Jurídica'], values=[val_pf, val_pj], hole=0.5, marker=dict(colors=['#2b2d42', '#8d99ae'])))
        
    # Caracterização
    fig_carac = go.Figure(empty_fig)
    df_carac = filter_df(dados_caf.get('caracterizacao', pd.DataFrame()), ano, mes)
    if not df_carac.empty:
        cols_ignore = ['UF', 'IBGE', 'TOTAL', 'ANO', 'MES']
        cols_metrics = [c for c in df_carac.columns if c not in cols_ignore and 'MUNIC' not in c.upper()]
        vals = df_carac[cols_metrics].sum(numeric_only=True).sort_values(ascending=True)
        fig_carac.add_trace(go.Bar(x=vals.values, y=vals.index, orientation='h', marker_color='#ef233c'))
        
    # Gênero e Jovens
    fig_genero_global = go.Figure(empty_fig)
    fig_genero_jovens = go.Figure(empty_fig)
    
    df_genero = filter_df(dados_caf.get('genero', pd.DataFrame()), ano, mes)
    if not df_genero.empty:
        cols_num = df_genero.select_dtypes(include='number').columns
        mulheres = df_genero[[c for c in cols_num if 'MULHER' in c.upper()]].sum().sum()
        homens = df_genero[[c for c in cols_num if 'HOMEN' in c.upper() or 'HOMEM' in c.upper()]].sum().sum()
        fig_genero_global.add_trace(go.Pie(labels=['Mulheres', 'Homens'], values=[mulheres, homens], hole=0.6, marker=dict(colors=['#c77dff', '#3c096c'])))
        
    df_jovens = filter_df(dados_caf.get('jovens', pd.DataFrame()), ano, mes)
    if not df_jovens.empty:
        cols_num = df_jovens.select_dtypes(include='number').columns
        mulheres_j = df_jovens[[c for c in cols_num if 'MULHER' in c.upper()]].sum().sum()
        homens_j = df_jovens[[c for c in cols_num if 'HOMEN' in c.upper() or 'HOMEM' in c.upper()]].sum().sum()
        fig_genero_jovens.add_trace(go.Bar(x=['Mulheres Jovens', 'Homens Jovens'], y=[mulheres_j, homens_j], marker_color=['#9d4edd', '#5a189a']))
        
    # Atividade
    fig_atividade = go.Figure(empty_fig)
    df_atividade = filter_df(dados_caf.get('atividade', pd.DataFrame()), ano, mes)
    if not df_atividade.empty:
        cols_ignore = ['UF', 'IBGE', 'TOTAL', 'ANO', 'MES']
        cols_metrics = [c for c in df_atividade.columns if c not in cols_ignore and 'MUNIC' not in c.upper()]
        vals = df_atividade[cols_metrics].sum(numeric_only=True).sort_values(ascending=False)
        fig_atividade.add_trace(go.Bar(x=vals.index, y=vals.values, marker_color='#2d6a4f'))
        
    # Tabelas
    df_pj = filter_df(dados_caf.get('pj', pd.DataFrame()), ano, mes)
    table_pj = dash_table.DataTable(
        data=df_pj.to_dict('records'),
        columns=[{"name": i, "id": i} for i in df_pj.columns],
        page_size=10,
        style_table={'overflowX': 'auto', 'width': '100%'},
        style_header={'backgroundColor': '#f1f5f9', 'color': 'black', 'fontWeight': 'bold'},
        style_data={'backgroundColor': 'white', 'color': 'black'},
        style_cell={'textAlign': 'left', 'padding': '10px', 'fontFamily': 'Public Sans, sans-serif'}
    ) if not df_pj.empty else html.P("Sem dados.")
    
    df_entidade = filter_df(dados_caf.get('entidade', pd.DataFrame()), ano, mes)
    table_entidade = dash_table.DataTable(
        data=df_entidade.to_dict('records'),
        columns=[{"name": i, "id": i} for i in df_entidade.columns],
        page_size=10,
        style_table={'overflowX': 'auto', 'width': '100%'},
        style_header={'backgroundColor': '#f1f5f9', 'color': 'black', 'fontWeight': 'bold'},
        style_data={'backgroundColor': 'white', 'color': 'black'},
        style_cell={'textAlign': 'left', 'padding': '10px', 'fontFamily': 'Public Sans, sans-serif'}
    ) if not df_entidade.empty else html.P("Sem dados.")

    return fig_geral, fig_carac, fig_genero_global, fig_genero_jovens, fig_atividade, table_pj, table_entidade


@callback(
    Output('caf-fig-renda-valor-total', 'figure'),
    Output('caf-fig-renda-qtd-total', 'figure'),
    Output('caf-fig-renda-valor-percapita', 'figure'),
    Output('caf-fig-renda-qtd-percapita', 'figure'),
    Input('caf-renda-ano', 'value'),
    Input('caf-renda-mes', 'value')
)
def update_renda(ano, mes):
    empty_fig = go.Figure().update_layout(margin=dict(t=10, b=10, l=10, r=10), paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)')
    fig_rvt, fig_rqt, fig_rvp, fig_rqp = go.Figure(empty_fig), go.Figure(empty_fig), go.Figure(empty_fig), go.Figure(empty_fig)
    
    df_renda_valor = filter_df(dados_caf.get('renda_valor', pd.DataFrame()), ano, mes)
    df_renda_qtd = filter_df(dados_caf.get('renda_qtd', pd.DataFrame()), ano, mes)
    
    def plot_renda(df, fig_tot, fig_per, color_tot, color_per):
        if df.empty: return
        cols = df.columns
        col_produto = [c for c in cols if 'PRODUTO' in c.upper()]
        if not col_produto: return
        produto_col = col_produto[0]
        
        cols_tot = [c for c in cols if 'TOTAL' in c.upper() and 'MEDIANA' not in c.upper()]
        cols_per = [c for c in cols if ('PER-CAPTA' in c.upper() or 'PER CAPITA' in c.upper()) and 'MEDIANA' not in c.upper()]
        
        if cols_tot:
            df_t = df.groupby(produto_col, as_index=False)[cols_tot[0]].sum().sort_values(by=cols_tot[0], ascending=True)
            fig_tot.add_trace(go.Bar(y=df_t[produto_col], x=df_t[cols_tot[0]], orientation='h', marker_color=color_tot))
            fig_tot.update_layout(showlegend=False)
            
        if cols_per:
            df_p = df.groupby(produto_col, as_index=False)[cols_per[0]].mean().sort_values(by=cols_per[0], ascending=True)
            fig_per.add_trace(go.Bar(y=df_p[produto_col], x=df_p[cols_per[0]], orientation='h', marker_color=color_per))
            fig_per.update_layout(showlegend=False)

    plot_renda(df_renda_valor, fig_rvt, fig_rvp, '#023e8a', '#0077b6')
    plot_renda(df_renda_qtd, fig_rqt, fig_rqp, '#1b4965', '#0096c7')
    
    return fig_rvt, fig_rqt, fig_rvp, fig_rqp
