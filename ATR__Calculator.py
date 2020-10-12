from datetime import datetime
import MetaTrader5 as mt5
import numpy as np

def ATR_Calculator():

    # display data on the MetaTrader 5 package
    print("MetaTrader5 package author: ", mt5.__author__)
    print("MetaTrader5 package version: ", mt5.__version__)

    # import the 'pandas' module for displaying data obtained in the tabular form
    import pandas as pd

    pd.set_option('display.max_columns', 500)  # number of columns to be displayed
    pd.set_option('display.width', 1500)  # max table width to display
    # import pytz module for working with time zone
    import pytz

    # establish connection to MetaTrader 5 terminal
    mt5.initialize()

    # set time zone to UTC
    timezone = pytz.timezone("Etc/UTC")
    # create 'datetime' object in UTC time zone to avoid the implementation of a local time zone offset
    utc_from = datetime(2020, 10, 12, tzinfo=timezone)
    # get 10 EURUSD H4 bars starting from 01.10.2020 in UTC time zone
    rates = mt5.copy_rates_from("SAFAB99", mt5.TIMEFRAME_D1, utc_from, 11)

    # create DataFrame out of the obtained data
    rates_frame = pd.DataFrame(rates)
    # convert time in seconds into the datetime format
    rates_frame['time'] = pd.to_datetime(rates_frame['time'], unit='s')
    print(rates_frame)
    TR = np.zeros(10)
    atr_list = np. zeros(10)
    for i in range(1,10):
        TR[i-1] = max(rates_frame['high'][i],rates_frame['close'][i-1])-min(rates_frame['low'][i],rates_frame['close'][i-1])
    atr_list[0] = np.mean(TR)
    for j in range(1,10):
        atr_list[j] = (atr_list[j-1]*9+TR[j])/10
    ATR = pd.DataFrame({'time' : rates_frame["time"][1:], 'ATR' : atr_list})
    return ATR
print(ATR_Calculator())
