from . import Riveter

#Child class of Riveter that checks for dates and standardizes them
# @author MWK
class DateFormatRiveter(Riveter.Riveter):

    def __init__(self):
        self.register()
        self.scream()

    def analyze(self, column):
        return {}

    def apply(self, column):
        pass

    def scream(self):
        print("DateFormatRiveter")
        return "DateFormatRiveter"

DateFormatRiveter()