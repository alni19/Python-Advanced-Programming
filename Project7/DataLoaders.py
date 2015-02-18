'''
Created on Sep 20, 2014

@author: fkaddoura
'''
import csv
import datetime
from BusinessObjects import SecurityObjects as SecurityMaster
from BusinessObjects import MarketDataObjects as md
from BusinessObjects import PortfolioObjects as port


class BaseLoader(object):
    
    'base helper class that makes loading data from a CSV file a little bit less tedious'
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
       
       
       
       
    
class PortfolioLoader(BaseLoader):
    'loads a portfolio object from CSV file'

    def __init__(self, positionFile):
        super(PortfolioLoader, self).__init__(positionFile)
        pass
    
    
    def GetAllPositionsTimeSeries(self):
        try:
           
            results = []
            dictReader = self.GetDictionaryReader()        
            #dictReader is list of dictionaries where the keys are the column headers and the values represent one row of values
            #iterate over 
            
            
            for dictRow in dictReader:
                securityCode = dictRow["SecurityCode"]
                pos = self.PositionFromDataRow(None, dictRow)
                pos.SecurityCode = securityCode
                pos.PortfolioCode = dictRow["PortfolioCode"]
                pos.Date = self.GetDateFromString(dictRow["BusinessDate"])
                #we added the following columns
                pos.AvgCostLocal = dictRow["AvgCostLocal"]
                pos.AvgCostBook = dictRow["AvgCostBook"]
                pos.MktValueLocal = dictRow["MktValLocal"]
                pos.dayPnLLocal = dictRow["DtdPnlTotal"]
                results.append(pos)
        except Exception, e:
            raise Exception("GetAllPositionsTimeSeries failed. Error Message: " + str(e))
        finally:
            if self.DataFile != None :
                self.DataFile.close()
        return results
    
    
    
        
    def GetPortfolio(self, requestedBusinessDate, bAllDates = False):
        try:
            secLoader = SecurityLoader(self.FileName) 
            securities = secLoader.GetSecurityObjects(requestedBusinessDate)
            
            dictReader = self.GetDictionaryReader()        
            #dictReader is list of dictionaries where the keys are the column headers and the values represent one row of values
            portfolio = port.Portfolio("ABC Capital", requestedBusinessDate)
            #iterate over 
            for dictRow in dictReader:
                businessDate = self.GetDateFromString(dictRow["BusinessDate"])
                if(bAllDates or businessDate == requestedBusinessDate):
                    securityCode = dictRow["SecurityCode"]
                    pos = self.PositionFromDataRow(securities[securityCode], dictRow)
                    portfolio.Positions.append(pos)
            
        except Exception, e:
            raise Exception("GetPortfolio failed. Error Message: " + str(e))
        finally:
            if self.DataFile != None :
                self.DataFile.close()
        return portfolio
        
                
    def PositionFromDataRow(self, security, dictRow):
        
        holdingDirection = dictRow["HoldingDirection"]
        custodian = dictRow["CustodianCode"]
        quantity = self.GetDecimalValue(dictRow["Quantity"])
        marketValueBook = self.GetDecimalValue(dictRow["MktValBook"])
        dtdTotalPnL = self.GetDecimalValue(dictRow["DtdPnlTotal"])
        pos = port.Position(security, holdingDirection, custodian, quantity, marketValueBook, dtdTotalPnL)
        
        return pos 
            
        
        
class SecurityLoader(BaseLoader):
    
    def __init__(self, positionFile):
        super(SecurityLoader, self).__init__(positionFile)
        pass
    

    def GetAllSecurities(self):
        try:
           
            dictReader = self.GetDictionaryReader()
                    
            #dictReader is list of dictionaries where the keys are the column headers and the values represent one row of values
            dictResults = {}
            #iterate over 
            for dictRow in dictReader:
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
                        self.AddMarketDataFromDataRow(security, dictRow)
                        dictResults[securityCode] = security
                    else:
                        security = dictResults[securityCode]
                        
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
            #we added the frequency and issue date, and eliminated issue date 1753-01-01
            frequency = dictRow["FrequencyCode"]
            if(frequency.upper() != "NULL" and frequency.upper() !='NOT SPECIFIED'): 
                security.CouponFrequency = frequency
            issueDate = dictRow["IssuedDate"]
            if(issueDate.upper() != "NULL" and issueDate.upper() != '1753-01-01'): 
                security.IssueDate = datetime.datetime.strptime(dictRow["IssuedDate"], "%m/%d/%Y").date()
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
        security.UnderlierSecurityDesc = dictRow["UnderlierSecurityDesc"]
        return security 
       
        
    
    #adds a market data to securityObject
    def AddMarketDataFromDataRow(self, security, dictRow):
        businessDate = datetime.datetime.strptime(dictRow["BusinessDate"], "%m/%d/%Y").date() 
        if not (businessDate in security.MarketData):
            mktData = md.MarketData(security.SecurityCode)
            mktData.Date = businessDate
            mktData.LastPrice = self.GetDecimalValue(dictRow["PriceLocal"])
            mktData.LastPriceBook = self.GetDecimalValue(dictRow["PriceBook"])
            mktData.UnderlyingPrice = self.GetDecimalValue(dictRow["UnderlierPriceLocal"])
            mktData.UnderlyingPriceBook = self.GetDecimalValue(dictRow["UnderlierPriceBook"])    
            mktData.Delta = self.GetDecimalValue(dictRow["Delta"])
            mktData.Beta = self.GetDecimalValue(dictRow["Beta"])
            security.MarketData[businessDate] = mktData
                
