from BBG import BBGAccess as BBGModule
import csv

class DataWriter():
    #initialzer
    def __init__(self,bbgcode,fields,fields2):
        self.bbgcode=bbgcode
        #fields stands for the fields of nmemonics for reference data
        self.fields=fields
        #fields stands for the fields of nmemonics for historical data
        self.fields2=fields2

    #writes reference data into csv file    
    def referenceDataWriter(self):
        dictResults = BBGModule.BBGAccess().GetCurrentData(self.bbgcode, self.fields, None)
        with open("Reference Data.csv",'wb') as csvfile:
            datawriter=csv.writer(csvfile,delimiter=',')
            datawriter.writerow(["SECURITY","TICKER",	"SECURITY_TYP",	"SECURITY_TYP2",	"ID_CUSIP",	"ID_ISIN",	"ID_SEDOL1",	"CRNCY",	"ISSUER",	"UNDERLYING_SECURITY_DES",	"OPT_STRIKE_PX",	"OPT_CONT_SIZE_REAL",	"OPT_EXPIRE_DT",	"OPT_PUT_CALL",	"OPT_EXER_TYP",	"OCC_SYMBOL",	"OPRA_SYMBOL",	"MATURITY",	"CPN",	"CPN_TYP",	"CPN_FREQ",	"DAY_CNT_DES",	"MARKET_SECTOR_DES"])
            for symbol in dictResults:
                lst=[symbol];
                for nametag in self.fields:
                    if dictResults[symbol].has_key(nametag):
                        lst.append(dictResults[symbol][nametag])
                    else:
                        lst.append("NULL")
                datawriter.writerow(lst)

    #writes historical data into csv file            
    def historicalDataWriter(self):
        dictResults = BBGModule.BBGAccess().GetHistoricalData("20131001", "20131031", self.bbgcode, self.fields2, None)
        with open("Historical Data.csv",'wb') as csvfile:
            datawriter=csv.writer(csvfile,delimiter=',')
            datawriter.writerow(["DATE" , "SECURITY" , "PX_LAST", "PX_VOLUME",	"CUR_MKT_CAP",	"DELTA",	"GAMMA",	"VEGA",	"THETA",	"YLD_YTM_MID",	"YLD_CUR_MID"])
            for symbol in dictResults:
                for date in dictResults[symbol]:
                    lst=[date,symbol]
                    for nametag in self.fields2:
                        if dictResults[symbol][date].has_key(nametag):
                            lst.append(dictResults[symbol][date][nametag])
                        else:
                            lst.append("NULL")
                    datawriter.writerow(lst)

    #returns a dictionary of securities and corresponding betas(6 month beta or overridable beta for a certain time period)
    def betaRetriever(self,betatypecode,overriderDict):
        dictResults = BBGModule.BBGAccess().GetCurrentData(self.bbgcode, ["SECURITY_TYP","UNDERLYING_SECURITY_DES",betatypecode], overriderDict)
        displaydict={}
        for symbol in dictResults:
            if dictResults[symbol]["SECURITY_TYP"]=="Common Stock":
                if  dictResults[symbol].has_key(betatypecode):
                    displaydict[symbol] = dictResults[symbol][betatypecode]
                else:
                    displaydict[symbol]="Data Not Available"
            elif dictResults[symbol]["SECURITY_TYP"]=="Equity Option":
                if dictResults[symbol]["UNDERLYING_SECURITY_DES"] in self.bbgcode:
                    if dictResults[dictResults[symbol]["UNDERLYING_SECURITY_DES"]].has_key(betatypecode):
                        displaydict[symbol] = dictResults[dictResults[symbol]["UNDERLYING_SECURITY_DES"]][betatypecode]
                    else:
                        displaydict[symbol]="Data Not Available"
                else:
                    newdictResults = BBGModule.BBGAccess().GetCurrentData([dictResults[symbol]["UNDERLYING_SECURITY_DES"]], [betatypecode], overriderDict)
                    for syml in newdictResults:
                        if newdictResults[syml].has_key(betatypecode):
                            displaydict[symbol] = newdictResults[syml][betatypecode]
                        else:
                            displaydict[symbol] = "NULL"
        return displaydict
