# Sentiment
Sentiment is a project that analyzes the emotions of Bwog comments.

## Data Sources
Data for the sentiment project is taken from a Columbia campus news site, [Bwog](bwog.com). In the future, the project may expand to include the [Columbia Spectator](columbiaspectator.com).

## Sentiment Analysis
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
        |-- scraper.py
        |-- __init__.py
    |-- static
        \
        |-- css
            \
            |-- colors.css
            |-- style.css
        |-- js
            \
            |-- readmore.js
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
