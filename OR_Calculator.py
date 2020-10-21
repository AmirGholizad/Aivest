# first import packages that you need
import datetime
import MetaTrader5 as mt5
import pandas as pd
from Time_shift import Time_Shift
pd.set_option('display.max_columns', 500) # number of columns to be displayed
pd.set_option('display.width', 1500)      # max table width to display
import pytz

# make the OR_Calculator
def OR_Calculator(symbol,y,m,d,h1,m1,s1,h2,m2,s2):
    #connect to Metatrader 5
    mt5.initialize()
    # set time zone to UTC
    timezone = pytz.timezone("Etc/UTC")
    # create 'datetime' objects in UTC time zone to avoid the implementation of a local time zone offset
    OR_Start = datetime.datetime(y, m, d, h1, m1, s1,  tzinfo=timezone)
    OR_Stop = datetime.datetime(y, m, d, h2, m2, s2, tzinfo=timezone)
    # request any symbol that you want and it's ticks within different Opening Ranges that you want
    ticks = mt5.copy_ticks_range(symbol , OR_Start, OR_Stop, mt5.COPY_TICKS_ALL)

    # in case that symbol has not been traded this day
    if len(ticks) == 0:
        return None
    # calculate the OR_high and OR_low
    ticks_frame = pd.DataFrame(ticks)
    ticks_frame['time'] = pd.to_datetime(ticks_frame['time'], unit='s')

    # find the start time which is the time that first trade is done
    #print(ticks_frame)
    start = 0
    for i in range(0,len(ticks_frame)):
        if (ticks_frame["bid"][i] == ticks_frame["last"][i]) or (ticks_frame["ask"][i] == ticks_frame["last"][i]):
            ticks_frame = ticks_frame[i:]
            start = i
            break
    for j in range(start,len(ticks_frame)):
        timediff = ticks_frame["time"][j] - ticks_frame["time"][start]
        timediff = int(datetime.timedelta.total_seconds(timediff)) / 60
        if timediff >= 15:
            ticks_frame = ticks_frame[:j]
            print(ticks_frame)
            stop = j
            break
    H = datetime.datetime.time(ticks_frame["time"].iloc[0]).hour
    M = datetime.datetime.time(ticks_frame["time"].iloc[0]).minute
    S = datetime.datetime.time(ticks_frame["time"].iloc[0]).second
    # find the OR_high and OR_low
    OR_high = max(ticks_frame["last"])
    OR_low = min(ticks_frame["last"])
    return [OR_high, OR_low, H, M, S]
print(OR_Calculator("غبهار",2020,10,20,9,0,0,12,30,0))