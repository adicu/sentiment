import os

from flask import Flask, render_template
from flask.ext.sqlalchemy import SQLAlchemy
from datetime import datetime, timedelta, date
from scraper import scraper
from textblob import TextBlob
import json

import days


app = Flask(__name__)
app.config.from_object('config')

# all dates in April 2015 work with the database
test = date(2015,4,22)
d = test.strftime("%B %d, %Y")
day = days.get_entry("days", test)
week = days.get_entry("weeks", test)
month = days.get_entry("months", test)
year = days.get_entry("years", test)

@app.route("/")
def home():
    """
    Displays the top 3 comments
    of the day/week/month/year
    """
    mood, color = get_mood(day.sentiment)

    return render_template('index.html',
                            date = d,
                            mood = mood,
                            header_color = color,
                            day = day,
                            week = week,
                            month = month,
                            year = year)


def get_mood(sentiment):

    if sentiment <= -0.7:
        mood = "Terrible &#x1F621;"
        color = "#ff4c40"
    elif sentiment > -0.7 and sentiment <= -0.4:
        mood = "Bad &#x1F625;"
        color = "#ff6459"
    elif sentiment > -0.4 and sentiment <= -0.1:
        mood = "Meh &#x1F615;"
        color = "#ff9359"
    elif sentiment == 0.0:
        mood = "Sleeping &#x1f634"
        color = "#808080"
    elif sentiment > -0.1 and sentiment <= 0.1:
        mood = "Neutral &#x1F610;"
        color = "#fdd835"
    elif sentiment > 0.1 and sentiment <= 0.4:
        mood = "Fine &#x1F600;"
        color = "#a9e66c"
    elif sentiment > 0.4 and sentiment <= 0.7:
        mood = "Cheery &#x1F60E;"
        color = "#50e582"
    else:
        mood = "Ecstatic &#x1F60D;"
        color = "#4ce659"

    return mood, color


def get_sentiments(comment):
    polarity = "{0:.2f}".format(TextBlob(comment).sentiment.polarity)
    subjectivity = "{0:.2f}".format(TextBlob(comment).sentiment.subjectivity)
    return "Polarity: {0} | Subjectivity: {1}".format(polarity, subjectivity)

# only works for /chart/days so far
@app.route("/chart/<table_name>")
def chart(table_name):
    mood, color = get_mood(day.sentiment)
    dates, data = get_data(table_name, test)
    return render_template('chart.html', table_name = table_name,
                            sentiment_data = data,
                            dates = json.dumps(dates),
                            color = color)


def get_data(table_name, d):
    start = d - timedelta(days=7)
    dates = []
    data = []
    while start <= d:
        day = days.get_entry("days", start)
        dates.append(day.date.strftime("%B %d, %Y"))
        data.append(day.sentiment)
        start = start + timedelta(days=1)
    return dates, data


app.jinja_env.globals.update(get_sentiments=get_sentiments)

if __name__ == "__main__":
    app.debug = True
    app.run(host="0.0.0.0")