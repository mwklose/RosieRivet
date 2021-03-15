import csv
#Parent class for all riveter types
sessionRiveters = []
# @author MWK

def getRiveters():
    return sessionRiveters

class Riveter:
    # Define a constructor in each Riveter. 
    @classmethod
    def __init__(self):
        return

    # Analyze should pass back a dictionary with at least two keys: detected (potential errors) and confidence (fraction of errors in that column)
    @classmethod
    def analyze(cls, csvFileDescriptor): pass

    @classmethod
    def apply(cls, csvFileAsListOfLists, options, confidence): pass

    @classmethod
    def scream(cls):pass

    # Define method to determine delimiter. 
    def sniffDelimiter(self, csvFilePath):
        f = open(csvFilePath)
        sniff = csv.Sniffer().sniff(f.read(1024), delimiters=",;\t")
        f.close()
        return sniff

    # Define method to register for system. 
    def register(self):
        sessionRiveters.append(self)


    # Jennings suggestions:
    # Make a min-max riveter (analysis only), shows extensibility
    # Make design that offers to not fix anything
    # SYLK riveter?
    # Max file size riveter?
    # Offer more than one way to fix something?
    # Design issue: how does a riveter know what is in a column?

    # Assume homogenous columns for scientific data
    # "Typical spreadsheets" not one of our use cases, simplifies code somewhat
    # Find actual examples from real life?