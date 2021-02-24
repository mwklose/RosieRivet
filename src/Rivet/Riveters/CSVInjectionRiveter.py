from . import Riveter

# Child class of Riveter that checks for potential harmful CSV injections
# @author MWK
class CSVInjectionRiveter(Riveter.Riveter):

    def __init__(self):
        self.register()
        self.scream()

    def analyze(self, column):
        return {}

    def apply(self, column):
        pass

    def scream(self):
        print("CSVInjectionRiveter")
        return "CSVInjectionRiveter"

CSVInjectionRiveter()