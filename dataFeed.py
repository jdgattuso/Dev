import json
from application_only_auth import Client
import time
import sqlite3
import urllib2
import os

# Twitter API authentication credentials
CONSUMER_KEY = # INSERT KEY
CONSUMER_SECRET = # INSERT SECRET

def cls():
    # Function to clear console
    os.system(['clear','cls'][os.name == 'nt'])

def initialSearch():
    global meta
    client = Client(CONSUMER_KEY, CONSUMER_SECRET)
    tweet = client.request('https://api.twitter.com/1.1/search/tweets.json?q=%23bitcoin&count=100')
    meta = tweet['search_metadata']['refresh_url']

def twitterSearch():
    global meta, count
    client = Client(CONSUMER_KEY, CONSUMER_SECRET)
    tweet = client.request('https://api.twitter.com/1.1/search/tweets.json'+meta+'&count=100')
    meta = tweet['search_metadata']['refresh_url']
    count= len(tweet['statuses'])

def getDate():
    # Record date and time
    global dates, times
    dates = (time.strftime("%m/%d/%Y"))
    times = (time.strftime("%H%M"))
    # Console message
    print 'last performed dataFeed at:'
    print dates + ' ' + times

def getBTCprice():
    # Return current Bitcoin price
    url = 'http://api.cryptocoincharts.info/tradingPair/BTC_USD'
    req = urllib2.Request(url, headers={'User-Agent' : "Magic Browser"})
    con = urllib2.urlopen( req )
    http = con.read()
    j = json.loads(http)
    global price
    price = j['price']

def sqlite():
    conn = sqlite3.connect('data.db')
    c = conn.cursor()
    c.execute("CREATE TABLE IF NOT EXISTS data(Date TEXT,  Time INT, Count INT, Price FLOAT)")
    c.execute("INSERT OR REPLACE INTO data (Date, Time, Count, Price) VALUES(?,?,?,?)", (dates, times, totalCount, price))
    conn.commit()
    conn.close()

# Begin script logic to query APIs and record data
global totalCount
interCount = 0
initialSearch()
time.sleep(10)
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

while 1:
    intercount = 0
    time.sleep(10)
    cls()
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


