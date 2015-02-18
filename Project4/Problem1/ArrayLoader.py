import numpy as np
class ArrayLoader(object):
    'Creates an ArrayLoader object that helps load column data from csv files.'
    def __init__(self,filename):
        '''User should provide filename to initialize an instance.'''
        self.filename=filename
    def getcolumndata(self,col=0,tp='float'):
        #gets a certain column of data
        try:
            data=np.genfromtxt(self.filename, dtype=tp, delimiter=',', skip_header=1, usecols=col)
            return data
        except Exception,e:
            print e
