from datetime import date

class Day(object):

    def __init__(self, date, sentiment, comment1, comment1_url,
    			comment1_title, comment2, comment2_url, comment2_title, 
                comment3, comment3_url, comment3_title):
        self.date = date
        self.sentiment = sentiment
        self.comment1 = comment1
        self.comment1_url = comment1_url
        self.comment1_title = comment1_title
        self.comment2 = comment2
        self.comment2_url = comment2_url
        self.comment2_title = comment2_title
        self.comment3 = comment3
        self.comment3_url = comment3_url
        self.comment3_title = comment3_title

    def get_id(self):
        return self.id

    def __repr__(self):
        return self.date