'''
Bernardo Bravo-Benitez, bb2699
Chendi Ni, cn2367
Oct, 2014
IEOR4728
'''

#We import the module BlackScholesObjects where the BlackScholes object is defined
from BlackScholesObjects import BlackScholes
import numpy as np

#Here we define some sample inputs for a portfolio of two options:
#Spot price of the underlying assets
vect_S=np.array([100,42])
#Strike prices
vect_K=np.array([100,40])
#Maturities
vect_T=np.array([3,.5])
#Risk free interest rate
vect_r=np.array([.1,.1])
#Volatilities
vect_sigma=np.array([.3,.2])
#Continuous dividend yields
vect_q=np.array([0.0,.02])
#Call option (0) or put (1)
vect_type=np.array([1,0])

#create an instance of the class
BS=BlackScholes()

#We use the method GetPriceGreeks from the object BlackScholes to calculate the list of arrays with the Prices and Greeks
PriceGreeks=BS.GetPriceGreeks(vect_S,vect_K,vect_T,vect_r,vect_sigma,vect_q,vect_type)
 
print 'Result:' 
print 'Prices=', PriceGreeks[0]
print 'Deltas=', PriceGreeks[1]
print 'Gammas=', PriceGreeks[2]
print 'Vegas=', PriceGreeks[3]
print 'Thetas=', PriceGreeks[4]