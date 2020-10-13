# first import packages that you need
from OR_Calculator import OR_Calculator
from ATR__Calculator import ATR_Calculator
import MetaTrader5 as mt5
import pandas as pd
import pytz
import datetime



def Score_Calculator(symbol,orlist,y,m,d,h1,m1,s1,h3,m3,s3):
    # set time zone to UTC
    timezone = pytz.timezone("Etc/UTC")
    # create 'datetime' objects in UTC time zone to avoid the implementation of a local time zone offset
    Session_Start = datetime.datetime(y, m, d, h1, m1, s1, tzinfo=timezone)
    Session_Stop = datetime.datetime(y, m, d, h3, m3, s3, tzinfo=timezone)
    # request any symbol that you want and it's ticks within different Opening Ranges that you want
    ticks = mt5.copy_ticks_range(symbol , Session_Start, Session_Stop, mt5.COPY_TICKS_ALL)
    # make the dataframe of ticks
    ticks_frame = pd.DataFrame(ticks)
    # convert time in seconds into the datetime format
    ticks_frame['time'] = pd.to_datetime(ticks_frame['time'], unit='s')
    # get the closing price
    LAST = ticks_frame["last"].iloc[-1]
    # from orlist find OR_high and OR_low
    OR_high = orlist[0]
    OR_low = orlist[1]
    # yesterday's ATR is used for today's Macro_Calculator
    timeshift = datetime.datetime(y, m, d)
    timeshift = timeshift - datetime.timedelta(days=1)
    timeshift = str(timeshift.date())
    timeshift = timeshift.split('-')
    Y = int(timeshift[0])
    M = int(timeshift[1])
    D = int(timeshift[2])
    # get the ATR and make the A and C levels
    A_up = (ATR_Calculator(Y,M,D,symbol).iloc[-1])*0.1 + OR_high
    A_down = (ATR_Calculator(Y, M, D, symbol).iloc[-1])*0.1 - OR_low
    C_up = (ATR_Calculator(Y, M, D, symbol).iloc[-1])*0.15 + OR_high
    C_down = (ATR_Calculator(Y, M, D, symbol).iloc[-1])*0.15 - OR_low
    # calculate the score
    if (LAST < OR_high) and (LAST > OR_low):
        return 0
    elif LAST >= A_up:
        for i in range(0, len(ticks)):
            if ticks_frame["last"][i] <= A_down:
                return 4
            else:
                continue
        return 2

    elif LAST <= A_down:
        for i in range(0, len(ticks)):
            if ticks_frame["last"][i] >= A_up:
                return -4
            else:
                continue
        return -2
# calculate the macro
"""
def Macro_Calculator(symbol,y,m,d,h1,m1,s1,h2,m2,s2,h3,m3,s3):
    Score = []
    date = []
    Macro_10 = []
    adate = datetime.date(y,m,d)
    print(adate)
    for j in range(0, 30):
        orlist = OR_Calculator(symbol,y,m,d,h1,m1,s1,h2,m2,s2)
        if orlist == None:
            adate = adate + datetime.timedelta(days=1)
            d = adate.day
            m = adate.month
            y = adate.year
            continue
        Score.append(Score_Calculator(symbol,orlist,y,m,d,h1,m1,s1,h3,m3,s3))
        date.append(adate)
        adate = adate + datetime.timedelta(days=1)
        d = adate.day
        m = adate.month
        y = adate.year
    for k in range(0,len(Score)):
        if k<9:
            Macro_10.append('-')
        else:
            Macro_10.append(sum(Score[k-9:k]))
    MACROs = pd.DataFrame({ 'Date' : date ,'Score' : Score , 'Macro' : Macro_10})
    return MACROs
"""
orlist = OR_Calculator("SAFAB99",2020,10,12,10,30,0,10,45,0)
print(Score_Calculator("SAFAB99",orlist,2020,10,12,10,30,0,15,0,0))
