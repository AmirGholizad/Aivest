import numpy as np
import pandas as pd
from datetime import datetime

def Pivot_Arrange(Daily):
        """
        This function calculates the pivots
        """
        High = Daily['<HIGH>']
        Low = Daily['<LOW>']
        Close = Daily['<LAST>']

        P5h_list = []
        P5l_list = []
        P1h_list = []
        P1l_list = []

        for i in range(0, 30):
            x = (High[i] + Low[i]) / 2
            y = (High[i] + Low[i] + Close[i]) / 3
            w = abs(x - y)

            P1_low = y - w
            P1_high = y + w

            X = (max(High[i:i + 5]) + min(Low[i:i + 5])) / 2
            Y = (max(High[i:i + 5]) + min(Low[i:i + 5]) + Close[i]) / 3
            W = abs(X - Y)

            P5_low = Y - W
            P5_high = Y + W

            P5h_list.append(P5_high)
            P5l_list.append(P5_low)

            P1h_list.append(P1_high)
            P1l_list.append(P1_low)

        PIVOTS = pd.DataFrame({'P5H': P5h_list, 'P5L': P5l_list, 'P1H': P1h_list, 'P1L': P1l_list},
                              index=Daily['<DTYYYYMMDD>'][0:30])

        return (PIVOTS)

"""
def Opening_Range(Instant)
    t1 = datetime.now().time()
    t2 = datetime(2020, 9, 27, 9, 15, 0).time()
    if datetime.now().time() != datetime(2020,9,27,9,15,0).time():
        min(Instant)=OR_Low
        max(Instant)=OR_High

def UP_DOWN(Instant)
    if Last >= OR
"""


df = pd.read_csv("S_I..N..C..Ind..csv")
print(Pivot_Arrange(df))

