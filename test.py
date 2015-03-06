from bs4 import BeautifulSoup
import datetime, requests

# Gets today's date.
d = datetime.date.today()
urls = []

# Loops through last seven days on Bwog.
for day in range(7):
    url_date = str(d).replace('-', '/')
    r = requests.get("http://bwog.com/" + url_date)
    data = r.text
    soup = BeautifulSoup(data)
    article_times = soup.findAll(class_="post-datetime")

    # Prints and stores all article URLs for that day.
    for dt in article_times:
        time_string = dt.get_text()
        link = dt.find("a")
        url = link.get("href")
        if url != "":
            urls.append(url)
            print("URL:", url)

    d -= datetime.timedelta(days = 1)

# Get all comments, likes, and dislikes for each article.
for a in urls:
    r2 = requests.get(a)
    data2 = r2.text
    soup2 = BeautifulSoup(data2)
    all_comments = soup2.findAll(class_ = "reg-comment-body")
    all_likes = soup2.findAll(class_ = "like-count")
    all_dislikes = soup2.findAll(class_ = "dislike-count")
    for c, l, d in zip(all_comments, all_likes, all_dislikes):
        comment = c.get_text()
        like = l.get_text()
        dislike = d.get_text()
        print(comment)
        print("Likes: " + like)
        print("Dislikes: " + dislike)