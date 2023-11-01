# pos-ia-ml-2021-puc-minas
Repositório da Especialização em Inteligência Artificial e Aprendizado de Máquina na PUC Minas iniciado em 2021.

Este projeto aplica um modelo de Análise de Sentimento nos discursos proferidos pelos Deputados Federais em Plenário.

---
## Paths disponíveis

| Path     | HTTP Method | Description                                                                               | Required parameters (type)                                                    |
|----------| ----------- |-------------------------------------------------------------------------------------------|-------------------------------------------------------------------------------|
| `/` | GET         | Endpoint para verificar se a API está online.                                             | N / A                                                                         |
| `/svm`   | GET         | Endpoint para classificação dos discursos utilizando modelo de classificação SVM.         | - `nome_orador` (string) <br> - `data_inicio` (date) <br> - `data_fim` (date) |
| `/bert`  | GET         | Endpoint para classificação dos discursos utilizando modelo pré-treinado `pysentimiento`. | - `nome_orador` (string) <br> - `data_inicio` (date) <br> - `data_fim` (date) |
---

## Executar o projeto localmente

1. Primeiro é preciso gerar imagem Docker. O comando a seguir ao ser executado cria a imagem com a tag sentimento-discursos:
`docker build -t sentimento-discursos`

2. Após criar a imagem, excutar o container por meio do seguinte comando:
`docker run -d -p 5000:5000 sentimento-discursos`