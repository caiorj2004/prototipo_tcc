import dash
from dash import html, dcc
import plotly.graph_objects as go
import plotly.express as px
import pandas as pd
import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from data_pipeline_mcdr import load_mcdr_data

dash.register_page(__name__, path='/credito-rural', name='Crédito Rural (MCDR)')

# Carregar os dados reais
dados_mcdr = load_mcdr_data()

# ==========================================
# Helpers para Gráficos
# ==========================================

# 1. Distribuição do Crédito por Finalidade
fig_finalidade = go.Figure()
df_finalidade = dados_mcdr.get('finalidade', pd.DataFrame())
if not df_finalidade.empty:
    fig_finalidade.add_trace(go.Pie(
        labels=df_finalidade['Finalidade'], 
        values=df_finalidade['Valor'], 
        hole=0.5, 
        marker=dict(colors=['#2b2d42', '#8d99ae', '#ef233c', '#d90429'])
    ))
fig_finalidade.update_layout(margin=dict(t=10, b=10, l=10, r=10), paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)')

# 2. Concentração Bancária (Top Instituições)
fig_if = go.Figure()
df_if = dados_mcdr.get('if', pd.DataFrame())
if not df_if.empty:
    # Selecionar os top 15 (como está sorted ascending, pegamos o tail)
    df_if_top = df_if.tail(15)
    fig_if.add_trace(go.Bar(
        y=df_if_top['NOMEIF'], 
        x=df_if_top['VALORTOTAL'], 
        orientation='h', 
        marker_color='#2b2d42'
    ))
fig_if.update_layout(
    margin=dict(t=10, b=10, l=10, r=10), 
    paper_bgcolor='rgba(0,0,0,0)', 
    plot_bgcolor='rgba(0,0,0,0)',
    xaxis=dict(title="Valor Total (R$)", tickformat='~s')
)

# 3. Crédito por Categoria Financeira e Atividade
fig_cat = go.Figure()
df_cat = dados_mcdr.get('categoria', pd.DataFrame())
if not df_cat.empty:
    # Separar por atividade
    atividades = df_cat['ATIVIDADE'].unique()
    colors = ['#ef233c', '#8d99ae', '#2b2d42', '#edf2f4']
    for i, atividade in enumerate(atividades):
        df_sub = df_cat[df_cat['ATIVIDADE'] == atividade]
        fig_cat.add_trace(go.Bar(
            x=df_sub['NOMESEGMENTOCATEGORIA'],
            y=df_sub['VALORTOTAL'],
            name=atividade,
            marker_color=colors[i % len(colors)]
        ))
fig_cat.update_layout(
    barmode='group', 
    margin=dict(t=10, b=10, l=10, r=10), 
    paper_bgcolor='rgba(0,0,0,0)', 
    plot_bgcolor='rgba(0,0,0,0)',
    yaxis=dict(title="Valor Total (R$)", tickformat='~s'),
    legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
)

# 4. Dispersão: Intensidade de Capital (Valor vs Área)
fig_disp = go.Figure()
df_disp = dados_mcdr.get('dispersao', pd.DataFrame())
if not df_disp.empty:
    atividades = df_disp['ATIVIDADE'].unique()
    colors = ['#ef233c', '#2b2d42', '#8d99ae', '#d90429']
    
    # Calcular tamanho relativo da bolha
    max_qtd = df_disp['QTDTOTAL'].max()
    
    for i, atividade in enumerate(atividades):
        df_sub = df_disp[df_disp['ATIVIDADE'] == atividade]
        fig_disp.add_trace(go.Scatter(
            x=df_sub['AREATOTAL'],
            y=df_sub['VALORTOTAL'],
            mode='markers',
            name=atividade,
            marker=dict(
                size=df_sub['QTDTOTAL'],
                sizemode='area',
                sizeref=2.*max_qtd/(40.**2) if max_qtd > 0 else 1,
                sizemin=4,
                color=colors[i % len(colors)],
                opacity=0.6,
                line=dict(width=1, color='white')
            )
        ))
fig_disp.update_layout(
    margin=dict(t=10, b=10, l=10, r=10), 
    paper_bgcolor='rgba(0,0,0,0)', 
    plot_bgcolor='rgba(0,0,0,0)',
    xaxis=dict(title="Área Total (Hectares)", tickformat='~s', type='log'),
    yaxis=dict(title="Valor Total (R$)", tickformat='~s', type='log'),
    legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
)

# ==========================================
# Layout da Página
# ==========================================

layout = html.Div(className="w-full p-6 md:p-8 bg-background", children=[
    
    # Header
    html.Div(className="mb-8 flex items-end justify-between", children=[
        html.Div([
            html.H1("Crédito Rural (MCDR)", className="font-h1 text-h1 text-primary"),
            html.P("Painel de distribuição, concentração bancária e intensidade de capital do crédito rural.", className="font-body-lg text-body-lg text-on-surface-variant mt-2")
        ]),
        html.Div(className="flex items-center gap-2 text-sm text-on-surface-variant font-data-tabular", children=[
            html.Span("account_balance", className="material-symbols-outlined text-[18px]"),
            html.Span("Fonte: Matriz de Crédito Rural (Distrito Federal)")
        ])
    ]),
    
    # Linha 1: Finalidade e Concentração Bancária
    html.Div(className="grid grid-cols-1 lg:grid-cols-2 gap-6 w-full mb-6", children=[
        html.Div(className="bg-surface-container-lowest border border-outline-variant rounded-xl p-card-padding flex flex-col", children=[
            html.H3("Distribuição do Crédito por Finalidade", className="font-label-lg text-on-surface mb-2"),
            html.Div(className="flex-1 min-h-[300px]", children=[
                dcc.Graph(figure=fig_finalidade, style={'height': '100%', 'width': '100%'})
            ])
        ]),
        html.Div(className="bg-surface-container-lowest border border-outline-variant rounded-xl p-card-padding flex flex-col", children=[
            html.H3("Concentração Bancária (Top 15 Instituições)", className="font-label-lg text-on-surface mb-2"),
            html.Div(className="flex-1 min-h-[300px]", children=[
                dcc.Graph(figure=fig_if, style={'height': '100%', 'width': '100%'})
            ])
        ])
    ]),
    
    # Linha 2: Categoria e Atividade
    html.Div(className="w-full mb-6 bg-surface-container-lowest border border-outline-variant rounded-xl p-card-padding flex flex-col", children=[
        html.H3("Crédito por Categoria Financeira e Atividade", className="font-label-lg text-on-surface mb-2"),
        html.Div(className="flex-1 min-h-[350px]", children=[
            dcc.Graph(figure=fig_cat, style={'height': '100%', 'width': '100%'})
        ])
    ]),
    
    # Linha 3: Dispersão (Capital vs Área)
    html.Div(className="w-full mb-8 bg-surface-container-lowest border border-outline-variant rounded-xl p-card-padding flex flex-col", children=[
        html.H3("Intensidade de Capital: Valor Total vs Área Total", className="font-label-lg text-on-surface mb-2"),
        html.Div(className="flex-1 min-h-[450px]", children=[
            dcc.Graph(figure=fig_disp, style={'height': '100%', 'width': '100%'})
        ])
    ])
])
