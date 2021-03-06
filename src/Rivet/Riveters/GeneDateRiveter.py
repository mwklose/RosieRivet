
from . import Riveter
import rosie
import collections
import csv

# Child class of Riveter that checks for gene names that could be misread as dates by Excel
# @author MWK
class GeneDateRiveter(Riveter.Riveter):

    #Initialize Riveter along with rosie engine 
    def __init__(self):
        self.register()
        self.scream()
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
        self.date_check = [engine.compile("{ { \"APR\" / \"OCT\" / \"DEC\" / \"MARCH\" / \"SEPT\" } [:digit:]* }"), engine.compile("{ { date.month { \"-\" / [/] } short_year} / { date.day { \"-\" / [/] } date.month } }")]

    #Analyzes file, takes a given file and applies rosie date matching to detect elements that 
    #can be misinterpreted as dates.
    def analyze(self, csvFile):
        # Added by @mwk due to needing to check delimiter on test files. 
        delimiter = self.sniffDelimiter(csvFile)
        # Added definition for delimiter due to input reading errors. 
        csvReader = csv.reader(open(csvFile), delimiter)
        
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

        # # Commented out by Mark - made more pythonic right before this, more straightforward to read. 
        # for row_num,row in enumerate(csvReader):
        #     for col_num,element in enumerate(row):
        #         if(element):
        #             total_counter[col_num] += 1
        #         if(self.date_patterns.fullmatch(element.upper())):
        #             actual_date_counter[col_num] += 1
        #             self.all[(row_num+1,col_num+1)] = {"row_no" : row_num+1, "col_no":  col_num + 1, "data" : element, "type": "ACTUALDATE"}
        #         if(any([check.fullmatch(element.upper()) for check in self.date_check])):
        #             date_counter[col_num] += 1
        #             self.gene_date_analysis["detected"][(row_num+1, col_num+1, keys[col_num].upper())] = element
        #             self.all[(row_num+1,col_num+1)]  = {"row_no" : row_num+1, "col_no":  col_num + 1, "data" : element, "type": "NOTADATE"}

        # Old written by Shawn:
        self.gene_date_analysis["DATESTAT"] = [[a / c, b / c] for a, b, c in zip(date_counter, actual_date_counter, total_counter) ]

        # Add guaranteed lines for printing/display
        self.gene_date_analysis["confidence"] = [(a + 1) / (a + b + 1) for a, b, c in zip(date_counter, actual_date_counter, total_counter)]
        self.gene_date_analysis["hits"] = [a for a, b, c in zip(date_counter, actual_date_counter, total_counter)]

        return self.gene_date_analysis
    
    def scream(self):
        return "GeneDateRiveter"


    #Given an element, according to stat provided, determines the correct way to remedy data in order to prevent
    #excel from possible misinterpretation 
    def find_remedy(self, elem, typ, stat):
        THRESHOLD = 0.8
        if typ == "NOTADATE":
            if stat[1] >= THRESHOLD or (stat[1] != 0.0 and stat[1] + stat[0] >= 0.9):
                return elem
            else:
                return solve(elem)
        elif typ == "ACTUALDATE":
            date = date_format(elem)
            if "," in date:
                date = make_dates_uniform(date)
            return date
        else:
            return solve(elem)

    #Determines the correct date to use
    def date_format(element):
        #print(element)
        librosiedir = './lib'
        rosie.load(librosiedir, quiet=True)
        engine = rosie.engine()
        engine.import_package("date")
        date_patterns = engine.compile("date.any")
        match = date_patterns.fullmatch(element).rosie_match
        type_of_format = match['subs'][0]['type']
        #print(type_of_format)
        if type_of_format == "date.us_long":
            #print("us long")
            if match['subs'][0]['subs'][0]['type'] == "date.day_name":
                return match['subs'][0]['subs'][1]['data'] + " " + match['subs'][0]['subs'][2]['data'] + ", " + match['subs'][0]['subs'][3]['data']
            else:
                return match['subs'][0]['subs'][0]['data'] + " " + match['subs'][0]['subs'][1]['data'] + ", " + match['subs'][0]['subs'][2]['data']
        elif type_of_format == "date.eur":
            #print("europe")
            return match['subs'][0]['subs'][1]['data'] + "/" + match['subs'][0]['subs'][0]['data'] + "/" + match['subs'][0]['subs'][2]['data']
        elif type_of_format == "date.spaced":
            #print("spaced")
            return element.replace(" ", "/")
        elif type_of_format == "date.spaced_en" or (type_of_format == "date.rfc2822" and "," not in element):
            #print("eng or rfc")
            return match['subs'][0]['subs'][1]['data'] + " " + match['subs'][0]['subs'][2]['data'] + ", " + match['subs'][0]['subs'][0]['data']
        elif type_of_format == "date.rfc2822" and "," in element:
            #print("big rfc")
            index = element.rindex(",")
            return date_format(element[index + 1:].strip())
        elif type_of_format == "date.us_short":
            #print(match['subs'][0]['subs'])
            return match['subs'][0]['subs'][1]['data'] + " " + match['subs'][0]['subs'][0]['data'] + ", " + match['subs'][0]['subs'][2]['data']
        return element

    def solve(elem):
        return "\"=\"" + "\"" + elem + "\"" + "\"" + "\""

    def make_dates_uniform(date):
        month_dict = {
            "january": 1,
            "jan": 1,
            "february": 2,
            "feb": 2,
            "march": 3,
            "mar": 3,
            "april": 4,
            "apr": 4,
            "may": 5,
            "june": 6,
            "jun": 6,
            "july": 7,
            "jul": 7,
            "august": 8,
            "aug": 8,
            "september": 9,
            "sep": 9,
            "october": 10,
            "oct": 10,
            "november": 11,
            "nov": 11,
            "december": 12,
            "dec": 12
        }
        date = date.lower()
        index_month = date.find(" ")
        index_day = date.find(",")
        return str(month_dict[date[0: index_month]]) + "/" + date[index_month + 1: index_day] + "/" + date[index_day + 2:]


    #Processes file and outputs new file aimed to protect csv file against misinterpretation
    def apply(self, csvFile, options, confidence):
        stats = self.gene_date_analysis["DATESTAT"]
        # Get all detections
        detections = options[self.scream()]["detected"]
        # Iterate through each detection
        for k in detections.keys():
            row = k[0] - 1
            col = k[1] - 1
            # Check against confidence
            if 1 - stats[col][1] < confidence: 
                # Get value by row and column
                
                value = csvFile[row][col] 
                # Find remedy for row/column
                csvFile[row][col] = "'" + value
        return

GeneDateRiveter()