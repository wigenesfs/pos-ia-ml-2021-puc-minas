# pos-ia-ml-2021-puc-minas
Repositório da Especialização em Inteligência Artificial e Aprendizado de Máquina na PUC Minas iniciado em 2021.

Este projeto aplica um modelo de Análise de Sentimento nos discursos proferidos pelos Deputados Federais em Plenário.

---

## Paths disponíveis

| Path     | HTTP Method | Description                                                                              | Required parameters (type)                                                                                                                               |
|----------| ----------- |------------------------------------------------------------------------------------------|-------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| `/check` | GET         | Endpoint para verificação da API online.                                                 | N/A                                                                                                                                                               |
| `/svm`   | GET         | Endpoint para classificação dos discursos utilizando modelo de classificação SVM.        |  - `nome_orador` (string) <br> - `data_inicio` (date) <br> - `data_fim` (date) |
| `/bert`  | GET         | Endpoint para classificação dos discursos utilizando modelo pré-treinado `pysentimiento`. | - `nome_orador` (string) <br> - `data_inicio` (date) <br> - `data_fim` (date)|
---