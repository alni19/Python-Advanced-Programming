'''
Bernardo Bravo-Benitez, bb2699
Chendi Ni, cn2367
Oct, 2014
'''

import numpy as np
#from scipy import stats
from scipy.stats import norm

#To make this assignment 'OOP-Pythonic' we define the BlackScholes class, its methods help us to calculate the prices and Greeks
class BlackScholes(object):
    def __init__(self):
        pass
    
    #We define a method that will calculate the prices and greeks vectors, for a portfolio of options
    #The inputs are vectors, ordered as follows:
    #AssetPrice(S),Strike(K),Maturity(T),RiskFreeInterest(r),Volatility(sigma),DividendRate(q),Call/Put(0/1)
    #the output is a list of np.arrays = [price array, delta array, gamma array, vega array, theta array] of the options considered
    def GetPriceGreeks(self,S,K,T,r,sigma,q,type):
        try:
            '''
            we get vectorized versions of the methods defined below
            '''
            vect_d1=np.vectorize(self.d1)
            vect_d2=np.vectorize(self.d2)
            vect_Price=np.vectorize(self.Price)
            vect_Delta=np.vectorize(self.Delta)
            vect_Gamma=np.vectorize(self.Gamma)
            vect_Vega=np.vectorize(self.Vega)
            vect_Theta=np.vectorize(self.Theta)
            
            #we calculate vectors of d1 and d2
            d1=vect_d1(S,K,T,r,sigma,q,type)
            d2=vect_d2(d1,sigma,T)
            
            #we call the vectorized methods to calculate prices and greeks 
            result=[vect_Price(S,K,T,r,sigma,q,type,d1,d2),vect_Delta(S,K,T,r,sigma,q,type,d1),vect_Gamma(S,K,T,r,sigma,q,type,d1),vect_Vega(S,K,T,r,sigma,q,type,d1),vect_Theta(S,K,T,r,sigma,q,type,d1,d2)]
                
            return result
        
        except Exception:
            raise Exception("ExceptionPriceGreeks")
    
    '''
    The following methods ARE NOT vector methods, we vectorized them at GetPriceGreeks method
    '''
    #These functions calculate the arguments of the cumulative normal distribution functin (d1 and d2)
    def d1(self,S,K,T,r,sigma,q,type):
        F=S*np.exp(T*(r-q))
        d1=(np.log(F/K)+(r+(sigma**2)/2)*T)/(sigma*np.sqrt(T))
        
        return d1
    
    def d2(self,d1,sigma,T):
        d2= d1-sigma*np.sqrt(T)
        
        return d2
    
    #This method calculates the price via the BS formula for European options
    #We followed the forulas from the website:
    #http://en.wikipedia.org/wiki/Black%E2%80%93Scholes_model#Instruments_paying_continuous_yield_dividends
    def Price(self,S,K,T,r,sigma,q,type,d1,d2):
        try:
            F=S*np.exp(T*(r-q))
            #Calls are represented by 0
            if type==0:
                price=np.exp(-T*r)*(norm.cdf(d1)*F-norm.cdf(d2)*K)
            #Calls are represented by 1
            elif type==1:
                price=np.exp(-T*r)*(norm.cdf(-d2)*K-norm.cdf(-d1)*F)
            else: 
                print 'Error: Not a put nor call'
        
            return price
       
        except Exception:
            raise Exception("ExceptionPrice")
    
    #This method calculates the Delta
    def Delta(self,S,K,T,r,sigma,q,type,d1):
        try:
            #Calls are represented by 0
            if type==0:
                delta=np.exp(-q*T)*norm.cdf(d1)
            #Calls are represented by 1
            elif type==1:
                delta=np.exp(-q*T)*(norm.cdf(d1)-1)
            else: 
                print 'Error: Not a put nor call'
        
            return delta
        
        except Exception:
            raise Exception("ExceptionDelta")
    
    #This method calculates the Gamma
    def Gamma(self,S,K,T,r,sigma,q,type,d1):
        try:
            gamma=np.exp(-q*T)*norm.cdf(d1)/(sigma*S*np.sqrt(T))
            return gamma
        
        except Exception:
            raise Exception("ExceptionGamma")
    
    #This method calculates the Vega
    def Vega(self,S,K,T,r,sigma,q,type,d1):
        try:
            vega=np.exp(-q*T)*norm.cdf(d1)*S*np.sqrt(T)
            return vega
        
        except Exception:
            raise Exception("ExceptionVega")
    
    #This method calculates the Theta
    def Theta(self,S,K,T,r,sigma,q,type,d1,d2):
        try:
            #Calls are represented by 0
            if type==0:
                theta=-np.exp(-q*T)*S*norm.cdf(d1)*sigma/(2*np.sqrt(T))
                theta=theta+q*np.exp(-q*T)*S*norm.cdf(d1)
                theta=theta-r*K*np.exp(-r*T)*norm.cdf(d2)
            elif type==1:
                theta=-np.exp(-q*T)*S*norm.cdf(d1)*sigma/(2*np.sqrt(T))
                theta=theta-q*np.exp(-q*T)*S*norm.cdf(d1)
                theta=theta+r*K*np.exp(-r*T)*norm.cdf(d2)
            else: 
                print 'Error: Not a put nor call'
        
            return theta
        
        except Exception:
            raise Exception("ExceptionTheta")