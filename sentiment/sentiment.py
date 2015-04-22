import os

from flask import Flask, render_template
from flask.ext.sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.config.from_object('config')


@app.route("/")
def home():
    today = datetime.now()
    date = today.strftime("%B %d, %Y")
    return render_template('index.html',
                            date = date)

if __name__ == "__main__":
    app.debug = True
    app.run(host="0.0.0.0")