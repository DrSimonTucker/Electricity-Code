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
    hours = [0]*6
    for hour in range(0,24,4):

        start = year + "-" + month + "-" + day + " " + `hour` + ":00"
        end = year + "-" + month + "-" + day + " " + `hour+4` + ":00"
        query = "select sum(watts)/count(watts) from leccy where sensor = 0 AND dt > '"+start+"' and dt < '"+end+"'"

        res = pgr.query(query)
        if res.getresult()[0][0] != None:
            hours[hour/4] = res.getresult()[0][0]

    hours2 = [0]*6
    yesterday = date.today() - timedelta(2)
    year2 = `yesterday.year`
    month2 = `yesterday.month`
    day2 = `yesterday.day`
    for hour in range(0,24,4):

        start = year2 + "-" + month2 + "-" + day2 + " " + `hour` + ":00"
        end = year2 + "-" + month2 + "-" + day2 + " " + `hour+4` + ":00"
        query = "select sum(watts)/count(watts) from leccy where sensor = 0 AND dt > '"+start+"' and dt < '"+end+"'"

        res = pgr.query(query)
        if res.getresult()[0][0] != None:
            hours2[hour/4] = res.getresult()[0][0]

    hours3 = [9999999]*6
    for val in range(1,8):

        day = date.today() - timedelta(val)

        year3 = `day.year`
        month3 = `day.month`
        day3 = `day.day`

        for hour in range(0,24,4):

            start = year3 + "-" + month3 + "-" + day3 + " " + `hour` + ":00"
            end = year3 + "-" + month3 + "-" + day3 + " " + `hour+4` + ":00"
            query = "select sum(watts)/count(watts) from leccy where sensor = 0 AND dt > '"+start+"' and dt < '"+end+"'"

            res = pgr.query(query)
            if len(res.getresult()) > 0:
                use = res.getresult()[0][0]
                if use != None:
                    hours3[hour/4] += use/7.0


    lefts = np.arange(6*4)
    b1 = matplotlib.pyplot.bar(lefts[2::4],hours)
    b2 = matplotlib.pyplot.bar(lefts[1::4],hours2,color='red')
    b3 = matplotlib.pyplot.bar(lefts[::4],hours3,color='green')
    
    matplotlib.pyplot.xlabel('Hour of Day')
    matplotlib.pyplot.ylabel('Average Watts Used')
    matplotlib.pyplot.xticks(lefts[1::4],('0-4','4-8','8-12','12-16','16-20','20-00'))
    matplotlib.pyplot.legend((b1[0],b2[0],b3[0]),('Yesterday','2 Days Ago','Week Best'))
    matplotlib.pyplot.savefig(fileout)

buildGraph('tester.png')
