import csv
from DataProcessor import DataProcessor as DP
                
if (__name__=="__main__"):
    try:
        #Reads BBG codes from Research.csv
        bbergCodes=[]
        with open("Research.csv","rb") as csvfile:
            linereader=csv.reader(csvfile,delimiter=',')
            for row in linereader:
                bbergCodes.append(row[0])   
        fields = ["TICKER",	"SECURITY_TYP",	"SECURITY_TYP2",	"ID_CUSIP",	"ID_ISIN",	"ID_SEDOL1",	"CRNCY",	"ISSUER",	"UNDERLYING_SECURITY_DES",	"OPT_STRIKE_PX",	"OPT_CONT_SIZE_REAL",	"OPT_EXPIRE_DT",	"OPT_PUT_CALL",	"OPT_EXER_TYP",	"OCC_SYMBOL",	"OPRA_SYMBOL",	"MATURITY",	"CPN",	"CPN_TYP",	"CPN_FREQ",	"DAY_CNT_DES",	"MARKET_SECTOR_DES"]
        fields2=["PX_LAST",	"PX_VOLUME",	"CUR_MKT_CAP",	"DELTA",	"GAMMA",	"VEGA",	"THETA",	"YLD_YTM_MID",	"YLD_CUR_MID"]
               
        #DataWriter instance
        dw=DP.DataWriter(bbergCodes,fields,fields2)
        #write reference data
        #problem 3(a)
        dw.referenceDataWriter()
        #write historical data
        #problem 3(b)
        dw.historicalDataWriter()
        #problem 4
        print "Problem 4:"
        print dw.betaRetriever("EQY_BETA_6M",None)
        #problem 5
        startDate = "20131001"
        endDate = "20131031"
        overridesDict={"BETA_OVERRIDE_START_DT":startDate,"BETA_OVERRIDE_END_DT":endDate}
        print "Problem 5:"
        print dw.betaRetriever("BETA_ADJ_OVERRIDABLE",overridesDict)

    except Exception,e:
        print ("Error:"+str(e))
            

        
