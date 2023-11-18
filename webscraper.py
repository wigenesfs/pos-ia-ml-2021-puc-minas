import re
import requests
import pandas as pd
import numpy as np
import nltk

from nltk import ToktokTokenizer, RSLPStemmer
from nltk.corpus import stopwords

from bs4 import BeautifulSoup
from datetime import timedelta
from datetime import datetime


# Cria instância do TokTokTokenizer
tokenizer = ToktokTokenizer()

# Gera lista de stopwords em Português
nltk.download('stopwords')
stopword_list = nltk.corpus.stopwords.words('portuguese')


# Configura stopwords para Português
stop = set(stopwords.words('portuguese'))


# Função para remover stopwords
def fn_rm_stopwords(text, is_lower_case=False):
    tokens = tokenizer.tokenize(text)
    tokens = [token.strip() for token in tokens]
    if is_lower_case:
        filtered_tokens = [token for token in tokens if token not in stopword_list]
    else:
        filtered_tokens = [token for token in tokens if token.lower() not in stopword_list]
    filtered_text = ' '.join(filtered_tokens)
    return filtered_text


# Função para remover caracteres especiais
def fn_rm_special_char(text, remove_digits=True):
    pattern = "[@!^&\/\\#,+()$~%.'\":*?<>{}\[\]0-9\_]"
    text = re.sub(pattern, '', text)
    return text


# Baixa o algoritmo RSLP Stemmer (Removedor de Sufixos da Língua Portuguesa)
nltk.download('rslp')


# Função de stemming
def fn_stemmer(text):
    stemmer = RSLPStemmer()
    text = ' '.join([stemmer.stem(word) for word in text.split()])
    return text


def fn_get_proxima_data(data):
    proximo_dia = pd.to_datetime(data) + pd.DateOffset(days=1)
    return proximo_dia


def fn_get_notas_taquigafricas(orador, data_inicial, data_final, link):
    discursos = []
    data_discurso = []
    df = pd.DataFrame()
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
            fn_busca_tabela(dados, link_base, discursos, data_discurso)

        data_atual = fn_get_proxima_data(data_atual)

        df = pd.DataFrame(list(zip(data_discurso, discursos)), columns=['data_discurso', 'discurso'])

    df['discurso_tratado'] = df['discurso'].apply(fn_rm_stopwords)
    df['discurso_tratado'] = df['discurso'].apply(fn_rm_special_char)
    df['discurso_tratado'] = df['discurso'].apply(fn_stemmer)
    return df


def fn_busca_tabela(tabela, link_base, discursos, data_discurso):
    for linha in tabela.findAll('tr'):
        celula = linha.findAll('td')

        if len(celula) == 8:
            data_discurso.append((((celula[0].find(text=True)).replace('\r', '')).replace('\n', '')).replace('\t', ''))

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