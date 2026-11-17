import dash
from dash import html, dcc
import plotly.express as px

# Paletas acessíveis a daltônicos (Viridis, Cividis, Tealrose, High Contrast)
VIRIDIS_PALETTE = px.colors.sequential.Viridis
CIVIDIS_PALETTE = px.colors.sequential.Cividis
ACCESSIBLE_COLORS = ['#004d40', '#00796b', '#009688', '#26a69a', '#80cbc4', '#b2dfdb', '#e0f2f1']
ACCESSIBLE_DIVERGING = ['#00405e', '#0077b6', '#0096c7', '#03045e', '#57cc99', '#38b000', '#70e000']

def render_institutional_banner(extra_text=None):
    """
    Retorna o banner institucional transparente sobre a realidade do Distrito Federal.
    """
    return html.Div(
        className="w-full bg-amber-50 dark:bg-amber-950/40 border border-amber-300 dark:border-amber-700/60 rounded-xl p-4 md:p-5 mb-8 text-amber-950 dark:text-amber-100 flex gap-4 items-start shadow-sm font-public-sans",
        children=[
            html.Span("warning", className="material-symbols-outlined text-amber-600 dark:text-amber-400 text-2xl shrink-0 mt-0.5"),
            html.Div(className="text-sm leading-relaxed", children=[
                html.P(className="font-bold text-amber-950 dark:text-amber-100 mb-1", children=[
                    "Nota Metodológica & Realidade Institucional do DF:"
                ]),
                html.P(
                    "O Distrito Federal é tratado como um único município pelo IBGE e Banco Central. As bases de Crédito Rural (MCDR) e CAF não descem nativamente ao nível de Região Administrativa (RA). O painel AgroTec-DF foi projetado estritamente para o suporte institucional a gestores e extensionistas (EMATER-DF, IPEDF, SEAGRI-DF)."
                ),
                html.P(extra_text, className="mt-1 font-medium") if extra_text else None
            ])
        ]
    )

def render_chart_footer(source="IBGE", ref_date="2024", note="Dados sujeitos a revisões oficiais.", download_id=None):
    """
    Retorna a nota de rastreabilidade, fonte, data de referência e o botão de download em CSV.
    """
    children = [
        html.Div(className="flex flex-col sm:flex-row sm:items-center justify-between gap-3 text-xs text-slate-500 dark:text-slate-400 pt-3 border-t border-slate-200 dark:border-slate-800 font-public-sans", children=[
            html.Div(className="flex flex-wrap items-center gap-x-4 gap-y-1", children=[
                html.Span(children=[html.Strong("Fonte: "), source]),
                html.Span(children=[html.Strong("Data Ref.: "), ref_date]),
                html.Span(children=[html.Strong("Nota: "), note])
            ]),
            html.Div(children=[
                html.Button(
                    id=download_id,
                    className="flex items-center gap-1.5 text-xs font-semibold text-emerald-800 dark:text-emerald-300 hover:text-emerald-950 dark:hover:text-emerald-100 bg-emerald-50 dark:bg-emerald-950/60 hover:bg-emerald-100 dark:hover:bg-emerald-900 border border-emerald-300 dark:border-emerald-700 px-2.5 py-1.5 rounded-lg transition-colors cursor-pointer",
                    children=[
                        html.Span("download", className="material-symbols-outlined text-sm"),
                        html.Span("Baixar CSV")
                    ]
                ) if download_id else None
            ])
        ])
    ]
    if download_id:
        children.append(dcc.Download(id=f"dcc-{download_id}"))
        
    return html.Div(children=children)
