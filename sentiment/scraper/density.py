import requests
import cPickle as pickle 
from bs4 import BeautifulSoup
from datetime import timedelta, date as d, datetime
   

def get_day(density, date, key):
    
    day = date.strftime("%Y-%m-%d")
    
    url = 'http://density.adicu.com/day/{0}/group/130?auth_token={1}'
    
    r = requests.get(url.format(day, key)).json()
    
    data = r["data"]

    traffic = {i: data[i]["percent_full"] for i in range(len(data))}
    
    density[date] = float(sum(traffic.values()))/float(len(traffic))

    print 'completed {0}'.format(date)

    return density
    

def main():

    density = {}

    key = raw_input("Enter API key: ")

    date = d(2014,7,1)

    while (date <= d.today()):
        density = get_day(density, date, key)
        date = date + timedelta(days=1)

    pickle.dump(density, open("density.p", "wb"))


if __name__ == "__main__":
    main()

