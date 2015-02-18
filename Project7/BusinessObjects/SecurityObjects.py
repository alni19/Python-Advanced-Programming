
import datetime
import abc


# a neat trick to work around the lack of enums in Python
def enum(**enums):
    return type('Enum', (), enums)


#define enums for security types
SecurityType = enum(Unknown = "Unknown", Stock = "Stock", Option = "Option", Bond = "Bond",  Other = "Other")


#define enums for OptionType    
PutCall = enum(Unknown= "Unknown", Call = "C", Put = "P")

#define enums for ExcerciseType 
ExcerciseType = enum(Unknown= "Unknown", American = 'American', European = 'European')

#define enums for CouponFrequency
CouponFrequencyType = enum(Unknown = "Unknown", Annual = "Annual", SemiAnnual = "Semi Annual", Quarterly = "Quarterly", Monthly = "Monthly", Weekly = "Weekly", Daily = "Daily")

#define enums for Future SettlementType


           

#define an issuer class
class Issuer (object):    
    def __init__(self, issuerCode, issuerName):
        self.IssuerCode = issuerCode
        self.IssuerName = issuerName
        


class Security(object):
    'Abstract Base class for Security Objects'
    
    __metaclass__ = abc.ABCMeta

    #lets prevent instantiating this abstract class
    @abc.abstractmethod
    def __init__(self, issuer, securityCode, securityDesc, currencyCode, exchangeCode, secType):
        self.SecurityType = SecurityType.Unknown
        self.Issuer = issuer
        self.SecurityCode = securityCode
        self.SecurityDesc = securityDesc
        self.CurrencyCode = currencyCode
        self.ExchangeCode = exchangeCode
        self.SecurityType = secType
        self.BbergCode = ""
        self.BloombergMarketSectorCode = ""
        self.Cusip = ""
        self.Isin = ""
        self.Sedol = ""   
        self.SectorDesc = ""  
        self.GeographyRegionDesc = ""    
        self.GicsSectorDesc = ""
        
        #a dictionary of Market data objects for each day
        self.MarketData = {} 

    @abc.abstractmethod
    def GetExposure(self):
        raise Exception("Not implemented")
        
#define a class to represent Stock security
class Stock(Security):
    
    'Represents a Stock class'
    def __init__ (self, issuer, securityCode, securityDesc, currencyCode, exchangeCode, secType):
        super(Stock, self).__init__(issuer, securityCode, securityDesc, currencyCode, exchangeCode, secType)
        #initialize your member variables in the constructor. Good practice
        self.SecurityType = SecurityType.Stock
        
    def GetExposure(self):
        return self.MarketData.LastPriceBook  
        
        
#define a class to represent Option security        
class Option(Security):
    
    'Represents a Option class'
    
    
    def __init__ (self, issuer, securityCode, securityDesc, currencyCode, exchangeCode, secType):
        super(Option, self).__init__(issuer, securityCode, securityDesc, currencyCode, exchangeCode, secType)
        #initialize your member variables in the constructor. Good practice
        self.SecurityType = SecurityType.Option
        
        self.Strike = 0.0
        self.PutCall = PutCall.Unknown
        self.ExpirationDate = datetime.datetime.strptime("1/1/1900", "%m/%d/%Y").date()
        self.OptionType = ExcerciseType.Unknown #American/European
        self.ContractSize = 100 #default to 100
        
        self.UnderlierSecurityDesc = ''
        
    def GetExposure(self):
        return self.MarketData.UnderlyingPriceBook * self.ContractSize * self.MarketData.Delta 
        
 #define a class to represent Bond security       
class Bond(Security):
    
    'Represents a Bond class'
    
    def __init__ (self, issuer, securityCode, securityDesc, currencyCode, exchangeCode, secType): 
        super(Bond, self).__init__(issuer, securityCode, securityDesc, currencyCode, exchangeCode, secType)
        self.SecurityType = SecurityType.Bond
        
        self.Coupon = 0
        self.CouponFrequency = CouponFrequencyType.Unknown
        self.Maturity = datetime.datetime.strptime("1/1/1900", "%m/%d/%Y").date()
        self.IssueDate = datetime.datetime.strptime("1/1/1900", "%m/%d/%Y").date()
        self.IssuePrice = 0.0

    def GetExposure(self):
        return self.MarketData.LastPriceBook  


#define a catch all OtherSecurity
class OtherSecurity(Security):
    def __init__ (self, issuer, securityCode, securityDesc, currencyCode, exchangeCode, secType): 
        super(OtherSecurity, self).__init__(issuer, securityCode, currencyCode, exchangeCode, securityDesc, secType) 
        self.SecurityType = SecurityType.Other
        
    def GetExposure(self):
        return 1 

