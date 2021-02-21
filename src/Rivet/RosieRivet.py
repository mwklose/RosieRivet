import rosie
import sys
from Rivet.Riveters import *
# https://stackoverflow.com/questions/1057431/how-to-load-all-modules-in-a-folder
# WE GON LOAD ALL THEM RIVETERS UP IN THIS HOE

sRiveters = {
    "GeneDateRiveter" : GeneDateRiveter.GeneDateRiveter(),
    "LargeIntRiveter" : LargeIntRiveter.LargeIntRiveter(),
    "CSVInjectionRiveter" : CSVInjectionRiveter.CSVInjectionRiveter(),
    "DateFormatRiveter" : DateFormatRiveter.DateFormatRiveter(),
    "LocaleSeparatorRiveter" : LocaleSeparatorRiveter.LocaleSeparatorRiveter()
}

# @author MWK
class RosieRivet():
    def __init__(self, confidence=0.80):
        self.riveters = self.initializeRiveters()
        self.confidence = confidence
        return

    def initializeRiveters(self):
        return sRiveters.values()

    #actual beginning of the analysis process, will go through each riveter and determine if this
        #CSV has the particular data type, marking column to be displayed to user in approveFile
        #myCSV the CSV file being analyzed
    def RivetFileAnalyzer(self, myCSV):
        print("RivetFileAnalyzer")
        pass
    #After file is approved will then be processed in some way \o/ \o/ \o/
    def RivetProcessor(self, myCSV, riveters, confidence=0.8, outfile=""):
        print("IN RIVET PROCESSOR")
        return
