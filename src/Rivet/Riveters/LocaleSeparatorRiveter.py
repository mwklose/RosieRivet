from . import Riveter

#Child class of Riveter that checks for dates and standardizes them
# @author MWK
class LocaleSeparatorRiveter(Riveter.Riveter):

    def __init__(self):
        self.scream()

    def analyze(self, column):
        pass

    def apply(self, column):
        pass

    def scream(self):
        print("I AM LOCALE SEPARATOR!")
        return
