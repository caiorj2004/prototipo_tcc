# Contexto do Projeto: Protótipo Sistema de Inteligência para Agricultura Familiar (TCC)

## 1. Visão Geral e Objetivo
Este projeto é o protótipo de um Trabalho de Conclusão de Curso (TCC) na área de Ciência de Dados e Inteligência Artificial. O objetivo central é desenvolver um Sistema de Inteligência focado em estruturar, centralizar e visualizar informações socioeconômicas estratégicas para a agricultura familiar. 

## 2. Filosofia de Engenharia e Stack Tecnológico
A arquitetura do projeto segue uma abordagem "Python-first", evitando ferramentas tradicionais e engessadas de Business Intelligence.
*   **Frontend/UI:** Construído inteiramente em Python utilizando Dash e Plotly, consumindo componentes estilizados via Tailwind CSS.
*   **Manipulação de Dados:** O processamento de dados, transformações e agregações devem ser feitos estritamente utilizando `pandas`.
*   **Ingestão e Automação:** A alimentação dos dados será automatizada via scripts em Python, utilizando técnicas de web scraping (com `BeautifulSoup` ou similares) e consumo de APIs para buscar dados de mercado, preços agrícolas e regulamentações.
*   **Deploy:** A aplicação é conteinerizada via Docker para hospedagem no Hugging Face Spaces.

## 3. Integridade e Fidelidade de Dados
É uma diretriz absoluta do projeto: o sistema deve refletir apenas os dados reais coletados ou fornecidos. Em hipótese alguma o código deve inventar dados, preencher tabelas com valores aleatórios não solicitados ou gerar porcentagens fictícias. A fidelidade ao material fonte é crítica para a validade do TCC.

## 4. Evolução e Machine Learning (Roadmap)
O código deve ser modular. Atualmente, o projeto está na fase descritiva (visualização de dados e histórico). No entanto, a arquitetura deve prever a futura integração de pipelines de Machine Learning. O escopo futuro inclui a aplicação de modelos preditivos e estatísticos — com preferência para Regressão Linear, dada sua interpretabilidade para dados socioeconômicos e correlações de variáveis — para prever tendências de preços e produtividade.

## 5. Dicionário de Dados e Fontes (Especificações de Extração)
O backend (ingestão e processamento Pandas) deve extrair dados de quatro fontes distintas para alimentar os placeholders do frontend. 

1. **Censo Agropecuário 2017:**
   * Distribuição e frequência de estabelecimentos por cor/raça.
   * Distribuição do valor de produção por cor/raça (Total/Média).
   * Quantidade produzida por cor/raça.

2. **IBGE 2024:**
   * Ranking Top 10 Agricultura.
   * Ranking Top 10 Pecuária.

3. **CNPO (Cadastro Nacional de Produtores Orgânicos):**
   * Distribuição de atividades por cidade.
   * Frequência das principais atividades focado apenas no DF.
   * Escopos operacionais por cidade e principais escopos focados no DF.
   * Tipos de Entidade certificadora/produtora.
   * Relação de Entidades ativas.

4. **CAF (Cadastro Nacional da Agricultura Familiar):**
   * *Atenção:* Operar com arquivos de múltiplas abas; gerar um DataFrame isolado para cada aba relevante. **Filtrar exclusivamente para UF = DF.**
   * **Aba CARACTERIZACAO (Perfil):** Classificar por Assentado pelo PNRA, Beneficiário do PNCE, Quilombola/indígena/povos tradicionais, e demais agricultores.
   * **Aba ATIVIDADE (Atividade Principal):** Categorizar entre Agricultura/pecuária, aquicultura, silvicultura, extrativista, pescador artesanal.
   * **Aba RENDA (Distribuição de Renda):** Calcular Produção total, renda per-capita e a mediana dos valores dos produtos.
   * *Regra estrita:* Ignorar sumariamente qualquer aba não listada acima.
