
from . import Riveter
import rosie
import collections
import csv

# Child class of Riveter that checks for gene names that could be misread as dates by Excel
# @author MWK
class GeneDateRiveter(Riveter.Riveter):

    #Initialize Riveter along with rosie engine 
    def __init__(self):
        self.register()
        self.scream()
        self.loadRosieEngine()
        self.gene_date_analysis = {}
        self.all = []
        

    def loadRosieEngine(self):
        librosiedir = './lib'
        rosie.load(librosiedir, quiet = True)
        engine = rosie.engine()
        engine.import_package("date")
        self.date_patterns = engine.compile("date.any")
        engine.load("short_year = [0-9]{ 2 }")
        self.date_check = [engine.compile("{ { \"APR\" / \"OCT\" / \"MARCH\" / \"SEPT\" } [:digit:]* }"), engine.compile("{ { date.month { \"-\" / [/] } short_year} / { date.day { \"-\" / [/] } date.month } }")]

     
    def analyze(self, csvFile):
        csvReader = csv.reader(open(csvFile))
        self.gene_date_analysis["detected"] = {}
        keys = next(csvReader)
        n = len(keys)
        date_counter = [0] * n
        total_counter = [0] * n
        actual_date_counter = [0] * n
        for row_num,row in enumerate(csvReader):
            for col_num,element in enumerate(row):
                if(element):
                    total_counter[col_num] += 1
                if(self.date_patterns.fullmatch(element.upper())):
                    actual_date_counter[col_num] += 1
                    self.all.append({"row_no" : row_num+1, "col_no":  col_num + 1, "data" : element, "type": "ACTUALDATE"})
                if(any([check.fullmatch(element.upper()) for check in self.date_check])):
                    date_counter[col_num] += 1
                    self.gene_date_analysis["detected"][(row_num+1, col_num+1, keys[col_num].upper())] = element
                    self.all.append({"row_no" : row_num+1, "col_no":  col_num + 1, "data" : element, "type": "NOTADATE"})

        self.gene_date_analysis["DATESTAT"] = [[a / c, b / c] for a, b, c in zip(date_counter, actual_date_counter, total_counter) ]

        
        return self.gene_date_analysis
    
    def scream(self):
        return "GeneDateRiveter"

    def apply(self, column):
        pass

GeneDateRiveter()