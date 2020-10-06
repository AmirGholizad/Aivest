from _datetime import datetime as datetime
import MetaTrader5 as mt5
import pandas as pd
pd.set_option('display.max_columns', 500) # number of columns to be displayed
pd.set_option('display.width', 1500)      # max table width to display
import pytz


def OR_Calculator(a,b,c):

    mt5.initialize()
    # set time zone to UTC
    timezone = pytz.timezone("Etc/UTC")
    # create 'datetime' objects in UTC time zone to avoid the implementation of a local time zone offset
    OR_Start = datetime(a,b,c, 10, 30, 0,  tzinfo=timezone)
    OR_Stop = datetime(a,b,c,10, 45, 0, tzinfo=timezone)
    # request SAFAB99 ticks within 10:30:00 - 10:45:00
    ticks = mt5.copy_ticks_range("SAFAB99", OR_Start, OR_Stop, mt5.COPY_TICKS_ALL)
    print("Ticks received:",len(ticks))

    ticks_frame = pd.DataFrame(ticks)
    OR_high = max(ticks_frame["last"])
    OR_low = min(ticks_frame["last"])
    return [OR_high,OR_low,ticks_frame]

Details = OR_Calculator(2020,10,6)

print("SAFAB99 details:\n ORlow={}\n ORhigh={}".format(Details[0],Details[1]))
