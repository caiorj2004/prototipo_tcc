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

O dashboard é estruturado em uma aplicação multi-página (`dash.page_container`), cobrindo cinco frentes estratégicas de dados públicos:

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

---

## 🛠️ Stack Tecnológica & Arquitetura

* **Frontend & UI:** Dash (Python), Plotly para gráficos dinâmicos, estilizado com **Tailwind CSS** injetado via template HTML base.
* **Processamento de Dados:** Manipulação pesada via **Pandas**, otimizada com `@lru_cache` para alocação eficiente em memória RAM.
* **Infraestrutura:** Aplicação conteinerizada via **Docker** (`python:3.10-slim`), preparada para orquestração em ambientes de nuvem (como Kubernetes / K8s).

---

## 📂 Estrutura do Repositório

```text
├── app.py                     # Arquivo principal (Roteamento, Layout base e Modal de Ajuda)
├── Dockerfile                 # Configuração do container para deploy
├── requirements.txt           # Dependências do projeto (Dash, Pandas, Plotly, Openpyxl, Odfpy)
├── pages/                     # Módulos visuais de cada aba (Censo, IBGE, CNPO, CAF, MCDR)
└── data_pipeline_*.py         # Scripts de ingestão, limpeza e tratamento de dados por fonte
