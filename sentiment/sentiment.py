import os

from flask import Flask, render_template, request
from flask.ext.sqlalchemy import SQLAlchemy
from datetime import datetime, timedelta, date
from dateutil.relativedelta import relativedelta
from scraper import scraper
from textblob import TextBlob
import json

import days


app = Flask(__name__)
app.config.from_object('config')

# all dates in April 2015 work with the database
test = date(2015,4,30)
d = test.strftime("%B %d, %Y")
day = days.get_entry("days", test)
week = days.get_entry("weeks", test)
month = days.get_entry("months", test)
year = days.get_entry("years", test)
mood, color = days.get_mood(day.sentiment)

@app.route("/")
def home():
    """
    Displays the top 3 comments
    of the day/week/month/year
    """

    return render_template('index.html',
                            date = d,
                            mood = mood,
                            header_color = color,
                            day = day,
                            week = week,
                            month = month,
                            year = year)


"""
created different routes for daily/weekly/monthly/yearly,
because each will be compared with different trends
(e.g. temperature, library wifi usage, twitter sentiment)
"""
active_page = {'Daily':'','Weekly':'','Monthly':'','Yearly':''}

@app.route("/days", methods=["GET", "POST"])
def day_chart():
    active_page = {'Daily':'active','Weekly':'','Monthly':'','Yearly':''}
    if request.method == "POST":
        dates, data = get_data("days", test, int(request.form["num"]))
        return render_template('chart.html', table_name = "days",
                                sentiment_data = data,
                                dates = json.dumps(dates),
                                color = color, active_page = active_page)
    else:
        dates, data = get_data("days", test, 7)
        return render_template('chart.html', table_name = "days",
                                sentiment_data = data,
                                dates = json.dumps(dates),
                                color = color, active_page = active_page)


@app.route("/weeks", methods=["GET", "POST"])
def week_chart():
    active_page = {'Daily':'','Weekly':'active','Monthly':'','Yearly':''}
    if request.method == "POST":
        dates, data = get_data("weeks", test, int(request.form["num"]))
        return render_template('chart.html', table_name = "weeks",
                                sentiment_data = data,
                                dates = json.dumps(dates),
                                color = color, active_page = active_page)
    else:
        dates, data = get_data("weeks", test, 4)
        return render_template('chart.html', table_name = "weeks",
                                sentiment_data = data,
                                dates = json.dumps(dates),
                                color = color, active_page = active_page)


@app.route("/months", methods=["GET", "POST"])
def month_chart():
    active_page = {'Daily':'','Weekly':'','Monthly':'active','Yearly':''}
    if request.method == "POST":
        dates, data = get_data("months", test, int(request.form["num"]))
        return render_template('chart.html', table_name = "months",
                                sentiment_data = data,
                                dates = json.dumps(dates),
                                color = color, active_page = active_page)
    else:
        dates, data = get_data("months", test, 3)
        return render_template('chart.html', table_name = "months",
                                sentiment_data = data,
                                dates = json.dumps(dates),
                                color = color, active_page = active_page)


@app.route("/years", methods=["GET", "POST"])
def year_chart():
    active_page = {'Daily':'','Weekly':'','Monthly':'','Yearly':'active'}
    if request.method == "POST":
        dates, data = get_data("years", test, int(request.form["num"]))
        return render_template('chart.html', table_name = "years",
                                sentiment_data = data,
                                dates = json.dumps(dates),
                                color = color, active_page = active_page)
    else:
        dates, data = get_data("years", test, 2)
        return render_template('chart.html', table_name = "years",
                                sentiment_data = data,
                                dates = json.dumps(dates),
                                color = color, active_page = active_page)



def get_data(table_name, d, num):
    if table_name == "days": start = d - timedelta(days=num-1) 
    if table_name == "weeks": start = d - timedelta(weeks=num-1) 
    if table_name == "months": start = d - relativedelta(months=+num-1) 
    if table_name == "years": start = d - relativedelta(years=+num-1) 
    dates = []
    data = []
    while start <= d:
        entry = days.get_entry(table_name, start)
        dates.append(entry.date.strftime("%B %d, %Y"))
        data.append(entry.sentiment)
        if table_name == "days": start = start + timedelta(days=1)
        if table_name == "weeks": start = start + timedelta(weeks=1) 
        if table_name == "months": start = start + relativedelta(months=+1) 
        if table_name == "years": start = start + relativedelta(years=+1) 
    return dates, data


def get_sentiments(comment):
    polarity = "{0:.2f}".format(TextBlob(comment).sentiment.polarity)
    subjectivity = "{0:.2f}".format(TextBlob(comment).sentiment.subjectivity)
    return "Polarity: {0} | Subjectivity: {1}".format(polarity, subjectivity)


app.jinja_env.globals.update(get_sentiments=get_sentiments)

if __name__ == "__main__":
    app.debug = True
    app.run(host="0.0.0.0")