import numpy as np
class CalculationTool(object):
    'A class that provides calculation tools. For this project it only contains a beta method.'
    def beta(self,x,y):
        #x be the target return, y be the benchmark. Returns -1 if there is an error.
        try:
            covmatrix=np.cov([x,y])
            return covmatrix[0,1]/covmatrix[1,1]
        except Exception,e:
            print e
            return -1