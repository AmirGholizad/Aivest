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
    elif LAST >= OR_high:
        for i in range(0, len(ticks)):
            if ticks_frame["last"][i] < OR_low:
                return 4
            else:
                continue
        return 2

    elif LAST <= OR_low:
        for i in range(0, len(ticks)):
            if ticks_frame["last"][i] > OR_high:
                return -4
            else:
                continue
        return -2

def Macro_Calculator(a,b,c,symbol):

    Score = []
    date = []
    Macro_10 = []
    adate = datetime.date(a,b,c)
    print(adate)
    for j in range(0, 90):
        orlist = OR_Calculator.OR_Calculator(a,b,c,symbol)
        if orlist == None:
            adate = adate + datetime.timedelta(days=1)
            c = adate.day
            b = adate.month
            continue
        #print(OR_Calculator(orlist))
        Score.append(Score_Calculator(symbol,orlist,a,b,c))
        date.append(adate)
        #print(Score , "{}-{}-{}".format(a,b,c))
        adate = adate + datetime.timedelta(days=1)
        c = adate.day
        b = adate.month
    for k in range(0,len(Score)):
        if k<10:
            Macro_10.append(None)
        else:
            Macro_10.append(sum(Score[k-9:k]))
    MACROs_dic = { 'Date' : date ,'Score' : Score , 'Macro' : Macro_10}
    MACROs = pd.DataFrame(MACROs_dic)
    MACROs = MACROs.dropna()
    print(MACROs)

Macro_Calculator(2020,8,13, "SAFAB99")
"""
for i in range(5):
    date = datetime.timedelta(days=1)
    print(date)
"""