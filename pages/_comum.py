"""Componentes de interface compartilhados pelas páginas do TCC."""
from dash import html, dcc
import plotly.graph_objects as go

FONTE = dict(family='Public Sans, sans-serif', size=12, color='#191c1c')

def cabecalho(titulo, subtitulo):
    return html.Div(className="mb-6", children=[
        html.H1(titulo, className="font-h1 text-h1 text-primary text-2xl font-bold"),
        html.P(subtitulo, className="text-on-surface-variant text-sm mt-1 max-w-4xl"),
    ])

def cartao(titulo, *filhos, nota=None, cls=""):
    return html.Div(className=f"bg-white border border-outline-variant rounded-xl p-5 {cls}", children=[
        html.H3(titulo, className="font-semibold text-primary text-base mb-3"),
        *filhos,
        html.P(nota, className="text-xs text-on-surface-variant mt-2") if nota else None,
    ])

def kpi(valor, rotulo):
    return html.Div(className="bg-white border border-outline-variant rounded-xl p-4", children=[
        html.Div(valor, className="text-2xl font-bold text-primary"),
        html.Div(rotulo, className="text-xs text-on-surface-variant mt-1"),
    ])

def aviso(texto, titulo="Como ler"):
    return html.Div(className="border-l-4 border-secondary bg-secondary-fixed/40 rounded p-4 text-sm text-on-secondary-fixed-variant", children=[
        html.Strong(titulo + ": "), texto])

def grafico(fig, altura=360):
    fig.update_layout(font=FONTE, paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', margin=dict(t=30, b=40, l=10, r=10), height=altura)
    return dcc.Graph(figure=fig, config={'displaylogo': False, 'responsive': True})

def tabela(df, colunas=None):
    df = df if colunas is None else df[colunas]
    return html.Div(className="overflow-x-auto", children=html.Table(className="w-full text-sm", children=[
        html.Thead(html.Tr([html.Th(c, className="text-left px-2 py-1 border-b border-outline-variant text-on-surface-variant font-medium") for c in df.columns])),
        html.Tbody([html.Tr([html.Td(v, className="px-2 py-1 border-b border-surface-variant") for v in row]) for row in df.itertuples(index=False)]),
    ]))

def rodape_fonte(texto):
    return html.P(texto, className="text-xs text-on-surface-variant mt-8")
