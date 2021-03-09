from . import Riveter

#Child class of Riveter. Checks for large int columns that could be misread by Excel.
# @author MWK
class LargeIntRiveter(Riveter.Riveter):

    def __init__(self):
        self.register()
        self.scream()

    def analyze(self, column):
        return {"detected" : {},
                "confidence" : {},
                "hits" : {}}

    def apply(self, csvFile, options, confidence):
        pass

    def scream(self):
        return "LargeIntRiveter"

LargeIntRiveter()
