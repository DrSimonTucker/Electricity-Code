import pg,matplotlib.pyplot

import numpy as np

pgr = pg.connect('leccy',user='leccy')

def buildGraph(year,month,day,fileout):

    matplotlib.pyplot.clf()

    days = [0]
    start = year + "-" + month + "-" + `day` + " 00:00"
    end = year + "-" + month + "-" + `(day+1)` + " 00:00"
    query = "select watts from leccy where sensor = 0 AND dt > '"+start+"' and dt < '"+end+"' ORDER BY dt ASC"
    print query
    
    res = pgr.query(query)
    for r in res.getresult():
        days.append(r[0])

    matplotlib.pyplot.plot(days)
    matplotlib.pyplot.savefig(fileout)

buildGraph("2011","10",15,'day.png')
