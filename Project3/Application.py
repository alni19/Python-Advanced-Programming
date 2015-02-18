'''
Created by:
    fkaddoura
Modified by:
    Chendi Ni cn2367
    Bernardo Bravo bb2699
'''

import DataLoaders as dl
import datetime

#Question 7. Creation of the PortfolioAnalyzer class
class PortfolioAnalyzer(object):
    def __init__(self):
        pass
    def gen(self, portfolioloader):
        datestringlist = portfolioloader.GetDateStringList()
        for i in range(len(datestringlist)):
            yield portfolioloader.GetPortfolio(portfolioloader.GetDateFromString(datestringlist[i]))
        

if __name__ == '__main__':
    
    try:
        positionFileName = "PortfolioAppraisal3.csv"
        
        #We get the portfolios for the day April 15th
        P = dl.PortfolioLoader(positionFileName)
        portfolio_day=P.GetPortfolio(P.GetDateFromString('4/15/2013'))
        portfolio_day.updatePositionsLen()
        totalexposure=0
        
        #Question 6. Portfolio's exposure to the Information Technology sector on April 15, 2013
        for position in portfolio_day:
            #We add up all the exposures for the sector Information Technology
            if position.Security.SectorDesc=='Information Technology':
                totalexposure=totalexposure+position.GetPositionExposure()
        print "The portfolio's exposure to Information Technology sector on 4/15/2013 is "+str(totalexposure)
        
        #Question 7. Time series of the portfolio exposure 
        pa = PortfolioAnalyzer()
        portfoliogenerator = pa.gen(P)
        for portfolio in portfoliogenerator:
            print "Market exposure for "+str(portfolio.BusinessDate)+" is:"
            print portfolio.getporfolioexposure()
    
    except Exception, e:
        print "An error ocurred: ", e
    
    