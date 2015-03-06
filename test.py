from bs4 import BeautifulSoup

import requests
# Assuming all articles are posted on the front page of Bwog, gets all the
# dates of the articles (and all the urls associated with the dates).
r = requests.get("http://bwog.com")
data = r.text

soup = BeautifulSoup(data)
article_dates = soup.findAll(class_="post-datetime")

# print(article_dates)
# This for loop is just to show that the posting date and the links associated
# with those dates can be parsed and used to determine which links are from
# the past 24 hours. dt contains the date, time, and url of the article.
for dt in article_dates:
    # Raw html text
    print("Full date html:", dt)

    # Gets unformatted date and time (it may or may not have a date in it).
    time_string = dt.get_text()

    # Gets the a attribute that has the date and the url in it.
    link = dt.find("a")
    # If the article explicitly lists a date, get that date. The date is only
    # listed on the most recent article from that day, not all of them from a
    # day. If it doesn't explicitly list a date (the text in link is empty),
    # use the date from the most recent article from that day.
    if not(link.get_text() is ""):
        date_string = link.get_text()
    print("Date:", date_string)

    # Splits the date into a list of month, day, year.
    date_list = date_string.replace(",", " ").split()
    print("Date list: ", date_list)

    # If the date is in the unformatted date and time string, remove the date
    # to get only the time.
    if date_string in time_string:
        time_string = time_string.replace(date_string, "")

    # Formats the string into a readable format: "hh:mm am/pm"
    time_string = time_string.replace("@", "")
    time_string = time_string.strip()
    print("Time: ", time_string)

    # Splits the time into hour, minute, period (am/pm).
    time_list = time_string.replace(":", " ").split()
    print("Time list: ", time_list)

    # Once the date and time have been divided up, they can be turned into
    # date objects and their time can be compared against the time right now.
    # Then, once the times have been compared, the ones that are within the
    # last 24 hours are the links that we want.

    # Once the dates and times have been compared, collect only the links
    # from the past 24 hours. This hasn't been done yet.
    url = link.get("href")
    print("URL:", url)



"""
# Gets information for a specific article
url = input("Enter the Bwog article URL: ")
r = requests.get(url)
data = r.text
soup = BeautifulSoup(data)
# Gets all comments, likes, and dislikes (in sequential order but not parsed
# out yet)
all_comments = soup.findAll(class_ = "reg-comment-body")
all_likes = soup.findAll(class_ = "like-count")
all_dislikes = soup.findAll(class_ = "dislike-count")
print(all_comments)
print(all_likes)
print(all_dislikes)
"""