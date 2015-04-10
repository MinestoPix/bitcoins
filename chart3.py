#!usr/bin/env python3
"""Experimental program for bitcoin trading
with scikit learn machine learning module
"""

import matplotlib.pyplot as plt
import matplotlib.dates as dates
from datetime import datetime
# from sklearn import svm


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






chart = open("table.csv")

# print(chart)

values = []
last_price = None
worths = [0]
buy_worth = 1.01
sell_worth = 0.99


for line in chart:
    # print(line)
    line = line.rstrip()
    # Timestamp	Open	High	Low	Close	Volume (BTC)	Volume (Currency)	Weighted Price
    # date, open_value, high, low, close_value, volume_BTC, volume_currency, price = line.split(',')
    date, *value = line.split(',')
    value = tuple([float(x) for x in value])
    value = (date,) + value
    date, open_value, high, low, close_value, volume_BTC, volume_currency, price = value
    date = datetime.strptime(date, "%Y-%m-%d %H:%M:%S")
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




price_y = []
open_value_y = []
close_value_y = []
dX = []

for date, open_value, high, low, close_value, volume_BTC, volume_currency, price in values:
    price_y.append(price)
    open_value_y.append(open_value)
    close_value_y.append(close_value)
    dX.append(date)


# Getting values for learn_len

learn_len = 10
learn_prices = []
for i in range(len(price_y) - learn_len):
    learn_prices.append(price_y[i:i+learn_len])
print("learn prices len:", len(learn_prices))


# Graphing

plt.plot_date(dX, price_y, fmt='-')

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
min_price_dev = 0
print("dX:", len(dX), "worths:", len(worths))
# !!! BUG: the wbuys and wsells must check since last wbuy or wsell, and dismiss the range.
for i, (date, worth) in enumerate( zip(dX, worths) ):
    max_price = 0
    min_price = 1000

    for j, value in enumerate(values[i-look_range:i+look_range]):
        if value[-1] > max_price:
            # print("value greater", j, value[-1])
            max_index, max_price = j, value[-1]
        if value[-1] < min_price:
            # print(value[-1], "<", min_price, value[-1] < min_price)
            # print("#######value smaller", j, value[-1])
            min_index, min_price = j, value[-1]
            # print(min_index, value[-1], min_price)

    if len(worths)>i+1:
        # print(worths[i+1], "> 0 and",
        #         last_worth, "< 1 and",
        #         min_index, "==", look_range,
        #         worths[i+1] > 0 and last_worth < 1 and min_index==look_range)
        if worths[i+1] > 0 and last_worth < 1 and min_index==look_range:# and values[i][-1] < values[wsells[-1]][-1] - min_price_dev:# and not last_bought:
            if last_bought and wbuys:
                if values[i][-1] <= values[wbuys[-1]][-1]:
                    del wbuys[-1]
                    del buy_dates[-1]
                else:
                    continue
            buy_dates.append( date )
            wbuys.append(i)
            last_bought = True
            markers.append(2)
        elif worths[i+1] < 0 and last_worth > -1 and max_index==look_range:
            if not last_bought and wsells:
                if values[i][-1] >= values[wsells[-1]][-1]:
                    del wsells[-1]
                    del sell_dates[-1]
                else:
                    continue
            sell_dates.append( date )
            wsells.append(i)
            last_bought = False
            markers.append(0)
        else:
            markers.append(1)

    last_worth = worth





print("buys:", len(wbuys))
print("sells:", len(wsells))




plt.scatter(buy_dates, [price_y[x] for x in wbuys], c='g')
plt.scatter(sell_dates, [price_y[x] for x in wsells], c='r')

plt.ylabel('BC to USD')
plt.show()

