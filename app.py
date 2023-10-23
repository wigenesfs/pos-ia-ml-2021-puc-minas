app = Flask(__name__)

@app.route("/")
def fn_health_check():
    return {"health": "ok"}, 200