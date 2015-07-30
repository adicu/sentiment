import requests
import cPickle as pickle 
from bs4 import BeautifulSoup
from datetime import timedelta, date as d, datetime
   

def get_month(weather_dict, date):
    
    month = date.strftime("%m/%d/%Y")
    
    url = 'http://www.accuweather.com/en/us/new-york-ny/10007/january-weather/349727?monyr={0}&view=table'
    
    r = requests.get(url.format(month))
    
    soup = BeautifulSoup(r.text).find('tbody')
    
    daily_temp = soup.find_all('tr', class_='pre')
    
    for day in daily_temp:
        d = datetime.strptime(day.find('th').contents[2], "%m/%d/%Y").date()
        temp = day.find('td').contents[0]
        temp = int(temp[0:len(temp)-1])
        weather_dict[d] = temp

    return weather_dict
    

def main():

	weather_dict = {}
	month = d(2014,1,1)

	for i in range(1,13):
		weather_dict = get_month(weather_dict, d(month.year, i, 1))

	month = d(2015,1,1)

	for i in range(1,8):
		weather_dict = get_month(weather_dict, d(month.year, i, 1))

	pickle.dump(weather_dict, open("weather.p", "wb"))


if __name__ == "__main__":
    main()

