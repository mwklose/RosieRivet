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
        self.date_patterns = engine.compile("date.any")

    def analyze(self, csvFile):
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
                        date_counter[cn] += 1 if match['type'] == "date.any" else 0
                        t = match['subs'][0]['type']
                        # Keep track of what types are in each column; should be consistent across worksheet???
                        try:
                            self.date_format_analysis['types'][t] += 1
                        except KeyError:
                            self.date_format_analysis['types'][t] = 1

                        self.all[(rn+1, cn+1)] = {
                            "row_no"    : rn+1, 
                            "col_no"    : cn+1,
                            "data"      : col,
                            "type"      : t,
                            "match"     : match
                        }
                    elif any(char.isdigit() for char in col):
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
            print(standardize_date(self.all[(row, col + 1)]))
            csvFile[row][col] = standardize_date(self.all[(row, col + 1)])
            # if stats[col] > confidence:
            #     print(standardize_date(self.all[(row, col + 1)]))
            #     csvFile[row][col] = standardize_date(self.all[(row, col + 1)])
        return

    
    def scream(self):
        return "DateFormatRiveter"

DateFormatRiveter()

M_MONTH, M_DAY, M_YEAR = 0, 1, 2
L_DAY, L_MONTH, L_YEAR = 0, 1, 2
B_YEAR, B_MONTH, B_DAY = 0, 1, 2

def standardize_date(element):
    match = element['match']
    type_of_format = match['subs'][0]['type']
    # Handle Dashed Dates: 2020-04-20
    if type_of_format == "date.dashed":
        print(type_of_format, match)
        day = match["subs"][0]["subs"][B_DAY]['data']
        month = match["subs"][0]["subs"][B_MONTH]['data']
        year = match["subs"][0]["subs"][B_YEAR]['data']
        return "{0:>04s}-{1:>02s}-{2:>02s}".format(year, month, day)
    # Handle US Slashed dates: 3/10/2021
    if type_of_format == "date.us_slashed":
        day = match["subs"][0]["subs"][M_DAY]['data']
        month = match["subs"][0]["subs"][M_MONTH]['data']
        year = match["subs"][0]["subs"][M_YEAR]['data']
        return "{0:>04s}-{1:>02s}-{2:>02s}".format(year, month, day)
    if type_of_format == "date.eur":
        day = match["subs"][0]["subs"][L_DAY]['data']
        month = match["subs"][0]["subs"][L_MONTH]['data']
        year = match["subs"][0]["subs"][L_YEAR]['data']
        return "{0:>04s}-{1:>02s}-{2:>02s}".format(year, month, day)
    print("--->", type_of_format, match)

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
        return "RFC TO DO"
    elif type_of_format == "date.us_short":
        #print(match['subs'][0]['subs'])
        return match['subs'][0]['subs'][1]['data'] + " " + match['subs'][0]['subs'][0]['data'] + ", " + match['subs'][0]['subs'][2]['data']
    return match
    