import requests
import pandas as pd
from bs4 import BeautifulSoup
from datetime import timedelta
from datetime import datetime
#from google.colab import files
#import matplotlib.pyplot as plt
import numpy as np
import nltk


## Criação de array pra cada coluna que será extraida do HTML da página da Câmara dos Deputados
CONTEUDO_SITE = [] ## COLUNA 8
LISTA = []


## Função para retornar o próximo dia com base na data informada
def fn_get_proxima_data(data):
  ProximoDia = pd.to_datetime(data) + pd.DateOffset(days=1)
  return ProximoDia


## Função para obter o conteúdo da página da Câmara dos Deputados com base nos argumentos informados
def fn_get_notas_taquigafricas(Orador, DataInicial, DataFinal, link):
    Orador = Orador.replace(" ", "+")
    LinkBase = link
    DataInicial = pd.to_datetime(DataInicial)
    DataFinal = pd.to_datetime(DataFinal)
    DataAtual = pd.to_datetime(DataInicial)

    while DataAtual <= DataFinal:
        InicioDia = DataAtual.day
        InicioMes = DataAtual.month
        InicioAno = DataAtual.year

        FimDia = DataAtual.day
        FimMes = DataAtual.month
        FimAno = DataAtual.year

        uri = f"https://www.camara.leg.br/internet/sitaqweb/resultadoPesquisaDiscursos.asp?txOrador={Orador}&txPartido=&txUF=&dtInicio={InicioDia}%2F{InicioMes}%2F{InicioAno}&dtFim={FimDia}%2F{FimMes}%2F{FimAno}&txTexto=&txSumario=&basePesq=plenario&CampoOrdenacao=dtSessao&PageSize=50&TipoOrdenacao=DESC&btnPesq=Pesquisar"

        r = requests.get(uri)
        conteudo = r.text

        soup = BeautifulSoup(conteudo, 'html.parser')
        Dados = soup.find('table', class_='variasColunas')

        if Dados is not None:
            print(DataAtual, "- Com Discurso")
            Resultado = fn_busca_tabela(Dados, LinkBase)

        else:
            print(DataAtual, "- Sem Discurso")

        DataAtual = fn_get_proxima_data(DataAtual)


## Função para iterar no HTML e obter apenas o texto do discurso
def fn_busca_tabela(Tabela, LinkBase):
    for Linha in Tabela.findAll('tr'):  # para tudo que estiver em <tr>
        Celula = Linha.findAll('td')  # variável para encontrar <td>

        if len(Celula) == 8:  # número de colunas

            # iterando sobre cada linha
            Texto = fn_retorna_conteudo(
                LinkBase + (((Celula[3].find('a', href=True)['href']).replace('\r', '')).replace('\n', '')).replace(
                    '\t', ''))
            CONTEUDO_SITE.append(Texto)
            LISTA.append(Texto)

def fn_retorna_conteudo(uri):
  Retorna_resultado = requests.get(uri)
  Retorna_conteudo = Retorna_resultado.text
  Dados = BeautifulSoup(Retorna_conteudo, 'html.parser')
  Dados = Dados.find('p').getText()
  return(Dados)




### Aqui são informados os valores dos argumentos para a função de obter o conteúdo
#Orador = "EDUARDO BOLSONARO"
#DataInicial = '2022-05-12'
#DataFinal = '2022-05-12'
#Link = "https://www.camara.leg.br/internet/sitaqweb/"

#fn_get_notas_taquigafricas(Orador, DataInicial, DataFinal, Link )

## Passo os dados da Lista para o DataSet
#df_discurso = pd.DataFrame()
#df_discurso['discurso'] = CONTEUDO_SITE
#df_discurso.to_csv('discurso.csv',index=False)