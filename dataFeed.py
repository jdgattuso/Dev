import json
from application_only_auth import Client
import time
import sqlite3
import urllib2
import os

# Twitter API authentication credentias
CONSUMER_KEY = # INSERT KEY
CONSUMER_SECRET = # INSERT SECRET

def cls():
    # Function to clear console
    os.system(['clear','cls'][os.name == 'nt'])

def initialSearch():
    global meta, exception
    while 1:
        try:
            client = Client(CONSUMER_KEY, CONSUMER_SECRET)
            tweet = client.request('https://api.twitter.com/1.1/search/tweets.json?q=%23bitcoin&count=100')
            meta = tweet['search_metadata']['refresh_url']
            exception = 0
        except:
            print 'Attempting intialSearch() - exception'
            exception = 1
            time.sleep(3)
            pass
        if exception == 0:
            break
        

def twitterSearch():
    global meta, count, exception
    while 1:
        try:
            client = Client(CONSUMER_KEY, CONSUMER_SECRET)
            tweet = client.request('https://api.twitter.com/1.1/search/tweets.json'+meta+'&count=100')
            meta = tweet['search_metadata']['refresh_url']
            count= len(tweet['statuses'])
        except:
            print 'Attempting twitterSearch() - exception'
            exception = 1
            time.sleep(3) 
            pass
        if exception == 0:
            break
    
def getDate():
    # Record date and time
    global dates, times, exception
    dates = (time.strftime("%m/%d/%Y"))
    times = (time.strftime("%H%M"))
    # Console message
    print 'last performed dataFeed at:'
    print dates + ' ' + times

def getBTCprice():
    while 1:
        try:
            # Return current Bitcoin price
            url = 'http://api.cryptocoincharts.info/tradingPair/BTC_USD'
            req = urllib2.Request(url, headers={'User-Agent' : "Magic Browser"})
            con = urllib2.urlopen( req )
            http = con.read()
            j = json.loads(http)
            global price
            price = j['price']
            exception = 0
        except:
            print 'Attempting getBTCprice() - exception'
            exception = 1
            time.sleep(3) 
            pass
        if exception == 0:
            break

def sqlite():
    conn = sqlite3.connect('data.db')
    c = conn.cursor()
    c.execute("CREATE TABLE IF NOT EXISTS data(Date TEXT,  Time INT, Count INT, Price FLOAT)")
    c.execute("INSERT OR REPLACE INTO data (Date, Time, Count, Price) VALUES(?,?,?,?)", (dates, times, totalCount, price))
    conn.commit()
    conn.close()

# Begin logic
initialSearch()
while 1:
    time.sleep(10)
    cls()
    interCount = 0
    while 1:
        twitterSearch()
        if count < 100:
            break
        else: 
            interCount = interCount + count
    totalCount = count + interCount
    getBTCprice()
    getDate()
    sqlite()       
