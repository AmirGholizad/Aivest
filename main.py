# first import packages that you need
import MetaTrader5 as mt5
import OR_Calculator
import MACRO_Calculator
import ATR__Calculator
import datetime
# get the symbol from user
"""
for i in range(0,1000):
    print("Please import the company name or symbol:   ")
    symbol = input()
    # check if symbol is correct
    mt5.initialize()
    selected=mt5.symbol_select(symbol,True)
    if selected == None:
        print("The symbol you've entered isn't correct!")
        print("Do you want to try again(type y or n):   ")
        answer = input()
        if answer.lower() == n:
            quit()
        elif answer.lower() == y:
    else:
        break
"""
mt5.initialize()
print("Please import the company name or symbol:   ")
symbol = input()
print("Which market:   ")
market = input()
if market.lower() == 'tse':
    h1 = 9
    m1 = 0
    s1 = 0
    h2 = 9
    m2 = 15
    s2 = 0
    h3 = 12
    m3 = 30
    s3 = 0
if market.lower() == 'ime':
    h1 = 10
    m1 = 30
    s1 = 0
    h2 = 10
    m2 = 45
    s2 = 0
    h3 = 15
    m3 = 0
    s3 = 0
todaydate = datetime.datetime.today().date()
todaydatestr = str(todaydate)
todaydatelist = todaydatestr.split('-')
y = int(todaydatelist[0])
m = int(todaydatelist[1])
d = int(todaydatelist[2])

date_and_time = [y,m,d,h1,m1,s1,h2,m2,s2,h3,m3,s3]

print(MACRO_Calculator.Macro_Calculator(symbol,y,m,d,h1,m1,s1,h2,m2,s2,h3,m3,s3))