#!usr/bin/env python3
"""Experimental program for bitcoin trading
with scikit learn machine learning module
"""

import matplotlib.pyplot as plt
import matplotlib.dates as dates
from datetime import datetime
from sklearn import linear_model
from sklearn.preprocessing import StandardScaler


# location of prices file
table_dir = "table.csv"


# Starting values
btc = 1.0
usd = 300.0

def btcToUsd(bitcoin, dollar):
    """Substracts bitcoin from btc and adds dollar to usd"""
    global btc
    global usd
    if btc>bitcoin:
        btc-=bitcoin
        usd+=dollar
        return True
    return False


def usdToBtc(dollar, bitcoin):
    """Substracts dollar from usd and adds bitcoin to btc"""
    global btc
    global usd
    if usd>dollar:
        usd-=dollar
        btc+=bitcoin
        return True
    return False





def trade(values):
    for i, value in enumerate(values[:50]):
        nworth = sum(worths)/len(worths)
        # print(nworth)

        # print(i, "\t", worths[i], "\t", value[7])






chart = open(table_dir)

# print(chart)

values = []
last_price = None
worths = []
buy_worth = 1.05
sell_worth = 0.96


for line in chart:
    # print(line)
    line = line.rstrip()
    # Timestamp	Open	High	Low	Close	Volume (BTC)	Volume (Currency)	Weighted Price
    # date, open_value, high, low, close_value, volume_BTC, volume_currency, price = line.split(',')
    date, *value = line.split(',')
    value = tuple([float(x) for x in value])
    value = (date,) + value
    date, open_value, high, low, close_value, volume_BTC, volume_currency, price = value
    date = datetime.fromtimestamp(int(date))
    date = dates.date2num(date)
    values.append( (date, open_value, high, low, close_value, volume_BTC, volume_currency, price) )
    if last_price:
        pricep = price/last_price
        if pricep > buy_worth:
            worths.append(2)
        elif pricep > 1:
            worths.append(1)
        elif pricep == 1:
            worths.append(0)
        elif pricep > sell_worth:
            worths.append(-1)
        else:
            worths.append(-2)
    last_price = price

value_list = [list(x) for x in values]

trade(values)


# Graphing

price_y = []
open_value_y = []
close_value_y = []
dX = []

for date, open_value, high, low, close_value, volume_BTC, volume_currency, price in values:
    price_y.append(price)
    open_value_y.append(open_value)
    close_value_y.append(close_value)
    dX.append(date)













# plt.plot_date(dX, price_y, fmt='-')

buy_dates = []
wbuys = []
sell_dates = []
wsells = []
markers = []

# Makes points at the dates they are reffering to

# for i, (date, worth) in enumerate( zip(dX, worths) ):
#     if worth==2:
#         buy_dates.append( date )
#         wbuys.append(i)
#     elif worth==0:
#         sell_dates.append( date )
#         wsells.append(i)

last_worth = 0
look_range = 10 # +++ ADD: look range in time
max_index = 0
min_index = 0
last_bought = True


# catch if i skipped one
temp_count = 0

for i, (date, worth) in enumerate( zip(dX, worths) ):
    max_price = 0
    min_price = 1000

    for j, value in enumerate(values[i-look_range:i+look_range]):
        if value[-1] > max_price:

            max_index, max_price = j, value[-1]
        if value[-1] < min_price:
            

            min_index, min_price = j, value[-1]


    if worth > 0 and last_worth < 1 and min_index==look_range:# and not last_bought:
        if last_bought and wbuys:
            if values[i][-1] <= values[wbuys[-1]][-1]:
                del wbuys[-1]
                del buy_dates[-1]
            else:
                continue
        buy_dates.append( date )
        wbuys.append(i)
        last_bought = True
        markers.append(1)
    elif worth < 0 and last_worth > -1 and max_index==look_range:# and last_bought:
        if not last_bought and wsells:
            if values[i][-1] >= values[wsells[-1]][-1]:
                del wsells[-1]
                del sell_dates[-1]
            else:
                continue
        sell_dates.append( date )
        wsells.append(i)
        last_bought = False
        markers.append(-1)
    else:
        markers.append(0)

    last_worth = worth

    # catch if i skipps one !!! check in more detail
    if not temp_count == i:
        markers.append(0)
        # print(i)
    temp_count = i+1




print("buys:", len(wbuys))
print("sells:", len(wsells))




# plt.scatter(buy_dates, [price_y[x] for x in wbuys], c='g')
# plt.scatter(sell_dates, [price_y[x] for x in wsells], c='r')

# plt.ylabel('BC to USD')
# plt.show()



dimensions = 200
X= []


for i in range(dimensions, len(worths)):
    X.append(price_y[i-dimensions:i])

y = markers[dimensions:]


scale = StandardScaler()
X = scale.fit_transform(X, y)


clf = linear_model.SGDRegressor()
clf.fit(X, y)


"""
224.73,224.59,224.73,223.61,223.61,223.61,224.72,224.38,224.79,224.43,224.89,224.2,224.89,224.9,223.77,224.88,224.96,225,223.97,224.99,224,224,224,224,224.09,223.7,223.67,223.66,223.6,224.24,224.21,224.51,223.66,223.7,224.45,224.49,223.73,223.71,223.8,224.33,224.28,223.72,224.33,224.52,224.77,223.66,224.63,223.48,223.33,223.24



221.16,221.82,221.95,220.99,220.89,220.9,221.48,221.06,221.78,221.96,221.1,221.56,221.72,221.25,221.89,222,222.1,222.1,221.57,222.09,221.22,221.3,221.47,222.04,222.09,221.58,221.49,221.42,221.35,221.35,221.35,221.43,221.55,222.05,221.95,221.71,222.09,221.99,221.69,221.62,221.92,222,221.9,221.96,222,221.86,221.99,221.99,222,221.99

2015-04-19 00:00:00	221.219	221.463	221.149	221.463	1.12	248.58	221.16
2015-04-19 00:10:00	221.382	221.971	220.877	220.877	1.2	266.99	221.82
2015-04-19 00:15:00	221.487	221.971	221.487	221.971	3.13	693.81	221.95
2015-04-19 00:20:00	221.607	221.607	220.879	220.879	0.07	15.69	220.99
2015-04-19 00:25:00	221	221	220.874	220.874	6.36	1405.86	220.89
2015-04-19 00:30:00	221.043	221.043	220.874	220.874	0.07	15.46	220.9
2015-04-19 00:35:00	221.043	221.647	221	221.647	4.88	1081.91	221.48
2015-04-19 00:40:00	221.323	221.971	221	221.971	1.37	303.6	221.06
2015-04-19 00:45:00	221.647	221.794	221.647	221.794	0.17	37.37	221.78
2015-04-19 00:50:00	221.878	221.971	221.818	221.877	0.59	130.78	221.96
2015-04-19 00:55:00	221.879	221.94	220.874	221.94	5.73	1267.58	221.1
2015-04-19 01:00:00	221.558	221.558	221.558	221.558	0.03	5.89	221.56
2015-04-19 01:05:00	221.455	221.9	221.455	221.723	1.67	370.47	221.72
2015-04-19 01:10:00	221.252	221.252	221.252	221.252	0.02	4.72	221.25
2015-04-19 01:15:00	221.252	221.9	221.252	221.9	0.83	184.98	221.89
2015-04-19 01:20:00	221.9	222.1	221.9	222.1	5.37	1191.58	222
2015-04-19 01:25:00	222.1	222.1	222.1	222.1	1.42	314.3	222.1
2015-04-19 01:30:00	222.1	222.1	222.1	222.1	0.86	190.48	222.1
2015-04-19 01:35:00	221.3	222.1	221.211	221.211	1.87	415.23	221.57
2015-04-19 01:40:00	221.833	222.1	221.833	222.1	0.68	150	222.09
2015-04-19 01:45:00	221.507	221.507	221.211	221.211	0.6	133.7	221.22
2015-04-19 01:50:00	221.3	221.3	221.3	221.3	0.01	2.21	221.3
2015-04-19 01:55:00	221.404	221.543	221.404	221.543	0.02	4.72	221.47
2015-04-19 02:00:00	221.543	222.185	221.543	222.185	0.23	50.06	222.04
2015-04-19 02:05:00	221.996	222.1	221.996	222.1	1.83	407.24	222.09
2015-04-19 02:10:00	222.1	222.1	221.21	221.917	8.44	1871.03	221.58
2015-04-19 02:20:00	221.514	221.56	221.423	221.423	0.03	5.98	221.49
2015-04-19 02:25:00	221.4	221.423	221.354	221.354	0.56	123.84	221.42
2015-04-19 02:35:00	221.354	221.354	221.354	221.354	0.03	7.58	221.35
2015-04-19 02:40:00	221.331	221.354	221.331	221.354	1.12	247.01	221.35
2015-04-19 02:45:00	221.354	221.354	221.354	221.354	2.82	624.48	221.35
2015-04-19 02:50:00	221.423	221.514	221.423	221.514	0.54	119.26	221.43
2015-04-19 02:55:00	221.514	221.56	221.514	221.56	0.14	31.45	221.55
2015-04-19 03:00:00	221.663	222.1	221.663	222.1	0.34	76.48	222.05
2015-04-19 03:05:00	222.1	222.1	221.663	222.1	6.1	1353.89	221.95
2015-04-19 03:10:00	221.6	222.1	221.6	222.1	1.74	386.44	221.71
2015-04-19 03:15:00	221.929	222.1	221.929	222.1	0.39	87.5	222.09
2015-04-19 03:20:00	222	222	221.971	221.971	0.36	80.14	221.99
2015-04-19 03:25:00	221.715	221.8	221.315	221.315	1.06	234.99	221.69
2015-04-19 03:30:00	221.793	221.793	221.2	221.2	1.08	238.52	221.62
2015-04-19 03:35:00	221.598	222	221.598	222	0.71	157.12	221.92
2015-04-19 03:40:00	222	222	222	222	0.08	17.76	222
2015-04-19 03:45:00	221.559	222	221.21	221.21	0.96	212.04	221.9
2015-04-19 03:50:00	222	222	221.21	222	2	443.86	221.96
2015-04-19 03:55:00	222	222	221.999	221.999	0.43	95.46	222
2015-04-19 04:00:00	221.999	221.999	221.563	221.998	0.31	69.86	221.86
2015-04-19 04:05:00	221.567	221.999	221.567	221.699	2.83	628.24	221.99
2015-04-19 04:10:00	221.699	222	221.699	222	81.95	18192.9	221.99
2015-04-19 04:15:00	222	222	221.766	221.766	2.72	603.78	222
2015-04-19 04:20:00	221.766	222	221.766	222	1.08	238.94	221.99

"""
