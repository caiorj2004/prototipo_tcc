---
title: Sistema de Inteligência para Agricultura Familiar
emoji: 🌾
colorFrom: green
colorTo: green
sdk: docker
app_port: 7860
pinned: false
---

# Sistema de Inteligência para Agricultura Familiar

Plataforma analítica e interativa desenvolvida em **Python (Dash/Plotly)** com o objetivo de centralizar, cruzar e visualizar dados socioeconômicos, estruturais, demográficos e financeiros da agricultura familiar no Distrito Federal (DF). 

O sistema adota uma arquitetura *Python-first* focada em desempenho, modularidade e controle analítico total via código.

---

## 🚀 Módulos e Análises Disponíveis

O dashboard é estruturado em uma aplicação multi-página (`dash.page_container`), cobrindo frentes estratégicas de dados públicos e os resultados do TCC:

1. **Censo Agropecuário 2017 (`/censo`)**
   * Análise demográfica por cor/raça, valor de produção e quantidade física.
   * Pirâmide etária do produtor e estrutura de mão de obra familiar.
   * Indicadores de uso da terra, mecanização (máquinas/tratores) e acesso a financiamento governamental.

2. **IBGE 2024 (`/ibge`)**
   * Indicadores recentes de valor da produção agrícola (Top culturas do DF).
   * Composição e efetivo do rebanho na pecuária local.

3. **CNPO - Produtores Orgânicos (`/cnpo`)**
   * Mapeamento de atividades e escopos de produção orgânica por região no DF.
   * Filtros dinâmicos por ano, mês e cidade (com padronização ortográfica de localidades).
   * Listagem detalhada de entidades ativas com paginação nativa.

4. **CAF - Cadastro Nacional da Agricultura Familiar (`/caf`)**
   * Perfil socioprodutivo (assentados, quilombolas, povos tradicionais).
   * Análise de gênero, juventude rural e atividades principais.
   * Distribuição de renda (produção total e per-capita) com filtros temporais semestrais e mensais independentes.

5. **Crédito Rural - MCDR (`/credito-rural`)**
   * Dados do Banco Central sobre financiamento agropecuário.
   * Distribuição por finalidade (custeio, investimento, comercialização).
   * Concentração bancária e gráfico de dispersão de intensidade de capital com cálculo automático da **Correlação de Pearson ($r$)**.

6. **Tipologia Rural (TCC) (`/tipologia`)**
   * Resultados do TCC (IESB): clustering de 49 segmentos (RA × subpopulação) da PDAD Rural 2022, modelo principal M2, K = 3.
   * Mapa das RAs por grupo, perfil dos grupos com IC 95%, validação externa, tabela de segmentos, comparação de modelos e estabilidade.
   * Aviso de leitura: a estrutura é um gradiente de urbanização formal, não tipos naturais; os grupos são hipóteses.

7. **PDAD Rural 2022 (`/pdad-rural`)**
   * Análise exploratória ponderada: amostra e população, pirâmide etária, renda, subpopulações e correlações.

## Dados e execução

* **Parquet:** `python convert_to_parquet.py` converte as bases de `data/` (CAF, CNPO, MCDR, IBGE, Censo) para Parquet; os pipelines usam o Parquet quando existe e o arquivo original como alternativa (resultados idênticos). Os Parquets ficam no Git LFS.
* Microdados da PDAD **nunca** entram no repositório (`.gitignore`).

* Páginas do TCC leem tabelas agregadas em `dados_tcc/` (sem microdados; geradas por `app/gerar_tabelas_dash.py` no repositório `pdad_tipologia_cluster`). Pasta alterável por `DADOS_TCC_DIR`.
* Local: `pip install -r requirements.txt && python app.py` (porta `PORT`, padrão 7860; `DASH_DEBUG=1` ativa o modo debug).
* Produção: `gunicorn app:server` (ver `Dockerfile`).

---

## 🛠️ Stack Tecnológica & Arquitetura

* **Frontend & UI:** Dash (Python), Plotly para gráficos dinâmicos, estilizado com **Tailwind CSS** injetado via template HTML base.
* **Processamento de Dados:** Manipulação via **Pandas**; os carregadores de cada fonte (`data_pipeline_*.py`) usam `@lru_cache` para ler cada base uma única vez por processo e preferem Parquet quando existe.
* **Infraestrutura:** Aplicação conteinerizada via **Docker** (`python:3.13-slim`), servida por **Gunicorn** (2 workers), com usuário não-root e `HEALTHCHECK`, no formato esperado por orquestradores como Kubernetes / K8s. O CI roda os testes em Python 3.10 e 3.13.

---

## 📂 Estrutura do Repositório

```text
├── app.py                     # Arquivo principal (Roteamento, Layout base e Modal de Ajuda)
├── Dockerfile                 # Configuração do container para deploy
├── requirements.txt           # Dependências do projeto (Dash, Pandas, Plotly, Openpyxl, Odfpy)
├── pages/                     # Módulos visuais de cada aba (Censo, IBGE, CNPO, CAF, MCDR)
└── data_pipeline_*.py         # Scripts de ingestão, limpeza e tratamento de dados por fonte
```

## Dados fora do Git (S3) e teste

Em ambientes com a regra "sem dados no repositório" (ex.: DataIESB), `dados_tcc/` fica fora do Git e é sincronizado pelo S3:

```bash
aws s3 sync ./dados_tcc/ s3://dataieb-tcc-caio-agrotec/dados_tcc/                      # subir
aws s3 sync s3://dataieb-tcc-caio-agrotec/dados_tcc/ ./dados_tcc/                      # baixar na instância
```

No Hugging Face Space, `dados_tcc/` vai dentro do repositório (o Space não acessa o S3). Teste rápido: `pip install pytest && pytest -q tests`.

Sem `dados_tcc/` (ex.: ambiente sem dados no repositório), as páginas `/tipologia` e `/pdad-rural` mostram um aviso e o app continua de pé; basta sincronizar a pasta (S3) ou apontar `DADOS_TCC_DIR` e reiniciar.
