# pos-ia-ml-2021-puc-minas
Repositório do projeto final da Especialização em Inteligência Artificial e Aprendizado de Máquina na PUC Minas, iniciado em 2021.

Este projeto aplica um modelo de classificação para Análise de Sentimento dos discursos proferidos pelos Deputados Federais em Plenário. Todos os discursos apresentados neste projeto estão com redação final.

Para consulta aos discursos diretamente no portal da Câmara dos Deputados, o endereço para pesquisa é https://www2.camara.leg.br/atividade-legislativa/discursos-e-notas-taquigraficas.

---
## Paths disponíveis

| Path     | HTTP Method | Description                                                                               | Required parameters (type)                                                    | Output                                                                                                              |
|----------| ----------- |-------------------------------------------------------------------------------------------|-------------------------------------------------------------------------------|---------------------------------------------------------------------------------------------------------------------|
| `/` | GET         | Endpoint para verificar se a API está online.                                             | - `nome_orador` (string) <br> - `data_inicio` (date) <br> - `data_fim` (date)                   | - `health: ok` (string) <br>                                          |
| `/svm`   | GET         | Endpoint para classificação dos discursos utilizando modelo de classificação SVM.         | - `nome_orador` (string) <br> - `data_inicio` (date) <br> - `data_fim` (date) | - `Data Discurso` (date) <br> - `Discurso` (string) <br> - `Sentimento` (string) <br> - `Probabilidade (%)` (float) |
| `/bert`  | GET         | Endpoint para classificação dos discursos utilizando modelo pré-treinado `pysentimiento`. | - `nome_orador` (string) <br> - `data_inicio` (date) <br> - `data_fim` (date) | - `Data Discurso` (date) <br> - `Discurso` (string) <br> - `Sentimento` (string) <br> - `Probabilidade (%)` (float) |
---

## Executar o projeto localmente

1. Primeiro é preciso gerar imagem Docker. O comando a seguir ao ser executado cria a imagem com a tag sentimento-discursos:
`docker build -t sentimento-discursos`

2. Após criar a imagem, executar o container por meio do seguinte comando:
`docker run -d -p 5000:5000 sentimento-discursos`