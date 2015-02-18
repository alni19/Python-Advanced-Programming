'''
Created by:
    fkaddoura
Modified by:
    Chendi Ni cn2367
    Bernardo Bravo bb2699
'''
import csv
import datetime
from BusinessObjects import SecurityObjects as SecurityMaster
from BusinessObjects import MarketDataObjects as md
from BusinessObjects import PortfolioObjects as port
from BusinessObjects import PortfolioObjects


class BaseLoader(object):
    'base helper class that makes loading data from a CSV file a little bit less tedious. SecurityLoader and PortfoliLoader can reuse some of the '
    def __init__(self, fileName):
        self.FileName = fileName
        self.DataFile = None
        
    def GetDictionaryReader(self):
        try:
            
            if not csv.Sniffer().has_header(self.FileName):
                raise Exception("GetSecurityObjects failed. Headers expected in position file. FileName: " + self.FileName)
                
            self.DataFile = open(self.FileName, 'rt')
            dictReader = csv.DictReader(self.DataFile)
            return dictReader
        except Exception, e:
            raise Exception("GetDictionaryReader failed. Error Message: " + str(e))
            
    def GetDecimalValue(self, val):
        'Helper method that works around NULL strings in some decimal cells'
        if(val.upper() == "NULL"):
            return 0.0
        else:
            return float(val)
        
    def GetDateFromString(self, dateAsString):
        return datetime.datetime.strptime(dateAsString, "%m/%d/%Y").date()
    
    def GetDateStringList(self):
        dictReader=  self.GetDictionaryReader()
        DateStringList=[]
        for dictRow in dictReader:
            if not dictRow["BusinessDate"] in DateStringList:
                DateStringList.append(dictRow["BusinessDate"])
        return DateStringList

#Question 3. Creation of the PortfolioLoader class with its GetPorfolio method
class PortfolioLoader(BaseLoader):
    
    #loads a portfolio object from CSV file
    def __init__(self, positionFile):
        super(PortfolioLoader, self).__init__(positionFile)
        pass
        
    #The method receives a date    
    def GetPortfolio(self, requestedBusinessDate):
        try:         
            #parse the securities
            secLoader = SecurityLoader(self.FileName) 
            securities = secLoader.GetSecurityObjects(requestedBusinessDate)
            dictReader = self.GetDictionaryReader()
            #load the positions
            positionlist=[]
            for dictRow in dictReader:
                businessDate = self.GetDateFromString(dictRow["BusinessDate"])
                if(requestedBusinessDate == businessDate):
                    securityCode = dictRow["SecurityCode"]
                    positionlist.append(self.PostionFromDataRow(securities[securityCode], dictRow))
            #need to implement the code that creates a portfolio object and load the positions
            portfolio=port.Portfolio('required portfolio',requestedBusinessDate)
            portfolio.Positions=positionlist
            
        except Exception, e:
            raise Exception("GetPortfolio failed. Error Message: " + str(e))
        finally:
            if self.DataFile != None :
                self.DataFile.close()
        return portfolio
    
    #gets position from a certain row    
    def PostionFromDataRow(self,security,DataRow):
        try:
            holdingDirection=DataRow['HoldingDirection']
            custodian=DataRow['CustodianCode']
            quantity=self.GetDecimalValue(DataRow['Quantity'])
            marketValueBook=self.GetDecimalValue(DataRow['MktValBook'])
            position=port.Position(security, holdingDirection, custodian, quantity, marketValueBook)
            return position
        except Exception, e:
            raise Exception("GetPosition Failed. Error Message:"+str(e))            
    
        

#this was completed in Assignment 2 solution        
class SecurityLoader(BaseLoader):
    
    def __init__(self, positionFile):
        super(SecurityLoader, self).__init__(positionFile)
        pass
    

    def GetSecurityObjects(self, requestedBusinessDate):
        try:
           
            dictReader = self.GetDictionaryReader()
                    
            #dictReader is list of dictionaries where the keys are the column headers and the values represent one row of values
            dictResults = {}
            #iterate over 
            for dictRow in dictReader:
                businessDate = self.GetDateFromString(dictRow["BusinessDate"])
                if(requestedBusinessDate == businessDate) :
                    securityCode = dictRow["SecurityCode"]
                    if(not securityCode in dictResults):
                        security = self.SecurityFromDataRow(securityCode, dictRow)
                        dictResults[securityCode] = security
                    else:
                        security = dictResults[securityCode]
                        
                    self.AddMarketDataFromDataRow(security, dictRow)    
            return dictResults
        except Exception, e:
            raise Exception("GetSecurityObjects failed. Error Message: " + str(e))
        finally:
            if self.DataFile != None :
                self.DataFile.close()

    #this is a factory method that will create objects based on sectype
    def SecurityFromDataRow(self, securityCode, dictRow):
        security = None
        secType = dictRow["SecurityTypeCode"]
        secType = secType.upper()
        securityDesc = dictRow["SecurityDesc"]
        currencyCode = dictRow["CurrencyCode"]
        exchange = dictRow["ExchangeCode"]
        issuerDesc = dictRow["IssuerDesc"]
           
        
        issuer = SecurityMaster.Issuer("", issuerDesc)
        
        
        if(secType == "STOCK"):
            security = SecurityMaster.Stock(issuer, securityCode, securityDesc, currencyCode, exchange, secType)
            
        elif(secType == "OPTION"):
            security = SecurityMaster.Option(issuer, securityCode, securityDesc, currencyCode, exchange, secType)
            security.ExpirationDate = datetime.datetime.strptime(dictRow["Expiration"], "%m/%d/%Y").date()
            security.Strike = float(dictRow["Strike"])
            security.ContractSize = float(dictRow["ContractSize"])
            
            
            putCall  = dictRow["PutCall"]
            if(putCall == "C"):
                security.PutCall = SecurityMaster.PutCall.Call
            elif(putCall == "P"):
                security.PutCall = SecurityMaster.PutCall.Put
            else:
                security.PutCall = SecurityMaster.PutCall.Unknown
            
            optType = dictRow["ExcerciseType"]
            if(optType == "European"):
                security.OptionType = SecurityMaster.ExcerciseType.European
            else:
                security.OptionType = SecurityMaster.ExcerciseType.American
                  
            security.UnderlyingSecurity = None #will be loaded from Bloomberg later
            
            
        elif(secType == "BOND"):
            security = SecurityMaster.Bond(issuer, securityCode, securityDesc, currencyCode, exchange, secType)
            maturity = dictRow["Maturity"]
            if(maturity.upper() != "NULL"): 
                security.Maturity = datetime.datetime.strptime(dictRow["Maturity"], "%m/%d/%Y").date()
            coupon = dictRow["Coupon"].upper()
            if(coupon!= "NULL"):
                security.Coupon = float(dictRow["Coupon"])
        else:
            security = SecurityMaster.OtherSecurity(issuer, securityCode, securityDesc, currencyCode, exchange, secType)
        
        #continue adding more attributes to the security
        security.BbergCode = dictRow["BbergCode"]
        security.BloombergMarketSectorCode = dictRow["BloombergMarketSectorCode"]
        security.Cusip = dictRow["Cusip"]
        security.Isin = dictRow["Isin"]
        security.Sedol = dictRow["Sedol"]
        security.SectorDesc = dictRow["SectorDesc"] 
        security.GeographyRegionDesc = dictRow["GeographyRegionDesc"]    
        security.GicsSectorDesc = dictRow["GicsSectorDesc"]
        return security 
       
        
    
    #adds a market data to securityObject
    def AddMarketDataFromDataRow(self, security, dictRow):
        businessDate = datetime.datetime.strptime(dictRow["BusinessDate"], "%m/%d/%Y").date() 
        mktData = md.MarketData(security.SecurityCode)
        mktData.Date = businessDate
        mktData.LastPrice = self.GetDecimalValue(dictRow["PriceLocal"])
        #had to modify this part (PriceBook instead of LastPriceBook):
        mktData.PriceBook = self.GetDecimalValue(dictRow["PriceBook"])
        mktData.UnderlyingPrice = self.GetDecimalValue(dictRow["UnderlierPriceLocal"])
        mktData.UnderlyingPriceBook = self.GetDecimalValue(dictRow["UnderlierPriceBook"])    
        mktData.Delta = self.GetDecimalValue(dictRow["Delta"])
        mktData.Beta = self.GetDecimalValue(dictRow["Beta"])
        security.MarketData = mktData
                