import pandas as pd
import requests
import webscrap
import bertweet
import re
import pysentimiento
from pysentimiento import analyzer,create_analyzer
from webscrap import fn_get_notas_taquigafricas, fn_busca_tabela
from bs4 import BeautifulSoup
from flask import Flask, request, jsonify, render_template

app = Flask(__name__)

LINK = "https://www.camara.leg.br/internet/sitaqweb/"
ANALYZER = create_analyzer(task="sentiment", lang="pt")

def get_discursos(discursos):
    results_per_discursos = []
    for i in range(len(discursos)):
        discursos[i] = re.sub("[\"\']", "", discursos[i])
        results_per_discursos.append({'texto_discurso': discursos[i]})

    return results_per_discursos


def get_discursos_bert(discursos):
    results_per_discursos = []
    for i in range(len(discursos)):
        #discursos[i][0] = re.sub("[\"\']", "", discursos[i][0])
        results_per_discursos.append({'texto_discurso': discursos[i][0],
                                      'sentimento': discursos[i][1],
                                      'probabilidade': discursos[i][2]})

    return results_per_discursos


def fn_get_sentimento(discursos):
    lista = []
    for i in discursos:
        sent = ANALYZER.predict(i)
        discurso = [i, sent.output, round(max(sent.probas.values())*100,2)]
        lista.append(discurso)

    return lista


@app.route("/check")
def fn_health_check():
    return {"health": "ok"}, 200


@app.route('/', methods=['GET'])
def index():
    return render_template('result.html', titulo='Análise de Sentimento de Discursos dos Deputados Federais')


@app.route('/bert', methods=['GET'])
def home():
    return render_template('result_bert.html', titulo='Análise de Sentimento de Discursos dos Deputados Federais')


@app.route('/web/api', methods=['POST'])
def fn_get_valores():
    nome_orador = request.form['nome_orador']
    data_inicio = request.form['data_inicio']
    data_fim = request.form['data_fim']
    discursos = fn_get_notas_taquigafricas(nome_orador, data_inicio, data_fim, LINK)
    results = get_discursos(discursos)
    return render_template('result.html',
                           results=results,
                           titulo='Análise de Sentimento de Discursos dos Deputados Federais',
                           nome_orador=nome_orador,
                           data_inicio=data_inicio,
                           data_fim=data_fim)


@app.route('/bert/api', methods=['POST'])
def fn_get_sentimentos_bert():
    nome_orador = request.form['nome_orador']
    data_inicio = request.form['data_inicio']
    data_fim = request.form['data_fim']
    discursos = fn_get_notas_taquigafricas(nome_orador, data_inicio, data_fim, LINK)
    sentimentos = fn_get_sentimento(discursos)
    results = get_discursos_bert(sentimentos)
    return render_template('result_bert.html',
                           results=results,
                           titulo='Análise de Sentimento de Discursos dos Deputados Federais',
                           nome_orador=nome_orador,
                           data_inicio=data_inicio,
                           data_fim=data_fim)


app.run(host='0.0.0.0', port=5000)