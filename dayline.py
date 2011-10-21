import pg,matplotlib.pyplot
from datetime import date,timedelta
import numpy as np

pgr = pg.connect('leccy',user='leccy')

def buildGraph(fileout):

    matplotlib.pyplot.clf()

    today = date.today() - timedelta(1)

    year = `today.year`
    month = `today.month`
    day = `today.day`
    day = "17"
    minutes = [0]*24*60
    
    for minute in range(0,24*60):

        hour = minute/60
        minutesval = minute-hour*60

        start = year + "-" + month + "-" + day + " " + `hour` + ":" + `minutesval`
        if minutesval != 59:
            end = year + "-" + month + "-" + day + " " + `hour` + ":" + `minutesval+1`
        else:
            end = year + "-" + month + "-" + day + " " + `hour+1` + ":" + `0`

        query = "select sum(watts)/count(watts) from leccy where sensor = 0 AND dt > '"+start+"' and dt < '"+end+"'"

        res = pgr.query(query)
        if res.getresult()[0][0] != None:
            minutes[minute] = res.getresult()[0][0]

    lefts = np.arange(24*60)

    b3 = matplotlib.pyplot.plot(lefts,minutes)
    
    matplotlib.pyplot.xlabel('Hour of Day')
    matplotlib.pyplot.ylabel('Average Watts Used')
    matplotlib.pyplot.savefig(fileout)

buildGraph('dayplot.png')
