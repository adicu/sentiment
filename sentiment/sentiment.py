import os

from flask import Flask, render_template
from flask.ext.sqlalchemy import SQLAlchemy
from datetime import datetime

from models.day import Day


app = Flask(__name__)
app.config.from_object('config')


@app.route("/")
def home():
    today = datetime.now()
    date = today.strftime("%B %d, %Y")
    day = Day.query.filter_by(date=today).first()
    if day.sentiment <= -0.7:
    	mood = "Terrible"
    	color = "#ff4c40"
    elif day.sentiment > -0.7 and day.sentiment <= -0.4:
    	mood = "Bad"
    	color = "#ff6459"
    elif day.sentiment > -0.4 and day.sentiment <= -0.1:
    	mood = "Meh"
    	color = "#ff9359"
    elif day.sentiment > -0.1 and day.sentiment <= 0.1:
    	mood = "Neutral"
    	color = "#fdd835"
    elif day.sentiment > 0.1 and day.sentiment <= 0.4:
    	mood = "Fine"
    	color = "#a9e66c"
    elif day.sentiment > 0.4 and day.sentiment <= 0.7:
    	mood = "Cheery"
    	color = "#50e582"
    else:
    	mood = "Ecstatic"
    	color = "#4ce659"
    return render_template('index.html',
                            date = date,
                            mood = mood,
                            header_color = color)

if __name__ == "__main__":
    app.debug = True
    app.run(host="0.0.0.0")