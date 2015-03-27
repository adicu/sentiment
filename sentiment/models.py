from datetime import datetime

from sentiment import db

class Day(db.Model):

    __tablename__ = "days"

    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.DateTime, nullable=False)
    sentiment = db.Column(db.Float, nullable=False)
    comment1 = db.Column(db.String, nullable=False)
    comment1_url = db.Column(db.String, nullable=False)
    comment2 = db.Column(db.String, nullable=False)
    comment2_url = db.Column(db.String, nullable=False)
    comment3 = db.Column(db.String, nullable=False)
    comment3_url = db.Column(db.String, nullable=False)

    def __init__(self, sentiment, comment1, comment1_url,
    			comment2, comment2_url, comment3, comment3_url):
        self.date = datetime.today()
        self.sentiment = sentiment
        self.comment1 = comment1
        self.comment1_url = comment1_url
        self.comment2 = comment2
        self.comment2_url = comment2_url
        self.comment3 = comment3
        self.comment3_url = comment3_url

    def get_id(self):
        return self.id

    def __repr__(self):
        return self.date