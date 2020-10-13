# first import packages that you need
import datetime
import MetaTrader5 as mt5
import pandas as pd
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
    OR_high = max(ticks_frame["last"])
    OR_low = min(ticks_frame["last"])
    return [OR_high,OR_low]
