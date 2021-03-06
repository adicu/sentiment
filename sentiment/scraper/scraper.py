from bs4 import BeautifulSoup
from textblob import TextBlob
import datetime, requests
from datetime import date


def get_urls(date, num_days):
    """
    Gets urls for the past num_days from date.
    :param date: the date to get urls from.
    :param num_days: the number of days to search.
    :return: the urls to the articles.
    """
    d = date
    urls = []

    # Loops through last N days on Bwog.
    for day in range(num_days):
        url_date = str(d).replace('-', '/')
        r = requests.get("http://bwog.com/" + url_date + "/")
        data = r.text
        soup = BeautifulSoup(data)
        article_times = soup.findAll(class_="blog-section")

        # Stores all article URLs for that day.
        for dt in article_times:
            time_string = dt.get_text()
            link = dt.find("a")
            url = link.get("href")
            if url != "":
                urls.append(url)

        d -= datetime.timedelta(days = 1)

    return urls


def get_title(url):
    """
    Gets the title of the article's url.
    :return: the title name, otherwise ""
    """
    if url == "":
        return ""
    else:
        r = requests.get(url)
        data = r.text
        soup = BeautifulSoup(data)
        titles = soup.findAll(class_="post_title")
        return titles[0].span.string


def scrape(urls):
    """
    Scrapes the webpages for information on comments.
    :param urls: the article urls.
    :return: a list of all comments, the top comments, and the votes on the
    top comments.
    """
    # Dictionary of top comments.
    top_comments = {}
    top_comments[1] = ""
    top_comments[2] = ""
    top_comments[3] = ""
    # Dictionary of votes on top comments.
    top_votes = {}
    top_votes[1] = 0
    top_votes[2] = 0
    top_votes[3] = 0
    # List of all comments.
    comments = []

    # Goes through all urls.
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

            # Finds comments with most upvotes.
            votes = int(like) - int(dislike)
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

    # Formats top comments to remove newline characters.
    for comment_num in top_comments:
        if top_comments[comment_num]:
            top_comments[comment_num][0] = top_comments[comment_num][0].strip()
        else:
            top_comments[comment_num] = ["", 0, ""]

    titles = {}
    titles[1] = get_title(top_comments[1][2])
    titles[2] = get_title(top_comments[2][2])
    titles[3] = get_title(top_comments[3][2])

    return comments, top_comments, top_votes, titles


def analyze(date, num_days):
    """
    Analyzes the articles for a date for the past num_days.
    :param date: the date to start analyzing from.
    :param num_days: the number of days back to analyze.
    :return: the sentiment, the top comments, and the top votes.
    """
    # Scrapes the urls for comments, top comments, and top votes.
    urls = get_urls(date, num_days)
    comments, top_comments, top_votes, titles = scrape(urls)

    # Gets the sentiment from all the comments combined together.
    all_comments = ""
    for comment in comments:
        all_comments += comment + "\t"
    comment_blob = TextBlob(all_comments)

    return comment_blob.sentiment, top_comments, top_votes, titles

def main():
    """
    Tests the scraper.
    :return: None
    """
    print get_urls(date(2015,4,2),1)
    print analyze(date(2015,4,2),1)
    print get_title("http://bwog.com/2015/04/02/bacchtails-2015/")

if __name__ == "__main__":
    main()