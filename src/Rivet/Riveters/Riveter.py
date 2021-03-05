import csv
#Parent class for all riveter types
sessionRiveters = []
# @author MWK

def getRiveters():
    return sessionRiveters

class Riveter:
    def __init__(self):
        pass
    @classmethod
    def analyze(cls, column): pass

    @classmethod
    def apply(cls, csvFile, options, confidence): pass

    @classmethod
    def scream(cls):pass

    # Define method to determine delimiter. 
    def sniffDelimiter(self, csvFilePath):
        return csv.Sniffer().sniff(open(csvFilePath).read(1024), delimiters=",;\t")

    def register(self):
        sessionRiveters.append(self)