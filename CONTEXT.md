# Contexto do Projeto: AgriSteward (Protótipo TCC)

## 1. Visão Geral e Objetivo
Este projeto é o protótipo de um Trabalho de Conclusão de Curso (TCC) na área de Ciência de Dados e Inteligência Artificial. O objetivo central é desenvolver uma plataforma de inteligência (AgriSteward) focada em estruturar, centralizar e visualizar informações socioeconômicas estratégicas para a agricultura familiar. 

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