# first import packages that you need
from OR_Calculator import OR_Calculator
from ATR__Calculator import ATR_Calculator
from Time_shift import Time_Shift
import MetaTrader5 as mt5
import pandas as pd
import numpy as np
import pytz
import datetime

def Score_Calculator(symbol,y,m,d,h1,m1,s1,h2,m2,s2,h3,m3,s3):
    mt5.initialize()
    # set time zone to UTC
    timezone = pytz.timezone("Etc/UTC")
    # create 'datetime' objects in UTC time zone to avoid the implementation of a local time zone offset
    Session_Start = datetime.datetime(y, m, d, h2, m2, s2, tzinfo=timezone)
    Session_Stop = datetime.datetime(y, m, d, h3, m3, s3, tzinfo=timezone)
    # request any symbol that you want and it's ticks within different Opening Ranges that you want
    ticks = mt5.copy_ticks_range(symbol , Session_Start, Session_Stop, mt5.COPY_TICKS_ALL)
    if len(ticks) == 0:
        return None
    # make the dataframe of ticks
    ticks_frame = pd.DataFrame(ticks)
    # convert time in seconds into the datetime format
    ticks_frame['time'] = pd.to_datetime(ticks_frame['time'], unit='s')
    # get the closing price
    LAST = ticks_frame["last"].iloc[-1]
    # from orlist find OR_high and OR_low
    orlist = OR_Calculator(symbol, y, m, d, h1, m1, s1, h2, m2, s2)
    OR_high = orlist[0]
    OR_low = orlist[1]
    # get the ATR and make the A and C levels
    A_up = OR_high + (ATR_Calculator(y,m,d,symbol)["ATR"])*0.1
    A_down = OR_low - (ATR_Calculator(y, m, d, symbol)["ATR"])*0.1
    C_up = OR_high + (ATR_Calculator(y, m, d, symbol)["ATR"])*0.15
    C_down = OR_low - (ATR_Calculator(y, m, d, symbol)["ATR"])*0.15

    i=0
    checklist = []
    while i < len(ticks_frame):
        # iterate through ticks_frame
        if ticks_frame['last'][i] >= A_up:
            # check if the price touched the A_up level
            for j in range(i+1,len(ticks_frame)):
                # for 8 minutes check if validation of A_up is confirmed
                timediff = ticks_frame["time"][j] - ticks_frame["time"][i]
                timediff = (datetime.timedelta.total_seconds(timediff)) / 60
                if ticks_frame["last"][j] < OR_high and timediff < 8:
                    # if price has returned below OR line, then call it A_up_fail
                    checklist.append("A_up_fail")
                    print("in time {} A_up fail!".format(ticks_frame["time"][j]))
                    i = j
                    # we should go on and check again for index i = j+1
                    break
                elif ticks_frame["last"][j] > OR_high and timediff >= 8:
                    checklist.append("A_up_valid")
                    print("in time {} A_up Valid!".format(ticks_frame["time"][j]))
                    for k in range(j+1, len(ticks_frame)):
                        if ticks_frame["last"][k] < OR_high:
                            checklist.append("A_up_stop")
                            print("in time {} Stop!".format(ticks_frame["time"][k]))
                            i = k
                            break
                        else:
                            continue
                    i = k+1
                    break
                else:
                    continue
        elif ticks_frame['last'][i] <= A_down:
            # check if the price touched the A_up level
            for m in range(i+1,len(ticks_frame)):
                # for 8 minutes check if validation of A_up is confirmed
                timediff = ticks_frame["time"][m] - ticks_frame["time"][i]
                timediff = (datetime.timedelta.total_seconds(timediff)) / 60
                if ticks_frame["last"][m] > OR_low and timediff < 8:
                    # if price has returned below OR line, then call it A_up_fail
                    checklist.append("A_down_fail")
                    print("in time {} A_down fail!".format(ticks_frame["time"][m]))
                    i = m
                    # we should go on and check again for index i = j+1
                    break
                elif ticks_frame["last"][m] < OR_low and timediff >= 8:
                    checklist.append("A_down_valid")
                    print("in time {} A_down Valid!".format(ticks_frame["time"][m]))
                    for n in range(m+1, len(ticks_frame)):
                        if ticks_frame["last"][n] > OR_low:
                            checklist.append("A_down_stop")
                            print("in time {} Stop!".format(ticks_frame["time"][n]))
                            i = n
                            break
                        else:
                            continue
                    i = n+1
                    break
                else:
                    continue
        else:
            i = i+1
            if i < len(ticks_frame):
                continue
            else:
                break
    print(checklist)

    # calculate the score
    Score = 10000
    checkset = sorted(set(checklist), key=checklist.index)
    if not OR_low == OR_high:
        if (OR_low < ticks_frame["last"].iloc[-1] < OR_high):
            if ("A_up_fail" in checklist) and len(set(checklist)) == 1:
                Score = -1
            elif ("A_down_fail" in checklist) and len(set(checklist)) == 1:
                Score = 1
            else: Score = 0

        elif (ticks_frame["last"].iloc[-1] <= OR_low):
            if checkset == ["A_up_fail", "A_down_valid"] or checkset == ["A_up_fail"]:
                Score = -3
            elif "A_up_valid" in checkset and "A_down_stop" not in checkset:
                Score = -4
            else:
                Score = -2

        elif (ticks_frame["last"].iloc[-1] >= OR_high):
            if checkset == ["A_down_fail", "A_up_valid"] or checkset == ["A_down_fail"]:
                Score = 3
            elif "A_down_valid" in checkset and "A_up_stop" not in checkset:
                Score = 4
            else:
                Score = 2

    elif (OR_low == OR_high):
        timeshift = Time_Shift(y,m,d,symbol)
        Y = timeshift[0]
        M = timeshift[1]
        D = timeshift[2]
        if OR_high > OR_Calculator(symbol, Y, M, D, h1, m1, s1, h2, m2, s2)[0]:
            if (ticks_frame["last"].iloc[-1] == OR_high):
                Score = 2
            elif OR_high/ticks_frame["last"].iloc[-1] >= 1.09:
                Score = -4
            elif (ticks_frame["last"].iloc[-1] < OR_high):
                Score = 0
        if OR_low > OR_Calculator(symbol, Y, M, D, h1, m1, s1, h2, m2, s2)[1]:
            if (ticks_frame["last"].iloc[-1] == OR_low):
                Score = -2
            elif ticks_frame["last"].iloc[-1]/OR_low >= 1.09:
                Score = 4
            elif (ticks_frame["last"].iloc[-1] > OR_low):
                Score = 0

    print(Score, checkset)

Score_Calculator("خودرو", 2020, 9, 23, 9, 0, 0, 9, 15, 0, 12, 30, 0)




"""
    adate = Time_Shift(y, m, d, symbol)
    Y = adate[0]
    M = adate[1]
    D = adate[2]
    # calculate the score
    if (OR_low == OR_high):
        if LAST > OR_Calculator(symbol, Y, M, D, h1, m1, s1, h2, m2, s2)[0]:
            if (LAST == OR_high):
                return 2
            elif (LAST < OR_high):
                return 0
        elif LAST < OR_Calculator(symbol, Y, M, D, h1, m1, s1, h2, m2, s2)[1]:
            if (LAST == OR_high):
                return -2
            elif (LAST > OR_high):
                return 0
        elif (LAST/ticks_frame["last"][0]) > 1.09:
            return 4
        elif (ticks_frame["last"][0]/LAST) > 1.09:
            return -4
    elif (LAST == OR_high):
        for i in range(0, len(ticks)):
            if not (ticks_frame["last"][i] > OR_high) :
                return 2
            else:
                continue
        return 0
    elif (LAST == OR_low):
        for i in range(0, len(ticks)):
            if not (ticks_frame["last"][i] < OR_low) :
                return -2
            else:
                continue
        return 0
    elif (LAST <= OR_high) and (LAST >= OR_low):
        return 0
    elif LAST > OR_high:
        for i in range(0, len(ticks)):
            if ticks_frame["last"][i] <= A_down:
                return 4
            else:
                continue
        return 2

    elif LAST < OR_low:
        for i in range(0, len(ticks)):
            if ticks_frame["last"][i] >= A_up:
                return -4
            else:
                continue
        return -2
"""