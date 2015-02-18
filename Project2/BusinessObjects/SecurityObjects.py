'''
Bernardo Bravo-Benitez, bb2699
Chendi Ni, cn2367
Sept.19th, 2014
'''
#this module defines the classes used to represent the securities from the csv file PrtfolioAppraisal2

# define the abstract Security class, the following subclasses inherit their attributes from this class
class Security(object):      

#constructor call with all the security attributes (column headers)
    def __init__(self,IssuerDesc,SecurityCode,SecurityDesc,HoldingDirection,CustodianCode,CurrencyCode,Quantity,
                 PriceLocal,PriceBook,UnderlierPriceBook,MktValLocal,MktValBook,AvgCostLocal,AvgCostBook,CostLocal,
                 CostBook,DtdPnlTotal,MtdPnlTotal,YtdPnlTotal,NetExposure,BbergCode,BloombergMarketSectorCode,Cusip,
                 Sedol,Isin,AccrualStartDate,FrequencyCode,Coupon,IssuedDate,Maturity,Strike,ContractSize,ExcerciseType,
                 PutCall,Expiration,ExchangeCode,SecurityTypeCode,SectorDesc,GeographyRegionDesc,GicsSectorDesc): 
        
        #the following attributes are common for every type of security
        self.IssuerDesc=IssuerDesc
        self.SecurityCode=SecurityCode
        self.SecurityDesc=SecurityDesc
        self.HoldingDirection=HoldingDirection
        self.CustodianCode=CustodianCode
        self.CurrencyCode=CurrencyCode
        self.Quantity=Quantity
        self.PriceLocal=PriceLocal
        self.PriceBook=PriceBook
        self.UnderlierPriceBook=UnderlierPriceBook
        self.MktValLocal=MktValLocal
        self.MktValBook=MktValBook
        self.AvgCostLocal=AvgCostLocal
        self.AvgCostBook=AvgCostBook
        self.CostLocal=CostLocal
        self.CostBook=CostBook
        self.DtdPnlTotal=DtdPnlTotal
        self.MtdPnlTotal=MtdPnlTotal
        self.YtdPnlTotal=YtdPnlTotal
        self.NetExposure=NetExposure
        self.BbergCode=BbergCode
        self.BloombergMarketSectorCode=BloombergMarketSectorCode
        self.Cusip=Cusip
        self.Sedol=Sedol
        self.Isin=Isin
        self.AccrualStartDate=AccrualStartDate
        self.FrequencyCode=FrequencyCode
        self.Coupon=Coupon
        self.IssuedDate=IssuedDate
        self.Maturity=Maturity
        self.Strike=Strike
        self.ContractSize=ContractSize
        self.ExcerciseType=ExcerciseType
        self.PutCall=PutCall
        self.Expiration=Expiration
        self.ExchangeCode=ExchangeCode
        self.SecurityTypeCode=SecurityTypeCode
        self.SectorDesc=SectorDesc
        self.GeographyRegionDesc=GeographyRegionDesc
        self.GicsSectorDesc=GicsSectorDesc

# define Stock subclass
class Stock(Security):
    def __init__(self,IssuerDesc,SecurityCode,SecurityDesc,HoldingDirection,CustodianCode,CurrencyCode,Quantity,
                                     PriceLocal,PriceBook,UnderlierPriceBook,MktValLocal,MktValBook,AvgCostLocal,AvgCostBook,CostLocal,
                                     CostBook,DtdPnlTotal,MtdPnlTotal,YtdPnlTotal,NetExposure,BbergCode,BloombergMarketSectorCode,Cusip,
                                     Sedol,Isin,AccrualStartDate,FrequencyCode,Coupon,IssuedDate,Maturity,Strike,ContractSize,ExcerciseType,
                                     PutCall,Expiration,ExchangeCode,SecurityTypeCode,SectorDesc,GeographyRegionDesc,GicsSectorDesc):
        
        #inherit attributes from abstract class Security
        super(Stock,self).__init__(IssuerDesc,SecurityCode,SecurityDesc,HoldingDirection,CustodianCode,CurrencyCode,Quantity,
                                     PriceLocal,PriceBook,UnderlierPriceBook,MktValLocal,MktValBook,AvgCostLocal,AvgCostBook,CostLocal,
                                     CostBook,DtdPnlTotal,MtdPnlTotal,YtdPnlTotal,NetExposure,BbergCode,BloombergMarketSectorCode,Cusip,
                                     Sedol,Isin,AccrualStartDate,FrequencyCode,Coupon,IssuedDate,Maturity,Strike,ContractSize,ExcerciseType,
                                     PutCall,Expiration,ExchangeCode,SecurityTypeCode,SectorDesc,GeographyRegionDesc,GicsSectorDesc)
       
# define Bond subclass
class Bond(Security):
    def __init__(self,IssuerDesc,SecurityCode,SecurityDesc,HoldingDirection,CustodianCode,CurrencyCode,Quantity,
                                     PriceLocal,PriceBook,UnderlierPriceBook,MktValLocal,MktValBook,AvgCostLocal,AvgCostBook,CostLocal,
                                     CostBook,DtdPnlTotal,MtdPnlTotal,YtdPnlTotal,NetExposure,BbergCode,BloombergMarketSectorCode,Cusip,
                                     Sedol,Isin,AccrualStartDate,FrequencyCode,Coupon,IssuedDate,Maturity,Strike,ContractSize,ExcerciseType,
                                     PutCall,Expiration,ExchangeCode,SecurityTypeCode,SectorDesc,GeographyRegionDesc,GicsSectorDesc):
        
        #inherit attributes from abstract class Security
        super(Bond,self).__init__(IssuerDesc,SecurityCode,SecurityDesc,HoldingDirection,CustodianCode,CurrencyCode,Quantity,
                                     PriceLocal,PriceBook,UnderlierPriceBook,MktValLocal,MktValBook,AvgCostLocal,AvgCostBook,CostLocal,
                                     CostBook,DtdPnlTotal,MtdPnlTotal,YtdPnlTotal,NetExposure,BbergCode,BloombergMarketSectorCode,Cusip,
                                     Sedol,Isin,AccrualStartDate,FrequencyCode,Coupon,IssuedDate,Maturity,Strike,ContractSize,ExcerciseType,
                                     PutCall,Expiration,ExchangeCode,SecurityTypeCode,SectorDesc,GeographyRegionDesc,GicsSectorDesc)
            
# define Option subclass
class Option(Security):
    def __init__(self,IssuerDesc,SecurityCode,SecurityDesc,HoldingDirection,CustodianCode,CurrencyCode,Quantity,
                                     PriceLocal,PriceBook,UnderlierPriceBook,MktValLocal,MktValBook,AvgCostLocal,AvgCostBook,CostLocal,
                                     CostBook,DtdPnlTotal,MtdPnlTotal,YtdPnlTotal,NetExposure,BbergCode,BloombergMarketSectorCode,Cusip,
                                     Sedol,Isin,AccrualStartDate,FrequencyCode,Coupon,IssuedDate,Maturity,Strike,ContractSize,ExcerciseType,
                                     PutCall,Expiration,ExchangeCode,SecurityTypeCode,SectorDesc,GeographyRegionDesc,GicsSectorDesc):
                
        #inherit attributes from abstract class Security
        super(Option,self).__init__(IssuerDesc,SecurityCode,SecurityDesc,HoldingDirection,CustodianCode,CurrencyCode,Quantity,
                                     PriceLocal,PriceBook,UnderlierPriceBook,MktValLocal,MktValBook,AvgCostLocal,AvgCostBook,CostLocal,
                                     CostBook,DtdPnlTotal,MtdPnlTotal,YtdPnlTotal,NetExposure,BbergCode,BloombergMarketSectorCode,Cusip,
                                     Sedol,Isin,AccrualStartDate,FrequencyCode,Coupon,IssuedDate,Maturity,Strike,ContractSize,ExcerciseType,
                                     PutCall,Expiration,ExchangeCode,SecurityTypeCode,SectorDesc,GeographyRegionDesc,GicsSectorDesc)

# define OtherSecurity subclass
class OtherSecurity(Security):
    def __init__(self,IssuerDesc,SecurityCode,SecurityDesc,HoldingDirection,CustodianCode,CurrencyCode,Quantity,
                                     PriceLocal,PriceBook,UnderlierPriceBook,MktValLocal,MktValBook,AvgCostLocal,AvgCostBook,CostLocal,
                                     CostBook,DtdPnlTotal,MtdPnlTotal,YtdPnlTotal,NetExposure,BbergCode,BloombergMarketSectorCode,Cusip,
                                     Sedol,Isin,AccrualStartDate,FrequencyCode,Coupon,IssuedDate,Maturity,Strike,ContractSize,ExcerciseType,
                                     PutCall,Expiration,ExchangeCode,SecurityTypeCode,SectorDesc,GeographyRegionDesc,GicsSectorDesc):
        
        #inherit attributes from abstract class Security
        super(OtherSecurity,self).__init__(IssuerDesc,SecurityCode,SecurityDesc,HoldingDirection,CustodianCode,CurrencyCode,Quantity,
                                     PriceLocal,PriceBook,UnderlierPriceBook,MktValLocal,MktValBook,AvgCostLocal,AvgCostBook,CostLocal,
                                     CostBook,DtdPnlTotal,MtdPnlTotal,YtdPnlTotal,NetExposure,BbergCode,BloombergMarketSectorCode,Cusip,
                                     Sedol,Isin,AccrualStartDate,FrequencyCode,Coupon,IssuedDate,Maturity,Strike,ContractSize,ExcerciseType,
                                     PutCall,Expiration,ExchangeCode,SecurityTypeCode,SectorDesc,GeographyRegionDesc,GicsSectorDesc)