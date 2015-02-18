'''
Created on Sep 24, 2013

@author: fkaddoura
'''


class MarketData(object):
    
    def __init__(self, securityCode):
        
        self.Date = None
        self.SecurityCode = securityCode
        self.LastPrice = 0.0
        self.LastPriceBook = 0.0
        self.UnderlyingPrice = 0.0
        self.UnderlyingPriceBook = 0.0
        self.Beta = 0.0
        self.Delta = 0.0
        self.Theta = 0.0
        self.Gamma = 0.0
        self.MarketCap = 0.0
        self.AvgDailyVolume = 0.0
        self.Vega = 0.0