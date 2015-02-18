import DataLoader as DL
import pandas as pd
import matplotlib.pyplot as plt
import MovieAnalyzer as MA

if __name__=='__main__':
    try:

        dataLoader=DL.DataLoader()
        #Problem 1(a): create data frames from database
        customers=dataLoader.GetDataFrame('SELECT * FROM Customers')
        orderitems=dataLoader.GetDataFrame('SELECT * FROM OrderItems')
        orders=dataLoader.GetDataFrame('SELECT * FROM Orders')
        products=dataLoader.GetDataFrame('SELECT * FROM products')
        vendors=dataLoader.GetDataFrame('SELECT * FROM Vendors')
        
        #Problem 1(b): simulates SQL in Python
        print "Problem 1(b):"
        
        DF=pd.DataFrame(columns=['cust_id','cust_name','vend_id','vend_name','total_business'])
        for cust_id in customers['cust_id']:
            cust_name=customers[customers['cust_id']==cust_id]['cust_name'].values[0]
            order_num_list=orders[orders['cust_id']==cust_id]['order_num']
            for order_num in order_num_list:
                tempFrame=orderitems[orderitems['order_num']==order_num]
                for prod_id in tempFrame['prod_id']:
                    #print tempFrame[tempFrame['prod_id']==prod_id]['item_price'].values[0]
                    productBusiness=tempFrame[tempFrame['prod_id']==prod_id]['item_price'].values[0]*tempFrame[tempFrame['prod_id']==prod_id]['quantity'].values[0]
                    for vend_id in products[products['prod_id']==prod_id]['vend_id']:
                        vend_name=vendors[vendors['vend_id']==vend_id]['vend_name'].values[0]
                        newDataRow=[cust_id,cust_name,vend_id,vend_name,productBusiness]
                        #bool matrix to verify whether the current combination of cust_id,vend_id is alreay in the data frame
                        boolMatrix=(DF['cust_id']==cust_id)&(DF['cust_name']==cust_name)&(DF['vend_id']==vend_id)&(DF['vend_name']==vend_name)
                        if not DF[boolMatrix].empty:
                            #get the row index first for future updating of total_business 
                            idx=DF[boolMatrix].index.values[0]
                            DF.ix[idx,'total_business']=DF.ix[idx,'total_business']+productBusiness
                        else:
                            DF.loc[len(DF)+1]=newDataRow
        df=DF.sort('total_business', ascending=False).drop(['cust_id','vend_id'],axis=1)
        print df
                            
        #Problem 2(a)
        volframe = pd.read_csv('Volsurface.csv')
        
        #Problem 2(b)
        date=20060504
        print "\nProblem 2: Plot for day:", date
        dataLoader.volsurface(date,volframe)
        
        #Problem 3
        #Look at the modified Excel spreadsheet for details on the following calculations
        print "\nProblem 3(c):"
        print "The delta-gamma-vega approximation:\nPnL=$Delta*pricemove + $Gamma*pricemove^2 + vega * volatilitymove = (-17485)*0.02 + (-458145)*0.02^2 + (-3808)*(-5)\n yields PnL of 18,507"     
        print "The actual PnL computed from Excel pivot table is 18,846"
        print "We notice that the estimation is fairly accurate"
        
        print "\nProblem 3(d):"
        print "Similarly, the delta-gamma-vega approximation yields PnL of 16,257"  
        print "The actual PnL computed from Excel pivot table is 17,546"
        print "We notice that the estimation is accurate locally, i.e. it's useful only for small perturbations."
        print "In this case we are introducing large variations in our variables. Therefore the taylor expansion is no longer so accurate yet still ok."
        
        #Problem 4
        print "\nProblem 4:"
        StressData=pd.read_csv('StressData.csv')
        UnderlyingIndex='SPX Index'
        pivot= dataLoader.PivotTable(StressData,UnderlyingIndex)
        print pivot
                
        #Problem 5(a)
        df=dataLoader.dataframeforskew(volframe)
        print "\nProblem 5:"
        print df
        #Problem 5(b)
        #As the scale of data is big it might take some time to load the figure
        #The x-axis is really annoying. I cannot find a nice way to format the x-axis of dates.
        dataLoader.skewplot(df)
        
        #Problem 6
        #As the data scale is relatively big it might take some time to display the result.
        n=2
        df=MA.MovieAnalyzer().topMovie(n)
        print "\nProblem 6:"
        print df
        
        #this was placed here so the graph window wouldn't close
        plt.show()
                        
    except Exception, e:
        print "Error", e
        