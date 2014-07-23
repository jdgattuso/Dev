import urllib2
from BeautifulSoup import BeautifulSoup
from django.template.defaultfilters import slugify
import sqlite3

conn = sqlite3.connect('jobss.db')
c = conn.cursor()
c.execute("CREATE TABLE IF NOT EXISTS Jobs(Title TEXT, Company TEXT, Link TEXT)")
#c.executemany('INSERT INTO Jobs VALUES(?,?)', jobsiter())
keyword = slugify('')
response = urllib2.urlopen('http://api.indeed.com/ads/apisearch?publisher=8215028440716713&q='+keyword+'&l=Syracuse+ny&sort=&radius=&st=&jt=&start=&limit=99&fromage=&filter=&latlong=&co=us&chnl=&userip=&useragent=Mozilla/%2F4.0%28Firefox%29&v=2')
http = response.read() 
soup = BeautifulSoup(http)
jobtitle = [] 
company = []
links = []
results = soup.findAll('jobtitle')
companies = soup.findAll('company')  
urls = soup.findAll('url')
for (p, k, q) in zip(companies, results, urls):
    c.execute('INSERT INTO Jobs(Title,Company,Link) VALUES(?,?,?)', ((k.text),(p.text),(q.text)))
    
# save changes
conn.commit()
# close connection
conn.close()