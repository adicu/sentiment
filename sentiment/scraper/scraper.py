from bs4 import BeautifulSoup
import datetime, requests
from textblob import TextBlob


def get_urls(num_days):
    d = datetime.date.today()
    urls = []

    # Loops through last N days on Bwog.
    for day in range(num_days):
        url_date = str(d).replace('-', '/')
        r = requests.get("http://bwog.com/" + url_date)
        data = r.text
        soup = BeautifulSoup(data)
        article_times = soup.findAll(class_="post-datetime")

        # Stores all article URLs for that day.
        for dt in article_times:
            time_string = dt.get_text()
            link = dt.find("a")
            url = link.get("href")
            if url != "":
                urls.append(url)

        d -= datetime.timedelta(days = 1)

    return urls


def scrape(urls):
    top_votes = {}
    top_votes[1] = 0
    top_votes[2] = 0
    top_votes[3] = 0
    top_comments = {}
    top_comments[1] = ""
    top_comments[2] = ""
    top_comments[3] = ""
    comments = []

    for a in urls:
        r = requests.get(a)
        data2 = r.text
        soup2 = BeautifulSoup(data2)

        # Get all comments, likes, and dislikes for each article.
        all_comments = soup2.findAll(class_ = "reg-comment-body")
        all_likes = soup2.findAll(class_ = "like-count")
        all_dislikes = soup2.findAll(class_ = "dislike-count")

        for c, l, d in zip(all_comments, all_likes, all_dislikes):
            comment = c.get_text()
            comments.append(comment.lstrip().rstrip())
            like = l.get_text()
            dislike = d.get_text()

            # Finds comments with most interactions.
            votes = int(like) + int(dislike)
            if votes > top_votes[3]:
                if votes < top_votes[2]:
                    top_votes[3] = votes
                    top_comments[3] = [comment, votes, a]
                elif votes < top_votes[1]:
                    top_votes[3] = top_votes[2]
                    top_votes[2] = votes
                    top_comments[3] = top_comments[2]
                    top_comments[2] = [comment, votes, a]
                else:
                    top_votes[3] = top_votes[2]
                    top_votes[2] = top_votes[1]
                    top_votes[1] = votes
                    top_comments[3] = top_comments[2]
                    top_comments[2] = top_comments[1]
                    top_comments[1] = [comment, votes, a]

    for comment_num in top_comments:
        top_comments[comment_num][0] = top_comments[comment_num][0].rstrip().\
            lstrip()

    return comments, top_comments, top_votes


def analyze():
    num_days = 7
    urls = get_urls(num_days)
    comments, top_comments, top_votes = scrape(urls)
    all_comments = ""
    for comment in comments:
        all_comments += comment + "\t"
    comment_blob = TextBlob(all_comments)

    return comment_blob.sentiment, top_comments, top_votes

analyze()