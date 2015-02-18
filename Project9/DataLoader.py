import pyodbc
import pandas as pd
import numpy as np
from mpl_toolkits.mplot3d import Axes3D
from matplotlib import cm
import matplotlib.pyplot as plt
from __builtin__ import isinstance

import pylab as pl

class DataLoader(object):
    ConnectionString = '''DRIVER={SQL Server};SERVER=ALAN-PC\SQLEXPRESS;DATABASE=tysql;Trusted_Connection=True'''
    
    def GetDataFrame(self,executionString):
        try:
            #open connection to DB
            cnxn = pyodbc.connect(DataLoader.ConnectionString)
            cursor = cnxn.execute(executionString)
            #column headers from the database
            col=[t[0] for t in cursor.description]
            df=pd.DataFrame(columns=col)
            #adding data rows to the data frame
            for row in cursor:
                df.loc[len(df)+1]=DataLoader.TrimUselessSpace(self, row)           
            #close the connection
            cnxn.close()
            return df
        except Exception, e:
            print "Error:", e
    
    
    #trims the annoying white spaces from strings retrieved from the database
    def TrimUselessSpace(self,row):
        lst=[]
        for i in range(len(row)):
            lst.append(row[i])
            if (isinstance(lst[i],basestring)):
                lst[i]=lst[i].strip()
        return lst       

    #creates the volatility smile surface 
    def volsurface(self,date,volframe):
        try:
            #plt.ion()
            volframe_date=volframe[volframe['Date']==date]        
            vol_filtered=volframe_date.sort_index(by=['Implied strike','Days to maturity'])
            fig = plt.figure()
            fig.suptitle(date, fontsize=14, fontweight='bold')
            
            ax = fig.gca(projection='3d')
            X=vol_filtered['Implied strike']
            Y=vol_filtered['Days to maturity']
            Z=vol_filtered['Implied vol']*100
            
            surf = ax.plot_trisurf(X, Y, Z,cmap=cm.jet)
            ax.set_xlabel('Implied strike')
            ax.set_ylabel('Days to maturity')
            ax.set_zlabel('Implied vol')
            plt.show(block=False)
            #return fig
             
        except Exception, e:
            print "Error", e
    
    
    
    def dataframeforskew(self,volframe):
        def skew(df):
            return df[df['Delta']==60]['Implied vol'].values[0]-df[df['Delta']==40]['Implied vol'].values[0]
        filteredvolframe=volframe[(volframe['Delta']==60)|(volframe['Delta']==40)][['Date','Days to maturity','Delta','Implied vol']]
        groupedvolframe=filteredvolframe.groupby(['Date','Days to maturity']).apply(skew)
        date=pd.to_datetime(np.array(zip(*groupedvolframe.index)[0]),format='%Y%m%d')
        MTD=np.array(zip(*groupedvolframe.index)[1])
        skew=np.array(groupedvolframe.values)
        df=pd.DataFrame({'Days to maturity':MTD,'Skew':skew,'Date':date})
        return df
    
    def skewplot(self,df):
        fig = plt.figure()
        fig.suptitle('Time Series Skew', fontsize=14, fontweight='bold')
        ax = fig.gca(projection='3d')
        surf = ax.plot_trisurf(df['Date'], df['Days to maturity'], df['Skew'],cmap=cm.jet)
        ax.set_xlabel('Date')
        ax.set_ylabel('Days to maturity')
        ax.set_zlabel('skew')
    
    #creates the pivot table for problem 4
    def PivotTable(self,dataframe,index):
        filtered_data=dataframe[dataframe['Underlying'].map(lambda x: x.startswith(index))]
        summary_data=filtered_data[['Underlying Stress', 'Volatility Stress','PnL']]
        return np.round(summary_data.pivot_table('PnL', index=['Underlying Stress'], columns='Volatility Stress', aggfunc=sum))