from . import Riveter
import rosie, csv

#Child class of Riveter. Checks for large int columns that could be misread by Excel.
# @author MWK
class SYLKRiveter(Riveter.Riveter):
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
                self.sylk_analysis["detected"][(0,0, keys[0].upper())] = keys[0]
                self.sylk_analysis["hits"] = [1]
        
        # Make empty list of confidences; either its there or it isn't. 
        self.sylk_analysis["confidence"] = [1] * n
        
        return self.sylk_analysis

    def apply(self, csvFileAsListOfLists, options, confidence):
        if(self.scream() not in options):
            return
        detections = options[self.scream()]["detected"]
        for k in detections.keys():
            row, col = 0, 0
            csvFileAsListOfLists[0][0] = '\'{:s}'.format(csvFileAsListOfLists[0][0])
        return
    
    def scream(self):
        return "SYLKRiveter"

SYLKRiveter()