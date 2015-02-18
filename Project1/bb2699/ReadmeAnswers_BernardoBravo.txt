Assignment 1 - Bernardo Bravo B - bb2699

Answers:

1. I have set up the environment in a similar way as Faddi's presentation. The difference is that I installed Anaconda, to get Python 2.7, Numpy Scipy, Pandas and Ipython at the same time.

2. I've created a Project called Assignment1_BernardoBravo with the module PortfolioConcentration and placed it on the zip file attached.

3. The program already implemented uses the method GetMeasureTotalBySlice to sum the BaseMarketValues (measure) for each strategy (slice) and prints the result. 

4. I used the debugger: resume, step into ... Now I'm familiarized with the debugger. 

5. The firm's exposure to ValueEquities is 515901344.1399999, considering the BaseMarketValues

6. I implemented the method GetTopandBottomSlices: it receives the dictionary produced by the GetMeasureTotalBySlice method and creates two lists, one containing the values and the other one the keys of the dictionary
   Then it uses the index function and max and min functions to find the indexes from the list associated to such values.
   The function returns the min max values and the keys associated to such values

7. Considering the BaseMarketValues, the Security associated to the biggest short position is: SPDR S&P MIDCAP 400 ETF TRST 
   With a position of: -537973500

8. The top performer strategy for this year is: Event Equities 
   With a profit of: 444626160
   The bottom performer strategy for this year is: Equity Index Hedges 
   With a loss of: -139333718

9. The top performer security type for this year is: Stock 
   With a profit of: 530136308
   The bottom performer security type for this year is: Put Option 
   With a loss of: -21440118

Disclaimer: The codes on this site provided some inspiration
http://stackoverflow.com/questions/268272/getting-key-with-maximum-value-in-dictionary