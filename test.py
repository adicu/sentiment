from bs4 import BeautifulSoup
import requests

url = raw_input("Enter the Bwog article URL: ")

r = requests.get("http://" + url)

data = r.text

soup = BeautifulSoup(data)
all_comments = soup.findAll("div", "reg-comment-body")

print all_comments

