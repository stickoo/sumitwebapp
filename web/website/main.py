#!/usr/bin/env python
#
from flask import Flask, render_template, Response

from prometheus_client import Counter, generate_latest, CONTENT_TYPE_LATEST

c = Counter('covilha', 'Covilha hits')
h = Counter('homer', 'Homer hits')

app = Flask(__name__, static_url_path='/static')

@app.route('/metrics')
def metrics():
    return Response(generate_latest(), mimetype=CONTENT_TYPE_LATEST)

@app.route("/covilha")
def covilha():
   c.inc(1)
   return render_template("covilha.html")

@app.route("/homersimpson")
def homer():
   h.inc(1)
   return render_template("homer.html")


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000, debug=True)
