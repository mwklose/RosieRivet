from . import Riveter
import rosie
# Child class of Riveter that checks for gene names that could be misread as dates by Excel
# @author MWK
class GeneDateRiveter(Riveter.Riveter):

    #Initialize Riveter along with rosie engine 
    def __init__(self):
        self.register()
        self.scream()
        self.loadRosieEngine()
        

    def loadRosieEngine(self):
        librosiedir = './lib'
        rosie.load(librosiedir, quiet = True)
        engine = rosie.engine()
       # self.date_check = [engine.compile("{ { \"APR\" / \"OCT\" / \"MARCH\" / \"SEPT\" } [:digit:]* }"), engine.compile("{ { date.month { \"-\" / [/] } date.short_year } / { date.day { \"-\" / [/] } date.month } }")]


    def analyze(self, column_num, column):
        gene_date_analysis = {}
        n = len(column)
        for i,element in enumerate(column):
            if(any([check.fullmatch(element.upper()) for check in self.date_check])):
                print("Column:" + str(column_num) + " Row: " + str(i+1) + " " + element)

    def scream(self):
        print("I AM GENE DATE RIVETER!")
        return

    def apply(self, column):
        pass

GeneDateRiveter()