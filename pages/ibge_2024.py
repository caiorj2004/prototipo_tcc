import dash
from dash import html, dcc
import plotly.express as px
from data_pipeline_2024 import load_data_2024

dash.register_page(__name__, path='/ibge', name='IBGE 2024')

# Carrega os dados
dados = load_data_2024()
df_agri = dados['agricultura']
df_pec = dados['pecuaria']

# 1. Gráfico Agricultura (Top 10)
top10_agri = df_agri.head(10).sort_values(by='Valor', ascending=True)
fig_agri = px.bar(
    top10_agri, 
    x='Valor', 
    y='Produto', 
    orientation='h',
    text='Valor',
    color_discrete_sequence=['#1b4332']
)
fig_agri.update_traces(texttemplate='R$ %{text:,.0f}', textposition='outside')
fig_agri.update_layout(
    margin=dict(t=20, l=10, r=60, b=10), 
    paper_bgcolor='rgba(0,0,0,0)', 
    plot_bgcolor='rgba(0,0,0,0)',
    xaxis_title="Valor de Produção (R$)",
    yaxis_title="",
    separators=".,", # Usa ponto para milhar e vírgula para decimal no Brasil
    font=dict(family="Public Sans")
)

# 2. Gráfico Pecuária (Barras Horizontais com Escala Logarítmica)
df_pec_sorted = df_pec.sort_values(by='Valor', ascending=True)
fig_pec = px.bar(
    df_pec_sorted,
    x='Valor',
    y='Produto',
    orientation='h',
    text='Valor',
    log_x=True, # Escala logarítmica para evidenciar rebanhos menores frente aos Galináceos
    color_discrete_sequence=['#00405e']
)
fig_pec.update_traces(texttemplate='%{text:,.0f}', textposition='outside')
fig_pec.update_layout(
    margin=dict(t=20, l=10, r=60, b=10), 
    paper_bgcolor='rgba(0,0,0,0)',
    plot_bgcolor='rgba(0,0,0,0)',
    xaxis_title="Número de Cabeças (Escala Log)",
    yaxis_title="",
    separators=".,",
    font=dict(family="Public Sans")
)

# Layout da Página
layout = html.Div(className="w-full p-6 md:p-8 bg-background", children=[
    
    # Page Header
    html.Div(className="mb-8 flex items-end justify-between", children=[
        html.Div([
            html.H1("Produção Agrícola e Pecuária", className="font-h1 text-h1 text-primary"),
            html.P("Análise de faturamento das culturas e efetivo de rebanhos no DF.", className="font-body-lg text-body-lg text-on-surface-variant mt-2")
        ]),
        html.Div(className="flex items-center gap-2 text-sm text-on-surface-variant font-data-tabular", children=[
            html.Span("calendar_today", className="material-symbols-outlined text-[18px]"),
            html.Span("Fonte: IBGE/PAM e PPM 2024")
        ])
    ]),
    
    # Grid de 2 Colunas
    html.Div(className="grid grid-cols-1 xl:grid-cols-2 gap-6 w-full pb-12", children=[
        
        # Coluna 1: Agricultura
        html.Div(className="w-full bg-surface-container-lowest border border-outline-variant rounded-xl flex flex-col relative overflow-hidden", children=[
            html.Div(className="p-card-padding border-b border-surface-variant flex justify-between items-center", children=[
                html.Div([
                    html.H2("Top 10 Culturas por Faturamento", className="font-h3 text-h3 text-primary"),
                    html.P("Valor de produção das lavouras em R$.", className="font-data-tabular text-data-tabular text-on-surface-variant mt-1")
                ]),
                html.Button(html.Span("local_florist", className="material-symbols-outlined"), className="text-[#1b4332] bg-[#a5d0b9]/30 p-2 rounded-lg cursor-default")
            ]),
            html.Div(className="p-card-padding flex-1 min-h-[400px] flex flex-col justify-end relative bg-surface-container-low/30", children=[
                dcc.Graph(figure=fig_agri, style={'height': '100%', 'width': '100%'})
            ])
        ]),
        
        # Coluna 2: Pecuária
        html.Div(className="w-full bg-surface-container-lowest border border-outline-variant rounded-xl flex flex-col relative overflow-hidden", children=[
            html.Div(className="p-card-padding border-b border-surface-variant flex justify-between items-center", children=[
                html.Div([
                    html.H2("Distribuição do Efetivo de Animais", className="font-h3 text-h3 text-primary"),
                    html.P("Número de cabeças por tipo de rebanho.", className="font-data-tabular text-data-tabular text-on-surface-variant mt-1")
                ]),
                html.Button(html.Span("cruelty_free", className="material-symbols-outlined"), className="text-[#00405e] bg-[#c9e6ff]/50 p-2 rounded-lg cursor-default")
            ]),
            html.Div(className="p-card-padding flex-1 min-h-[400px] flex flex-col justify-end relative bg-surface-container-low/30", children=[
                dcc.Graph(figure=fig_pec, style={'height': '100%', 'width': '100%'})
            ])
        ])
    ])
])
