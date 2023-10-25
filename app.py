import pandas as pd
import requests

import webscrap
from webscrap import fn_get_notas_taquigafricas
from bs4 import BeautifulSoup
from flask import Flask, request, jsonify, render_template

app = Flask(__name__)

LINK = "https://www.camara.leg.br/internet/sitaqweb/"
#CONTEUDO_SITE = []  ## COLUNA 8
LISTA = []

#def get_discursos(discursos):
#    results_per_discursos = []
#    for index, row in discursos.iterrows():
#        results_per_discursos.append({'Discurso': row['discurso']})
#    return results_per_discursos

def get_discursos(discursos):
    results_per_discursos = []
    for i in range(len(discursos)):
        results_per_discursos.append({'texto_discurso': discursos[i]})
    return results_per_discursos

@app.route("/check")
def fn_health_check():
    return {"health": "ok"}, 200


@app.route('/', methods=['GET'])
def index():
    return render_template('result.html', titulo='Análise de Sentimento de Discursos Parlamentares')


@app.route('/web/api', methods=['POST'])
def fn_get_valores():
    nome_orador = request.form['nome_orador']
    data_inicio = request.form['data_inicio']
    data_fim = request.form['data_fim']
    fn_get_notas_taquigafricas(nome_orador, data_inicio, data_fim, LINK)
    #discursos = pd.DataFrame()
    #print(webscrap.CONTEUDO_SITE)
    discursos = webscrap.CONTEUDO_SITE
    #results = pd.DataFrame()
    results = get_discursos(discursos)
    #return jsonify({'Discursos': get_discursos(results)})
    return render_template('result.html',
                           results=results,
                           titulo='Análise de Sentimento de Discursos Parlamentares',
                           nome_orador=nome_orador,
                           data_inicio=data_inicio,
                           data_fim=data_fim)

#def process():
#    input_text = request.form['input_text']
#    results = make_predictions(input_text)
#    return render_template('result.html', results=results, titulo='Demandas Conle', input_text=input_text)


app.run(host='0.0.0.0', port=5000)