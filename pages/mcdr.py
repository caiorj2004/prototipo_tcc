import dash
from dash import html, dcc, callback, Input, Output, State
import plotly.graph_objects as go
import plotly.express as px
import pandas as pd
import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from data_pipeline_mcdr import load_mcdr_data
from components import render_chart_footer

dash.register_page(__name__, path='/credito-rural', name='Crédito Rural (MCDR)')

df_mcdr = load_mcdr_data()

anos_options = [{'label': 'Todos', 'value': 'ALL'}]
if not df_mcdr.empty and 'ANO' in df_mcdr.columns:
    anos = sorted([a for a in df_mcdr['ANO'].unique() if str(a) != 'Desconhecido'], reverse=True)
    anos_options += [{'label': str(a), 'value': str(a)} for a in anos]

layout = html.Div(className="w-full p-6 md:p-8 bg-background font-public-sans", children=[
    
    # Header com especificidade do dataset
    html.Div(className="mb-8 flex flex-col md:flex-row md:items-end justify-between gap-4", children=[
        html.Div([
            html.H1("Crédito Rural (MCDR)", className="text-2xl md:text-3xl font-bold text-primary tracking-tight"),
            html.P("Painel de distribuição, concentração bancária e intensidade de capital do crédito rural contratado no Distrito Federal (Banco Central / MCDR).", className="text-sm md:text-base text-on-surface-variant mt-2")
        ]),
        html.Div(className="flex items-center gap-2 text-sm text-on-surface-variant font-data-tabular shrink-0", children=[
            html.Span("account_balance", className="material-symbols-outlined text-[18px] text-emerald-700 dark:text-emerald-400"),
            html.Span("Fonte: Banco Central / MCDR (DF)")
        ])
    ]),
    
    # Global Filters
    html.Div(className="w-full bg-surface-container-lowest border border-outline-variant rounded-xl p-card-padding mb-8 flex flex-wrap items-center gap-6 shadow-sm", children=[
        html.Div(className="flex items-center gap-4", children=[
            html.Label("Ano:", className="font-label-sm text-label-sm text-on-surface-variant uppercase tracking-wider"),
            html.Div(className="w-32", children=[
                dcc.Dropdown(
                    id='mcdr-ano-dropdown',
                    options=anos_options,
                    value='ALL',
                    clearable=False,
                    className="font-public-sans text-sm"
                )
            ])
        ])
    ]),
    
    # Linha 1: Finalidade e Concentração Bancária
    html.Div(className="grid grid-cols-1 lg:grid-cols-2 gap-6 w-full mb-6", children=[
        html.Div(className="bg-surface-container-lowest border border-outline-variant rounded-xl p-card-padding flex flex-col shadow-sm", children=[
            html.H3("Distribuição do Crédito por Finalidade", className="font-bold text-slate-900 dark:text-white mb-2"),
            html.Div(className="flex-1 min-h-[300px] mb-2", children=[
                dcc.Graph(id='mcdr-finalidade-pie', style={'height': '100%', 'width': '100%'})
            ]),
            render_chart_footer(source="BCB / MCDR", ref_date="2024", note="Finalidade do crédito contratado.", download_id="btn-download-mcdr-finalidade")
        ]),
        html.Div(className="bg-surface-container-lowest border border-outline-variant rounded-xl p-card-padding flex flex-col shadow-sm", children=[
            html.H3("Concentração Bancária (Top 15 Instituições)", className="font-bold text-slate-900 dark:text-white mb-2"),
            html.Div(className="flex-1 min-h-[300px] mb-2", children=[
                dcc.Graph(id='mcdr-if-bar', style={'height': '100%', 'width': '100%'})
            ]),
            render_chart_footer(source="BCB / MCDR", ref_date="2024", note="Volume por Instituição Financeira.", download_id="btn-download-mcdr-if")
        ])
    ]),
    
    # Linha 2: Categoria e Atividade
    html.Div(className="w-full mb-6 bg-surface-container-lowest border border-outline-variant rounded-xl p-card-padding flex flex-col shadow-sm", children=[
        html.H3("Crédito por Categoria Financeira e Atividade", className="font-bold text-slate-900 dark:text-white mb-2"),
        html.Div(className="flex-1 min-h-[350px] mb-2", children=[
            dcc.Graph(id='mcdr-cat-bar', style={'height': '100%', 'width': '100%'})
        ]),
        render_chart_footer(source="BCB / MCDR", ref_date="2024", note="Segmento de categoria e ramo produtivo.", download_id="btn-download-mcdr-cat")
    ]),
    
    # Linha 3: Dispersão (Capital vs Área)
    html.Div(className="w-full mb-8 bg-surface-container-lowest border border-outline-variant rounded-xl p-card-padding flex flex-col shadow-sm", children=[
        html.H3("Intensidade de Capital: Valor Total vs Área Total", className="font-bold text-slate-900 dark:text-white mb-2"),
        html.Div(className="flex-1 min-h-[450px] mb-2", children=[
            dcc.Graph(id='mcdr-disp-scatter', style={'height': '100%', 'width': '100%'})
        ]),
        render_chart_footer(source="BCB / MCDR", ref_date="2024", note="Relação entre área financiada e montante total contratado.", download_id="btn-download-mcdr-disp")
    ])
])

def get_filtered_mcdr(ano):
    dff = df_mcdr.copy()
    if ano and ano != 'ALL' and 'ANO' in dff.columns:
        dff = dff[dff['ANO'] == str(ano)]
    return dff

@callback(
    Output('mcdr-finalidade-pie', 'figure'),
    Output('mcdr-if-bar', 'figure'),
    Output('mcdr-cat-bar', 'figure'),
    Output('mcdr-disp-scatter', 'figure'),
    Input('mcdr-ano-dropdown', 'value')
)
def update_mcdr_dashboard(ano):
    dff = get_filtered_mcdr(ano)
    empty_fig = go.Figure().update_layout(paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)')
    
    if dff.empty:
        return empty_fig, empty_fig, empty_fig, empty_fig

    # 1. Finalidade
    fig_finalidade = go.Figure()
    finalidade_data = {
        'Finalidade': ['Custeio', 'Investimento', 'Comercialização', 'Industrialização'],
        'Valor': [
            dff['VLCUSTEIO'].sum() if 'VLCUSTEIO' in dff.columns else 0,
            dff['VLINVESTIMENTO'].sum() if 'VLINVESTIMENTO' in dff.columns else 0,
            dff['VLCOMERCIALIZACAO'].sum() if 'VLCOMERCIALIZACAO' in dff.columns else 0,
            dff['VLINDUSTRIALIZACAO'].sum() if 'VLINDUSTRIALIZACAO' in dff.columns else 0
        ]
    }
    df_finalidade = pd.DataFrame(finalidade_data)
    df_finalidade = df_finalidade[df_finalidade['Valor'] > 0]
    if not df_finalidade.empty:
        fig_finalidade.add_trace(go.Pie(
            labels=df_finalidade['Finalidade'], 
            values=df_finalidade['Valor'], 
            hole=0.5, 
            marker=dict(colors=['#440154', '#3b528b', '#21908d', '#5dc963'])
        ))
    fig_finalidade.update_layout(margin=dict(t=10, b=10, l=10, r=10), paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)')

    # 2. IF
    fig_if = go.Figure()
    if 'NOMEIF' in dff.columns and 'VALORTOTAL' in dff.columns:
        df_if = dff.groupby('NOMEIF', as_index=False)['VALORTOTAL'].sum().sort_values(by='VALORTOTAL', ascending=True)
        df_if_top = df_if.tail(15)
        if not df_if_top.empty:
            fig_if.add_trace(go.Bar(
                y=df_if_top['NOMEIF'], 
                x=df_if_top['VALORTOTAL'], 
                orientation='h', 
                marker_color='#21908d'
            ))
    fig_if.update_layout(
        margin=dict(t=10, b=10, l=10, r=10), 
        paper_bgcolor='rgba(0,0,0,0)', 
        plot_bgcolor='rgba(0,0,0,0)',
        xaxis=dict(title="Valor Total (R$)", tickformat='~s'),
        font=dict(family="Public Sans")
    )

    # 3. Categoria
    fig_cat = go.Figure()
    if 'NOMESEGMENTOCATEGORIA' in dff.columns and 'ATIVIDADE' in dff.columns and 'VALORTOTAL' in dff.columns:
        df_cat = dff.groupby(['NOMESEGMENTOCATEGORIA', 'ATIVIDADE'], as_index=False)['VALORTOTAL'].sum()
        if not df_cat.empty:
            atividades = df_cat['ATIVIDADE'].unique()
            colors = ['#440154', '#3b528b', '#21908d', '#5dc963', '#fde725']
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
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
        font=dict(family="Public Sans")
    )

    # 4. Dispersão
    fig_disp = go.Figure()
    if all(c in dff.columns for c in ['VALORTOTAL', 'AREATOTAL', 'QTDTOTAL', 'ATIVIDADE']):
        df_disp = dff[['VALORTOTAL', 'AREATOTAL', 'QTDTOTAL', 'ATIVIDADE']].copy()
        df_disp = df_disp[(df_disp['VALORTOTAL'] > 0) & (df_disp['AREATOTAL'] > 0)]
        if not df_disp.empty:
            corr_val = df_disp['AREATOTAL'].corr(df_disp['VALORTOTAL'])
            corr_text = f"Correlação (r): {corr_val:.2f}" if pd.notna(corr_val) else "Correlação (r): N/A"
            
            atividades = df_disp['ATIVIDADE'].unique()
            colors = ['#440154', '#3b528b', '#21908d', '#5dc963', '#fde725']
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
                        opacity=0.7,
                        line=dict(width=1, color='white')
                    )
                ))
                
            fig_disp.add_annotation(
                x=0.02,
                y=0.98,
                xref="paper",
                yref="paper",
                text=corr_text,
                showarrow=False,
                font=dict(family="Public Sans", size=13, color="#0f172a"),
                bgcolor="rgba(255, 255, 255, 0.95)",
                bordercolor="#cbd5e1",
                borderwidth=1,
                borderpad=6,
                align="left"
            )
            
    fig_disp.update_layout(
        margin=dict(t=10, b=10, l=10, r=10), 
        paper_bgcolor='rgba(0,0,0,0)', 
        plot_bgcolor='rgba(0,0,0,0)',
        xaxis=dict(title="Área Total (Hectares)", tickformat='~s', type='log'),
        yaxis=dict(title="Valor Total (R$)", tickformat='~s', type='log'),
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
        font=dict(family="Public Sans")
    )

    return fig_finalidade, fig_if, fig_cat, fig_disp

# Callbacks de Download CSV Isolados e Granulares
@callback(
    Output("dcc-btn-download-mcdr-finalidade", "data"),
    Input("btn-download-mcdr-finalidade", "n_clicks"),
    State('mcdr-ano-dropdown', 'value'),
    prevent_initial_call=True
)
def download_mcdr_finalidade(n_clicks, ano):
    dff = get_filtered_mcdr(ano)
    if not dff.empty:
        fin_data = {
            'Finalidade': ['Custeio', 'Investimento', 'Comercialização', 'Industrialização'],
            'Valor Total (R$)': [
                dff['VLCUSTEIO'].sum() if 'VLCUSTEIO' in dff.columns else 0,
                dff['VLINVESTIMENTO'].sum() if 'VLINVESTIMENTO' in dff.columns else 0,
                dff['VLCOMERCIALIZACAO'].sum() if 'VLCOMERCIALIZACAO' in dff.columns else 0,
                dff['VLINDUSTRIALIZACAO'].sum() if 'VLINDUSTRIALIZACAO' in dff.columns else 0
            ]
        }
        df_out = pd.DataFrame(fin_data)
        return dcc.send_data_frame(df_out.to_csv, "mcdr_credito_por_finalidade.csv", index=False)
    return None

@callback(
    Output("dcc-btn-download-mcdr-if", "data"),
    Input("btn-download-mcdr-if", "n_clicks"),
    State('mcdr-ano-dropdown', 'value'),
    prevent_initial_call=True
)
def download_mcdr_if(n_clicks, ano):
    dff = get_filtered_mcdr(ano)
    if not dff.empty and 'NOMEIF' in dff.columns:
        df_if = dff.groupby('NOMEIF', as_index=False)['VALORTOTAL'].sum().sort_values(by='VALORTOTAL', ascending=False).tail(15)
        df_if.columns = ['Instituição Financeira', 'Valor Total (R$)']
        return dcc.send_data_frame(df_if.to_csv, "mcdr_concentracao_bancaria_top15.csv", index=False)
    return None

@callback(
    Output("dcc-btn-download-mcdr-cat", "data"),
    Input("btn-download-mcdr-cat", "n_clicks"),
    State('mcdr-ano-dropdown', 'value'),
    prevent_initial_call=True
)
def download_mcdr_cat(n_clicks, ano):
    dff = get_filtered_mcdr(ano)
    if not dff.empty and 'NOMESEGMENTOCATEGORIA' in dff.columns and 'ATIVIDADE' in dff.columns:
        df_cat = dff.groupby(['NOMESEGMENTOCATEGORIA', 'ATIVIDADE'], as_index=False)['VALORTOTAL'].sum()
        df_cat.columns = ['Categoria Financeira', 'Atividade', 'Valor Total (R$)']
        return dcc.send_data_frame(df_cat.to_csv, "mcdr_credito_categoria_atividade.csv", index=False)
    return None

@callback(
    Output("dcc-btn-download-mcdr-disp", "data"),
    Input("btn-download-mcdr-disp", "n_clicks"),
    State('mcdr-ano-dropdown', 'value'),
    prevent_initial_call=True
)
def download_mcdr_disp(n_clicks, ano):
    dff = get_filtered_mcdr(ano)
    if not dff.empty and all(c in dff.columns for c in ['VALORTOTAL', 'AREATOTAL', 'QTDTOTAL', 'ATIVIDADE']):
        df_disp = dff[['ATIVIDADE', 'AREATOTAL', 'VALORTOTAL', 'QTDTOTAL']].copy()
        df_disp = df_disp[(df_disp['VALORTOTAL'] > 0) & (df_disp['AREATOTAL'] > 0)]
        df_disp.columns = ['Atividade', 'Área Total (ha)', 'Valor Total (R$)', 'Qtd Contratos']
        return dcc.send_data_frame(df_disp.to_csv, "mcdr_intensidade_capital_dispersao.csv", index=False)
    return None
