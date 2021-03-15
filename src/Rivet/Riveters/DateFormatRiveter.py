from . import Riveter
import rosie
import csv

# @author MWK
# Child class of Riveter that checks for dates and standardizes them
class DateFormatRiveter(Riveter.Riveter):

    def __init__(self):
        self.register()
        self.loadRosieEngine()
        self.date_format_analysis = {}
        self.all = {}

    #Loads rosie engine and date patterns to detect
    def loadRosieEngine(self):
        librosiedir = './lib'
        rosie.load(librosiedir, quiet = True)
        engine = rosie.engine()
        engine.import_package("date")
        engine.import_package("char")
        # Use Rosie Built-in date types for recognition
        self.date_patterns = engine.compile("date.any")
        # Rosie missing functionality for little-endian dates; 
        self.little_endian = engine.compile("{date.day .[:space:]? date.month .[:space:]? date.year .?}")

        # Define own RPL file (use date.rpl) --> future PR into Rosie?

    def analyze(self, csvFile):

        # Define ambiguous date-month formats? Can be hardcoded based on stress-test
        # Show ambiguous analysis, get user input???
        # n number entries in ambiguous, interpret in certain style=all valid
            # Case: interpret all as US, see if valid, interpret all as EU, see if valid
            # Otherwise, make known that not interpreted
        delimiter = self.sniffDelimiter(csvFile)
        with open(csvFile) as f: 
            csvReader = csv.reader(f, delimiter)
            self.date_format_analysis['detected'] = {}
            self.date_format_analysis['types'] = {}
            keys = next(csvReader)
            n = len(keys)
            date_counter = [0] * n
            total_counter = [0] * n

            # Keep row and column counter
            rn = 0
            cn = 0
            for row in csvReader:
                for col in row:
                    # Keep count of elements if they exist
                    total_counter[cn] += 1
                    fm = self.date_patterns.fullmatch(col.upper())
                    # ISSUE: ROSIE DOES NOT RECOGNIZE LITTLE ENDIAN WITH DAY FIRST
                    # Get count of total number of matched dates based on Rosie built-in
                    if(fm):
                        self.date_format_analysis['detected'][(rn+1, cn+1, keys[cn].upper())] = col
                        # Get match via Rosie, and save some important info/type
                        match = fm.rosie_match
                        t = match['subs'][0]['type']
                        date_counter[cn] += 1 if match['type'] == "date.any" else 0
                        # Keep track of what types are in each column; should be consistent across worksheet???
                        try:
                            self.date_format_analysis['types'][t] += 1
                        except KeyError:
                            self.date_format_analysis['types'][t] = 1
                        # Add entry to all potential matches
                        self.all[(rn+1, cn+1)] = {
                            "row_no"    : rn+1, 
                            "col_no"    : cn+1,
                            "data"      : col,
                            "type"      : t, # Gets the type of match
                            "match"     : match
                        }
                    # If has potential to be date, then
                    elif any(char.isdigit() for char in col):
                        # If potential date, compare to little endian
                        fm = self.little_endian.fullmatch(col.upper())
                        if(fm):
                            date_counter[cn] += 1
                            self.date_format_analysis['detected'][(rn+1, cn+1, keys[cn].upper())] = col
                            try:
                                self.date_format_analysis['types']["date.littleEndian"] += 1
                            except KeyError:
                                self.date_format_analysis['types']["date.littleEndian"] = 1
                                
                            self.all[(rn+1, cn+1)] = {
                                "row_no"    : rn+1, 
                                "col_no"    : cn+1,
                                "data"      : col,
                                "type"      : "date.littleEndian", # Define own match type
                                "match"     : match
                            }
                        # # Debug print statement: TODO remove
                        else:
                            print(col)
                            

                    # Increase counter
                    cn += 1
            
                # Increase row number, reset column number
                rn += 1
                cn = 0

        # Add Confidence and number of hits per column
        self.date_format_analysis["confidence"] = [d / t for d,t in zip(date_counter, total_counter)]
        self.date_format_analysis["hits"] = [a for a in date_counter]
        print("MAX TYPE IS:", max(self.date_format_analysis["types"], key=self.date_format_analysis["types"].get))
        return self.date_format_analysis

    def apply(self, csvFile, options, confidence):
        stats = self.date_format_analysis["confidence"]
        detections = options[self.scream()]["detected"]
        for k in detections.keys():
            row = k[0]
            col = k[1] - 1
            if stats[col] > confidence:
            #     print(standardize_date(self.all[(row, col + 1)]))
                csvFile[row][col] = standardize_date(self.all[(row, col + 1)])
        return

    
    def scream(self):
        return "DateFormatRiveter"

DateFormatRiveter()

# M_MONTH, M_DAY, M_YEAR = 0, 1, 2
# L_DAY, L_MONTH, L_YEAR = 0, 1, 2
# B_YEAR, B_MONTH, B_DAY = 0, 1, 2

def standardize_date(element):
    # Initialize strings for later concatenation
    year, month, day = "0", "0", "0"

    # Loop through each SUB match to gather day, month, and year.
    # This is less efficient, but more comprehensive if Rosie gains more support for more date types.
    for val in element['match']["subs"][0]["subs"]:
        if "day" in val['type']:
            day = val['data']
        if "month" in val['type']:
            month = val['data']
        if "year" in val['type']:
            year = val['data']
    print("{0:>04s}-{1:>02s}-{2:>02s}".format(year, month, day), "OLD:", element['data'], "ELEMENT:", element)
    return "{0:>04s}-{1:>02s}-{2:>02s}".format(year, month, day)
    