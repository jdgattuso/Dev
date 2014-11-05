import pygal
import sqlite3

# Connect to database and retrieve data
conn = sqlite3.connect('data.db')
c = conn.cursor()
result = c.execute('select count(*) from data') 
print "rowcount = ",result.fetchone()[0]
c.execute("SELECT * FROM Data")
rows = c.fetchall()

# Create lists 
dateList = []
timeList = []
countList = []
priceList = []

# Add data to lists
for row in rows:
    dateList.append(row[0]) 
    timeList.append(row[1])
    countList.append(row[2])
    priceList.append(row[3])
conn.close()

print 'ranges from', min(countList), 'to', max(countList), 'posts'
print 'and from $', min(priceList), 'to $', max(priceList)


# Graph data
line_chart = pygal.Line(include_x_axis=True, show_dots=False, margin=75, range=(0,500))
line_chart.add('Bitcoin Price', priceList )
line_chart.add('# of tweets', countList)
line_chart.render_to_file('line_chart.svg')

