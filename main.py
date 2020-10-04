from datetime import datetime

def Pivot_Arrange(Daily)
    x=(High[0]+Low[0])/2
    y=(High[0]+Low[0]+Close[0])/3
    w=abs(x,y)
    P1_high=y-w
    P1_low=y+w
    X=(max(High[0:N])+min(Low[0;N]))/2
    Y=(max(High[0:N])+min(Low[0:N])+Close[0])/3
    W=abs(X,Y)
    P5_high=Y-W
    P5_low=Y+W
    retur([P1_high,P1_low,P5_high,P5_low])
def Opening_Range(Instant)
    t1 = datetime.now().time()
    t2 = datetime(2020, 9, 27, 9, 15, 0).time()
    if datetime.now().time() != datetime(2020,9,27,9,15,0).time():
        min(Instant)=OR_Low
        max(Instant)=OR_High

def UP_DOWN(Instant)
    if Last >= OR



