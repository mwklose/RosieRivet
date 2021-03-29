from . import Riveter
import rosie, csv
# Child class of Riveter that checks for potential harmful CSV injections
# @author MWK
class CSVInjectionRiveter(Riveter.Riveter):

    def __init__(self):
        self.register()
        self.loadRosieEngine()
        self.csv_injections_analysis = {}
        self.all = {}

     #Loads rosie engine and date patterns to detect
    def loadRosieEngine(self):
        librosiedir = './lib'
        rosie.load(librosiedir, quiet = True)
        engine = rosie.engine()
        self.csv_injections = engine.compile("{^[=@+\-] [^0-9] .*}")

    def analyze(self, csvFile):
        delimiter = self.sniffDelimiter(csvFile)
        with open(csvFile) as f: 
            csvReader = csv.reader(f, delimiter)
            self.csv_injections_analysis['detected'] = {}
            keys = next(csvReader)
            n = len(keys)
            error_counter = [0] * n
            total_counter = [0] * n

            rn = 0
            cn = 0
            for row in csvReader:
                for col in row:
                    # Keep count of elements if they exist
                    total_counter[cn] += 1
                    em = self.csv_injections.fullmatch(col.upper())
                    # Get count of total number of matched dates based on Rosie built-in
                    if(em):
                        error_counter[cn] += 1
                        self.csv_injections_analysis['detected'][(rn+1, cn+1, keys[cn].upper())] = col
                        # Get match via Rosie, and save some important info/type
                        match = em.rosie_match
                        # Add entry to all potential matches
                        self.all[(rn+1, cn+1)] = {
                            "row_no"    : rn+1, 
                            "col_no"    : cn+1,
                            "data"      : col,
                            "match"     : match
                        }
                

                    # Increase counter
                    cn += 1
            
                # Increase row number, reset column number
                rn += 1
                cn = 0

        # Add Confidence and number of hits per column
        self.csv_injections_analysis["confidence"] = [d / t for d,t in zip(error_counter, total_counter)]
        self.csv_injections_analysis["hits"] = [a for a in error_counter]
        return self.csv_injections_analysis

    def apply(self, csvFile, options, confidence):
        if(self.scream() not in options):
            return
        stats = self.csv_injections_analysis["confidence"]
        detections = options[self.scream()]["detected"]
        for k in detections.keys():
            row = k[0]
            col = k[1] - 1
            if stats[col] > confidence:
                csvFile[row][col] = '\'{:s}'.format(csvFile[row][col])
        return

    def scream(self):
        return "CSVInjectionRiveter"

CSVInjectionRiveter()