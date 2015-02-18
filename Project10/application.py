import pyodbc
import pandas as pd
import pandas.io.sql as sql
import datetime

#Decorator Tracer
def Tracer(f):
    def new_f(*args, **kwargs):
        #timing
        t1 = datetime.datetime.now()
        print "calling function " + f.__name__ + "@ " + str(t1)
        result = f(*args, **kwargs)
        t2 = datetime.datetime.now()
        print "running time: " + str(t2-t1)
        return result
    new_f.__name = f.__name__
    new_f.__doc__ = f.__doc__
    return new_f


class PnlCalculation(object): 
    def __init__(self,connectString):
        self.ConnectionString = connectString 

    @Tracer
    def GetSPXDataFrame(self,startDate,endDate):
        #startDate should be like date in code exec GetSPXMarkValDPnL '1/1/2012','1/31/2012'
        try:
            # connect the database
            cnxn = pyodbc.connect(self.ConnectionString)
            # get the data frame by calling stored proc
            SPXFrame = sql.read_sql("exec GetSPXMarkValDPnL " + "'" + startDate+"'," + "'" + endDate + "'",cnxn)
            cnxn.close()
            return SPXFrame
        
        except Exception, e:
            print "Error", e

    @Tracer
    def GetSecurityDataFrame(self,securityCode,startDate,endDate):#startDate should be like date in code exec GetSPXMarkValDPnL '1/1/2012','1/31/2012'
        try:
            # connect the database
            cnxn = pyodbc.connect(self.ConnectionString)
            # get the data frame by calling stored proc
            SecurityFrame = sql.read_sql("exec GetSecurityMarkValDPnL " +"'"+securityCode +"','" + startDate+"'," + "'" + endDate + "'",cnxn)
            cnxn.close()
            return SecurityFrame 
        
        except Exception, e:
            print "Error", e

    @Tracer
    def PnLCalculation(self,securityCode,startDate,endDate):
        #Time series data for SPX
        spxDF = self.GetSPXDataFrame(startdate, enddate)
        spxDF.columns=['Code','BusinessDate','SPXPnl']
        #Time series data for securities
        secDF=self.GetSecurityDataFrame(securitycode, startdate, enddate)
        secDF.columns=['SecurityCode','BusinessDate','SecurityPnl','MKTValue']
        #Joined Data Frame
        DF=pd.merge(spxDF, secDF, how='inner', on='BusinessDate')
        DF['BetaPnl'] = DF.MKTValue*DF.SPXPnl/100
        betapnl = sum(DF['BetaPnl'])
        print 'The Pnl for '+securitycode+' from '+startdate+' to '+enddate+' is:'  
        print 'Beta Pnl:'
        print betapnl
        print 'Alpha Pnl:'
        print sum(DF['SecurityPnl'])-betapnl


if __name__ == '__main__':
    
    try:    
        #Please change SERVER name to your SQL server name. 
        #Please do not forget to execute the stored procedure file before running the Python code
        connectString = "DRIVER={SQL Server};SERVER=ALAN-PC\SQLEXPRESS;DATABASE=Assignment9"
        #Parameters
        securitycode="GOOG"
        startdate="01/01/2012"
        enddate="05/01/2012"
        #Parameters end
        PnlCalc = PnlCalculation(connectString)
        PnlCalc.PnLCalculation(securitycode,startdate, enddate)

    except Exception, e:
        print "An error ocurred: ", e