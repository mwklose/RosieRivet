import rosie
import sys
import csv
from Rivet.Riveters import *

# import JSON to pass back from Rivet processor
import json
import pprint

pp = pprint.PrettyPrinter()
# @author MWK
class RosieRivet():
    def __init__(self, myfile, confidence=0.80):
        self.riveters = self.initializeRiveters()
        # store filename; need to create multiple readers for each analysis
        self.csv = myfile
        
        self.confidence = confidence
        return

    # Grabs all Riveters registered by the system
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
        return analysis

    #After file is approved will then be processed in some way \o/ \o/ \o/
    def RivetProcessor(self, options, confidence=0.8, outfile="outfile"):
        csvf = self.RivetReadCSV()
        for r in self.riveters:
            # Hand in a CSV reader, seek back to the start guarantee after each one. 
            csvf = r.apply(csvf, options, confidence)
        return csvf, options
    
    def RivetReadCSV(self):
        out = []
        delimiter = csv.Sniffer().sniff(open(self.csv).read(1024), delimiters=",;\t")
        with open(self.csv) as f:
            for row in csv.reader(f, delimiter):
                out.append(row)
        return out