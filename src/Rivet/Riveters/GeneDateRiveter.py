from . import Riveter

# Child class of Riveter that checks for gene names that could be misread as dates by Excel
# @author MWK
class GeneDateRiveter(Riveter.Riveter):

    def __init__(self):
        self.scream()

    def analyze(self, column):
        pass

    def apply(self, column):
        pass

    def scream(self):
        print("I AM GENE DATE")
        return
