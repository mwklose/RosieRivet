from . import Riveter

#Child class of Riveter. Checks for large int columns that could be misread by Excel.
# @author MWK
class LargeIntRiveter(Riveter.Riveter):

    def __init__(self):
        self.scream()

    def analyze(self, column):
        pass

    def apply(self, column):
        pass

print("I AM LARGE INT")
