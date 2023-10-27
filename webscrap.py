import requests
import pandas as pd
import numpy as np
import nltk

from bs4 import BeautifulSoup
from datetime import timedelta
from datetime import datetime


def fn_get_proxima_data(data):
    proximo_dia = pd.to_datetime(data) + pd.DateOffset(days=1)
    return proximo_dia


def fn_get_notas_taquigafricas(orador, data_inicial, data_final, link):
    discursos = []
    orador = orador.replace(" ", "+")
    link_base = link
    data_inicial = pd.to_datetime(data_inicial)
    data_final = pd.to_datetime(data_final)
    data_atual = pd.to_datetime(data_inicial)

    while data_atual <= data_final:
        inicio_dia = data_atual.day
        inicio_mes = data_atual.month
        inicio_ano = data_atual.year

        fim_dia = data_atual.day
        fim_mes = data_atual.month
        fim_ano = data_atual.year

        uri = f"https://www.camara.leg.br/internet/sitaqweb/resultadoPesquisaDiscursos.asp?txOrador={orador}&txPartido=&txUF=&dtInicio={inicio_dia}%2F{inicio_mes}%2F{inicio_ano}&dtFim={fim_dia}%2F{fim_mes}%2F{fim_ano}&txTexto=&txSumario=&basePesq=plenario&CampoOrdenacao=dtSessao&PageSize=50&TipoOrdenacao=ASC&btnPesq=Pesquisar"

        r = requests.get(uri)
        conteudo = r.content

        soup = BeautifulSoup(conteudo, 'html.parser')
        dados = soup.find('table', class_='variasColunas')

        if dados is not None:
            fn_busca_tabela(dados, link_base, discursos)

        data_atual = fn_get_proxima_data(data_atual)

    return discursos


def fn_busca_tabela(tabela, link_base, discursos):
    for linha in tabela.findAll('tr'):
        celula = linha.findAll('td')

        if len(celula) == 8:
            texto = fn_retorna_conteudo(
                link_base + (((celula[3].find('a', href=True)['href']).replace('\r', '')).replace('\n', '')).replace(
                    '\t', ''))
            discursos.append(texto)


def fn_retorna_conteudo(uri):
    retorna_resultado = requests.get(uri)
    retorna_conteudo = retorna_resultado.content
    dados = BeautifulSoup(retorna_conteudo, 'html.parser')
    dados = dados.find('p').getText()
    return(dados)