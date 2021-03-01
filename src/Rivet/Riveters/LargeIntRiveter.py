from . import Riveter

#Child class of Riveter. Checks for large int columns that could be misread by Excel.
# @author MWK
class LargeIntRiveter(Riveter.Riveter):

    def __init__(self):
        self.register()
        self.scream()

    def analyze(self, column):
        return {}

    def apply(self, column):
        pass

    def scream(self):
        return "LargeIntRiveter"

LargeIntRiveter()
