'''
Created by:
    fkaddoura
Modified by:
    Chendi Ni cn2367
    Bernardo Bravo bb2699
'''

#Question 1. It was all done
class MarketData(object):
    
    def __init__(self, securityCode):
        
        self.Date = None
        self.SecurityCode = securityCode
        self.PriceLocal = 0.0
        self.PriceBook = 0.0
        self.UnderlyingPrice = 0.0
        self.UnderlyingPricebook = 0.0
        self.Beta = 0.0
        self.Delta = 0.0
        
        #self.Theta = 0.0,
        #self.Gamma = 0.0
        #self.MarketCap = 0.0
        #self.AvgDailyVolume = 0.0
        #self.Vega = 0.0
        #and the list goes on