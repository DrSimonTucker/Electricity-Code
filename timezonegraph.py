import pg,matplotlib.pyplot
from datetime import date,timedelta
import numpy as np

pgr = pg.connect('leccy',user='leccy')

def buildGraph(fileouts):

    timezones = [("00","06"),("07","16"),("17","23")]
    days = [0]*7

    for i in range(len(timezones)):
        matplotlib.pyplot.clf()

        hours = [0]*7
        for sub in range(1,8):
            today = date.today() - timedelta(sub)

            year = `today.year`
            month = `today.month`
            day = `today.day`
        
            days[7-sub] = today.strftime('%A')

            start = year + "-" + month + "-" + day + " " + timezones[i][0] + ":59:59"
            end = year + "-" + month + "-" + day + " " + timezones[i][1] + ":59:59"
            query = "select sum(watts)/count(watts) from leccy where sensor = 0 AND dt > '"+start+"' and dt < '"+end+"'"
            print query
                
            res = pgr.query(query)
            if res.getresult()[0][0] != None:
                hours[7-sub] = res.getresult()[0][0]

        lefts = np.arange(7)
        b1 = matplotlib.pyplot.bar(lefts,hours)
    
        matplotlib.pyplot.title("Usage between " + timezones[i][0] + ":00 and " + timezones[i][1] + ":00")
        matplotlib.pyplot.xlabel('Days Previous')
        matplotlib.pyplot.ylabel('Average Watts Used')
        matplotlib.pyplot.xticks((lefts+0.4),days)
        matplotlib.pyplot.savefig(fileouts[i])

buildGraph(['t1.png','t2.png','t3.png'])
