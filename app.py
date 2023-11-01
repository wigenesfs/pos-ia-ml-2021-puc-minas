import pandas as pd
import requests
import webscrap
import pysentimiento
import pickle
import sklearn
from pysentimiento import analyzer,create_analyzer
from webscrap import fn_get_notas_taquigafricas, fn_busca_tabela
from flask import Flask, request, jsonify, render_template
from sklearn.feature_extraction.text import TfidfVectorizer

app = Flask(__name__)

LINK = "https://www.camara.leg.br/internet/sitaqweb/"
ANALYZER = create_analyzer(task="sentiment", lang="pt")
TFIDF_VECTORIZER = 'models/tfidf_vectorizer.pkl'
MODEL_FILENAME = 'models/svc_model.pkl'
with open(MODEL_FILENAME, 'rb') as file:
    svc_model = pickle.load(file)
with open(TFIDF_VECTORIZER, 'rb') as file:
    tfidf = pickle.load(file)

LABEL_SENTIMENT_SVM = {
    'pos': 'Positivo',
    'neg': 'Negativo'}

LABEL_SENTIMENT_BERT = {
    'POS': 'Positivo',
    'NEG': 'Negativo',
    'NEU': 'Neutro'}


def fn_get_discursos_svm(discursos):
    results_per_discursos = []
    for i in range(len(discursos)):
        results_per_discursos.append({'texto_discurso': discursos[i][0],
                                      'sentimento': discursos[i][1],
                                      'probabilidade': discursos[i][2]})

    return results_per_discursos


def fn_get_discursos_bert(discursos):
    results_per_discursos = []
    for i in range(len(discursos)):
        results_per_discursos.append({'texto_discurso': discursos[i][0],
                                      'sentimento': discursos[i][1],
                                      'probabilidade': discursos[i][2]})

    return results_per_discursos


def fn_get_sentimento_svm(discursos):
    lista = []
    for i in discursos:
        sent = svc_model.predict(tfidf.transform([i]))
        proba = svc_model.predict_proba(tfidf.transform([i]))
        discurso = [i, LABEL_SENTIMENT_SVM[sent.item()], round(proba.max()*100,2)]
        lista.append(discurso)

    return lista


def fn_get_sentimento_bert(discursos):
    lista = []
    for i in discursos:
        sent = ANALYZER.predict(i)
        discurso = [i, LABEL_SENTIMENT_BERT[sent.output], round(max(sent.probas.values())*100,2)]
        lista.append(discurso)

    return lista


@app.route("/check")
def fn_health_check():
    return {"health": "ok"}, 200


@app.route('/svm', methods=['GET'])
def fn_predict():
    return render_template('result_svm.html', titulo='Análise de Sentimento de Discursos dos Deputados Federais')


@app.route('/bert', methods=['GET'])
def home():
    return render_template('result_bert.html', titulo='Análise de Sentimento de Discursos dos Deputados Federais')


@app.route('/svm/api', methods=['POST'])
def fn_svm():
    nome_orador = request.form['nome_orador']
    data_inicio = request.form['data_inicio']
    data_fim = request.form['data_fim']
    discursos = fn_get_notas_taquigafricas(nome_orador, data_inicio, data_fim, LINK)
    sentimentos = fn_get_sentimento_svm(discursos)
    results = fn_get_discursos_svm(sentimentos)
    return render_template('result_svm.html',
                           results=results,
                           titulo='Análise de Sentimento de Discursos dos Deputados Federais',
                           nome_orador=nome_orador,
                           data_inicio=data_inicio,
                           data_fim=data_fim)


@app.route('/bert/api', methods=['POST'])
def fn_bert():
    nome_orador = request.form['nome_orador']
    data_inicio = request.form['data_inicio']
    data_fim = request.form['data_fim']
    discursos = fn_get_notas_taquigafricas(nome_orador, data_inicio, data_fim, LINK)
    sentimentos = fn_get_sentimento_bert(discursos)
    results = fn_get_discursos_bert(sentimentos)
    return render_template('result_bert.html',
                           results=results,
                           titulo='Análise de Sentimento de Discursos dos Deputados Federais',
                           nome_orador=nome_orador,
                           data_inicio=data_inicio,
                           data_fim=data_fim)


app.run(host='0.0.0.0', port=5000)