import pg,matplotlib.pyplot
from datetime import date,timedelta
import numpy as np

pgr = pg.connect('leccy',user='leccy')

def buildGraph(fileout):

    matplotlib.pyplot.clf()

    today = date.today()

    year = `today.year`
    month = `today.month`
    day = "17"
    hours = []
    for hour in range(0,24):

        start = year + "-" + month + "-" + day + " " + `hour` + ":00"
        end = year + "-" + month + "-" + day + " " + `hour+1` + ":00"
        query = "select sum(watts)/count(watts) from leccy where sensor = 0 AND dt > '"+start+"' and dt < '"+end+"'"

        print query
        res = pgr.query(query)
        hours.append(res.getresult()[0][0])

    hours2 = []
    yesterday = date.today() - timedelta(1)
    year2 = `yesterday.year`
    month2 = `yesterday.month`
    day2 = "16"
    for hour in range(0,24):

        start = year2 + "-" + month2 + "-" + day2 + " " + `hour` + ":00"
        end = year2 + "-" + month2 + "-" + day2 + " " + `hour+1` + ":00"
        query = "select sum(watts)/count(watts) from leccy where sensor = 0 AND dt > '"+start+"' and dt < '"+end+"'"

        res = pgr.query(query)
        hours2.append(res.getresult()[0][0])

    hours3 = [9999999]*24
    for val in range(2,8):

        day = date.today() - timedelta(val)

        year3 = `day.year`
        month3 = `day.month`
        day3 = `17-val`

        print day3

        for hour in range(0,24):

            start = year3 + "-" + month3 + "-" + day3 + " " + `hour` + ":00"
            end = year3 + "-" + month3 + "-" + day3 + " " + `hour+1` + ":00"
            query = "select sum(watts)/count(watts) from leccy where sensor = 0 AND dt > '"+start+"' and dt < '"+end+"'"
            print "HERE",day3,query

            res = pgr.query(query)
            if len(res.getresult()) > 0:
                use = res.getresult()[0][0]
                if use != None:
                    if use < hours3[hour]:
                        hours3[hour] = use


    print hours,hours2,hours3

    lefts = np.arange(24*4)
    b1 = matplotlib.pyplot.bar(lefts[2::4],hours)
    b2 = matplotlib.pyplot.bar(lefts[1::4],hours2,color='red')
    b3 = matplotlib.pyplot.bar(lefts[::4],hours3,color='green')
    
    matplotlib.pyplot.xlabel('Hour of Day')
    matplotlib.pyplot.ylabel('Average Watts Used')
    matplotlib.pyplot.xticks(lefts[1::4],('0','1','2','3','4','5','6','7','8','9','10','11','12','13','14','15','16','17','18','19','20','21','22','23'))
    matplotlib.pyplot.legend((b1[0],b2[0],b3[0]),('Yesterday','2 Days Ago','Week Best'))
    matplotlib.pyplot.savefig(fileout)

buildGraph('tester.png')
