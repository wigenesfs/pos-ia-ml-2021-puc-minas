import webscrap
import pysentimiento
from pysentimiento import analyzer


def fn_get_sentimento(discurso):
    for i in discurso:
        sent = analyzer.predict(i)
        lista = [[i, sent.output, round(max(sent.probas.values()),4)]]
        return lista