from urllib.request import urlopen
import datetime
import json
import math





# location of prices file
table_dir = "table.csv"



# http://bitcoincharts.com/charts/btceUSD#rg1zig1-minzczsg2013-12-01zeg2013-12-02ztgSzm1g10zm2g25zv
# m=btceUSD&SubmitButton=Draw&r=1&i=1-min&c=1&s=2013-12-01&e=2013-12-02&Prev=&Next=&t=S&b=&a1=&m1=10&a2=&m2=25&x=0&i1=&i2=&i3=&i4=&v=1&cv=0&ps=0&l=0&p=0&
# http://bitcoincharts.com/charts/chart.json?
# http://bitcoincharts.com/charts/chart.json?m=btceUSD&i=1-min&c=1&s=2013-12-01&e=2013-12-02


def to_url(date):
    """Returns bitcoin chart url from int date"""

    chart_url = "http://bitcoincharts.com/charts/chart.json?"

    output = chart_url + "m=btceUSD&i=1-min&c=1&s="
    output += str(datetime.date.fromordinal(date))
    output += "&e="
    output += str(datetime.date.fromordinal(date+1))
    return output



# ordinal of December, 1st 2013
start = 735203
# current downloaded
last_date = 0

with open(table_dir, "r") as data:
    for line in data:
        last_line = line
    start = int(line.split(",")[0])
    last_date = start
    start = math.floor(datetime.date.toordinal(datetime.date.fromtimestamp(start)))


# ordinal of 100 days back
end = datetime.date.toordinal(datetime.date.today()) - 100
# end = 735206



for i in range(start, end):
    with open(table_dir, "a") as data_file:
        output = ""
        data = urlopen(to_url(i)).read().decode()
        data = data[2:-2]
        data = data.replace(" ", "")
        data = data.split("],[")

        for x in data:
            if int(x.split(",")[0]) <= last_date:
                continue
            last_date = int(x.split(",")[0])
            corrupted = False
            for y in x.split(","):
                if "e" in y:
                    corrupted = True
            if corrupted:
                continue
            output += x + "\n"
            print(x)

        data_file.write(output)










