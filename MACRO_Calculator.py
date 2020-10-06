import OR_Calculator
import MetaTrader5 as mt5
import pandas as pd
import pytz
from _datetime import datetime


#print(orlist)
def MACRO_Calculator(orlist):
    mt5.initialize()
    # set time zone to UTC
    timezone = pytz.timezone("Etc/UTC")
    # create 'datetime' objects in UTC time zone to avoid the implementation of a local time zone offset
    OR_Start = datetime(2020, 10, 6, 10, 30, 0, tzinfo=timezone)
    OR_Stop = datetime(2020, 10, 6, 15, 0, 0, tzinfo=timezone)
    # request SAFAB99 ticks within 10:30:00 - 10:45:00
    ticks = mt5.copy_ticks_range("SAFAB99", OR_Start, OR_Stop, mt5.COPY_TICKS_ALL)
    ticks_frame = pd.DataFrame(ticks)
    print(ticks_frame["last"].iloc[-1])
    LAST = ticks_frame["last"].iloc[-1]
    OR_high = orlist[0]
    OR_low = orlist[1]
    if (LAST < OR_high) and (LAST > OR_low):
        return 0
    elif LAST > OR_high:
        return 2
    elif LAST < OR_low:
        return -2


orlist = OR_Calculator.OR_Calculator(2020,10,6)
print(MACRO_Calculator(orlist))
