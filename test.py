from bs4 import BeautifulSoup

import requests
# Assuming all articles are posted on the front page of Bwog, gets all the
# dates of the articles (and all the urls associated with the dates).
r = requests.get("http://bwog.com")
data = r.text

soup = BeautifulSoup(data)
article_dates = soup.findAll(class_="post-datetime")
print(article_dates)


# Gets information for a specific article
url = input("Enter the Bwog article URL: ")
r = requests.get("http://" + url)

# Gets all comments, likes, and dislikes (in sequential order but not parsed
# out yet)
all_comments = soup.findAll(class_="reg-comment-body")
all_likes = soup.findAll(class_="like-count")
all_dislikes = soup.findAll(class_="dislike-count")

print(all_comments)
print(all_likes)
print(all_dislikes)
