
from . import Riveter
import rosie
import collections

# Child class of Riveter that checks for gene names that could be misread as dates by Excel
# @author MWK
class GeneDateRiveter(Riveter.Riveter):

    #Initialize Riveter along with rosie engine 
    def __init__(self):
        self.register()
        self.scream()
        self.loadRosieEngine()
        self.gene_date_analysis = {}
        

    def loadRosieEngine(self):
        librosiedir = './lib'
        rosie.load(librosiedir, quiet = True)
        engine = rosie.engine()
        engine.import_package("date")
        date_patterns = engine.compile("date.any")
        engine.load("short_year = [0-9]{ 2 }")
        self.date_check = [engine.compile("{ { \"APR\" / \"OCT\" / \"MARCH\" / \"SEPT\" } [:digit:]* }"), engine.compile("{ { date.month { \"-\" / [/] } short_year} / { date.day { \"-\" / [/] } date.month } }")]

     
    def analyze(self, csvReader):
        self.gene_date_analysis["detected"] = {}
        for row_num,row in enumerate(csvReader):
            for col_num,(column,element) in enumerate(row.items()):
                if(any([check.fullmatch(element.upper()) for check in self.date_check])):
                    self.gene_date_analysis["detected"][(row_num, col_num)] = element
        
        #csvReader.seek(0) DESTROY OLD READER, CREATE NEW ONE
        return self.gene_date_analysis
    
    def scream(self):
        return "GeneDateRiveter"

    def apply(self, column):
        pass

GeneDateRiveter()