import dash
from dash import html, dcc, dash_table, callback, Input, Output, State
import plotly.graph_objects as go
import plotly.express as px
import pandas as pd
import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from data_pipeline_caf import load_caf_data
from components import render_chart_footer, VIRIDIS_PALETTE

dash.register_page(__name__, path='/caf', name='CAF')

# Carregar os dados reais otimizados em Parquet
dados_caf = load_caf_data()

meses_nomes = {
    '1': 'Janeiro', '2': 'Fevereiro', '3': 'Março', '4': 'Abril',
    '5': 'Maio', '6': 'Junho', '7': 'Julho', '8': 'Agosto',
    '9': 'Setembro', '10': 'Outubro', '11': 'Novembro', '12': 'Dezembro',
    '01': 'Janeiro', '02': 'Fevereiro', '03': 'Março', '04': 'Abril',
    '05': 'Maio', '06': 'Junho', '07': 'Julho', '08': 'Agosto', '09': 'Setembro'
}

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

keys_renda = ['renda_qtd', 'renda_valor']
anos_renda = get_unique_options(dados_caf, keys_renda, 'ANO')

def get_meses_options(ano_selecionado, df_dict, keys):
    opts = set()
    for k in keys:
        df = df_dict.get(k, pd.DataFrame())
        if not df.empty and 'MES' in df.columns:
            if ano_selecionado == 'ALL':
                opts.update(df['MES'].dropna().unique().tolist())
            elif 'ANO' in df.columns:
                dff = df[df['ANO'] == str(ano_selecionado)]
                opts.update(dff['MES'].dropna().unique().tolist())
    
    opts_clean = [str(x) for x in opts if str(x) not in ['Desconhecido', 'nan', '']]
    try:
        opts_clean = sorted(opts_clean, key=lambda x: int(x))
    except:
        opts_clean = sorted(opts_clean)
        
    options = [{'label': 'Todos', 'value': 'ALL'}]
    for o in opts_clean:
        options.append({'label': meses_nomes.get(o, o), 'value': o})
    return options

layout = html.Div(className="w-full p-6 md:p-8 bg-background font-public-sans", children=[
    
    # Header com nome "CAF" e especificidade do dataset
    html.Div(className="mb-8 flex flex-col md:flex-row md:items-end justify-between gap-4", children=[
        html.Div([
            html.H1("Cadastro Nacional da Agricultura Familiar (CAF)", className="text-2xl md:text-3xl font-bold text-primary tracking-tight"),
            html.P("Painel de acompanhamento do perfil, atividade e renda dos inscritos no Cadastro Nacional da Agricultura Familiar no Distrito Federal (MDA / CAF).", className="text-sm md:text-base text-on-surface-variant mt-2")
        ]),
        html.Div(className="flex items-center gap-2 text-sm text-on-surface-variant font-data-tabular shrink-0", children=[
            html.Span("assignment", className="material-symbols-outlined text-[18px] text-emerald-700 dark:text-emerald-400"),
            html.Span("Fonte: MDA / CAF (Distrito Federal)")
        ])
    ]),
    
    # Filtros Gerais
    html.Div(className="w-full bg-surface-container-lowest border border-outline-variant rounded-xl p-card-padding mb-8 shadow-sm", children=[
        html.H3("Filtros Gerais (Perfil e Atividade)", className="font-bold text-slate-900 dark:text-white mb-4"),
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
                    dcc.Dropdown(id='caf-geral-mes', options=[{'label': 'Todos', 'value': 'ALL'}], value='ALL', clearable=False, className="font-public-sans text-sm")
                ])
            ])
        ])
    ]),
    
    # Linha 1: Geral e Caracterização
    html.Div(className="grid grid-cols-1 xl:grid-cols-2 gap-6 w-full mb-6", children=[
        html.Div(className="bg-surface-container-lowest border border-outline-variant rounded-xl p-card-padding flex flex-col shadow-sm", children=[
            html.H3("Geral: Pessoa Física vs Jurídica", className="font-bold text-slate-900 dark:text-white mb-2"),
            html.Div(className="flex-1 min-h-[300px] mb-2", children=[
                dcc.Graph(id='caf-fig-geral', style={'height': '100%', 'width': '100%'})
            ]),
            render_chart_footer(source="MDA / CAF", ref_date="2024", note="Total de cadastros no DF.", download_id="btn-download-caf-geral")
        ]),
        html.Div(className="bg-surface-container-lowest border border-outline-variant rounded-xl p-card-padding flex flex-col shadow-sm", children=[
            html.H3("Caracterização: Minorias e Assentados", className="font-bold text-slate-900 dark:text-white mb-2"),
            html.Div(className="flex-1 min-h-[300px] mb-2", children=[
                dcc.Graph(id='caf-fig-carac', style={'height': '100%', 'width': '100%'})
            ]),
            render_chart_footer(source="MDA / CAF", ref_date="2024", note="Perfil dos produtores inscritos.", download_id="btn-download-caf-carac")
        ])
    ]),
    
    # Linha 2: Gênero, Jovens e Atividade (Cartões Individuais com CSVs Granulares)
    html.Div(className="grid grid-cols-1 md:grid-cols-3 gap-6 w-full mb-6", children=[
        html.Div(className="bg-surface-container-lowest border border-outline-variant rounded-xl p-card-padding flex flex-col shadow-sm", children=[
            html.H3("Gênero Global", className="font-bold text-slate-900 dark:text-white mb-2 text-center text-sm"),
            html.Div(className="flex-1 min-h-[250px] mb-2", children=[
                dcc.Graph(id='caf-fig-genero-global', style={'height': '100%', 'width': '100%'})
            ]),
            render_chart_footer(source="MDA / CAF", ref_date="2024", note="Distribuição por gênero.", download_id="btn-download-caf-genero")
        ]),
        html.Div(className="bg-surface-container-lowest border border-outline-variant rounded-xl p-card-padding flex flex-col shadow-sm", children=[
            html.H3("Distribuição de Jovens (16-29)", className="font-bold text-slate-900 dark:text-white mb-2 text-center text-sm"),
            html.Div(className="flex-1 min-h-[250px] mb-2", children=[
                dcc.Graph(id='caf-fig-genero-jovens', style={'height': '100%', 'width': '100%'})
            ]),
            render_chart_footer(source="MDA / CAF", ref_date="2024", note="Jovens produtores rurais.", download_id="btn-download-caf-jovens")
        ]),
        html.Div(className="bg-surface-container-lowest border border-outline-variant rounded-xl p-card-padding flex flex-col shadow-sm", children=[
            html.H3("Áreas de Atividade", className="font-bold text-slate-900 dark:text-white mb-2 text-center text-sm"),
            html.Div(className="flex-1 min-h-[250px] mb-2", children=[
                dcc.Graph(id='caf-fig-atividade', style={'height': '100%', 'width': '100%'})
            ]),
            render_chart_footer(source="MDA / CAF", ref_date="2024", note="Segmentos de atividade agrícola.", download_id="btn-download-caf-atividade")
        ])
    ]),
    
    # DataTables com Exportação CSV Granular
    html.Div(className="w-full mb-10", children=[
        html.H2("Detalhamento Institucional", className="text-xl font-bold text-primary mb-4"),
        html.Div(className="grid grid-cols-1 gap-6 w-full", children=[
            html.Div(className="bg-surface-container-lowest border border-outline-variant rounded-xl p-card-padding flex flex-col overflow-hidden shadow-sm", children=[
                html.H3("Pessoas Jurídicas Registradas", className="font-bold text-slate-900 dark:text-white mb-4"),
                html.Div(id='caf-table-pj', className="mb-4"),
                render_chart_footer(source="MDA / CAF", ref_date="2024", note="Cooperativas e associações rurais.", download_id="btn-download-caf-pj")
            ]),
            html.Div(className="bg-surface-container-lowest border border-outline-variant rounded-xl p-card-padding flex flex-col overflow-hidden shadow-sm", children=[
                html.H3("Entidades Emissoras", className="font-bold text-slate-900 dark:text-white mb-4"),
                html.Div(id='caf-table-entidade', className="mb-4"),
                render_chart_footer(source="MDA / CAF", ref_date="2024", note="Entidades autorizadas a emitir o CAF no DF.", download_id="btn-download-caf-entidades")
            ])
        ])
    ]),

    # Filtros de Renda
    html.Div(className="w-full bg-surface-container-lowest border border-outline-variant rounded-xl p-card-padding mb-8 shadow-sm", children=[
        html.H3("Filtros de Renda", className="font-bold text-slate-900 dark:text-white mb-4"),
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
                    dcc.Dropdown(id='caf-renda-mes', options=[{'label': 'Todos', 'value': 'ALL'}], value='ALL', clearable=False, className="font-public-sans text-sm")
                ])
            ])
        ])
    ]),
    
    # Linha 3: Renda (Produção Total)
    html.Div(className="grid grid-cols-1 xl:grid-cols-2 gap-6 w-full mb-6", children=[
        html.Div(className="bg-surface-container-lowest border border-outline-variant rounded-xl p-card-padding flex flex-col shadow-sm", children=[
            html.H3("Produção Total (Por Valor Total de Produção)", className="font-bold text-slate-900 dark:text-white mb-2"),
            html.Div(className="flex-1 min-h-[350px] mb-2", children=[
                dcc.Graph(id='caf-fig-renda-valor-total', style={'height': '100%', 'width': '100%'})
            ]),
            render_chart_footer(source="MDA / CAF Renda", ref_date="2024", note="Valor total bruto de produção.", download_id="btn-download-caf-renda-valor")
        ]),
        html.Div(className="bg-surface-container-lowest border border-outline-variant rounded-xl p-card-padding flex flex-col shadow-sm", children=[
            html.H3("Produção Total (Por Quantidade de Cadastros)", className="font-bold text-slate-900 dark:text-white mb-2"),
            html.Div(className="flex-1 min-h-[350px] mb-2", children=[
                dcc.Graph(id='caf-fig-renda-qtd-total', style={'height': '100%', 'width': '100%'})
            ]),
            render_chart_footer(source="MDA / CAF Renda", ref_date="2024", note="Quantidade de produtores declarantes.", download_id="btn-download-caf-renda-qtd")
        ])
    ]),
    
    # Linha 4: Renda (Produção Per-capita com Cartões Granulares Independentes)
    html.Div(className="grid grid-cols-1 xl:grid-cols-2 gap-6 w-full mb-8", children=[
        html.Div(className="bg-surface-container-lowest border border-outline-variant rounded-xl p-card-padding shadow-sm flex flex-col", children=[
            html.H3("Produção Per-capita (Por Valor Total de Produção)", className="font-bold text-slate-900 dark:text-white mb-2 text-sm"),
            html.Div(className="flex-1 min-h-[350px] mb-2", children=[
                dcc.Graph(id='caf-fig-renda-valor-percapita', style={'height': '100%', 'width': '100%'})
            ]),
            render_chart_footer(source="MDA / CAF Renda", ref_date="2024", note="Valor per-capita de produção.", download_id="btn-download-caf-renda-valor-percapita")
        ]),
        html.Div(className="bg-surface-container-lowest border border-outline-variant rounded-xl p-card-padding shadow-sm flex flex-col", children=[
            html.H3("Produção Per-capita (Por Quantidade de Cadastros)", className="font-bold text-slate-900 dark:text-white mb-2 text-sm"),
            html.Div(className="flex-1 min-h-[350px] mb-2", children=[
                dcc.Graph(id='caf-fig-renda-qtd-percapita', style={'height': '100%', 'width': '100%'})
            ]),
            render_chart_footer(source="MDA / CAF Renda", ref_date="2024", note="Quantidade per-capita declarada.", download_id="btn-download-caf-renda-qtd-percapita")
        ])
    ])
])

@callback(
    Output('caf-geral-mes', 'options'),
    Input('caf-geral-ano', 'value')
)
def update_meses_gerais(ano):
    return get_meses_options(ano, dados_caf, keys_gerais)

@callback(
    Output('caf-renda-mes', 'options'),
    Input('caf-renda-ano', 'value')
)
def update_meses_renda(ano):
    return get_meses_options(ano, dados_caf, keys_renda)

def agrega_renda(df, tipo):
    """Agrega a renda do CAF por produto, exatamente como o gráfico mostra.
    tipo='total'     -> soma da primeira coluna TOTAL
    tipo='percapita' -> média da primeira coluna PER-CAPITA
    Devolve (DataFrame agregado, nome do produto, nome da coluna) ou (None, None, None)."""
    if df is None or df.empty:
        return None, None, None
    col_produto = [c for c in df.columns if 'PRODUTO' in c.upper()]
    if not col_produto:
        return None, None, None
    prod = col_produto[0]
    if tipo == 'total':
        cols = [c for c in df.columns if 'TOTAL' in c.upper() and 'MEDIANA' not in c.upper()]
        func = 'sum'
    else:
        cols = [c for c in df.columns if ('PER-CAPTA' in c.upper() or 'PER CAPITA' in c.upper()) and 'MEDIANA' not in c.upper()]
        func = 'mean'
    if not cols:
        return None, None, None
    out = df.groupby(prod, as_index=False)[cols[0]].agg(func).sort_values(by=cols[0], ascending=True)
    return out, prod, cols[0]

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
    
    df_pf = filter_df(dados_caf.get('pf', pd.DataFrame()), ano, mes)
    df_pj_area = filter_df(dados_caf.get('pj_area', pd.DataFrame()), ano, mes)
    
    fig_geral = go.Figure(empty_fig)
    val_pf = df_pf.select_dtypes(include='number').sum().sum() if not df_pf.empty else 0
    val_pj = df_pj_area.select_dtypes(include='number').sum().sum() if not df_pj_area.empty else 0
    if val_pf + val_pj > 0:
        fig_geral.add_trace(go.Pie(
            labels=['Pessoa Física', 'Pessoa Jurídica'], 
            values=[val_pf, val_pj], 
            hole=0.5, 
            marker=dict(colors=['#440154', '#21908d'])
        ))
        
    fig_carac = go.Figure(empty_fig)
    df_carac = filter_df(dados_caf.get('caracterizacao', pd.DataFrame()), ano, mes)
    if not df_carac.empty:
        cols_ignore = ['UF', 'IBGE', 'TOTAL', 'ANO', 'MES']
        cols_metrics = [c for c in df_carac.columns if c not in cols_ignore and 'MUNIC' not in c.upper()]
        vals = df_carac[cols_metrics].sum(numeric_only=True).sort_values(ascending=True)
        fig_carac.add_trace(go.Bar(x=vals.values, y=vals.index, orientation='h', marker_color='#3b528b'))
        
    fig_genero_global = go.Figure(empty_fig)
    fig_genero_jovens = go.Figure(empty_fig)
    
    df_genero = filter_df(dados_caf.get('genero', pd.DataFrame()), ano, mes)
    if not df_genero.empty:
        cols_num = df_genero.select_dtypes(include='number').columns
        mulheres = df_genero[[c for c in cols_num if 'MULHER' in c.upper()]].sum().sum()
        homens = df_genero[[c for c in cols_num if 'HOMEN' in c.upper() or 'HOMEM' in c.upper()]].sum().sum()
        fig_genero_global.add_trace(go.Pie(
            labels=['Mulheres', 'Homens'], 
            values=[mulheres, homens], 
            hole=0.6, 
            marker=dict(colors=['#5dc963', '#21908d'])
        ))
        
    df_jovens = filter_df(dados_caf.get('jovens', pd.DataFrame()), ano, mes)
    if not df_jovens.empty:
        cols_num = df_jovens.select_dtypes(include='number').columns
        mulheres_j = df_jovens[[c for c in cols_num if 'MULHER' in c.upper()]].sum().sum()
        homens_j = df_jovens[[c for c in cols_num if 'HOMEN' in c.upper() or 'HOMEM' in c.upper()]].sum().sum()
        fig_genero_jovens.add_trace(go.Bar(
            x=['Mulheres Jovens', 'Homens Jovens'], 
            y=[mulheres_j, homens_j], 
            marker_color=['#5dc963', '#3b528b']
        ))
        
    fig_atividade = go.Figure(empty_fig)
    df_atividade = filter_df(dados_caf.get('atividade', pd.DataFrame()), ano, mes)
    if not df_atividade.empty:
        cols_ignore = ['UF', 'IBGE', 'TOTAL', 'ANO', 'MES']
        cols_metrics = [c for c in df_atividade.columns if c not in cols_ignore and 'MUNIC' not in c.upper()]
        vals = df_atividade[cols_metrics].sum(numeric_only=True).sort_values(ascending=False)
        fig_atividade.add_trace(go.Bar(x=vals.index, y=vals.values, marker_color='#21908d'))
        
    df_pj = filter_df(dados_caf.get('pj', pd.DataFrame()), ano, mes)
    if not df_pj.empty and 'TOTA ATIVOS' in df_pj.columns:
        df_pj = df_pj.drop(columns=['TOTA ATIVOS'])
        
    table_pj = dash_table.DataTable(
        data=df_pj.to_dict('records'),
        columns=[{"name": i, "id": i} for i in df_pj.columns],
        page_size=10,
        style_table={'overflowX': 'auto', 'width': '100%'},
        style_header={'backgroundColor': '#012d1d', 'color': 'white', 'fontWeight': 'bold'},
        style_data={'backgroundColor': 'white', 'color': '#191c1c'},
        style_cell={'textAlign': 'left', 'padding': '10px', 'fontFamily': 'Public Sans, sans-serif'}
    ) if not df_pj.empty else html.P("Sem dados.", className="p-4 text-slate-500")
    
    df_entidade = filter_df(dados_caf.get('entidade', pd.DataFrame()), ano, mes)
    table_entidade = dash_table.DataTable(
        data=df_entidade.to_dict('records'),
        columns=[{"name": i, "id": i} for i in df_entidade.columns],
        page_size=10,
        style_table={'overflowX': 'auto', 'width': '100%'},
        style_header={'backgroundColor': '#012d1d', 'color': 'white', 'fontWeight': 'bold'},
        style_data={'backgroundColor': 'white', 'color': '#191c1c'},
        style_cell={'textAlign': 'left', 'padding': '10px', 'fontFamily': 'Public Sans, sans-serif'}
    ) if not df_entidade.empty else html.P("Sem dados.", className="p-4 text-slate-500")

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
        for tipo, fig, cor in (('total', fig_tot, color_tot), ('percapita', fig_per, color_per)):
            agg, prod, col = agrega_renda(df, tipo)
            if agg is None:
                continue
            fig.add_trace(go.Bar(y=agg[prod], x=agg[col], orientation='h', marker_color=cor))
            fig.update_layout(showlegend=False)

    plot_renda(df_renda_valor, fig_rvt, fig_rvp, '#440154', '#21908d')
    plot_renda(df_renda_qtd, fig_rqt, fig_rqp, '#3b528b', '#5dc963')
    
    return fig_rvt, fig_rqt, fig_rvp, fig_rqp

# Callbacks de Exportação CSV Granular por Componente
@callback(
    Output("dcc-btn-download-caf-geral", "data"),
    Input("btn-download-caf-geral", "n_clicks"),
    State('caf-geral-ano', 'value'),
    State('caf-geral-mes', 'value'),
    prevent_initial_call=True
)
def download_caf_geral(n_clicks, ano, mes):
    df_pf = filter_df(dados_caf.get('pf', pd.DataFrame()), ano, mes)
    if not df_pf.empty:
        return dcc.send_data_frame(df_pf.to_csv, "caf_pessoas_fisicas_df.csv", index=False)
    return None

@callback(
    Output("dcc-btn-download-caf-carac", "data"),
    Input("btn-download-caf-carac", "n_clicks"),
    State('caf-geral-ano', 'value'),
    State('caf-geral-mes', 'value'),
    prevent_initial_call=True
)
def download_caf_carac(n_clicks, ano, mes):
    df_carac = filter_df(dados_caf.get('caracterizacao', pd.DataFrame()), ano, mes)
    if not df_carac.empty:
        return dcc.send_data_frame(df_carac.to_csv, "caf_caracterizacao_df.csv", index=False)
    return None

@callback(
    Output("dcc-btn-download-caf-genero", "data"),
    Input("btn-download-caf-genero", "n_clicks"),
    State('caf-geral-ano', 'value'),
    State('caf-geral-mes', 'value'),
    prevent_initial_call=True
)
def download_caf_genero(n_clicks, ano, mes):
    df_g = filter_df(dados_caf.get('genero', pd.DataFrame()), ano, mes)
    if not df_g.empty:
        return dcc.send_data_frame(df_g.to_csv, "caf_genero_global_df.csv", index=False)
    return None

@callback(
    Output("dcc-btn-download-caf-jovens", "data"),
    Input("btn-download-caf-jovens", "n_clicks"),
    State('caf-geral-ano', 'value'),
    State('caf-geral-mes', 'value'),
    prevent_initial_call=True
)
def download_caf_jovens(n_clicks, ano, mes):
    df_j = filter_df(dados_caf.get('jovens', pd.DataFrame()), ano, mes)
    if not df_j.empty:
        return dcc.send_data_frame(df_j.to_csv, "caf_jovens_df.csv", index=False)
    return None

@callback(
    Output("dcc-btn-download-caf-atividade", "data"),
    Input("btn-download-caf-atividade", "n_clicks"),
    State('caf-geral-ano', 'value'),
    State('caf-geral-mes', 'value'),
    prevent_initial_call=True
)
def download_caf_atividade(n_clicks, ano, mes):
    df_at = filter_df(dados_caf.get('atividade', pd.DataFrame()), ano, mes)
    if not df_at.empty:
        return dcc.send_data_frame(df_at.to_csv, "caf_atividades_df.csv", index=False)
    return None

@callback(
    Output("dcc-btn-download-caf-pj", "data"),
    Input("btn-download-caf-pj", "n_clicks"),
    State('caf-geral-ano', 'value'),
    State('caf-geral-mes', 'value'),
    prevent_initial_call=True
)
def download_caf_pj(n_clicks, ano, mes):
    df_pj = filter_df(dados_caf.get('pj', pd.DataFrame()), ano, mes)
    if not df_pj.empty and 'TOTA ATIVOS' in df_pj.columns:
        df_pj = df_pj.drop(columns=['TOTA ATIVOS'])  # mesma visão da tabela na tela
    if not df_pj.empty:
        return dcc.send_data_frame(df_pj.to_csv, "caf_pessoas_juridicas_df.csv", index=False)
    return None

@callback(
    Output("dcc-btn-download-caf-entidades", "data"),
    Input("btn-download-caf-entidades", "n_clicks"),
    State('caf-geral-ano', 'value'),
    State('caf-geral-mes', 'value'),
    prevent_initial_call=True
)
def download_caf_entidades(n_clicks, ano, mes):
    df_ent = filter_df(dados_caf.get('entidade', pd.DataFrame()), ano, mes)
    if not df_ent.empty:
        return dcc.send_data_frame(df_ent.to_csv, "caf_entidades_emissoras_df.csv", index=False)
    return None

@callback(
    Output("dcc-btn-download-caf-renda-valor", "data"),
    Input("btn-download-caf-renda-valor", "n_clicks"),
    State('caf-renda-ano', 'value'),
    State('caf-renda-mes', 'value'),
    prevent_initial_call=True
)
def download_caf_renda_valor(n_clicks, ano, mes):
    agg, prod, col = agrega_renda(filter_df(dados_caf.get('renda_valor', pd.DataFrame()), ano, mes), 'total')
    if agg is not None:
        agg = agg.rename(columns={col: 'Total: ' + col})
        return dcc.send_data_frame(agg.to_csv, "caf_renda_valor_total_df.csv", index=False)
    return None

@callback(
    Output("dcc-btn-download-caf-renda-qtd", "data"),
    Input("btn-download-caf-renda-qtd", "n_clicks"),
    State('caf-renda-ano', 'value'),
    State('caf-renda-mes', 'value'),
    prevent_initial_call=True
)
def download_caf_renda_qtd(n_clicks, ano, mes):
    agg, prod, col = agrega_renda(filter_df(dados_caf.get('renda_qtd', pd.DataFrame()), ano, mes), 'total')
    if agg is not None:
        agg = agg.rename(columns={col: 'Total: ' + col})
        return dcc.send_data_frame(agg.to_csv, "caf_renda_quantidade_total_df.csv", index=False)
    return None

@callback(
    Output("dcc-btn-download-caf-renda-valor-percapita", "data"),
    Input("btn-download-caf-renda-valor-percapita", "n_clicks"),
    State('caf-renda-ano', 'value'),
    State('caf-renda-mes', 'value'),
    prevent_initial_call=True
)
def download_caf_renda_valor_percapita(n_clicks, ano, mes):
    agg, prod, col = agrega_renda(filter_df(dados_caf.get('renda_valor', pd.DataFrame()), ano, mes), 'percapita')
    if agg is not None:
        agg = agg.rename(columns={col: 'Média per capita: ' + col})
        return dcc.send_data_frame(agg.to_csv, "caf_renda_valor_percapita_df.csv", index=False)
    return None

@callback(
    Output("dcc-btn-download-caf-renda-qtd-percapita", "data"),
    Input("btn-download-caf-renda-qtd-percapita", "n_clicks"),
    State('caf-renda-ano', 'value'),
    State('caf-renda-mes', 'value'),
    prevent_initial_call=True
)
def download_caf_renda_qtd_percapita(n_clicks, ano, mes):
    agg, prod, col = agrega_renda(filter_df(dados_caf.get('renda_qtd', pd.DataFrame()), ano, mes), 'percapita')
    if agg is not None:
        agg = agg.rename(columns={col: 'Média per capita: ' + col})
        return dcc.send_data_frame(agg.to_csv, "caf_renda_quantidade_percapita_df.csv", index=False)
    return None
