from . import Riveter

#Child class of Riveter that checks for dates and standardizes them
# @author MWK
class LocaleSeparatorRiveter(Riveter.Riveter):

    def __init__(self):
        self.register()
        self.scream()

    def analyze(self, column):
        return {}

    def apply(self, column):
        pass

    def scream(self):
        return "LocaleSeparatorRiveter"
LocaleSeparatorRiveter()