from loadmodels import LoadModel
from binanceapibase import binanceAPI
from positionsymbol import Symbol
from position import Position
from log import Log
import time
from sklearn.preprocessing import PolynomialFeatures
import numpy as np

class Bot:
    def __init__(self, symbols : list, regtype:str):
        self.__Symbols = symbols
        self.__InPosition = False
        self.__Position = None
        self.__RegType = regtype
        binanceAPI.apiKey = "s5GgONkYNu9Vdzhw9A0Q0YiPPVWJN96huS3VSMRWVyuwwj4xjPln4Aic3EUPf9gA"
        binanceAPI.apiSecret = "4scsNT2GvO1KR6jLn9zPv9yfqarnhlt3lNNvEBxdMHdWZAN9dasGtrvlyatf3iF8"

    @property
    def Models(self):
        models = {}
        for symbol in self.__Symbols:
            model = LoadModel(symbol=symbol, type=self.__RegType)
            models[symbol] = model.Model   
        return models

    @property
    def Position(self):
        return self.__Position

    def __SearchForPosition(self):
        for symbol in self.__Symbols:
            currentPrice = binanceAPI.currentPrice(symbol=symbol)
            if self.__RegType == "PolynomialRegression":
                pf = PolynomialFeatures(degree=2)
                le = pf.fit_transform(np.array([len(binanceAPI.priceHistory(symbol)) - 1]).reshape(1,-1))
            else:
                le = [[len(binanceAPI.priceHistory(symbol)) - 1]]
            predict = self.Models[symbol].predict(le)
            errorMargin = ((predict - currentPrice) / currentPrice) * 100
            st = f"""
**********
SYMBOL : {symbol}
PREDICTION : {predict}
CURRENT PRICE : {currentPrice}
ERROR MARGIN : {errorMargin}
ALGORITHM : {self.__RegType}
**********
"""
            print(st)
            if currentPrice < predict:
                sp = currentPrice + (currentPrice * 5) / 100
                stp = currentPrice - (currentPrice * 5) / 100
                PSymbol = Symbol(symbol=symbol, buyprice=currentPrice, sellprice=sp, stopprice=stp)
                self.__Position = Position(symbol=PSymbol)
                self.__Position.StartPosition()
                log = Log(self.__Position.PositionDetails)
                log.EnterLog()
                self.__InPosition = True
    
    def __ManagePosition(self):
        currentPrice = binanceAPI.currentPrice(self.__Position.PositionDetails.Symbol)
        st = f"""
***IN POSITION***
SYMBOL : {self.__Position.PositionDetails.Symbol}
BUY PRICE : {self.__Position.PositionDetails.Buyprice}
SELL PRICE : {self.__Position.PositionDetails.Sellprice}
STOP PRICE : {self.__Position.PositionDetails.Stopprice}
CURRENT PRICE : {currentPrice}
ALGORITHM : {self.__RegType}
***IN POSITION***
"""
        print(st)
        if self.__Position.PositionDetails.Sellprice <= currentPrice:
            profit = ((currentPrice - self.__Position.PositionDetails.Buyprice) / self.__Position.PositionDetails.Buyprice) * 100
            st = f"""
***TARGET SELL***
SYMBOL : {self.__Position.PositionDetails.Symbol}
BUY PRICE : {self.__Position.PositionDetails.Buyprice}
SELL PRICE : {self.__Position.PositionDetails.Sellprice}
PROFIT : {profit}
ALGORITHM : {self.__RegType}
***TARGET SELL***
"""
            self.__Position.ExitPosition()
            print(st)
            self.__InPosition = False
            log = Log(self.__Position.PositionDetails)
            log.ExitLog(currentPrice)

        if self.__Position.PositionDetails.Stopprice >= currentPrice:
            loss = ((self.__Position.PositionDetails.Buyprice - currentPrice) / self.__Position.PositionDetails.Buyprice) * 100
            st = f"""
***STOP SELL***
SYMBOL : {self.__Position.PositionDetails.Symbol}
BUY PRICE : {self.__Position.PositionDetails.Buyprice}
SELL PRICE : {self.__Position.PositionDetails.Sellprice}
PROFIT : {loss}
ALGORITHM : {self.__RegType}
***STOP SELL***
"""
            self.__Position.ExitPosition() 
            print(st)
            self.__InPosition = False
            log = Log(self.__Position.PositionDetails)
            log.ExitLog(currentPrice)

    def Start(self):
        if not self.__InPosition:
            self.__SearchForPosition()
        else:
            self.__ManagePosition()
            
            



