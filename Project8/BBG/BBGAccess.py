
import blpapi

'''
    Two modes supported in this implementation. Static and Historical 
'''

class BBGRequest():
    def __init__(self):
        self.Static="Static"
        self.Historical="Historical"
        
BBGRequestMode = BBGRequest();

    
#helper class that abstracts access to Bloomberg
class BBGAccess :
    
    #define those global settings 
    serverName = 'localhost'
    port = 8194
    MAX_DATA_POINTS = 10000 #always good to setup a maximum on the number of data points you expect. This protects you in case your application has a bug and you end up getting tons of data from Bloomberg
    
    
    #Gets current/static data from Bloomberg
    def GetCurrentData(self, bbergCodes, bbgFields, overridesDictionary):
        try:
            #open sessions
            session = self.OpenBBGSession()
            refDataService = session.getService("//blp/refdata")
            request = refDataService.createRequest("ReferenceDataRequest")
            
            #prepare the request and a get a dictionary to store the output
            dictResults = self.PrepareRequest(request, bbergCodes, bbgFields, overridesDictionary)
            
            #send the request and get the output in in dictResults
            self.ExecuteRequest(session, request, BBGRequestMode.Static, dictResults)
            return dictResults
        except Exception, e:
            raise Exception("GetCurrentData failed! Error Message: " + str(e))
    
    
    
    #gets historical data from Bloomberg
    def GetHistoricalData(self, startDate, endDate, bbergCodes, bbgFields, overridesDictionary):
        try:
            session = self.OpenBBGSession()
            refDataService = session.getService("//blp/refdata")
            request = refDataService.createRequest("HistoricalDataRequest")
            
            request.set("startDate", startDate)
            request.set("endDate", endDate)
            request.set("maxDataPoints", BBGAccess.MAX_DATA_POINTS)
            
            #prepare the request and a get a dictionary to store the output
            dictResults = self.PrepareRequest(request, bbergCodes, bbgFields, overridesDictionary)
            
            #send the request and get the output in in dictResults
            self.ExecuteRequest(session, request, BBGRequestMode.Historical, dictResults)
            return dictResults
        except Exception, e:
            raise Exception("GetHistoricalData failed! Error Message: " + str(e))
    

    #This method opens a connection to Bloomberg and will start a Bloomberg session
    def OpenBBGSession(self):
        # Fill SessionOptions
        sessionOptions = blpapi.SessionOptions()
        sessionOptions.setServerHost(self.serverName)
        sessionOptions.setServerPort(self.port)
        # Create a Session
        session = blpapi.Session(sessionOptions)
        # Start a Session
        if not session.start():
            raise Exception("Failed to start Bloomberg session.")
            
        if not session.openService("//blp/refdata"):
            raise Exception("Failed to open Bloomberg //blp/refdata")
        
        return session
    
        
    
    
    def PrepareRequest(self, request, bbergCodes, bbgFields, overridesDictionary):
        
        #iterate over the fields and then
        for fld in bbgFields:
            request.append("fields", fld)
        
        if(overridesDictionary != None and len(overridesDictionary)>0):    
            for overrideField in overridesDictionary:
                overrideElement= request.getElement("overrides").appendElement()
                overrideElement.setElement("fieldId", overrideField);
                overrideElement.setElement("value", overridesDictionary[overrideField]);
        
        #prepare a dictionary of dictionaries to store the output        
        dictResult = {}
        
        # append securities to request
        for bbergCode in bbergCodes: 
            request.append("securities", bbergCode)
            dictResult[bbergCode] = {}
            
        return dictResult
    
    
    
    def ExecuteRequest(self, session, request, requestMode, dictResults):
        # fire away
        session.sendRequest(request)
        try:
            # Process received events
            continueToLoop = True;
            while continueToLoop :
                nextEvent = session.nextEvent(5000)
                if nextEvent.eventType() == blpapi.Event.RESPONSE or nextEvent.eventType() == blpapi.Event.PARTIAL_RESPONSE:
                    if(requestMode == BBGRequestMode.Historical):
                        self.HandleHistoricalResponseEvent(nextEvent, dictResults)
                    else:
                        self.HandleResponseEvent(nextEvent, dictResults)
                    #if the response was a full response , we need to exit the loop
                    if(nextEvent.eventType() == blpapi.Event.RESPONSE):
                        continueToLoop = False
                elif nextEvent.eventType() == blpapi.Event.TIMEOUT:
                            raise Exception("Bloomberg Sapi Request timed out.");
                #else:
                    # These are status events - we can ignore for now
        except Exception, e:
            # Stop the session
            session.stop()
            raise e
        else:
            # Stop the session
            session.stop()
    
        
    def HandleResponseEvent(self, responseEvent, dictResult):
        try:
            symbol = ""        
            for message  in responseEvent:
                if message.messageType() == "ReferenceDataResponse":
                    element = message.getElement("securityData")
                    for security in element.values():
                        for innerElement in security.elements():
                            if innerElement.name() == "security":
                                symbol =  innerElement.getValueAsString(0)
                            else: 
                                if innerElement.name() == "fieldExceptions":
                                    print "Some of the fields you requested were invalid for symbol: " + symbol
                                else: 
                                    if innerElement.name() == "fieldData":
                                        for fieldData in innerElement.elements():
                                            
                                            if fieldData.isArray():
                                                raise Exception("This implementation does not support array types: mnemonic: ")
                                            else:
                                                mnominc = str(fieldData.name())
                                                dictResult[symbol][mnominc] = fieldData.getValueAsString(0)
                else:
                    raise Exception("Expecting a static/current data response event type")                                          
        except Exception as e:
            print e
            raise e
            
            
            
    
            
    def HandleHistoricalResponseEvent(self, responseEvent, dictResult):
        try:
            symbol = ""  
            for message  in responseEvent:
                # print message
                if message.messageType() == "HistoricalDataResponse":
                    #the expectation is that securityData is the first element in the message
                    securityDataArray = message.getElement("securityData")
                    for innerElement in securityDataArray.elements():
                        if innerElement.name() == "security":
                            #this element will tell us what the security symbol is
                            symbol =  innerElement.getValueAsString(0)
                        elif innerElement.name() == "fieldExceptions":
                            if(innerElement.numValues() > 0):
                                print "Some fields generated errors for security: " + symbol
                                #todo - iterate and report on errors
                        elif innerElement.name() == "securityError":
                            if(innerElement.numValues() > 0):
                                print "Error Occurred for security:" + symbol
                        elif innerElement.name() == "fieldData":
                            # the data is coming in as sequence
                            for dayElement in innerElement.values():
                                for fld in dayElement.elements():
                                    if fld.isArray():
                                        raise Exception("This implementation does not support array types: mnemonic: ")
                                    else:
                                        if(str(fld.name()) == "date"):
                                            date  = str(fld.getValueAsString(0))
                                            if not dictResult[symbol].has_key(date):
                                                dictResult[symbol][date] = {}
                                        else:
                                            mnominc =  str(fld.name())
                                            dictResult[symbol][date][mnominc] = fld.getValueAsString(0)
                                        
        except Exception as e:
            print e
            raise e
            
    
    
    
   

    
