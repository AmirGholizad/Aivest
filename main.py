import numpy as np
import pandas as pd
from datetime import datetime

def Pivot_Arrange(Daily):
    """
    This function calculates the pivots from csv files downloaded from TSE
    """
    High=Daily['<HIGH>']
    Low = Daily['<LOW>']
    Close = Daily['<LAST>']
    x=(High[0]+Low[0])/2
    y=(High[0]+Low[0]+Close[0])/3
    w=abs(x-y)
    P1_low=y-w
    P1_high=y+w
    X=(max(High[0:5])+min(Low[0:5]))/2
    Y=(max(High[0:5])+min(Low[0:5])+Close[0])/3
    W=abs(X-Y)
    P5_low=Y-W
    P5_high=Y+W
    return([P1_high,P1_low,P5_high,P5_low])

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
