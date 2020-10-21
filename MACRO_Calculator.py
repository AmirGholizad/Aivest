# first import packages that you need
from OR_Calculator import OR_Calculator
from Score_Calculator import Score_Calculator
from Time_shift import Time_Shift
from ATR__Calculator import ATR_Calculator
import MetaTrader5 as mt5
import pandas as pd
import numpy as np
import pytz
import datetime

# calculate the macro
def Macro_Calculator(symbol,y,m,d,h1,m1,s1,h2,m2,s2):
    mt5.initialize()
    Score = np.zeros(30)
    Date = np.zeros(30, datetime.date)
    Macro_10 = np.zeros(30)
    adate = datetime.date(y,m,d)
    for j in range(0, 30):
        orlist = OR_Calculator(symbol, y, m, d, h1, m1, s1, h2, m2, s2)
        if orlist == None:
            adate = Time_Shift(y, m, d, symbol)
            y = adate[0]
            m = adate[1]
            d = adate[2]
            continue
        if Score_Calculator(symbol,y,m,d,h1,m1,s1,h2,m2,s2) == None:
            adate = Time_Shift(y, m, d, symbol)
            y = adate[0]
            m = adate[1]
            d = adate[2]
            continue
        Score[j] = Score_Calculator(symbol,y,m,d,h1,m1,s1,h2,m2,s2)[0]
        Date[j] = datetime.datetime(y,m,d)
        adate = Time_Shift(y, m, d, symbol)
        y = adate[0]
        m = adate[1]
        d = adate[2]
    for k in range(0,len(Score)):
        if k<20:
            Macro_10[k] = (sum(Score[k:k+6]))
        else:
            Macro_10[k] = None
    MACROs = pd.DataFrame({ 'Date' : Date ,'Score' : Score , 'Macro' : Macro_10})
    return MACROs
print(Macro_Calculator("SAFAB99",2020,10,20,10,30,0,15,0,0))
