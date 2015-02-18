# -15. Still don't have correct github folder structure as there are no project files.
#Otherwise a good job. 85/100.

# Revised grade 95. folder structure: 1 and only 1 .project file in assignment root directory. 
# Each assignment is a folder under that single project.

from ArrayLoader import ArrayLoader
from CalculationToolbox import CalculationTool
import matplotlib.pyplot as plt
from datetime import datetime
from matplotlib.ticker import Formatter
try:
    filename1='StockAssessment\GOOG.csv'
    filename2='StockAssessment\SPX.csv'
       
    #Question 1(a):
    #parses returns of GOOG
    retrn_goog=ArrayLoader(filename1).getcolumndata(3)
    #parses returns of SPX
    retrn_spx=ArrayLoader(filename2).getcolumndata(3)
    
    #Question 1(b):calculates GOOG's beta relative to SPX
    cal=CalculationTool()
    print 'Question 1(b): Beta = '+str(cal.beta(retrn_goog,retrn_spx))
    
    #Question 1(c):
    #gets dates in the form of ndarray
    datenplist=ArrayLoader(filename1).getcolumndata(1,'str')
    #get a list of date objects for future use
    datelist=[]
    for i in range(len(datenplist)):
        datelist.append(datetime.strptime(datenplist[i], "%m/%d/%Y").date())
    #get prices
    price_goog=ArrayLoader(filename1).getcolumndata(2)
    price_spx=ArrayLoader(filename2).getcolumndata(2)
    #use a formatter to make market open dates consecutive. I borrowed some codes from the matplotlib gallery.
    class MyFormatter(Formatter):
        def __init__(self, dates, fmt='%Y-%m-%d'):
            self.dates = dates
            self.fmt = fmt

        def __call__(self, x, pos=0):
            'Return the label for time x at position pos'
            ind = int(round(x))
            if ind>=len(self.dates) or ind<0: return ''

            return self.dates[ind].strftime(self.fmt)
    print datelist
    formatter = MyFormatter(datelist)
    fig, ax = plt.subplots()
    ax2=ax.twinx()
    ax.xaxis.set_major_formatter(formatter)
    lns1=ax.plot(price_goog, 'ro-',label='GOOG')
    ax.set_ylabel(r"Google stock price")
    lns2=ax2.plot(price_spx, 'bo-',label='SPX')
    ax2.set_ylabel(r"S&P500 Index")
    lns=lns1+lns2
    labs=[l.get_label() for l in lns]
    ax2.legend(lns,labs,loc=0)
    fig.autofmt_xdate()
    #grid on
    ax.xaxis.grid(True, which='major') # `which` can be 'minor', 'major', or 'both'
    ax.yaxis.grid(True, which='major')
    plt.show()
   
except Exception,e:
    print e
