
from . import Riveter
import rosie
import collections
import csv

# Child class of Riveter that checks for gene names that could be misread as dates by Excel
# @author MWK
class GeneDateRiveter(Riveter.DataRiveter):

    #Initialize Riveter along with rosie engine 
    def __init__(self):
        self.register()
        self.loadRosieEngine()
        self.gene_date_analysis = {}
        self.all = {}

        
    #Loads rosie engine and date patterns to detect
    def loadRosieEngine(self):
        librosiedir = './lib'
        rosie.load(librosiedir, quiet = True)
        engine = rosie.engine()
        engine.import_package("date")
        self.date_patterns = engine.compile("date.any")
        engine.load("short_year = [0-9]{ 2 }")
        self.date_check = [engine.compile("{ { \"APR\" / \"OCT\" / \"DEC\" / \"MARCH\" / \"SEPT\" / \"SEP\" } [:digit:]* }")] #, 
                           # engine.compile("{ { date.month { \"-\" / [/] } short_year} / { date.day { \"-\" / [/] } date.month } }")]

    #Analyzes file, takes a given file and applies rosie date matching to detect elements that 
    #can be misinterpreted as dates.
    def analyze(self, csvFile):
        # Added by @mwk due to needing to check delimiter on test files. 
        delimiter = self.sniffDelimiter(csvFile)
        # Added definition for delimiter due to input reading errors. 
        with open(csvFile) as f: 
            csvReader = csv.reader(f, delimiter)
            
            self.gene_date_analysis["detected"] = {}
            keys = next(csvReader)
            n = len(keys)
            date_counter = [0] * n
            total_counter = [0] * n
            actual_date_counter = [0] * n

            # Start rewrite for more pythonic: Mark
            rn = 0
            cn = 0
            for row in csvReader:
                for col in row:
                    # Keep count of elements if they exist
                    total_counter[cn] += 1

                    # Get count of total number of matched dates based on Rosie built-in
                    if(self.date_patterns.fullmatch(col.upper())):
                        actual_date_counter[cn] += 1
                        self.all[(rn+1,cn+1)] = {"row_no" : rn+1, "col_no":  cn + 1, "data" : col, "type": "ACTUALDATE"}
                    
                    # Check against known issues in Excel
                    if(any([check.fullmatch(col.upper()) for check in self.date_check])):
                        date_counter[cn] += 1
                        self.gene_date_analysis["detected"][(rn+1, cn+1, keys[cn].upper())] = col
                        self.all[(rn+1,cn+1)]  = {"row_no" : rn+1, "col_no":  cn + 1, "data" : col, "type": "NOTADATE"}
                    
                    # Increase counter
                    cn += 1
            
                # Increase row number, reset column number
                rn += 1
                cn = 0

        # Old written by Shawn:
        self.gene_date_analysis["DATESTAT"] = [[a / c, b / c] for a, b, c in zip(date_counter, actual_date_counter, total_counter) ]

        # Add guaranteed lines for printing/display
        self.gene_date_analysis["confidence"] = [(a + 1) / (a + b + 1) for a, b, c in zip(date_counter, actual_date_counter, total_counter)]
        self.gene_date_analysis["hits"] = [a for a, b, c in zip(date_counter, actual_date_counter, total_counter)]

        return self.gene_date_analysis
    
    def scream(self):
        return "GeneDateRiveter"


    
    #Processes file and outputs new file aimed to protect csv file against misinterpretation
    def apply(self, csvFile, options, confidence):
        if(self.scream() not in options):
            return
        stats = self.gene_date_analysis["confidence"]
        # Get all detections
        detections = options[self.scream()]["detected"]
        # Iterate through each detection
        for k in detections.keys():
            # Rows are 1-index; 0-index is headers
            row = k[0]
            # Columns are 0-index; no labels on columns
            col = k[1] - 1
            # Check against confidence
            if stats[col] > confidence: 
                value = csvFile[row][col]  # Get value by row and column
                csvFile[row][col] = "'" + value # Find remedy for row/column
        return csvFile

GeneDateRiveter()