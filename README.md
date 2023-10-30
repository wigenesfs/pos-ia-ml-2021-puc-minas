# pos-ia-ml-2021-puc-minas
Repositório da Especialização em Inteligência Artificial e Aprendizado de Máquina na PUC Minas iniciado em 2021.

Este projeto aplica um modelo de Análise de Sentimento nos discursos proferidos pelos Deputados Federais em Plenário.

---

## Paths disponíveis

| Path                | HTTP Method | Required parameters (type)                                                    | Optional parameters (type, default)                                                                                                                               |
|---------------------| ----------- |-------------------------------------------------------------------------------|-------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| `/`            | GET         | N/A                                                                           | N/A                                                                                                                                                               |
| `/check`            | GET         | - `nome_orador` (string) <br> - `data_inicio` (date) <br> - `data_fim` (date) | N/A |
| `/bert`             | GET         | - `nome_orador` (string) <br> - `data_inicio` (date) <br> - `data_fim` (date) | N/A|

---