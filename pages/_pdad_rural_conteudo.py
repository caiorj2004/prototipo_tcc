import dash
import numpy as np, pandas as pd
import plotly.graph_objects as go
from dash import html, dcc, Input, Output, callback
from data_pipeline_tcc import pdad, ROTULO_VAR
from pages._comum import cabecalho, cartao, kpi, aviso, grafico, tabela, rodape_fonte


P = pdad()
tot = P['totais'].iloc[0]
br = lambda x, d=0: f"{x:,.{d}f}".replace(',', 'X').replace('.', ',').replace('X', '.')
COR = ['#1b4332', '#3f6653', '#a5d0b9', '#974729']

def fig_subpop():
    d = P['subpopulacao']
    fig = go.Figure()
    fig.add_trace(go.Bar(x=d.subpopulacao, y=d['% amostra'], name='% da amostra', marker_color='#a5d0b9'))
    fig.add_trace(go.Bar(x=d.subpopulacao, y=d['% ponderado'], name='% ponderado (população)', marker_color='#1b4332'))
    fig.update_layout(barmode='group', yaxis_title='%', legend=dict(orientation='h', y=-0.2))
    return fig

def fig_ra():
    d = P['ra'].sort_values('% ponderado')
    fig = go.Figure(go.Bar(y=d.ra, x=d['% ponderado'], orientation='h', marker_color='#1b4332',
                           hovertemplate='%{y}<br>%{x:.1f}% dos domicílios (amostra: %{customdata})<extra></extra>', customdata=d.n_amostra))
    fig.update_layout(xaxis_title='% ponderado dos domicílios')
    return fig

def fig_piramide():
    d = P['piramide']
    fig = go.Figure()
    fig.add_trace(go.Bar(y=d.faixa_etaria, x=-d.Masculino, orientation='h', name='Homens', marker_color='#00405e', customdata=d.Masculino, hovertemplate='%{y}: %{customdata:.1f}%<extra>Homens</extra>'))
    fig.add_trace(go.Bar(y=d.faixa_etaria, x=d.Feminino, orientation='h', name='Mulheres', marker_color='#fe9974', hovertemplate='%{y}: %{x:.1f}%<extra>Mulheres</extra>'))
    t = [-8, -4, 0, 4, 8]
    fig.update_layout(barmode='relative', xaxis=dict(tickvals=t, ticktext=[abs(v) for v in t], title='% da população'), legend=dict(orientation='h', y=-0.2))
    return fig

def fig_renda_esc():
    d = P['renda_escolaridade']
    fig = go.Figure()
    fig.add_trace(go.Bar(x=d.categoria, y=d.mediana, name='Mediana', marker_color='#1b4332'))
    fig.add_trace(go.Bar(x=d.categoria, y=d.media, name='Média ponderada', marker_color='#a5d0b9'))
    fig.update_layout(barmode='group', yaxis_title='Renda individual (R$)', legend=dict(orientation='h', y=-0.35))
    return fig

def fig_beneficio():
    d = P['renda_beneficio']
    fig = go.Figure()
    fig.add_trace(go.Bar(x=d.categoria, y=d.mediana, name='Mediana', marker_color='#1b4332'))
    fig.add_trace(go.Bar(x=d.categoria, y=d.media, name='Média ponderada', marker_color='#a5d0b9'))
    fig.update_layout(barmode='group', yaxis_title='Renda individual (R$)', legend=dict(orientation='h', y=-0.2))
    return fig

def fig_heatmap():
    s = P['spearman_segmentos'].set_index('variavel')
    r = [ROTULO_VAR.get(v, v) for v in s.index]
    fig = go.Figure(go.Heatmap(z=s.values, x=r, y=r, zmin=-1, zmax=1, colorscale='RdBu', text=s.round(2).values, texttemplate='%{text}', textfont=dict(size=10)))
    fig.update_layout(yaxis=dict(autorange='reversed'), xaxis=dict(tickangle=-35))
    return fig

IND = [c for c in P['indicadores_subpopulacao'].columns if c != 'subpopulacao']
PROP = [c for c in IND if c not in ('renda_domiciliar_pc', 'escolaridade_adulto')]

def fig_indicadores(vars_):
    d = P['indicadores_subpopulacao'].set_index('subpopulacao')
    fig = go.Figure()
    for i, s in enumerate(d.index):
        y = d.loc[s, vars_]
        fig.add_trace(go.Bar(y=[ROTULO_VAR.get(v, v) for v in vars_], x=(y * 100).values, orientation='h', name=s, marker_color=COR[i % 4]))
    fig.update_layout(barmode='group', yaxis=dict(autorange='reversed'), xaxis_title='%', legend=dict(orientation='h', y=-0.12))
    return fig

def fig_renda_sub():
    d = P['indicadores_subpopulacao']
    fig = go.Figure(go.Bar(x=d.subpopulacao, y=d.renda_domiciliar_pc, marker_color=COR[:len(d)], text=[br(v) for v in d.renda_domiciliar_pc], textposition='outside'))
    fig.update_layout(yaxis_title='Média ponderada, R$ per capita')
    return fig

R = P['renda_resumo'].copy()
R_tab = pd.DataFrame({'Variável': R.variavel, 'N válidos': R.n_validos.map(br), 'Média pond.': R.media_pond.map(lambda v: br(v)), 'Q1': R.q1.map(lambda v: br(v)),
                      'Mediana': R.mediana.map(lambda v: br(v)), 'Q3': R.q3.map(lambda v: br(v)), 'P90': R.p90.map(lambda v: br(v))})

layout = html.Div(className="w-full p-6 md:p-8 bg-background", children=[
    cabecalho("PDAD Rural 2022 · análise exploratória",
              "Resultados ponderados da Pesquisa Distrital por Amostra de Domicílios Rural (IPE-DF), base da tipologia do TCC. Estimativas expandidas pelos pesos amostrais."),
    html.Div(className="grid grid-cols-2 md:grid-cols-4 gap-4 mb-6", children=[
        kpi(br(tot.domicilios_amostra), "domicílios na amostra"), kpi(br(tot.moradores_amostra), "moradores na amostra"),
        kpi(br(tot.domicilios_expandidos), "domicílios expandidos"), kpi(f"R$ {br(tot.renda_pc_mediana_pond)}", "mediana da renda domiciliar per capita"),
    ]),
    aviso("a PDAD Rural usa amostragem por subpopulação (agricultura familiar, empresarial, assentamento/agrovila e moradia e lazer) e por RA. "
          "Sempre que houver '% ponderado', o valor representa a população, e não a amostra. Boa parte dos moradores não tem renda própria (crianças, estudantes, donas de casa), e isso puxa as medianas individuais para zero.", "Como ler"),
    dcc.Tabs(id='tabs-pdad', value='perfil', className="mt-6", children=[
        dcc.Tab(label='Perfil e amostra', value='perfil'), dcc.Tab(label='Renda', value='renda'),
        dcc.Tab(label='Subpopulações', value='sub'), dcc.Tab(label='Correlações', value='corr'),
    ]),
    html.Div(id='conteudo-pdad', className="mt-6 flex flex-col gap-6"),
    rodape_fonte("Fonte: PDAD Rural 2022 (IPE-DF). Cálculos do TCC com ponderação amostral. Tabelas agregadas, sem microdados."),
])

@callback(Output('conteudo-pdad', 'children'), Input('tabs-pdad', 'value'))
def troca(v):
    if v == 'perfil':
        return [html.Div(className="grid grid-cols-1 lg:grid-cols-2 gap-6", children=[
            cartao("Subpopulações: amostra × população", grafico(fig_subpop(), 340)),
            cartao("Pirâmide etária", grafico(fig_piramide(), 340), nota=f"Idade média ponderada: {br(tot.idade_media_pond, 1)} anos.")]),
            cartao("Distribuição dos domicílios por RA", grafico(fig_ra(), 560), nota="Percentual ponderado. A amostra é desproporcional por desenho (RAs menores são sobreamostradas).")]
    if v == 'renda':
        z = P['renda_sem_renda'].set_index('grupo')
        t = z.loc['Todos os moradores com informação']; ad = z.loc['Adultos (18 anos ou mais)']
        return [html.Div(className="grid grid-cols-1 md:grid-cols-3 gap-4", children=[
                    kpi(f"{br(t.pct_sem_renda, 1)}%", "dos moradores não têm renda individual"),
                    kpi(f"R$ {br(t.mediana)}", "mediana da renda individual (todos os moradores)"),
                    kpi(f"R$ {br(ad.mediana)}", f"mediana entre adultos ({br(ad.pct_sem_renda, 1)}% sem renda)")]),
                cartao("Resumo de renda", tabela(R_tab), nota=f"{br(tot.pct_renda_dom_abaixo_2000, 1)}% dos domicílios (ponderado) têm renda domiciliar total abaixo de R$ 2.000. Medianas ponderadas; a renda individual considera os {br(t.n)} moradores com informação de renda."),
                html.Div(className="grid grid-cols-1 lg:grid-cols-2 gap-6", children=[
                    cartao("Renda individual por escolaridade", grafico(fig_renda_esc(), 420), nota="Mediana zero em 'sem instrução' reflete que mais da metade desse grupo (crianças inclusive) não tem renda."),
                    cartao("Renda individual por recebimento de benefício", grafico(fig_beneficio(), 420),
                           nota=f"Entre quem não recebe benefício, {br(z.loc['Não recebem benefício social'].pct_sem_renda, 1)}% não têm renda (mediana R$ {br(z.loc['Não recebem benefício social'].mediana, 2)}); entre quem recebe, {br(z.loc['Recebem benefício social'].pct_sem_renda, 1)}% (mediana R$ {br(z.loc['Recebem benefício social'].mediana)}).")])]
    if v == 'sub':
        return [html.Div(className="grid grid-cols-1 lg:grid-cols-2 gap-6", children=[
            cartao("Renda domiciliar per capita por subpopulação", grafico(fig_renda_sub(), 340)),
            cartao("Infraestrutura e conectividade", grafico(fig_indicadores(['agua_rede', 'solucao_sanitaria_estruturada', 'rua_pavimentada', 'internet_banda_larga_fixa', 'possui_computador']), 420))]),
            cartao("Trabalho, proteção social e acesso digital", grafico(fig_indicadores(['trabalhou_30d', 'tem_ctps', 'contribui_previdencia', 'recebe_beneficios_sociais', 'internet_uso_3m']), 420))]
    return [cartao("Correlação de Spearman entre segmentos", grafico(fig_heatmap(), 560),
                   nota="Calculada sobre os segmentos (RA × subpopulação), não sobre domicílios. Base exploratória para a escolha das dimensões do PCA no TCC.")]
