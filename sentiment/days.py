from sqlalchemy import *
from sqlalchemy.orm import *
import scraper
import models
from datetime import timedelta, date as d


def create_table():
    """
    Creates the table.
    :return:
    """
    db = create_engine("sqlite:///db/app.db", echo=False)
    metadata = MetaData(db)

    days = Table("days", metadata,
                 Column("id", Integer, primary_key=True),
                 Column("date", Date, nullable=False),
                 Column("sentiment", Float, nullable=False),
                 Column("comment1", String, nullable=False),
                 Column("comment1_url", String, nullable=False),
                 Column("comment2", String, nullable=False),
                 Column("comment2_url", String, nullable=False),
                 Column("comment3", String, nullable=False),
                 Column("comment3_url", String, nullable=False)
                 )

    days.create()


def delete_table():
    """
    Deletes all data.
    :return: None
    """
    db = create_engine("sqlite:///db/app.db", echo=False)
    metadata = MetaData(db)
    days = Table("days", metadata, autoload=True)

    days.drop(db)


def add_entry(date):
    """
    Adds an entry for today. Includes today's date, the sentiment, the top
    3 comments and their associated article urls.
    :param: date: the date to be added.
    :return: None
    """
    db = create_engine("sqlite:///db/app.db", echo=False)
    metadata = MetaData(db)
    days = Table("days", metadata, autoload=True)

    mapper(models.Day, days)

    session = Session()

    comment_index = 0
    url_index = 2

    num_days = 7

    sentiment, top_comments, top_votes = scraper.analyze(date, num_days)

    today = models.Day(date=date,
                       sentiment=sentiment.polarity,
                       comment1=top_comments[1][comment_index],
                       comment1_url=top_comments[1][url_index],
                       comment2=top_comments[2][comment_index],
                       comment2_url=top_comments[2][url_index],
                       comment3=top_comments[3][comment_index],
                       comment3_url=top_comments[3][url_index],
                       )
    session.add(today)
    session.commit()
    session.flush()


def delete_entry(date):
    """
    Deletes the entry on a date.
    :param date: the date to remove.
    :return: None
    """
    db = create_engine("sqlite:///db/app.db", echo=False)
    metadata = MetaData(db)
    days = Table("days", metadata, autoload=True)

    d = days.delete(days.c.date == date)
    d.execute()


def display_table():
    """
    Displays the entire days table.
    :return: None
    """
    db = create_engine("sqlite:///db/app.db", echo=False)

    metadata = MetaData(db)

    # The table of data
    days = Table("days", metadata, autoload=True)

    s = days.select()
    rs = s.execute()

    for row in rs:
        print(row)


def get_entry(date):
    """
    Gets an entry from a specific date.
    :param date: the date of the entry to get.
    :return: the row in the table selected.
    """
    db = create_engine("sqlite:///db/app.db", echo=False)
    metadata = MetaData(db)
    days = Table("days", metadata, autoload=True)

    selection = days.select(days.c.date == date)
    return selection


def display_entry(selection):
    """
    Displays an entry in the table.
    :param selection: the selected entry.
    :return: None
    """
    rs = selection.execute()
    for row in rs:
        print(row)


def main():
    """
    Tests the database.
    :return: None
    """
    day = d.today() - timedelta(days=0)
    add_entry(day)
    # delete_entry(day)
    #display_table()
    # selection = get_entry(day)
    # display_entry(selection)
main()