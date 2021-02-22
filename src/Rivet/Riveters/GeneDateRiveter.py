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

print("I AM GENE DATE AND I HAVE BEEN CREATED")
