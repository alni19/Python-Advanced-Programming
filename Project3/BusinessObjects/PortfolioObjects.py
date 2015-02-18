'''
Created by:
    fkaddoura
Modified by:
    Chendi Ni cn2367
    Bernardo Bravo bb2699
'''
import SecurityObjects as SecurityMaster
import math

# a neat trick to work around the lack of enums in python
def enum(**enums):
    return type('Enum', (), enums)

#Question 1. It was all done
#this portfolio class stores a list of positions
class Portfolio(object):
    def __init__(self, name, businessDate):
        self.Name = name
        self.BusinessDate = businessDate
        #list of positions
        self.Positions = []
        self.iterpointer = -1
        self.PositionsLen = 0
        
    def updatePositionsLen(self):
        self.PositionsLen=len(self.Positions)
    
    #Question 5. Define the iterator to move through the position object
    def __iter__(self):
        return self
    
    def next(self):
        if self.iterpointer==self.PositionsLen-1:
            raise StopIteration
        self.iterpointer+=1
        return self.Positions[self.iterpointer]
    
    def getporfolioexposure(self):
        exposure=0
        for i in range(len(self.Positions)):
            exposure=exposure+self.Positions[i].GetPositionExposure()
        return exposure
            
        
class Position(object):
    def __init__(self, security, holdingDirection, custodian, quantity, marketValueBook):
        
        #these are all the fields we need for this excercise
        self.Security = security
        self.HoldingDirection = holdingDirection
        self.Custodian = custodian
        self.Quantity = quantity
        self.MarketValue = marketValueBook
    
    #Question 4. We define the method by calling the GetExposure method and multiply it by the quantity    
    def GetPositionExposure(self):
        return self.Security.GetExposure()*self.Quantity

    