import pg,matplotlib.pyplot

import numpy as np

pgr = pg.connect('leccy',user='leccy')

def buildGraph(year,year2,year3,month,month2,month3,day,day2,day3,fileout):

    matplotlib.pyplot.clf()

    hours = []
    for hour in range(0,24,2):

        start = year + "-" + month + "-" + day + " " + `hour` + ":00"
        end = year + "-" + month + "-" + day + " " + `hour+2` + ":00"
        query = "select sum(watts)/count(watts) from leccy where sensor = 0 AND dt > '"+start+"' and dt < '"+end+"'"

        res = pgr.query(query)
        hours.append(res.getresult()[0][0])

    hours2 = []
    for hour in range(0,24,2):

        start = year2 + "-" + month2 + "-" + day2 + " " + `hour` + ":00"
        end = year2 + "-" + month2 + "-" + day2 + " " + `hour+2` + ":00"
        query = "select sum(watts)/count(watts) from leccy where sensor = 0 AND dt > '"+start+"' and dt < '"+end+"'"

        res = pgr.query(query)
        hours2.append(res.getresult()[0][0])

    hours3 = []
    for hour in range(0,24,2):

        start = year3 + "-" + month3 + "-" + day3 + " " + `hour` + ":00"
        end = year3 + "-" + month3 + "-" + day3 + " " + `hour+2` + ":00"
        query = "select sum(watts)/count(watts) from leccy where sensor = 0 AND dt > '"+start+"' and dt < '"+end+"'"

        res = pgr.query(query)
        hours3.append(res.getresult()[0][0])



    lefts = np.arange(12*4)
    matplotlib.pyplot.bar(lefts[::4],hours)
    matplotlib.pyplot.bar(lefts[1::4],hours2,color='red')
    matplotlib.pyplot.bar(lefts[2::4],hours3,color='green')
    matplotlib.pyplot.savefig(fileout)

buildGraph("2011","2011","2011","10","10","10","15","16","17",'tester.png')
