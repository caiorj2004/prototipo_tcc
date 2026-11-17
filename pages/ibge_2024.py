import dash
from dash import html, dcc, callback, Input, Output
import plotly.express as px
import pandas as pd
import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from data_pipeline_2024 import load_data_2024
from components import render_chart_footer, VIRIDIS_PALETTE, CIVIDIS_PALETTE

dash.register_page(__name__, path='/ibge', name='IBGE 2024')

# Carrega os dados otimizados em Parquet
dados = load_data_2024()
df_agri = dados['agricultura']
df_pec = dados['pecuaria']

# 1. Gráfico Agricultura (Top 10) com paleta acessível Viridis
top10_agri = df_agri.head(10).sort_values(by='Valor', ascending=True)
fig_agri = px.bar(
    top10_agri, 
    x='Valor', 
    y='Produto', 
    orientation='h',
    text='Valor',
    color='Valor',
    color_continuous_scale='Viridis'
)
fig_agri.update_traces(texttemplate='R$ %{text:,.0f}', textposition='outside')
fig_agri.update_layout(
    margin=dict(t=20, l=10, r=60, b=10), 
    paper_bgcolor='rgba(0,0,0,0)', 
    plot_bgcolor='rgba(0,0,0,0)',
    xaxis_title="Valor de Produção (R$)",
    yaxis_title="",
    coloraxis_showscale=False,
    separators=".,",
    font=dict(family="Public Sans")
)

# 2. Gráfico Pecuária com paleta Cividis
df_pec_sorted = df_pec.sort_values(by='Valor', ascending=True)
fig_pec = px.bar(
    df_pec_sorted,
    x='Valor',
    y='Produto',
    orientation='h',
    text='Valor',
    log_x=True,
    color='Valor',
    color_continuous_scale='Cividis'
)
fig_pec.update_traces(texttemplate='%{text:,.0f}', textposition='outside')
fig_pec.update_layout(
    margin=dict(t=20, l=10, r=60, b=10), 
    paper_bgcolor='rgba(0,0,0,0)',
    plot_bgcolor='rgba(0,0,0,0)',
    xaxis_title="Número de Cabeças (Escala Log)",
    yaxis_title="",
    coloraxis_showscale=False,
    separators=".,",
    font=dict(family="Public Sans")
)

# Layout da Página
layout = html.Div(className="w-full p-6 md:p-8 bg-background font-public-sans", children=[
    
    # Page Header com especificidade do dataset
    html.Div(className="mb-8 flex flex-col md:flex-row md:items-end justify-between gap-4", children=[
        html.Div([
            html.H1("Produção Agrícola e Pecuária (IBGE 2024)", className="text-2xl md:text-3xl font-bold text-primary tracking-tight"),
            html.P("Estimativas oficiais de faturamento das culturas (PAM) e efetivo de rebanhos (PPM) agregadas para o Distrito Federal (IBGE 2024).", className="text-sm md:text-base text-on-surface-variant mt-2")
        ]),
        html.Div(className="flex items-center gap-2 text-sm text-on-surface-variant font-data-tabular shrink-0", children=[
            html.Span("calendar_today", className="material-symbols-outlined text-[18px] text-emerald-700 dark:text-emerald-400"),
            html.Span("Fonte: IBGE/PAM e PPM 2024")
        ])
    ]),
    
    # Grid de 2 Colunas
    html.Div(className="grid grid-cols-1 xl:grid-cols-2 gap-6 w-full pb-12", children=[
        
        # Coluna 1: Agricultura
        html.Div(className="w-full bg-surface-container-lowest border border-outline-variant rounded-xl flex flex-col relative overflow-hidden shadow-sm p-card-padding", children=[
            html.Div(className="border-b border-surface-variant pb-4 flex justify-between items-center mb-4", children=[
                html.Div([
                    html.H2("Top 10 Culturas por Faturamento", className="text-lg font-bold text-primary"),
                    html.P("Valor de produção das lavouras em R$.", className="text-xs text-on-surface-variant mt-0.5")
                ]),
                html.Button(html.Span("local_florist", className="material-symbols-outlined"), className="text-emerald-800 bg-emerald-100 dark:bg-emerald-950 p-2 rounded-lg cursor-default")
            ]),
            html.Div(className="flex-1 min-h-[380px] flex flex-col justify-end relative bg-surface-container-low/30 rounded-lg p-2 mb-4", children=[
                dcc.Graph(figure=fig_agri, style={'height': '100%', 'width': '100%'})
            ]),
            render_chart_footer(source="IBGE / PAM 2024", ref_date="2024", note="Pesquisa Agrícola Municipal.", download_id="btn-download-agri-2024")
        ]),
        
        # Coluna 2: Pecuária
        html.Div(className="w-full bg-surface-container-lowest border border-outline-variant rounded-xl flex flex-col relative overflow-hidden shadow-sm p-card-padding", children=[
            html.Div(className="border-b border-surface-variant pb-4 flex justify-between items-center mb-4", children=[
                html.Div([
                    html.H2("Distribuição do Efetivo de Animais", className="text-lg font-bold text-primary"),
                    html.P("Número de cabeças por tipo de rebanho.", className="text-xs text-on-surface-variant mt-0.5")
                ]),
                html.Button(html.Span("cruelty_free", className="material-symbols-outlined"), className="text-blue-800 bg-blue-100 dark:bg-blue-950 p-2 rounded-lg cursor-default")
            ]),
            html.Div(className="flex-1 min-h-[380px] flex flex-col justify-end relative bg-surface-container-low/30 rounded-lg p-2 mb-4", children=[
                dcc.Graph(figure=fig_pec, style={'height': '100%', 'width': '100%'})
            ]),
            render_chart_footer(source="IBGE / PPM 2024", ref_date="2024", note="Pesquisa da Pecuária Municipal.", download_id="btn-download-pec-2024")
        ])
    ])
])

# Callbacks para Download CSV
@callback(
    Output("dcc-btn-download-agri-2024", "data"),
    Input("btn-download-agri-2024", "n_clicks"),
    prevent_initial_call=True
)
def download_agri(n_clicks):
    if not df_agri.empty:
        return dcc.send_data_frame(df_agri.to_csv, "ibge_agricultura_2024.csv", index=False)
    return None

@callback(
    Output("dcc-btn-download-pec-2024", "data"),
    Input("btn-download-pec-2024", "n_clicks"),
    prevent_initial_call=True
)
def download_pec(n_clicks):
    if not df_pec.empty:
        return dcc.send_data_frame(df_pec.to_csv, "ibge_pecuaria_2024.csv", index=False)
    return None
