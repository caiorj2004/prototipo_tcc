import dash
import numpy as np, pandas as pd
import plotly.graph_objects as go
from dash import html, dcc, Input, Output, callback
from data_pipeline_tcc import tipologia, COR_GRUPO, COR_NEUTRA, ROTULO_VAR, centroide
from pages._comum import cabecalho, cartao, kpi, aviso, grafico, tabela, rodape_fonte

dash.register_page(__name__, path='/tipologia', name='Tipologia Rural (TCC)')

T = tipologia()
G = T['grupos'].set_index('grupo')
NOME = {g: f"{g} · {G.loc[g, 'nome']}" for g in G.index}
PERFIL = T['perfil_grupos']
SEG = T['segmentos']
tot = T['totais'].iloc[0]

# ---------------- mapa
def fig_mapa():
    W, H = T['mapa_dim'].iloc[0]
    fig = go.Figure()
    shapes, cx, cy, txt = [], [], [], []
    for r in T['mapa_ras'].itertuples():
        cor = COR_GRUPO.get(r.grupo_predominante, COR_NEUTRA) if isinstance(r.grupo_predominante, str) else COR_NEUTRA
        shapes.append(dict(type='path', path=r.caminho + 'Z' if not r.caminho.strip().endswith('Z') else r.caminho,
                           fillcolor=cor, line=dict(color='white', width=0.8), opacity=1 if r.pdad else 0.55, layer='below'))
        x, y = centroide(r.caminho); cx.append(x); cy.append(y)
        if r.pdad:
            gs = str(r.grupos).split(',')
            txt.append(f"<b>{r.ra}</b><br>Grupo predominante: {NOME.get(r.grupo_predominante, '—')}"
                       + ("<br>Segmentos em mais de um grupo: " + ', '.join(gs) if len(gs) > 1 else ''))
        else:
            txt.append(f"<b>{r.ra}</b><br>Fora da PDAD Rural 2022 (sem segmentos rurais)")
    fig.add_trace(go.Scatter(x=cx, y=cy, mode='markers', marker=dict(size=14, opacity=0), hovertext=txt, hoverinfo='text', showlegend=False))
    for g in G.index:
        fig.add_trace(go.Scatter(x=[None], y=[None], mode='markers', marker=dict(size=12, color=COR_GRUPO[g]), name=NOME[g]))
    fig.add_trace(go.Scatter(x=[None], y=[None], mode='markers', marker=dict(size=12, color=COR_NEUTRA), name='Fora da amostra'))
    fig.update_layout(shapes=shapes, xaxis=dict(range=[0, W], visible=False, constrain='domain'),
                      yaxis=dict(range=[H, 0], visible=False, scaleanchor='x'), legend=dict(orientation='h', y=-0.05), hoverlabel=dict(bgcolor='white'))
    return grafico(fig, 560)

# ---------------- perfil dos grupos
def _blocos(bloco):
    p = PERFIL[PERFIL.bloco == bloco]
    return p
VAR_PERFIL = [v for v in PERFIL[PERFIL.bloco == 'perfil'].variavel.unique() if v != 'ivs_df']
VAR_VALID = list(PERFIL[PERFIL.bloco == 'valid'].variavel.unique())

def fig_perfil(var_lista, bloco):
    fig = go.Figure()
    p = PERFIL[(PERFIL.bloco == bloco) & PERFIL.variavel.isin(var_lista)].copy()
    if bloco == 'perfil':  # proporções (0-1) -> %
        p[['estimativa', 'ic_inf', 'ic_sup']] *= 100
    for g in G.index:
        d = p[p.grupo == g].set_index('variavel').reindex(var_lista)
        fig.add_trace(go.Bar(y=[ROTULO_VAR.get(v, v) for v in d.index], x=d.estimativa, orientation='h', name=NOME[g], marker_color=COR_GRUPO[g],
                             error_x=dict(type='data', symmetric=False, array=(d.ic_sup - d.estimativa).values, arrayminus=(d.estimativa - d.ic_inf).values, thickness=1),
                             hovertemplate='%{y}<br>%{x:.2f} (IC 95%: ' + '%{customdata[0]:.2f} a %{customdata[1]:.2f})<extra>' + NOME[g] + '</extra>',
                             customdata=np.c_[d.ic_inf, d.ic_sup]))
    fig.update_layout(barmode='group', yaxis=dict(autorange='reversed'), xaxis_title='% (IC 95%)', legend=dict(orientation='h', y=-0.12))
    return fig

def perfil_secao():
    # proporções (0-1) num gráfico; renda e escolaridade em escalas próprias, em tabela
    prop = [v for v in VAR_PERFIL if v not in ('renda_domiciliar_pc', 'escolaridade_adulto')]
    p = PERFIL[PERFIL.bloco == 'perfil'].pivot(index='variavel', columns='grupo', values='estimativa')
    escala = pd.DataFrame({'Indicador': ['Renda domiciliar per capita (R$)', 'Escolaridade do adulto (anos)', 'IVS-DF'],
                           **{f'Grupo {g}': [f"{p.loc['renda_domiciliar_pc', g]:,.0f}".replace(',', '.'), f"{p.loc['escolaridade_adulto', g]:.1f}".replace('.', ','),
                                             f"{p.loc['ivs_df', g]:.2f}".replace('.', ',')] for g in G.index}})
    return [
        cartao("Indicadores de formação dos grupos (proporções de domicílios/moradores)", grafico(fig_perfil(prop, 'perfil'), 520),
               nota="Barras de erro: intervalo de confiança de 95%, por bootstrap dos domicílios."),
        cartao("Renda, escolaridade e vulnerabilidade", tabela(escala), nota="Estimativas ponderadas por grupo. O IVS-DF não entra na formação dos grupos."),
        cartao("Validação externa: variáveis que NÃO entraram na formação dos grupos", grafico(fig_perfil(VAR_VALID, 'valid'), 460),
               nota="Insegurança alimentar (EBIA), inscrição no CadÚnico, benefícios sociais e posse do imóvel são usados só para conferir os grupos depois de formados."),
    ]

# ---------------- segmentos
def lista_ras(): return sorted(SEG.ra.unique())

def fig_segmentos(filtro_grupo, filtro_ra):
    d = SEG.copy()
    if filtro_grupo: d = d[d.grupo.isin(filtro_grupo)]
    if filtro_ra: d = d[d.ra.isin(filtro_ra)]
    d = d.assign(seg=d.ra + ' — ' + d.subpopulacao).sort_values(['grupo', 'saneamento'])
    fig = go.Figure(go.Scatter(x=d.saneamento, y=d.renda_pc, mode='markers', text=d.seg, customdata=np.c_[d.grupo, d.amostra_n, d.situacao, d.coligacao],
        marker=dict(size=np.clip(np.sqrt(d.dom_expandidos) / 3, 6, 40), color=[COR_GRUPO[g] for g in d.grupo], line=dict(color='white', width=1), opacity=.85),
        hovertemplate='<b>%{text}</b><br>Grupo %{customdata[0]} · situação %{customdata[2]}<br>Amostra: %{customdata[1]} dom.<br>Coligação: %{customdata[3]:.2f}<br>'
                      'Saneamento adequado: %{x}%<br>Renda per capita: R$ %{y:,.0f}<extra></extra>'))
    fig.update_layout(xaxis_title='Solução sanitária estruturada (% dos domicílios)', yaxis_title='Renda domiciliar per capita (R$)')
    return fig

def tabela_segmentos(filtro_grupo, filtro_ra):
    d = SEG.copy()
    if filtro_grupo: d = d[d.grupo.isin(filtro_grupo)]
    if filtro_ra: d = d[d.ra.isin(filtro_ra)]
    d = d.sort_values(['grupo', 'ra', 'subpopulacao'])
    out = pd.DataFrame({'RA': d.ra, 'Subpopulação': d.subpopulacao, 'Grupo': d.grupo, 'Situação': d.situacao, 'Amostra (dom.)': d.amostra_n,
                        'Dom. expandidos': d.dom_expandidos, 'Renda pc (R$)': d.renda_pc, 'Saneamento %': d.saneamento, 'Pavimentação %': d.pavimentacao,
                        'Banda larga %': d.banda_larga, 'Coligação': d.coligacao.round(2)})
    return tabela(out)

# ---------------- modelos e estabilidade
def secao_modelos():
    ids = ['M0_antigo_K3', 'M1_revisado_K3', 'M2_semEscadas_K3', 'M2b_aguaILR_K3']
    a = T['ari_modelos'].set_index('modelo').loc[ids, ids]
    rot = {'M0_antigo_K3': 'M0', 'M1_revisado_K3': 'M1', 'M2_semEscadas_K3': 'M2 (principal)', 'M2b_aguaILR_K3': 'M2b'}
    fig = go.Figure(go.Heatmap(z=a.values, x=[rot[i] for i in ids], y=[rot[i] for i in ids], zmin=0, zmax=1, colorscale='Greens', text=a.round(2).values, texttemplate='%{text}'))
    fig.update_layout(yaxis=dict(autorange='reversed'))
    m = T['modelos'].set_index('id').loc[ids]
    tab = pd.DataFrame({'Modelo': [rot[i] for i in ids], 'K': 3, 'Variáveis': m.vars.values, 'Silhueta': m.silh.round(3).values,
                        'Menor grupo (%)': m.menor.round(1).values, 'ARI bootstrap': m.boot.round(2).values, 'ARI nulo': m.boot_nulo.round(2).values})
    return [cartao("Concordância entre modelos (ARI)", grafico(fig, 360),
                   nota="M0 e M1 são comparação; M2 é o modelo principal; M2b é análise de sensibilidade (água em transformação ILR)."),
            cartao("Comparação dos modelos (K = 3)", tabela(tab))]

def secao_estabilidade():
    r = T['estabilidade_resumo'].set_index('teste')
    k = T['escolha_k']
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=k.K, y=k.silh, name='Silhueta', mode='lines+markers', marker_color='#1b4965'))
    fig.add_trace(go.Scatter(x=k.K, y=k.est, name='Estabilidade (ARI)', mode='lines+markers', marker_color='#b5432a'))
    fig.update_layout(xaxis_title='Número de grupos (K)', legend=dict(orientation='h', y=-0.25))
    b = r.loc['bootstrap_domicilios']
    return [
        html.Div(className="grid grid-cols-1 md:grid-cols-3 gap-4", children=[
            kpi(f"{b.obs:.2f}".replace('.', ','), "ARI médio do bootstrap de domicílios"),
            kpi(f"{b.nulo:.2f}".replace('.', ','), "ARI de um nulo sem grupos"),
            kpi(f"p = {b.p:.2f}".replace('.', ','), "Teste contra o nulo"),
        ]),
        aviso("O ARI observado fica próximo do nulo: a estrutura é fraca. Os grupos descrevem um gradiente de urbanização formal recortado em categorias descritivas, "
              "não tipos naturais. Devem ser lidos como hipóteses para investigar.", "Leitura"),
        cartao("Escolha de K: silhueta e estabilidade", grafico(fig, 320)),
    ]

# ---------------- layout
layout = html.Div(className="w-full p-6 md:p-8 bg-background", children=[
    cabecalho("Tipologia dos Territórios Rurais do DF",
              "Resultados do TCC (IESB): clustering de 49 segmentos territoriais (Região Administrativa × subpopulação) da PDAD Rural 2022, modelo principal M2, K = 3."),
    html.Div(className="grid grid-cols-2 md:grid-cols-4 gap-4 mb-6", children=[
        kpi(f"{int(tot.n_seg)}", "segmentos analisados"), kpi(f"{int(tot.n_ra)}", "Regiões Administrativas"),
        kpi(f"{int(tot.amostra):,}".replace(',', '.'), "domicílios na amostra efetiva"), kpi(f"{int(tot.dom):,}".replace(',', '.'), "domicílios expandidos"),
    ]),
    aviso("os grupos são um gradiente de urbanização formal agrupado em três categorias descritivas, e a estabilidade amostral é baixa (ver aba Estabilidade). "
          "Servem como hipótese de trabalho, não como diagnóstico definitivo.", "Atenção"),
    dcc.Tabs(id='tabs-tip', value='mapa', className="mt-6", children=[
        dcc.Tab(label='Mapa e grupos', value='mapa'), dcc.Tab(label='Perfil dos grupos', value='perfil'), dcc.Tab(label='Segmentos', value='seg'),
        dcc.Tab(label='Modelos', value='modelos'), dcc.Tab(label='Estabilidade', value='estab'),
    ]),
    html.Div(id='conteudo-tip', className="mt-6 flex flex-col gap-6"),
    rodape_fonte("Fonte: PDAD Rural 2022 (IPE-DF). Cálculos do TCC, com ponderação amostral. Tabelas agregadas por segmento, sem microdados."),
])

def _mapa_conteudo():
    cards = [html.Div(className="bg-white border border-outline-variant rounded-xl p-4", style={'borderTop': f'4px solid {COR_GRUPO[g]}'}, children=[
        html.Div(NOME[g], className="font-semibold text-primary"),
        html.Div(f"{int(G.loc[g,'n_seg'])} segmentos · {G.loc[g,'pct_dom']:.1f}% dos domicílios".replace('.', ','), className="text-sm text-on-surface-variant"),
    ]) for g in G.index]
    n_multi = int((T['mapa_ras'].grupos.fillna('').str.contains(',')).sum())
    return [html.Div(className="grid grid-cols-1 md:grid-cols-3 gap-4", children=cards),
            cartao("Mapa das RAs por grupo predominante", grafico_mapa,
                   nota=f"Cor = grupo com mais domicílios na RA. {n_multi} RAs têm segmentos em mais de um grupo (detalhe ao passar o mouse). RAs em cinza não têm segmentos na PDAD Rural.")]

grafico_mapa = fig_mapa()

def _seg_conteudo():
    return [html.Div(className="flex flex-wrap gap-4", children=[
        dcc.Dropdown(id='f-grupo', options=[{'label': NOME[g], 'value': g} for g in G.index], multi=True, placeholder='Grupo', className="w-72"),
        dcc.Dropdown(id='f-ra', options=lista_ras(), multi=True, placeholder='Região Administrativa', className="w-72")]),
        cartao("Saneamento × renda, por segmento", html.Div(id='graf-seg'), nota="Tamanho do ponto proporcional ao número de domicílios expandidos."),
        cartao("Tabela de segmentos", html.Div(id='tab-seg'))]

@callback(Output('conteudo-tip', 'children'), Input('tabs-tip', 'value'))
def troca_aba(v):
    if v == 'mapa': return _mapa_conteudo()
    if v == 'perfil': return perfil_secao()
    if v == 'seg': return _seg_conteudo()
    if v == 'modelos': return secao_modelos()
    return secao_estabilidade()

@callback(Output('graf-seg', 'children'), Output('tab-seg', 'children'), Input('f-grupo', 'value'), Input('f-ra', 'value'))
def atualiza_seg(g, r):
    return grafico(fig_segmentos(g, r), 420), tabela_segmentos(g, r)
