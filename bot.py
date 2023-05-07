# Stock Trading Bot that uses the Supertrend Indicator to buy and sell stocks
# Uses the Aplaca paper trading platform

import datetime
import alpaca_trade_api as tradeapi
import yfinance as yf
import time
import sys

buy = 'buy'
sell = 'sell'
global buyQty
buyQty = 10
buyTime = int

# Add your stock name here *Make sure all are uppercase*
alpacaName = "AAPl"

# Add your API key and secret key here from the alpaca paper website
API_KEY = "ADD YOUR API KEY HERE"
SECRET_KEY = "ADD YOUR SECRET KEY HERE"
BASE_URL = "https://paper-api.alpaca.markets"

# instantiate REST API
def Instantiate():
    global api
    api = tradeapi.REST(API_KEY, SECRET_KEY, BASE_URL, api_version='v2')

    # obtain account information
    account = api.get_account()

    positions = api.list_positions()

def Time():
    clock = api.get_clock()
    closingTime = clock.next_close.replace(tzinfo=datetime.timezone.utc).timestamp()
    currTime = clock.timestamp.replace(tzinfo=datetime.timezone.utc).timestamp()
    api.timeToClose = closingTime - currTime

    global timeTillOpen
    global timeLeft
    timeTillOpen = api.timeToClose - 23400
    timeLeft = api.timeToClose
    timeLeft = timeLeft / 60

def StockNumber():
    global qty
    qty = 0

    orders = api.list_positions()
    for position in orders:
        qty = abs(int(float(position.qty)))

    print("QTY = ", qty)

# Buys the number of stocks you want from the variable buyQty
def BuyOrder():
    api.submit_order(symbol=alpacaName, qty=buyQty, side=buy, time_in_force='gtc', type='market')
    print("I'm buying", buyQty, 'stocks!')
    PrintData()

# Sell all stocks that you have bought it checks the amount of stocks 
# you have and then removes your position in them
def SellOrder():
    if qty == 0:
        print("We don't have any positions in this stock going idle")
        pass
    elif qty > 0:
        api.submit_order(symbol=alpacaName, qty=qty, side=sell, time_in_force='gtc', type='market')
        print("I'm selling all stocks:", qty)
        PrintData()


# ---------------------------------------------------------------------------------------------------


def DownloadData():
    # Put your desired stock name at the variable stockN *Make sure all are uppercase*
    global stockN
    stockN = 'AAPL'
    # Put your period and interval for the supertrend
    global data
    data = yf.download(stockN, period="1d", interval="2m")
    data = data.reset_index(drop=True)

    data['tr0'] = abs(data["High"] - data["Low"])
    data['tr1'] = abs(data["High"] - data["Close"].shift(1))
    data['tr2'] = abs(data["Low"] - data["Close"].shift(1))
    data["TR"] = round(data[['tr0', 'tr1', 'tr2']].max(axis=1), 2)
    data["ATR"] = 0.00
    data['BUB'] = 0.00
    data["BLB"] = 0.00
    data["FUB"] = 0.00
    data["FLB"] = 0.00
    data["ST"] = 0.00

    global currentPrice
    global buyTime
    buyTime = 390 - timeLeft
    buyTime = buyTime / 2
    buyTime = buyTime - 1.49
    buyTime = int(buyTime)
    print("Buy Time: ", buyTime)

    currentPrice = data["High"][buyTime]
    currentPrice = float(currentPrice)
    print("Current Price: ", currentPrice)

# This decides if you should buy or sell buy is True sell is False
stockBool = False

# This function runs the code to calculate the supertrend
def RunBot():
    # Calculating ATR
    global stockBool
    for i, row in data.iterrows():
        if i == 0:
            data.loc[i, 'ATR'] = 0.00  # data['ATR'].iat[0]
        else:
            data.loc[i, 'ATR'] = ((data.loc[i - 1, 'ATR'] * 13) + data.loc[i, 'TR']) / 14

    data['BUB'] = round(((data["High"] + data["Low"]) / 2) + (2 * data["ATR"]), 2)
    data['BLB'] = round(((data["High"] + data["Low"]) / 2) - (2 * data["ATR"]), 2)

    # FINAL UPPERBAND = IF( (Current BASICUPPERBAND < Previous FINAL UPPERBAND) or (Previous Close > Previous FINAL
    # UPPERBAND)) THEN (Current BASIC UPPERBAND) ELSE Previous FINALUPPERBAND)

    for i, row in data.iterrows():
        if i == 0:
            data.loc[i, "FUB"] = 0.00
        else:
            if (data.loc[i, "BUB"] < data.loc[i - 1, "FUB"]) | (data.loc[i - 1, "Close"] > data.loc[i - 1, "FUB"]):
                data.loc[i, "FUB"] = data.loc[i, "BUB"]
            else:
                data.loc[i, "FUB"] = data.loc[i - 1, "FUB"]

    # FINAL LOWERBAND = IF( (Current BASIC LOWERBAND > Previous FINAL LOWERBAND) or (Previous Close < Previous FINAL
    # LOWERBAND)) THEN (Current BASIC LOWERBAND) ELSE Previous FINAL LOWERBAND)

    for i, row in data.iterrows():
        if i == 0:
            data.loc[i, "FLB"] = 0.00
        else:
            if (data.loc[i, "BLB"] > data.loc[i - 1, "FLB"]) | (data.loc[i - 1, "Close"] < data.loc[i - 1, "FLB"]):
                data.loc[i, "FLB"] = data.loc[i, "BLB"]
            else:
                data.loc[i, "FLB"] = data.loc[i - 1, "FLB"]

    for i, row in data.iterrows():
        if i == 0:
            data.loc[i, "ST"] = 0.00
        elif (data.loc[i - 1, "ST"] == data.loc[i - 1, "FUB"]) & (data.loc[i, "Close"] <= data.loc[i, "FUB"]):
            data.loc[i, "ST"] = data.loc[i, "FUB"]
        elif (data.loc[i - 1, "ST"] == data.loc[i - 1, "FUB"]) & (data.loc[i, "Close"] > data.loc[i, "FUB"]):
            data.loc[i, "ST"] = data.loc[i, "FLB"]
        elif (data.loc[i - 1, "ST"] == data.loc[i - 1, "FLB"]) & (data.loc[i, "Close"] >= data.loc[i, "FLB"]):
            data.loc[i, "ST"] = data.loc[i, "FLB"]
        elif (data.loc[i - 1, "ST"] == data.loc[i - 1, "FLB"]) & (data.loc[i, "Close"] < data.loc[i, "FLB"]):
            data.loc[i, "ST"] = data.loc[i, "FUB"]

    # Buy Sell Indicator
    for i, row in data.iterrows():
        if i == 0:
            data["ST_BUY_SELL"] = "NA"
        elif data.loc[i, "ST"] < data.loc[i, "Close"]:
            data.loc[i, "ST_BUY_SELL"] = stockBool = True  # TRUE MEANS TO BUY
        else:
            data.loc[i, "ST_BUY_SELL"] = stockBool = False  # FALSE MEANS TO SELL

# This function decides if it is a buy or sell depending on the stockBool value
def main():
    global boughtPrice

    if stockBool == True and qty == 0:
        boughtPrice = currentPrice
        print("ITS A BUY!")
        BuyOrder()
    elif not stockBool:
        print("ITS A SELL!")
        SellOrder()
        boughtPrice = 0
    elif float(currentPrice) < boughtPrice:
        print("ITS GETTING TOO LOW IM SELLING")
        SellOrder()
        boughtPrice = 0
    else:
        print('We already have this stock, not buying anymore')

# This function runs the code and displays data
def DisplayData():
    DownloadData()
    StockNumber()
    RunBot()
    main()
    print("Bought Price: ", boughtPrice)

def PrintData():
    print(data)


# ----------------------------------------------------------------------------------------------------


# This function prevent the code from running if the market is not open
def TimeRun():
    Time()
    if api.timeToClose > 23400:
        print('Market is closed now it opens in', int(timeTillOpen / 60), 'minutes')
        exit("Try again in " + str(int(timeTillOpen / 60)) + " minutes!")
    if api.timeToClose < 23400:
        print('Market is open running code...')
    else:
        exit()

def SuperTrend():
    Instantiate()
    TimeRun()
    DisplayData()

Instantiate()
TimeRun()

# This is the main loop that runs the code
# Runs every 30 seconds you can change the values to your liking
while api.timeToClose < 23400:
    SuperTrend()
    time.sleep(30)
