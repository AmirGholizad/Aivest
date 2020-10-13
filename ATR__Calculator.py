# first import packages that you need
import datetime
import MetaTrader5 as mt5
import numpy as np
import pandas as pd
import pytz
pd.set_option('display.max_columns', 500)  # number of columns to be displayed
pd.set_option('display.width', 1500)  # max table width to display

def ATR_Calculator(y,m,d,symbol):

    # set time zone to UTC
    timezone = pytz.timezone("Etc/UTC")
    # create 'datetime' object in UTC time zone to avoid the implementation of a local time zone offset
    utc_from = datetime.datetime(y, m, d, tzinfo=timezone)
    # get 11 bars of any symbol that you want in 1D timeframe starting from given time in format of y=Year,m=Month,d=Day
    rates = mt5.copy_rates_from(symbol, mt5.TIMEFRAME_D1, utc_from, 11)
    # create DataFrame out of the obtained data
    rates_frame = pd.DataFrame(rates)
    # convert time in seconds into the datetime format
    rates_frame['time'] = pd.to_datetime(rates_frame['time'], unit='s')
    # if you need to see the data print rates_frame. Otherwise let it be as a comment
    # print(rates_frame)
    # make the TR and atr_list as arrays with specified length
    TR = np.zeros(10)
    atr_list = np. zeros(10)
    # start to fill the TR and atr_list. I used the ATR formula from WikiPedia
    for i in range(1,10):
        TR[i-1] = max(rates_frame['high'][i],rates_frame['close'][i-1])-min(rates_frame['low'][i],rates_frame['close'][i-1])
    atr_list[0] = np.mean(TR)
    for j in range(1,10):
        atr_list[j] = (atr_list[j-1]*9+TR[j])/10
    # now make the ATR dataframe
    ATR = pd.DataFrame({'time' : rates_frame["time"][1:], 'ATR' : atr_list})
    return ATR
