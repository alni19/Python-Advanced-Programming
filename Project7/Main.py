import pyodbc
import DataLoaders as DL

class ODBCSample(object):
    fileName = "PortfolioAppraisal4.csv"
    #Security data loaded from csv file into a dictionary
    SecurityDict = DL.SecurityLoader(fileName).GetAllSecurities()
    #Portfolio data(including position data, market data) loaded from csv file into a list
    PortfolioList = DL.PortfolioLoader(fileName).GetAllPositionsTimeSeries()
    #We changed the ConnectionString according to our needs, you should change the server name to your local sql server name
    #ConnectionString is a static variable
    ConnectionString = '''DRIVER={SQL Server};SERVER=ALAN-PC\SQLEXPRESS;DATABASE=Assignment6_2014;Trusted_Connection=True'''
       
    def insertSecuritData(self):
    #actually inserts security and issuer at the same time as the stored procedure InsertSecurity does both things...
        try:
            cnxn = pyodbc.connect(ODBCSample.ConnectionString)
         
            #fetches data from iterating through SecurityDict
            for key,security in ODBCSample.SecurityDict.iteritems() :
                securityCode =  security.SecurityCode
                securityDesc = security.SecurityDesc
                securityTypeCode = security.SecurityType
                issuerDesc = security.Issuer.IssuerName
                exchangeCode = security.ExchangeCode
                currencyCode = security.CurrencyCode
                cusip = security.Cusip
                isin = security.Isin
                sedol  = security.Sedol
                BbergCode = security.BbergCode
                bloombergMarketSectorCode = security.BloombergMarketSectorCode
                sectorDesc = security.SectorDesc
                geographyRegion= security.GeographyRegionDesc
                if (securityTypeCode == "Option"):
                    StrikePrice = security.Strike
                    AE = security.OptionType
                    PC = security.PutCall
                    Expiration = str(security.ExpirationDate)
                    contractSize = security.ContractSize
                else:
                    StrikePrice = None
                    AE = None
                    PC = None
                    Expiration = None
                    contractSize = None
                    
                if (securityTypeCode == "Bond"):
                    bondCoupon = security.Coupon
                    bondFrequency = security.CouponFrequency
                    bondMaturity = str(security.Maturity)
                    bondIssueDate = str(security.IssueDate)
                    bondIssuePrice = security.IssuePrice
                    couponType = None
                else:
                    bondCoupon = None
                    couponType = None
                    bondFrequency = None
                    bondMaturity = None
                    bondIssueDate = None
                    bondIssuePrice = None
                #invoke stored procedure InsertSecurity
                cursor = cnxn.execute("""exec InsertSecurity 
                        @securityCode=?,@securityDesc=?,@securityTypeCode= ?,@issuerDesc=?,@exchangeCode=?,@currencyCode= ?,
                        @cusip=?,@isin=?,@sedol = ?,@bbergCode=?,@bbergMarketSectorCode= ?,@strike=?,@pc=?,@expiration= ?,
                        @AE=?,@contractSize= ?,@couponTypeCode= ?,@coupon=?,@couponFrequencyCode=?,@maturity=?,
                        @issueDate=?,@issuePrice=?,@riskCurrencyCode =?,@geographyRegionDesc= ?,@sectorDesc=? """, 
                        (securityCode,securityDesc,securityTypeCode,issuerDesc,exchangeCode,currencyCode,cusip,isin,sedol,BbergCode,bloombergMarketSectorCode ,StrikePrice ,PC,Expiration,AE,contractSize,couponType,bondCoupon,bondFrequency,bondMaturity,bondIssueDate,bondIssuePrice,'USD',geographyRegion,sectorDesc))
                cnxn.commit()
            cnxn.close()
        except Exception, e:
            print "Error", e
    
    def insertMarketData(self):
    #inserts market data
        try:
            cnxn = pyodbc.connect(ODBCSample.ConnectionString)
            for key1, security in ODBCSample.SecurityDict.iteritems() :
                    for key2, mktdata in security.MarketData.iteritems():
                        securityCode =  mktdata.SecurityCode
                        businessDate = str(mktdata.Date)
                        lastPrice = mktdata.LastPrice
                        underlyingPrice = mktdata.UnderlyingPrice
                        underlyingPriceBook = mktdata.UnderlyingPriceBook
                        beta = mktdata.Beta
                        delta = mktdata.Delta
                        gamma = mktdata.Gamma
                        theta = mktdata.Theta
                        vega = mktdata.Vega
                        avgdailyvolume = mktdata.AvgDailyVolume
                        marketCap = mktdata.MarketCap
                        #call stored procedure
                        cursor = cnxn.execute("""exec InsertMarketData 
                                @securityCode =?,@businessDate =?,@lastPrice =?,@UnderlyingPrice =?,
                                @UnderlyingPriceBook =?,@Beta =?, @delta =?,@gamma =?,@theta =?,
                                @vega =?,@tradingVolume =?,@marketCap =? """,
                                (securityCode,businessDate,lastPrice,underlyingPrice,underlyingPriceBook,beta,delta,gamma,theta,vega,avgdailyvolume,marketCap))
                        cnxn.commit()
            cnxn.close()
        except Exception, e:
            print "Error", e
            
    def insertPositionData(self):
    #inserts position data    
        try:
            cnxn = pyodbc.connect(ODBCSample.ConnectionString)
            for value in ODBCSample.PortfolioList :
                securityCode =  value.SecurityCode
                portfolioCode = 'ABC Capital'
                positionDirection = value.HoldingDirection
                custodianCode = value.Custodian
                businessDate = str(value.Date)
                quantity = value.Quantity
                baseMarketValue = value.MarketValueBook
                dayTotalPnLBase = value.DayTotalPnLBook
                avgCostLocal = value.AvgCostLocal
                avgCostBase  = value.AvgCostBook
                mktValueLocal = value.MktValueLocal
                dtdPnlLocal = value.dayPnLLocal
                dayFXPnLBase = 1 #no such variable in position object, set it to be 1
                cursor = cnxn.execute("""exec InsertPositionData 
                        @securityCode =?, @portfolioCode =?, @positionDirection =?,@custodianCode =?,@businessDate =?,
                        @quantity =?,@marketValueBase =?,@dayTotalPnLBase =?,@averageCostLocal =?,@averageCostBase =?,
                        @marketValueLocal =?,@dayPnLLocal =?,@dayFXPnLBase =? """, 
                        (securityCode,portfolioCode,positionDirection,custodianCode,businessDate,quantity,baseMarketValue,dayTotalPnLBase,avgCostLocal,avgCostBase,mktValueLocal,dtdPnlLocal,dayFXPnLBase))
                cnxn.commit()
            cnxn.close()
        except Exception, e:
            print "Error", e
    
#Application part    
try:
    odbcSample = ODBCSample()
    #Calls 3 inserting methods
    odbcSample.insertSecurityData()
    odbcSample.insertPositionData()
    odbcSample.insertMarketData()
except Exception, e:
    print "Error", e    
