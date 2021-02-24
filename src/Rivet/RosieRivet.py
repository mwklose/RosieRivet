import rosie
import sys
import csv
from Rivet.Riveters import *

# @author MWK
class RosieRivet():
    def __init__(self, myfile, confidence=0.80):
        self.riveters = self.initializeRiveters()
        self.csv = csv.DictReader(open(myfile))
        self.confidence = confidence
        return

    def initializeRiveters(self):
        # Return all riveters defined by the session
        return Riveter.getRiveters()

    #actual beginning of the analysis process, will go through each riveter and determine if this
        #CSV has the particular data type, marking column to be displayed to user in approveFile
        #myCSV the CSV file being analyzed
    def RivetFileAnalyzer(self):
        analysis = {}
        for r in self.riveters:
            analysis[r.scream()] = r.analyze(self.csv)
            
            

        print(analysis)   
        return analysis
    #After file is approved will then be processed in some way \o/ \o/ \o/
    def RivetProcessor(self, myCSV, riveters, confidence=0.8, outfile=""):
        print("IN RIVET PROCESSOR")
        return
