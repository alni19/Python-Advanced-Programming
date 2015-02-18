#import the csv module
import csv

class PortfolioConcentration(object):
    
    #open a comma delimited file and return the output
    #I wrote this function so that it takes any column and returns the sum of market value by that column    
    def GetMeasureTotalBySlice(self, slice, measure):
        try:
            positionsFile = None
            # raw string
            fileName = r".\PortfolioAppraisalReport.csv"
            if not csv.Sniffer().has_header(fileName):
                raise Exception("headers expected in position file. FileName: " + fileName)
            positionsFile = open(fileName, 'rt')
            dictReader = csv.DictReader(positionsFile)
            #dictReader is list of dictionaries where the keys are the column headers and the values represent one row of values
             
            dictTag = {}
            #iterate over 
            for dictRow in dictReader:
                mv = dictRow[measure]
                strat = dictRow[slice]
                #need to cast to float
                if(dictTag.has_key(strat)):
                    dictTag[strat] += float(mv)
                else:
                    dictTag[strat] = float(mv)
            return dictTag
        except Exception, e:
            print e
            raise e
        finally:
            #print 'Finalizer called'
            if positionsFile != None :
                positionsFile.close()
    
    #This function accepts the dictionary and return that max and the min value in the dictionary
    def GetTopandBottomSlices(self, sliceData):
        
        try:
                        
            #we create lists with the values and the keys of the dictionary
            values=list(sliceData.values())
            keys=list(sliceData.keys())
            
            #we get the index of the max values in the list 
            index_max=values.index(max(values))
            #we get the key and value associated to the index obtained above
            max_key=keys[index_max]
            max_value=values[index_max]
            
            #we perform an analogous procedure to get the min
            index_min=values.index(min(values))
            min_key=keys[index_min]
            min_value=values[index_min]
            
            #the function returns the top and bottom values as well as the keys associated to such values
            return [max_key, max_value, min_key, min_value]                     
                                   
        except Exception, e:
            print e
            raise e
                            
try:
    
    #what is the security corresponding to the biggest short position of the firm?
    slice = "SecurityDesc"
    measure = "BaseMarketValue"
    portfolioConcentration = PortfolioConcentration()
    sliceData = portfolioConcentration.GetMeasureTotalBySlice(slice, measure)
    [max_key, max_value, min_key, min_value] = portfolioConcentration.GetTopandBottomSlices(sliceData)
    print('\nThe Security associated to the biggest short position is: %s \nWith a position of: %d') %(min_key,min_value)
    
    #Which Strategies are the top and bottom performers this year?     
    slice = "StrategyDesc"
    measure = "YTDTotalPnL"
    portfolioConcentration = PortfolioConcentration()
    sliceData = portfolioConcentration.GetMeasureTotalBySlice(slice, measure)
    [max_key, max_value, min_key, min_value] = portfolioConcentration.GetTopandBottomSlices(sliceData)
    print('\nThe top performer strategy for this year is: %s \nWith a profit of: %d') %(max_key,max_value)
    print('The bottom performer strategy for this year is: %s \nWith a loss of: %d')  %(min_key,min_value)
    
    #Which AssetTypes are the top and bottom performers this year?
    slice="SecurityTypeDesc"
    portfolioConcentration = PortfolioConcentration()
    sliceData = portfolioConcentration.GetMeasureTotalBySlice(slice, measure)
    [max_key, max_value, min_key, min_value] = portfolioConcentration.GetTopandBottomSlices(sliceData)
    print('\nThe top performer security type for this year is: %s \nWith a profit of: %d') %(max_key,max_value)
    print('The bottom performer security type for this year is: %s \nWith a loss of: %d') %(min_key,min_value)
    
    
except Exception, e:
    print e    
    