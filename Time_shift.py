# first import packages that you need
import datetime
import MetaTrader5 as mt5
import numpy as np
import pandas as pd
import pytz
pd.set_option('display.max_columns', 500)  # number of columns to be displayed
pd.set_option('display.width', 1500)  # max table width to display

def Time_Shift(y,m,d,symbol):
    mt5.initialize()
    # set time zone to UTC
    timezone = pytz.timezone("Etc/UTC")
    # create 'datetime' object in UTC time zone to avoid the implementation of a local time zone offset
    utc_from = datetime.datetime(y, m, d, tzinfo=timezone)
    # get 11 bars of any symbol that you want in 1D timeframe starting from given time in format of y=Year,m=Month,d=Day
    rates = mt5.copy_rates_from(symbol, mt5.TIMEFRAME_D1, utc_from, 32)
    # create DataFrame out of the obtained data
    rates_frame = pd.DataFrame(rates)
    # convert time in seconds into the datetime format
    rates_frame['time'] = pd.to_datetime(rates_frame['time'], unit='s')
    # if you need to see the data print rates_frame. Otherwise let it be as a comment
    # print(rates_frame)
    # now shift the time to day before
    timeshift = rates_frame['time'].iloc[-2].date()
    timeshift = str(timeshift)
    timeshift = timeshift.split('-')
    Y = int(timeshift[0])
    M = int(timeshift[1])
    D = int(timeshift[2])
    return [Y,M,D]