import csv
#Parent class for all riveter types
sessionRiveters = []
# @author MWK

def getRiveters():
    return sessionRiveters

class Riveter:
    # Define a constructor in each Riveter. 
    def __init__(self):
        pass

    # Analyze should pass back a dictionary with at least two keys: detected (potential errors) and confidence (fraction of errors in that column)
    @classmethod
    def analyze(cls, column): pass

    @classmethod
    def apply(cls, csvFile, options, confidence): pass

    @classmethod
    def scream(cls):pass

    # Define method to determine delimiter. 
    def sniffDelimiter(self, csvFilePath):
        return csv.Sniffer().sniff(open(csvFilePath).read(1024), delimiters=",;\t")

    # Define method to register for system. 
    def register(self):
        sessionRiveters.append(self)