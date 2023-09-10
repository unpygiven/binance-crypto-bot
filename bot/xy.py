import pandas as pd
import numpy as np
import requests
from binanceapibase import binanceAPI

class XY:
    def __init__(self, symbol):
        self.__Symbol = symbol
        binanceAPI.apiKey = "s5GgONkYNu9Vdzhw9A0Q0YiPPVWJN96huS3VSMRWVyuwwj4xjPln4Aic3EUPf9gA"
        binanceAPI.apiSecret = "4scsNT2GvO1KR6jLn9zPv9yfqarnhlt3lNNvEBxdMHdWZAN9dasGtrvlyatf3iF8"
        self.__X : pd.DataFrame
        self.__Y : pd.DataFrame
        self.__All : pd.DataFrame

    def SetXY(self):
        klines = binanceAPI.priceHistory(self.__Symbol)
        prices = []
        for kline in klines:
            prices.append(float(kline[4]))

        x = list(range(len(prices)))
        pricesDF = pd.DataFrame(data=prices, index=x, columns=['price'])
        xDF = pd.DataFrame(data=x, index=x, columns=['index'])
        all = pd.concat([xDF, pricesDF], axis=1)
        self.__All = all
        self.__X = all.iloc[:,0:1]
        self.__Y = all.iloc[:,1:2]

    @property
    def X(self):
        return self.__X
    
    @property
    def Y(self):
        return self.__Y
    
    @property
    def All(self):
        return self.__All
    