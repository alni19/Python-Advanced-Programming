'''
Created on Sep 24, 2013

@author: fkaddoura
'''
import SecurityObjects as SecurityMaster
import math

# a neat trick to work around the lack of enums in python
def enum(**enums):
    return type('Enum', (), enums)


#this portfolio class stores a list of positions
class Portfolio(object):
    def __init__(self, name, businessDate):
        self.Name = name
        self.BusinessDate = businessDate
        #list of positions
        self.Positions = []
        self.Counter = 0
    
    #iterators methods     
    def __iter__(self):
        self.Counter = 0
        return self  
        
    def next(self):
        if self.Counter >= len(self.Positions):
            raise StopIteration
        else:
            pos = self.Positions[self.Counter]
            self.Counter += 1
            return pos    
            
        
class Position(object):
    def __init__(self, security, holdingDirection, custodian, quantity, marketValueBook, dtdTotalPnLBook):
        
        
        self.Security = security
        self.HoldingDirection = holdingDirection
        self.Custodian = custodian
        self.Quantity = quantity
        self.MarketValueBook = marketValueBook
        self.DayTotalPnLBook = dtdTotalPnLBook
        
        #added these properties to optimize the code and avoid loading a security object
        self.Date = ""
        self.PortfolioCode = ""
        self.SecurityCode = ""
        
        

    def GetPositionExposure(self):
        return self.Quantity * self.Security.GetExposure()
    
    