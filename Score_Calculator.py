# first import packages that you need
from OR_Calculator import OR_Calculator
from ATR__Calculator import ATR_Calculator
from Time_shift import Time_Shift
import MetaTrader5 as mt5
import pandas as pd
import numpy as np
import pytz
import datetime

def Score_Calculator(symbol,y,m,d,h1,m1,s1,h2,m2,s2,h3,m3,s3):
    mt5.initialize()
    # set time zone to UTC
    timezone = pytz.timezone("Etc/UTC")
    # create 'datetime' objects in UTC time zone to avoid the implementation of a local time zone offset
    Session_Start = datetime.datetime(y, m, d, h1, m1, s1, tzinfo=timezone)
    Session_Stop = datetime.datetime(y, m, d, h3, m3, s3, tzinfo=timezone)
    # request any symbol that you want and it's ticks within different Opening Ranges that you want
    ticks = mt5.copy_ticks_range(symbol , Session_Start, Session_Stop, mt5.COPY_TICKS_ALL)
    if len(ticks) == 0:
        return None
    # make the dataframe of ticks
    ticks_frame = pd.DataFrame(ticks)
    # convert time in seconds into the datetime format
    ticks_frame['time'] = pd.to_datetime(ticks_frame['time'], unit='s')
    # get the closing price
    LAST = ticks_frame["last"].iloc[-1]
    # from orlist find OR_high and OR_low
    orlist = OR_Calculator(symbol, y, m, d, h1, m1, s1, h2, m2, s2)
    OR_high = orlist[0]
    OR_low = orlist[1]
    # get the ATR and make the A and C levels
    A_up = OR_high + (ATR_Calculator(y,m,d,symbol)["ATR"])*0.1
    A_down = OR_low - (ATR_Calculator(y, m, d, symbol)["ATR"])*0.1
    C_up = OR_high + (ATR_Calculator(y, m, d, symbol)["ATR"])*0.15
    C_down = OR_low - (ATR_Calculator(y, m, d, symbol)["ATR"])*0.15
    adate = Time_Shift(y, m, d, symbol)
    Y = adate[0]
    M = adate[1]
    D = adate[2]
    # calculate the score
    if (OR_low == OR_high):
        if LAST > OR_Calculator(symbol, Y, M, D, h1, m1, s1, h2, m2, s2)[0]:
            if (LAST == OR_high):
                return 2
            elif (LAST < OR_high):
                return 0
        elif LAST < OR_Calculator(symbol, Y, M, D, h1, m1, s1, h2, m2, s2)[1]:
            if (LAST == OR_high):
                return -2
            elif (LAST > OR_high):
                return 0
        elif (LAST/ticks_frame["last"][0]) > 1.09:
            return 4
        elif (ticks_frame["last"][0]/LAST) > 1.09:
            return -4
    elif (LAST == OR_high):
        for i in range(0, len(ticks)):
            if not (ticks_frame["last"][i] > OR_high) :
                return 2
            else:
                continue
        return 0
    elif (LAST == OR_low):
        for i in range(0, len(ticks)):
            if not (ticks_frame["last"][i] < OR_low) :
                return -2
            else:
                continue
        return 0
    elif (LAST <= OR_high) and (LAST >= OR_low):
        return 0
    elif LAST > OR_high:
        for i in range(0, len(ticks)):
            if ticks_frame["last"][i] <= A_down:
                return 4
            else:
                continue
        return 2

    elif LAST < OR_low:
        for i in range(0, len(ticks)):
            if ticks_frame["last"][i] >= A_up:
                return -4
            else:
                continue
        return -2