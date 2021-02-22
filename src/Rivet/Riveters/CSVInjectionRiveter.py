from . import Riveter

# Child class of Riveter that checks for potential harmful CSV injections
# @author MWK
class CSVInjectionRiveter(Riveter.Riveter):

    def __init__(self):
        self.scream()

    def analyze(self, column):
        pass

    def apply(self, column):
        pass

print("I AM CSV INJECTION!")
