import os

from flask import Flask, render_template
from flask.ext.sqlalchemy import SQLAlchemy

app = Flask(__name__)


app.config.from_object('config')
db = SQLAlchemy(app)


@app.route("/")
def home():
    return render_template('index.html')

if __name__ == "__main__":
    app.debug = True
    app.run(host="0.0.0.0")