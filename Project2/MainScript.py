# Grader Comments:
# -5 Should put the main file outside the BusinessObjects module
# -2 for getting the stock number wrong
# -2 for getting the put number wrong
# -3 for insufficient comments
'''
Bernardo Bravo-Benitez, bb2699
Chendi Ni, cn2367
Sept.19th, 2014
'''
#import the csv module
import csv
#import SecurityObjects module
from SecurityObjects import Bond, Option, Stock
#import datetime module to compare dates
from datetime import datetime

class PortfolioConcentration(object):
    
    #open a comma delimited file and return the output
    '''
    This method loads the csv data into a dictionary which has the structure: {'Bond':[a list of 'Bond' objects ], 
    'Stock':[a list of 'Stock' objects], 'Option':[a list of 'Option' objects]} 
    '''
    def GetObjectList(self):
        try:
            positionsFile = None
            # raw string
            fileName = r".\PortfolioAppraisal2.csv"
            if not csv.Sniffer().has_header(fileName):
                raise Exception("headers expected in position file. FileName: " + fileName)
            positionsFile = open(fileName, 'rt')
            dictReader = csv.DictReader(positionsFile)
            #dictReader is list of dictionaries where the keys are the column headers and the values represent one row of values
            dictTag = {}
            #iterate over 
            for dictRow in dictReader:
                securitytype = dictRow['SecurityTypeCode']
                NewObject={'Bond':Bond(dictRow["IssuerDesc"],dictRow["SecurityCode"],dictRow["SecurityDesc"],dictRow["HoldingDirection"],dictRow["CustodianCode"],dictRow["CurrencyCode"],dictRow["Quantity"],dictRow["PriceLocal"],dictRow["PriceBook"],dictRow["UnderlierPriceBook"],dictRow["MktValLocal"],dictRow["MktValBook"],dictRow["AvgCostLocal"],dictRow["AvgCostBook"],dictRow["CostLocal"],dictRow["CostBook"],dictRow["DtdPnlTotal"],dictRow["MtdPnlTotal"],dictRow["YtdPnlTotal"],dictRow["NetExposure"],dictRow["BbergCode"],dictRow["BloombergMarketSectorCode"],dictRow["Cusip"],dictRow["Sedol"],dictRow["Isin"],dictRow["AccrualStartDate"],dictRow["FrequencyCode"],dictRow["Coupon"],dictRow["IssuedDate"],dictRow["Maturity"],dictRow["Strike"],dictRow["ContractSize"],dictRow["ExcerciseType"],dictRow["PutCall"],dictRow["Expiration"],dictRow["ExchangeCode"],dictRow["SecurityTypeCode"],dictRow["SectorDesc"],dictRow["GeographyRegionDesc"],dictRow["GicsSectorDesc"]),'Stock':Stock(dictRow["IssuerDesc"],dictRow["SecurityCode"],dictRow["SecurityDesc"],dictRow["HoldingDirection"],dictRow["CustodianCode"],dictRow["CurrencyCode"],dictRow["Quantity"],dictRow["PriceLocal"],dictRow["PriceBook"],dictRow["UnderlierPriceBook"],dictRow["MktValLocal"],dictRow["MktValBook"],dictRow["AvgCostLocal"],dictRow["AvgCostBook"],dictRow["CostLocal"],dictRow["CostBook"],dictRow["DtdPnlTotal"],dictRow["MtdPnlTotal"],dictRow["YtdPnlTotal"],dictRow["NetExposure"],dictRow["BbergCode"],dictRow["BloombergMarketSectorCode"],dictRow["Cusip"],dictRow["Sedol"],dictRow["Isin"],dictRow["AccrualStartDate"],dictRow["FrequencyCode"],dictRow["Coupon"],dictRow["IssuedDate"],dictRow["Maturity"],dictRow["Strike"],dictRow["ContractSize"],dictRow["ExcerciseType"],dictRow["PutCall"],dictRow["Expiration"],dictRow["ExchangeCode"],dictRow["SecurityTypeCode"],dictRow["SectorDesc"],dictRow["GeographyRegionDesc"],dictRow["GicsSectorDesc"]),'Option':Option(dictRow["IssuerDesc"],dictRow["SecurityCode"],dictRow["SecurityDesc"],dictRow["HoldingDirection"],dictRow["CustodianCode"],dictRow["CurrencyCode"],dictRow["Quantity"],dictRow["PriceLocal"],dictRow["PriceBook"],dictRow["UnderlierPriceBook"],dictRow["MktValLocal"],dictRow["MktValBook"],dictRow["AvgCostLocal"],dictRow["AvgCostBook"],dictRow["CostLocal"],dictRow["CostBook"],dictRow["DtdPnlTotal"],dictRow["MtdPnlTotal"],dictRow["YtdPnlTotal"],dictRow["NetExposure"],dictRow["BbergCode"],dictRow["BloombergMarketSectorCode"],dictRow["Cusip"],dictRow["Sedol"],dictRow["Isin"],dictRow["AccrualStartDate"],dictRow["FrequencyCode"],dictRow["Coupon"],dictRow["IssuedDate"],dictRow["Maturity"],dictRow["Strike"],dictRow["ContractSize"],dictRow["ExcerciseType"],dictRow["PutCall"],dictRow["Expiration"],dictRow["ExchangeCode"],dictRow["SecurityTypeCode"],dictRow["SectorDesc"],dictRow["GeographyRegionDesc"],dictRow["GicsSectorDesc"])}[securitytype]
                #need to cast to float
                if(dictTag.has_key(securitytype)):
                    dictTag[securitytype].append(NewObject)
                else:
                    dictTag[securitytype] = [NewObject]
            return dictTag
        except Exception, e:
            print e
            raise e
        finally:
            #print 'Finalizer called'
            if positionsFile != None :
                positionsFile.close()
    
    def Count(self,ObjList,tag1,tag2):
        '''
        This method counts the number of distinct certain securities
        tag1: security type column header,
        tag2: security name column header
        example:
        for problem(a) one should put tag1 as 'Bond' and tag2 as 'SecurityDesc'
        '''
        try:
            keylist=[]
            for Obj in ObjList[tag1]:
                if not getattr(Obj,tag2) in keylist:
                    keylist.append(getattr(Obj,tag2))
            return len(keylist)
        except Exception,e:
            print e
    
    def TagCount(self,ObjList,tag1, tag2, tagvalue):
        '''
        This method counts the number of certain securities that has certain values
        tag1: security type column header,
        tag2: the column header of the target attribute
        tagvalue: the target value of the target attribute
        example:
        for problem(b) one should put tag1 as 'Option' and tag2 as 'PutCall' and tagvalue as 'C'
        '''
        try:
            count=0
            for Obj in ObjList[tag1]:
                if getattr(Obj, tag2)==tagvalue:
                    count=count+1
            return count
        except Exception,e:    
            print e

    def DistinctTagCount(self,ObjList,tag1, tag2, tagvalue,tag3):
        '''
        This method counts the number of certain distinct securities that has certain values(which does not count duplicated securities)
        tag1: security type column header,
        tag2: the column header of the target attribute
        tagvalue: the target value of the target attribute
        tag3: tag for distinction use
        example:
        for problem(d) one should put tag1 as 'Bond', tag2 as 'SectorDesc', tagvalue as 'Health Care' and tag3 as "SecurityDesc"
        '''
        try:
            count=0
            keylist=[]
            for Obj in ObjList[tag1]:
                if getattr(Obj, tag2)==tagvalue:
                    if not getattr(Obj,tag3) in keylist:
                        count=count+1
                        keylist.append(getattr(Obj,tag3))
            return count
        except Exception,e:    
            print e
    
    def GetMax(self,ObjList,tag1,tag2,taginfo):
        '''
        This method finds the maximum of certain attribute of certain securities
        tag1: security type column header,
        tag2: the column header of the target attribute
        taginfo: the column header of the the name of the target attribute
        example:
        for problem(c) one should put tag1 as 'Bond' and tag2 as 'Maturity' and taginfo as 'SecurityDesc'
        '''
        try:
            #to compare 2 string-type dates we imported datetime method in datetime module that converts strings into date objects so that they can be compared
            if tag2=='Maturity':
                ansdict={}
                for Obj in ObjList[tag1]:
                    if getattr(Obj,tag2)=='NULL':
                        continue
                    if not bool(ansdict):
                        ansdict[tag2]=[getattr(Obj,tag2),getattr(Obj,taginfo)]
                    else:
                        if datetime.strptime(getattr(Obj,tag2),"%m/%d/%Y")>datetime.strptime(ansdict[tag2][0],"%m/%d/%Y"):
                            ansdict[tag2]=[getattr(Obj,tag2),getattr(Obj,taginfo)]
            else:
                ansdict={}
                for Obj in ObjList[tag1]:
                    if not bool(ansdict):
                        ansdict[tag2]=[getattr(Obj,tag2),getattr(Obj,taginfo)]
                    else:
                        if getattr(Obj,tag2)>ansdict['tag2'][0]:
                            ansdict[tag2]=[getattr(Obj,tag2),getattr(Obj,taginfo)]
            return ansdict
        except Exception,e:
                print e    
try:
    newtest=PortfolioConcentration()
    print('Problem(a):')
    print('Number of distinct bonds:'+str(newtest.Count(newtest.GetObjectList(), 'Bond','SecurityDesc')))
    print('Number of distinct stocks:'+str(newtest.Count(newtest.GetObjectList(), 'Stock','SecurityDesc')))
    print('Number of distinct options:'+str(newtest.Count(newtest.GetObjectList(), 'Option','SecurityDesc')))
    print('Problem(b):')
    print('Call Option Numbers:'+str(newtest.TagCount(newtest.GetObjectList(), 'Option','PutCall','C')))
    print('Put Option Numbers:'+str(newtest.TagCount(newtest.GetObjectList(), 'Option','PutCall','P')))
    print('Problem(c):')
    attrlist=newtest.GetMax(newtest.GetObjectList(), 'Bond', 'Maturity', 'SecurityDesc')['Maturity']
    print('Bond with the farthest maturity date and its maturity date:')
    print(attrlist[1]+', '+attrlist[0])
    print('Problem(d):')
    print('Number of securities in the portfolio belong to the Health Care sector:'+str(newtest.DistinctTagCount(newtest.GetObjectList(), 'Bond','SectorDesc','Health Care','SecurityDesc')+newtest.DistinctTagCount(newtest.GetObjectList(), 'Stock','SectorDesc','Health Care','SecurityDesc')+newtest.DistinctTagCount(newtest.GetObjectList(), 'Option','SectorDesc','Health Care','SecurityDesc')))    #print type(newtest.GetObjectList()['Bond'][0].Maturity)
    
except Exception, e:
    print e    