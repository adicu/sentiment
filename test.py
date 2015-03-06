from bs4 import BeautifulSoup
import datetime, requests, csv, re

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
            # print("URL:", url)

    d -= datetime.timedelta(days = 1)

# Gets all words and values from sentiments.csv
sentiments_file = open("sentiments.csv")
dialect = csv.Sniffer().sniff(sentiments_file.read(1024))
sentiments_file.seek(0)
reader = csv.reader(sentiments_file, dialect)

dictionary = {}
for line in reader:
    dictionary.update({line[0] : line[1]})

total_sentiment = 0
words_count = 0

# Get all comments, likes, and dislikes for each article.
for a in urls:
    r = requests.get(a)
    data2 = r.text
    soup2 = BeautifulSoup(data2)
    all_comments = soup2.findAll(class_ = "reg-comment-body")
    all_likes = soup2.findAll(class_ = "like-count")
    all_dislikes = soup2.findAll(class_ = "dislike-count")
    for c, l, d in zip(all_comments, all_likes, all_dislikes):
        comment = c.get_text()
        like = l.get_text()
        dislike = d.get_text()

        comment_words = re.findall(r"\w+", comment)
        # print(comment_words)

        # Determines if a word is a sentiment word.
        for word in comment_words:
            if word in dictionary:
                total_sentiment += float(dictionary[word])
                words_count += 1
                # print(word)
        # print(comment)
        # print("Likes: " + like)
        # print("Dislikes: " + dislike)

# Gives the average positivity/negativity for all comments.
print(total_sentiment / words_count)