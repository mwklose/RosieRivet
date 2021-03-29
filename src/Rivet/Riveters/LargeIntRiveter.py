from . import Riveter
import rosie, csv

#Child class of Riveter. Checks for large int columns that could be misread by Excel.
# @author MWK
class LargeIntRiveter(Riveter.Riveter):

    def __init__(self):
        self.register()
        self.loadRosieEngine()
        self.large_int_analysis = {}
        self.all = {}

    #Loads rosie engine and date patterns to detect
    def loadRosieEngine(self):
        librosiedir = './lib'
        rosie.load(librosiedir, quiet = True)
        engine = rosie.engine()
        
        # Rosie recognize scientific notation or IDs
        self.engines = {
            "sci_notation" : engine.compile("{[:digit:]* [E] [:digit:]*}"),
            "leading_zero" : engine.compile("{[0]{1,} [:alnum:]*}"),
            "long_integer" : engine.compile("{[:digit:]{12,}}")
        }

    def analyze(self, csvFile):
        delimiter = self.sniffDelimiter(csvFile)
        with open(csvFile) as f: 
            csvReader = csv.reader(f, delimiter)
            self.large_int_analysis['detected'] = {}
            keys = next(csvReader)
            n = len(keys)
            error_counter = [0] * n
            total_counter = [0] * n

            # Keep row and column counter
            for e in self.engines:
                rn = 0
                cn = 0
                # Get to the front of the file
                f.seek(0)
                # Throw away header lines
                next(csvReader)
                # Then, iterate through all values in csvReader to analyze.
                for row in csvReader:
                    for col in row:
                        # Keep count of elements if they exist
                        total_counter[cn] += 1
                        em = self.engines[e].fullmatch(col.upper())
                        # Get count of total number of matched dates based on Rosie built-in
                        if(em):
                            error_counter[cn] += 1
                            self.large_int_analysis['detected'][(rn+1, cn+1, keys[cn].upper())] = col
                            # Get match via Rosie, and save some important info/type
                            match = em.rosie_match
                            # Add entry to all potential matches
                            self.all[(rn+1, cn+1)] = {
                                "row_no"    : rn+1, 
                                "col_no"    : cn+1,
                                "data"      : col,
                                "type"      : e,
                                "match"     : match
                            }
                    

                        # Increase counter
                        cn += 1
                
                    # Increase row number, reset column number
                    rn += 1
                    cn = 0

        # Add Confidence and number of hits per column
        total_counter = [r / len(self.engines) for r in total_counter] # Number of total hits is triple counted, this resets the triple counting
        self.large_int_analysis["confidence"] = [d / t for d,t in zip(error_counter, total_counter)]
        self.large_int_analysis["hits"] = [a for a in error_counter]
        return self.large_int_analysis

    def apply(self, csvFile, options, confidence):
        if(self.scream() not in options):
            return
        stats = self.large_int_analysis["confidence"]
        detections = options[self.scream()]["detected"]
        for k in detections.keys():
            row = k[0]
            col = k[1] - 1
            if stats[col] > confidence:
                csvFile[row][col] = '\'{:s}'.format(csvFile[row][col])
        return

    def scream(self):
        return "LargeIntRiveter"

LargeIntRiveter()
