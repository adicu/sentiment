# Sentiment
Sentiment is a project that analyzes the emotions of Bwog comments.

## Data Sources
Data for the sentiment project is taken from a Columbia campus news site Bwog (bwog.com). In the future, the project may expand to include Columbia Spectator (columbiaspectator.com).

## Sentiment Analysis API
Currently, TextBlob is the library used to perform sentiment analysis on the comment data using natural language processing.

## App Structure
```
|-- README.md
|-- Vagrantfile
|-- bootstrap.sh
|-- sentiment
    \
    |-- days.py
    |-- sentiment.py
    |-- __init__.py
    |-- config
        \
        |-- __init__.py
    |-- db
        \
        |-- app.db
    |-- models
        \
        |-- day.py
        |-- __init__.py
    |-- scraper
        \
        |-- __init__.py
        |-- scraper.py
    |-- static
        \
        |-- css
            \
            |-- colors.css
            |-- style.css
        |-- js
            \
            |-- resources.js
    |-- templates
        \
        |-- index.html
        |-- layout.html
```

## List of Developers
- Kimberly Tao
- Sophie Stadler
- Jackie Luo
- Kevin Shen