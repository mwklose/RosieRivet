from . import Riveter

#Child class of Riveter that checks for dates and standardizes them
# @author MWK
class LocaleSeparatorRiveter(Riveter.MetaRiveter):

    def __init__(self):
        self.register()
        self.scream()

    def analyze(self, csvFile):
        d = self.sniffDelimiter(csvFile).delimiter
        return {"detected" : { "data" : "Separator used : " + '"'+ d + '"'},
                "hits" : [1]}

    def scream(self):
        return "LocaleSeparatorRiveter"

LocaleSeparatorRiveter()