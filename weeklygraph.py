import pg,matplotlib.pyplot

import numpy as np

pgr = pg.connect('leccy',user='leccy')

def buildGraph(year,month,dayst,dayen,fileout):

    matplotlib.pyplot.clf()

    days = [0]
    for day in range(dayst,dayen):

        start = year + "-" + month + "-" + `day` + " 00:00"
        end = year + "-" + month + "-" + `(day+1)` + " 00:00"
        query = "select sum(watts)/count(watts) from leccy where sensor = 0 AND dt > '"+start+"' and dt < '"+end+"'"
        print query

        res = pgr.query(query)
        days.append(res.getresult()[0][0])

    lefts = np.arange(7*2)
    print days
    matplotlib.pyplot.bar(lefts[::2],days)
    matplotlib.pyplot.savefig(fileout)

buildGraph("2011","10",11,17,'days.png')
