import os

from flask import Flask, render_template, request
from flask.ext.sqlalchemy import SQLAlchemy
from datetime import datetime, timedelta, date
from dateutil.relativedelta import relativedelta
from scraper import scraper
from textblob import TextBlob
import cPickle as pickle
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
weather_dict = pickle.load(open('weather.p', 'rb'))

@app.route("/days", methods=["GET", "POST"])
def day_chart():
    active_page = {'Daily':'active','Weekly':'','Monthly':'','Yearly':''}
    
    if request.method == "POST":
        if request.form["num"] == '':
            start = datetime.strptime(request.form["start"], "%m/%d/%y").date()
            end = datetime.strptime(request.form["end"], "%m/%d/%y").date()
            dates, data, weather = get_data("days", end, '', start)
        else: 
            dates, data, weather = get_data("days", test, int(request.form["num"]))
        return render_template('chart.html', table_name = "days",
                                sentiment_data = data, weather_data = weather,
                                dates = json.dumps(dates),
                                color = color, active_page = active_page)
    
    else:
        dates, data, weather = get_data("days", test, 7)
        return render_template('chart.html', table_name = "days",
                                sentiment_data = data, weather_data = weather,
                                dates = json.dumps(dates),
                                color = color, active_page = active_page)


@app.route("/weeks", methods=["GET", "POST"])
def week_chart():
    active_page = {'Daily':'','Weekly':'active','Monthly':'','Yearly':''}
    
    if request.method == "POST":
        if request.form["num"] == '':
            start = datetime.strptime(request.form["start"], "%m/%d/%y").date()
            end = datetime.strptime(request.form["end"], "%m/%d/%y").date()
            dates, data, weather = get_data("weeks", end, '', start)
        else: 
            dates, data, weather = get_data("weeks", test, int(request.form["num"]))
        return render_template('chart.html', table_name = "weeks",
                                sentiment_data = data, weather_data = weather,
                                dates = json.dumps(dates),
                                color = color, active_page = active_page)
    
    else:
        dates, data, weather = get_data("weeks", test, 4)
        return render_template('chart.html', table_name = "weeks",
                                sentiment_data = data, weather_data = weather,
                                dates = json.dumps(dates),
                                color = color, active_page = active_page)


@app.route("/months", methods=["GET", "POST"])
def month_chart():
    active_page = {'Daily':'','Weekly':'','Monthly':'active','Yearly':''}
    
    if request.method == "POST":
        if request.form["num"] == '':
            start = datetime.strptime(request.form["start"], "%m/%d/%y").date()
            end = datetime.strptime(request.form["end"], "%m/%d/%y").date()
            dates, data, weather = get_data("months", end, '', start)
        else: 
            dates, data, weather = get_data("months", test, int(request.form["num"]))
        return render_template('chart.html', table_name = "months",
                                sentiment_data = data, weather_data = weather,
                                dates = json.dumps(dates),
                                color = color, active_page = active_page)
    
    else:
        dates, data, weather = get_data("months", test, 3)
        return render_template('chart.html', table_name = "months",
                                sentiment_data = data, weather_data = weather,
                                dates = json.dumps(dates),
                                color = color, active_page = active_page)


@app.route("/years", methods=["GET", "POST"])
def year_chart():
    active_page = {'Daily':'','Weekly':'','Monthly':'','Yearly':'active'}
    
    if request.method == "POST":
        if request.form["num"] == '':
            start = datetime.strptime(request.form["start"], "%m/%d/%y").date()
            end = datetime.strptime(request.form["end"], "%m/%d/%y").date()
            dates, data, weather = get_data("years", end, '', start)
        else: 
            dates, data, weather = get_data("years", test, int(request.form["num"]))
        return render_template('chart.html', table_name = "years",
                                sentiment_data = data, weather_data = weather,
                                dates = json.dumps(dates),
                                color = color, active_page = active_page)
    
    else:
        dates, data, weather = get_data("years", test, 2)
        return render_template('chart.html', table_name = "years",
                                sentiment_data = data, weather_data = weather,
                                dates = json.dumps(dates),
                                color = color, active_page = active_page)



def get_data(table_name, end, num, start=None):
    """
    Gets data for the past number of
    days/weeks/months/years from today,
    or for the specified date range.
    :return: dates, data, weather lists
    """
    if start == None:
        if table_name == "days": start = end - timedelta(days=num-1) 
        if table_name == "weeks": start = end - timedelta(weeks=num-1) 
        if table_name == "months": start = end - relativedelta(months=+num-1) 
        if table_name == "years": start = end - relativedelta(years=+num-1) 
    else: 
        start = days.get_entry(table_name, start).date
    
    dates = []
    data = []
    weather = []
    
    while start <= end:
        entry = days.get_entry(table_name, start)
        data.append(entry.sentiment)
        
        if table_name == "days": 
            dates.append(entry.date.strftime("%B %d, %Y"))
            start = start + timedelta(days=1)
        if table_name == "weeks": 
            dates.append(entry.date.strftime("%B %d, %Y"))
            start = start + timedelta(weeks=1) 
        if table_name == "months": 
            dates.append(entry.date.strftime("%B %Y"))
            start = start + relativedelta(months=+1) 
        if table_name == "years": 
            dates.append(entry.date.strftime("%Y"))
            start = start + relativedelta(years=+1) 

        # 7/15/15 is the last entry in the current weather dictionary
        num_days = (min(start, date(2015,7,15)) - entry.date).days
        d = {entry.date + timedelta(days=i): weather_dict[entry.date + timedelta(days=i)] for i in range(num_days)}
        weather.append(float(sum(d.values()))/float(len(d)))

    return dates, data, weather


def get_sentiments(comment):
    polarity = "{0:.2f}".format(TextBlob(comment).sentiment.polarity)
    subjectivity = "{0:.2f}".format(TextBlob(comment).sentiment.subjectivity)
    return "Polarity: {0} | Subjectivity: {1}".format(polarity, subjectivity)


app.jinja_env.globals.update(get_sentiments=get_sentiments)

if __name__ == "__main__":
    app.debug = True
    app.run(host="0.0.0.0")