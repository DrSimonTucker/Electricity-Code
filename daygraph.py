import pg,matplotlib.pyplot
from datetime import date,timedelta
import numpy as np

pgr = pg.connect('leccy',user='leccy')

def buildGraph(fileout):

    days = [0]*7

    matplotlib.pyplot.clf()
    
    hours = [0]*7
    for sub in range(1,8):
        today = date.today() - timedelta(sub)
        
        year = `today.year`
        month = `today.month`
        day = `today.day`
        
        days[7-sub] = today.strftime('%A')
        
        start = year + "-" + month + "-" + day + " 00:00:00"
        end = year + "-" + month + "-" + day + " 23:59:59"
        query = "select sum(watts)/count(watts) from leccy where sensor = 0 AND dt > '"+start+"' and dt < '"+end+"'"
        
        res = pgr.query(query)
        if res.getresult()[0][0] != None:
            hours[7-sub] = res.getresult()[0][0]

    lefts = np.arange(7)
    b1 = matplotlib.pyplot.bar(lefts,hours)
    
    matplotlib.pyplot.title("Usage over the past week")
    matplotlib.pyplot.xlabel('Days Previous')
    matplotlib.pyplot.ylabel('Average Watts Used')
    matplotlib.pyplot.xticks((lefts+0.4),days)
    matplotlib.pyplot.plot([0,lefts[-1]],[hours[-1],hours[-1]],'r')    
    matplotlib.pyplot.savefig(fileout)

buildGraph('days.png')
