from . import Riveter
import rosie, csv

#Child class of Riveter. Checks for large int columns that could be misread by Excel.
# @author MWK
class SYLKRiveter(Riveter.MetaRiveter):
    def __init__(self):
        self.register()
        self.loadRosieEngine()
        self.sylk_analysis = {}
        self.all = {}

    #Loads rosie engine and date patterns to detect
    def loadRosieEngine(self):
        librosiedir = './lib'
        rosie.load(librosiedir, quiet = True)
        engine = rosie.engine()
        self.sylk = engine.compile("^ \"ID\" .*")

    def analyze(self, csvFileDescriptor):
        self.sylk_analysis["hits"] = [0]
        delimiter = self.sniffDelimiter(csvFileDescriptor)
        with open(csvFileDescriptor) as f:
            csvReader = csv.reader(f, delimiter)
            self.sylk_analysis["detected"] = {}
            keys = next(csvReader)
            n = len(keys)
            if "ID" in keys[0].upper():
                self.sylk_analysis["detected"]["data"] = "Detected Symbolic Link"
                self.sylk_analysis["hits"] = [1]
        
        # Make empty list of confidences; either its there or it isn't. 
        self.sylk_analysis["confidence"] = [1] * n
        
        return self.sylk_analysis
    
    def scream(self):
        return "SYLKRiveter"

SYLKRiveter()