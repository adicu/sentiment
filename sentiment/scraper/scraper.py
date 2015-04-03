from bs4 import BeautifulSoup
import datetime, requests


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
    max_votes1 = 0
    max_votes2 = 0
    max_votes3 = 0
    top_comments = {}
    top_comments[1] = ""
    top_comments[2] = ""
    top_comments[3] = ""

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
            like = l.get_text()
            dislike = d.get_text()

            # Finds comments with most interactions.
            votes = int(like) + int(dislike)
            if votes > max_votes3:
                if votes < max_votes2:
                    max_votes3 = votes
                    top_comments[3] = [comment, votes, a]
                elif votes < max_votes1:
                    max_votes3 = max_votes2
                    max_votes2 = votes
                    top_comments[3] = top_comments[2]
                    top_comments[2] = [comment, votes, a]
                else:
                    max_votes3 = max_votes2
                    max_votes2 = max_votes1
                    max_votes1 = votes
                    top_comments[3] = top_comments[2]
                    top_comments[2] = top_comments[1]
                    top_comments[1] = [comment, votes, a]

    return top_comments


def main():
    num_days = 7
    urls = get_urls(num_days)
    top_comments = scrape(urls)
    for comment_num in top_comments:
        print(top_comments[comment_num][1],
              top_comments[comment_num][0].rstrip().lstrip())
main()