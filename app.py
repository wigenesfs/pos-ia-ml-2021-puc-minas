from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route("/")
def fn_health_check():
    return {"health": "ok"}, 200


@app.route('/hello')
def hello():
    return 'Hello, World'

app.run(host='0.0.0.0', port=5000)