import dash
from dash import html, dcc, dash_table
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

# ==========================================
# Helpers para Gráficos
# ==========================================

# 1. Geral (Pessoa Física vs Pessoa Jurídica)
fig_geral = go.Figure()
df_geral = dados_caf.get('geral', pd.DataFrame())
if not df_geral.empty:
    labels = ['Pessoa Física', 'Pessoa Jurídica']
    values = [df_geral['PESSOA FISICA'].sum(), df_geral['PESSOA JURIDICA'].sum()]
    fig_geral.add_trace(go.Pie(labels=labels, values=values, hole=0.5, marker=dict(colors=['#2b2d42', '#8d99ae'])))
fig_geral.update_layout(margin=dict(t=10, b=10, l=10, r=10), paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)')

# 2. Caracterização (Minorias e Perfil)
fig_carac = go.Figure()
df_carac = dados_caf.get('caracterizacao', pd.DataFrame())
if not df_carac.empty:
    # Identificar as colunas de métrica dinamicamente para evitar problemas de encoding ('MUNICÍPIO', 'UF', 'IBGE', 'TOTAL')
    cols_ignore = ['UF', 'IBGE', 'TOTAL']
    cols_metrics = [c for c in df_carac.columns if c not in cols_ignore and 'MUNIC' not in c.upper()]
    
    # Agregar caso existam múltiplas linhas
    vals = df_carac[cols_metrics].sum()
    # Ordenar por valor
    vals = vals.sort_values(ascending=True)
    
    fig_carac.add_trace(go.Bar(x=vals.values, y=vals.index, orientation='h', marker_color='#ef233c'))
fig_carac.update_layout(margin=dict(t=10, b=10, l=10, r=10), paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)')

# 3. Gênero Global
fig_genero_global = go.Figure()
df_genero = dados_caf.get('genero_jovens', pd.DataFrame())
if not df_genero.empty:
    labels = ['Mulheres', 'Homens']
    values = [df_genero['Mulheres'].sum(), df_genero['Homens'].sum()]
    fig_genero_global.add_trace(go.Pie(labels=labels, values=values, hole=0.6, marker=dict(colors=['#c77dff', '#3c096c'])))
fig_genero_global.update_layout(margin=dict(t=10, b=10, l=10, r=10), paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', showlegend=True)

# 4. Jovens por Gênero
fig_genero_jovens = go.Figure()
if not df_genero.empty:
    labels = ['Mulheres Jovens', 'Homens Jovens']
    # Identificar colunas corretas
    col_mulheres_jovens = [c for c in df_genero.columns if 'Mulheres jovens' in c][0]
    col_homens_jovens = [c for c in df_genero.columns if 'Homens jovens' in c][0]
    
    values = [df_genero[col_mulheres_jovens].sum(), df_genero[col_homens_jovens].sum()]
    fig_genero_jovens.add_trace(go.Bar(x=labels, y=values, marker_color=['#9d4edd', '#5a189a']))
fig_genero_jovens.update_layout(margin=dict(t=10, b=10, l=10, r=10), paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', showlegend=False)

# 5. Atividade
fig_atividade = go.Figure()
df_atividade = dados_caf.get('atividade', pd.DataFrame())
if not df_atividade.empty:
    cols_ignore = ['UF', 'IBGE', 'TOTAL']
    cols_metrics = [c for c in df_atividade.columns if c not in cols_ignore and 'MUNIC' not in c.upper()]
    vals = df_atividade[cols_metrics].sum().sort_values(ascending=False)
    fig_atividade.add_trace(go.Bar(x=vals.index, y=vals.values, marker_color='#2d6a4f'))
fig_atividade.update_layout(margin=dict(t=10, b=10, l=10, r=10), paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)')

# 6. Renda (Valor Total vs Mediana) - VALOR TOTAL
fig_renda_valor = go.Figure()
df_renda_valor = dados_caf.get('renda_valor', pd.DataFrame())
if not df_renda_valor.empty:
    produtos = df_renda_valor['Produto'].tolist()
    col_producao = [c for c in df_renda_valor.columns if 'total' in c.lower() and 'mediana' not in c.lower()][0]
    col_mediana = [c for c in df_renda_valor.columns if 'mediana' in c.lower()][0]
    
    fig_renda_valor.add_trace(go.Bar(x=produtos, y=df_renda_valor[col_producao], name='Produção Total (R$)', marker_color='#023e8a'))
    fig_renda_valor.add_trace(go.Bar(x=produtos, y=df_renda_valor[col_mediana], name='Mediana (R$)', marker_color='#48cae4'))
fig_renda_valor.update_layout(barmode='group', margin=dict(t=10, b=10, l=10, r=10), paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1))

# 7. Renda (Valor Total vs Mediana) - QUANTIDADE DE CADASTROS
fig_renda_qtd = go.Figure()
df_renda_qtd = dados_caf.get('renda_qtd', pd.DataFrame())
if not df_renda_qtd.empty:
    produtos = df_renda_qtd['Produto'].tolist()
    col_producao = [c for c in df_renda_qtd.columns if 'total' in c.lower() and 'mediana' not in c.lower()][0]
    col_mediana = [c for c in df_renda_qtd.columns if 'mediana' in c.lower()][0]
    
    fig_renda_qtd.add_trace(go.Bar(x=produtos, y=df_renda_qtd[col_producao], name='Produção Total (R$)', marker_color='#1b4965'))
    fig_renda_qtd.add_trace(go.Bar(x=produtos, y=df_renda_qtd[col_mediana], name='Mediana (R$)', marker_color='#62b6cb'))
fig_renda_qtd.update_layout(barmode='group', margin=dict(t=10, b=10, l=10, r=10), paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1))

# ==========================================
# Layout da Página
# ==========================================

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
    
    # Linha 1: Geral e Caracterização
    html.Div(className="grid grid-cols-1 xl:grid-cols-2 gap-6 w-full mb-6", children=[
        html.Div(className="bg-surface-container-lowest border border-outline-variant rounded-xl p-card-padding flex flex-col", children=[
            html.H3("Geral: Pessoa Física vs Jurídica", className="font-label-lg text-on-surface mb-2"),
            html.Div(className="flex-1 min-h-[300px]", children=[
                dcc.Graph(figure=fig_geral, style={'height': '100%', 'width': '100%'})
            ])
        ]),
        html.Div(className="bg-surface-container-lowest border border-outline-variant rounded-xl p-card-padding flex flex-col", children=[
            html.H3("Caracterização: Minorias e Assentados", className="font-label-lg text-on-surface mb-2"),
            html.Div(className="flex-1 min-h-[300px]", children=[
                dcc.Graph(figure=fig_carac, style={'height': '100%', 'width': '100%'})
            ])
        ])
    ]),
    
    # Linha 2: Gênero, Jovens e Atividade
    html.Div(className="grid grid-cols-1 md:grid-cols-3 gap-6 w-full mb-6", children=[
        html.Div(className="bg-surface-container-lowest border border-outline-variant rounded-xl p-card-padding flex flex-col", children=[
            html.H3("Gênero Global", className="font-label-lg text-on-surface mb-2 text-center"),
            html.Div(className="flex-1 min-h-[250px]", children=[
                dcc.Graph(figure=fig_genero_global, style={'height': '100%', 'width': '100%'})
            ])
        ]),
        html.Div(className="bg-surface-container-lowest border border-outline-variant rounded-xl p-card-padding flex flex-col", children=[
            html.H3("Distribuição de Jovens (16-29)", className="font-label-lg text-on-surface mb-2 text-center"),
            html.Div(className="flex-1 min-h-[250px]", children=[
                dcc.Graph(figure=fig_genero_jovens, style={'height': '100%', 'width': '100%'})
            ])
        ]),
        html.Div(className="bg-surface-container-lowest border border-outline-variant rounded-xl p-card-padding flex flex-col", children=[
            html.H3("Áreas de Atividade", className="font-label-lg text-on-surface mb-2 text-center"),
            html.Div(className="flex-1 min-h-[250px]", children=[
                dcc.Graph(figure=fig_atividade, style={'height': '100%', 'width': '100%'})
            ])
        ])
    ]),
    
    # Linha 3: Renda
    html.Div(className="grid grid-cols-1 xl:grid-cols-2 gap-6 w-full mb-8", children=[
        html.Div(className="bg-surface-container-lowest border border-outline-variant rounded-xl p-card-padding flex flex-col", children=[
            html.H3("Produção e Mediana (Por Valor Total de Produção)", className="font-label-lg text-on-surface mb-2"),
            html.Div(className="flex-1 min-h-[350px]", children=[
                dcc.Graph(figure=fig_renda_valor, style={'height': '100%', 'width': '100%'})
            ])
        ]),
        html.Div(className="bg-surface-container-lowest border border-outline-variant rounded-xl p-card-padding flex flex-col", children=[
            html.H3("Produção e Mediana (Por Quantidade de Cadastros)", className="font-label-lg text-on-surface mb-2"),
            html.Div(className="flex-1 min-h-[350px]", children=[
                dcc.Graph(figure=fig_renda_qtd, style={'height': '100%', 'width': '100%'})
            ])
        ])
    ]),
    
    # DataTables
    html.Div(className="w-full mb-6", children=[
        html.H2("Detalhamento Institucional", className="font-h3 text-h3 text-primary mb-4"),
        html.Div(className="grid grid-cols-1 gap-6 w-full", children=[
            # Pessoa Jurídica
            html.Div(className="bg-surface-container-lowest border border-outline-variant rounded-xl p-card-padding flex flex-col overflow-hidden", children=[
                html.H3("Pessoas Jurídicas Registradas", className="font-label-lg text-on-surface mb-4"),
                dash_table.DataTable(
                    data=dados_caf.get('pj', pd.DataFrame()).to_dict('records') if not dados_caf.get('pj', pd.DataFrame()).empty else [],
                    columns=[{"name": i, "id": i} for i in dados_caf.get('pj', pd.DataFrame()).columns] if not dados_caf.get('pj', pd.DataFrame()).empty else [],
                    page_size=10,
                    style_table={'overflowX': 'auto', 'width': '100%'},
                    style_header={'backgroundColor': '#f1f5f9', 'color': 'black', 'fontWeight': 'bold'},
                    style_data={'backgroundColor': 'white', 'color': 'black'},
                    style_cell={'textAlign': 'left', 'padding': '10px', 'fontFamily': 'Public Sans, sans-serif'}
                )
            ]),
            # Entidades
            html.Div(className="bg-surface-container-lowest border border-outline-variant rounded-xl p-card-padding flex flex-col overflow-hidden", children=[
                html.H3("Entidades Emissoras", className="font-label-lg text-on-surface mb-4"),
                dash_table.DataTable(
                    data=dados_caf.get('entidade', pd.DataFrame()).to_dict('records') if not dados_caf.get('entidade', pd.DataFrame()).empty else [],
                    columns=[{"name": i, "id": i} for i in dados_caf.get('entidade', pd.DataFrame()).columns] if not dados_caf.get('entidade', pd.DataFrame()).empty else [],
                    page_size=10,
                    style_table={'overflowX': 'auto', 'width': '100%'},
                    style_header={'backgroundColor': '#f1f5f9', 'color': 'black', 'fontWeight': 'bold'},
                    style_data={'backgroundColor': 'white', 'color': 'black'},
                    style_cell={'textAlign': 'left', 'padding': '10px', 'fontFamily': 'Public Sans, sans-serif'}
                )
            ])
        ])
    ])
])
