import OR_Calculator
import MetaTrader5 as mt5
import pandas as pd
import pytz
import datetime


def Score_Calculator(symbol,orlist,a,b,c):
    #mt5.initialize()
    # set time zone to UTC
    timezone = pytz.timezone("Etc/UTC")
    # create 'datetime' objects in UTC time zone to avoid the implementation of a local time zone offset
    OR_Start = datetime.datetime(a, b, c, 10, 30, 0, tzinfo=timezone)
    OR_Stop = datetime.datetime(a, b, c, 15, 0, 0, tzinfo=timezone)
    # request SAFAB99 ticks within 10:30:00 - 10:45:00
    ticks = mt5.copy_ticks_range(symbol , OR_Start, OR_Stop, mt5.COPY_TICKS_ALL)
    ticks_frame = pd.DataFrame(ticks)
    # print(ticks_frame["last"].iloc[-1])

    LAST = ticks_frame["last"].iloc[-1]
    OR_high = orlist[0]
    OR_low = orlist[1]

    if (LAST < OR_high) and (LAST > OR_low):
        return 0
    elif LAST > OR_high:
        for i in range(0, len(ticks)):
            if ticks_frame["last"][i] < OR_low:
                return 4
            else:
                continue
        return 2

    elif LAST < OR_low:
        for i in range(0, len(ticks)):
            if ticks_frame["last"][i] > OR_high:
                return -4
            else:
                continue
        return -2

def Macro_Calculator(a,b,c,symbol):

    for j in range(0, 30):
        orlist = OR_Calculator.OR_Calculator(a,b,c,symbol)
        if orlist == None:
            c = c + 1
            continue
        #print(OR_Calculator(orlist))
        Score = Score_Calculator(symbol,orlist,a,b,c)
        print(Score)
        c = c + 1

Macro_Calculator(2020,8,25, "آگاس")
#date = datetime.datetime(2003,8,1,12,4,5)
"""
for i in range(5):
    date = datetime.timedelta(days=1)
    print(date)
"""